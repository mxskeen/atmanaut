import asyncio
from app.services.embedding_service import EmbeddingService
from app.core.database import get_db
from app.models.models import JournalEntry

async def main():
    """
    This script generates embeddings for new journal entries
    and updates them in the database.
    """
    db = next(get_db())
    embedding_service = EmbeddingService()

    # Get all journal entries that don't have an embedding
    entries_to_update = db.query(JournalEntry).filter(JournalEntry.embedding == None).all()

    if not entries_to_update:
        print("No new journal entries to generate embeddings for.")
        return

    print(f"Found {len(entries_to_update)} new journal entries to process.")

    texts = [entry.content for entry in entries_to_update]
    embeddings = await embedding_service.generate_embeddings_batch(texts)

    for entry, embedding in zip(entries_to_update, embeddings):
        entry.embedding = embedding

    db.commit()
    print(f"Successfully generated and saved embeddings for {len(entries_to_update)} entries.")

if __name__ == "__main__":
    asyncio.run(main())
