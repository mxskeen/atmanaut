import os
import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import openai
import asyncio
from concurrent.futures import ThreadPoolExecutor


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self, model_type: str = "sentence-transformers"):
        self.model_type = model_type
        self._model = None
        self._executor = ThreadPoolExecutor(max_workers=2)
        
    def _get_sentence_transformer_model(self):
        """Lazy load sentence transformer model"""
        if self._model is None:
            # Using a lightweight multilingual model good for semantic search
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
        return self._model
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a given text
        
        Args:
            text (str): Text to generate embedding for
            
        Returns:
            List[float]: Embedding vector
        """
        if not text or not text.strip():
            return []
            
        if self.model_type == "openai":
            return await self._generate_openai_embedding(text)
        else:
            return await self._generate_sentence_transformer_embedding(text)
    
    async def _generate_openai_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API"""
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
                
            client = openai.OpenAI(api_key=openai_api_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",  # 1536 dimensions
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error generating OpenAI embedding: {e}")
            # Fallback to sentence transformer
            return await self._generate_sentence_transformer_embedding(text)
    
    async def _generate_sentence_transformer_embedding(self, text: str) -> List[float]:
        """Generate embedding using sentence transformers"""
        try:
            loop = asyncio.get_event_loop()
            model = self._get_sentence_transformer_model()
            
            # Run in thread pool to avoid blocking
            embedding = await loop.run_in_executor(
                self._executor, 
                model.encode, 
                text
            )
            
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error generating sentence transformer embedding: {e}")
            return []
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        
        Args:
            texts (List[str]): List of texts to generate embeddings for
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        if not texts:
            return []
            
        if self.model_type == "openai":
            return await self._generate_openai_embeddings_batch(texts)
        else:
            return await self._generate_sentence_transformer_embeddings_batch(texts)
    
    async def _generate_openai_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch using OpenAI"""
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
                
            client = openai.OpenAI(api_key=openai_api_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            
            return [item.embedding for item in response.data]
            
        except Exception as e:
            print(f"Error generating OpenAI batch embeddings: {e}")
            # Fallback to sentence transformer
            return await self._generate_sentence_transformer_embeddings_batch(texts)
    
    async def _generate_sentence_transformer_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch using sentence transformers"""
        try:
            loop = asyncio.get_event_loop()
            model = self._get_sentence_transformer_model()
            
            # Run in thread pool to avoid blocking
            embeddings = await loop.run_in_executor(
                self._executor,
                model.encode,
                texts
            )
            
            return [emb.tolist() for emb in embeddings]
            
        except Exception as e:
            print(f"Error generating sentence transformer batch embeddings: {e}")
            return []
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1 (List[float]): First embedding
            embedding2 (List[float]): Second embedding
            
        Returns:
            float: Cosine similarity score (0-1)
        """
        if not embedding1 or not embedding2:
            return 0.0
            
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Compute cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            print(f"Error computing similarity: {e}")
            return 0.0


# Global embedding service instance
embedding_service = EmbeddingService()
