"""
Semantic search service for journal entries
"""
import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dateutil import parser
from app.services.supabase_service import SupabaseService
from app.services.embedding_service import embedding_service


class SemanticSearchService(SupabaseService):
    """Service for semantic search operations on journal entries"""
    
    def __init__(self):
        super().__init__()
        self.embedding_service = embedding_service
    
    async def search_entries(
        self, 
        user_id: str, 
        query: str, 
        limit: int = 10,
        similarity_threshold: float = 0.1,
        date_range: Optional[Tuple[datetime, datetime]] = None,
        mood_filter: Optional[str] = None,
        collection_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on journal entries
        
        Args:
            user_id (str): User ID to search entries for
            query (str): Search query
            limit (int): Maximum number of results
            similarity_threshold (float): Minimum similarity score
            date_range (Optional[Tuple[datetime, datetime]]): Date range filter
            mood_filter (Optional[str]): Mood filter
            collection_id (Optional[str]): Collection filter
            
        Returns:
            List[Dict[str, Any]]: Search results with similarity scores
        """
        try:
            # Parse date references from query if any
            parsed_date_range = self._parse_date_from_query(query)
            if parsed_date_range:
                date_range = parsed_date_range
            
            # Generate embedding for the search query
            query_embedding = await self.embedding_service.generate_embedding(query)
            if not query_embedding:
                return []
            
            # Build the search query
            search_query = self.supabase.table("entries").select(
                """
                id, title, content, mood, mood_score, mood_image_url, 
                collection_id, created_at, updated_at,
                content_embedding
                """
            ).eq("user_id", user_id)
            
            # Apply filters
            if date_range:
                search_query = search_query.gte("created_at", date_range[0].isoformat())
                search_query = search_query.lte("created_at", date_range[1].isoformat())
            
            if mood_filter:
                search_query = search_query.eq("mood", mood_filter)
            
            if collection_id:
                search_query = search_query.eq("collection_id", collection_id)
            
            # Execute search
            result = search_query.execute()
            entries = result.data if result.data else []
            
            # Calculate similarities and filter
            scored_entries = []
            for entry in entries:
                if entry.get('content_embedding'):
                    similarity = self.embedding_service.compute_similarity(
                        query_embedding, 
                        entry['content_embedding']
                    )
                    
                    if similarity >= similarity_threshold:
                        entry['similarity_score'] = similarity
                        scored_entries.append(entry)
            
            # Sort by similarity score (descending)
            scored_entries.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Return top results
            return scored_entries[:limit]
            
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []
    
    async def hybrid_search_entries(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
        date_range: Optional[Tuple[datetime, datetime]] = None,
        mood_filter: Optional[str] = None,
        collection_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search
        
        Args:
            user_id (str): User ID to search entries for
            query (str): Search query
            limit (int): Maximum number of results
            semantic_weight (float): Weight for semantic similarity
            keyword_weight (float): Weight for keyword matching
            date_range (Optional[Tuple[datetime, datetime]]): Date range filter
            mood_filter (Optional[str]): Mood filter
            collection_id (Optional[str]): Collection filter
            
        Returns:
            List[Dict[str, Any]]: Hybrid search results with combined scores
        """
        try:
            # Get semantic search results
            semantic_results = await self.search_entries(
                user_id=user_id,
                query=query,
                limit=limit * 2,  # Get more for hybrid ranking
                similarity_threshold=0.05,
                date_range=date_range,
                mood_filter=mood_filter,
                collection_id=collection_id
            )
            
            # Get keyword search results
            keyword_results = await self._keyword_search_entries(
                user_id=user_id,
                query=query,
                limit=limit * 2,
                date_range=date_range,
                mood_filter=mood_filter,
                collection_id=collection_id
            )
            
            # Combine and score results
            combined_results = self._combine_search_results(
                semantic_results, 
                keyword_results, 
                semantic_weight, 
                keyword_weight
            )
            
            # Sort by combined score and return top results
            combined_results.sort(key=lambda x: x.get('combined_score', 0), reverse=True)
            return combined_results[:limit]
            
        except Exception as e:
            print(f"Error in hybrid search: {e}")
            return []
    
    async def _keyword_search_entries(
        self,
        user_id: str,
        query: str,
        limit: int,
        date_range: Optional[Tuple[datetime, datetime]] = None,
        mood_filter: Optional[str] = None,
        collection_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Perform keyword-based search on entries"""
        try:
            # Build keyword search query using PostgreSQL full-text search
            search_query = self.supabase.table("entries").select(
                """
                id, title, content, mood, mood_score, mood_image_url, 
                collection_id, created_at, updated_at
                """
            ).eq("user_id", user_id)
            
            # Apply text search on content and title
            search_query = search_query.or_(
                f"content.ilike.%{query}%,title.ilike.%{query}%"
            )
            
            # Apply filters
            if date_range:
                search_query = search_query.gte("created_at", date_range[0].isoformat())
                search_query = search_query.lte("created_at", date_range[1].isoformat())
            
            if mood_filter:
                search_query = search_query.eq("mood", mood_filter)
            
            if collection_id:
                search_query = search_query.eq("collection_id", collection_id)
            
            result = search_query.limit(limit).execute()
            entries = result.data if result.data else []
            
            # Calculate keyword matching scores
            for entry in entries:
                entry['keyword_score'] = self._calculate_keyword_score(query, entry)
            
            return entries
            
        except Exception as e:
            print(f"Error in keyword search: {e}")
            return []
    
    def _calculate_keyword_score(self, query: str, entry: Dict[str, Any]) -> float:
        """Calculate keyword matching score for an entry"""
        try:
            query_words = query.lower().split()
            content = f"{entry.get('title', '')} {entry.get('content', '')}".lower()
            
            matches = sum(1 for word in query_words if word in content)
            score = matches / len(query_words) if query_words else 0
            
            return score
            
        except Exception:
            return 0.0
    
    def _combine_search_results(
        self, 
        semantic_results: List[Dict[str, Any]], 
        keyword_results: List[Dict[str, Any]],
        semantic_weight: float,
        keyword_weight: float
    ) -> List[Dict[str, Any]]:
        """Combine semantic and keyword search results"""
        # Create a dict to track entries by ID
        combined_entries = {}
        
        # Add semantic results
        for entry in semantic_results:
            entry_id = entry['id']
            combined_entries[entry_id] = entry.copy()
            combined_entries[entry_id]['semantic_score'] = entry.get('similarity_score', 0)
            combined_entries[entry_id]['keyword_score'] = 0
        
        # Add keyword results
        for entry in keyword_results:
            entry_id = entry['id']
            if entry_id in combined_entries:
                combined_entries[entry_id]['keyword_score'] = entry.get('keyword_score', 0)
            else:
                combined_entries[entry_id] = entry.copy()
                combined_entries[entry_id]['semantic_score'] = 0
                combined_entries[entry_id]['keyword_score'] = entry.get('keyword_score', 0)
        
        # Calculate combined scores
        for entry in combined_entries.values():
            semantic_score = entry.get('semantic_score', 0)
            keyword_score = entry.get('keyword_score', 0)
            entry['combined_score'] = (
                semantic_score * semantic_weight + 
                keyword_score * keyword_weight
            )
        
        return list(combined_entries.values())
    
    def _parse_date_from_query(self, query: str) -> Optional[Tuple[datetime, datetime]]:
        """Parse date references from natural language query"""
        try:
            query_lower = query.lower()
            now = datetime.now()
            
            # Handle relative dates
            if 'today' in query_lower:
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=1)
                return (start, end)
            
            if 'yesterday' in query_lower:
                start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=1)
                return (start, end)
            
            if 'this week' in query_lower:
                days_since_monday = now.weekday()
                start = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=7)
                return (start, end)
            
            if 'last week' in query_lower:
                days_since_monday = now.weekday()
                start = (now - timedelta(days=days_since_monday + 7)).replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=7)
                return (start, end)
            
            # Handle month names
            month_patterns = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            
            for month_name, month_num in month_patterns.items():
                if month_name in query_lower:
                    # Default to current year
                    year = now.year
                    start = datetime(year, month_num, 1)
                    if month_num == 12:
                        end = datetime(year + 1, 1, 1)
                    else:
                        end = datetime(year, month_num + 1, 1)
                    return (start, end)
            
            return None
            
        except Exception as e:
            print(f"Error parsing date from query: {e}")
            return None
    
    async def update_entry_embedding(self, entry_id: str, content: str) -> bool:
        """
        Update the embedding for a specific entry
        
        Args:
            entry_id (str): Entry ID
            content (str): Entry content to generate embedding for
            
        Returns:
            bool: True if successful
        """
        try:
            # Generate embedding
            embedding = await self.embedding_service.generate_embedding(content)
            if not embedding:
                return False
            
            # Update entry with embedding
            result = self.supabase.table("entries").update({
                "content_embedding": embedding,
                "updated_at": datetime.now().isoformat()
            }).eq("id", entry_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            print(f"Error updating entry embedding: {e}")
            return False
    
    async def batch_update_embeddings(self, user_id: str) -> int:
        """
        Update embeddings for all entries that don't have them
        
        Args:
            user_id (str): User ID to update entries for
            
        Returns:
            int: Number of entries updated
        """
        try:
            # Get entries without embeddings
            result = self.supabase.table("entries").select(
                "id, title, content"
            ).eq("user_id", user_id).is_("content_embedding", "null").execute()
            
            entries = result.data if result.data else []
            if not entries:
                return 0
            
            # Generate embeddings in batches
            batch_size = 10
            updated_count = 0
            
            for i in range(0, len(entries), batch_size):
                batch = entries[i:i + batch_size]
                
                # Generate embeddings for batch
                contents = [f"{entry['title']} {entry['content']}" for entry in batch]
                embeddings = await self.embedding_service.generate_embeddings_batch(contents)
                
                # Update entries
                for j, entry in enumerate(batch):
                    if j < len(embeddings) and embeddings[j]:
                        success = await self.update_entry_embedding(entry['id'], contents[j])
                        if success:
                            updated_count += 1
            
            return updated_count
            
        except Exception as e:
            print(f"Error batch updating embeddings: {e}")
            return 0


# Global semantic search service instance
semantic_search_service = SemanticSearchService()
