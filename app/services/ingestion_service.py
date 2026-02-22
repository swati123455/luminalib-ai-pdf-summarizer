import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.models.book import Book
from app.infrastructure.db.session import AsyncSessionLocal
from app.services.pdf_service import PDFService

def splitText(text:str, chunk_size: int = 2000, overlap:int= 200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
class IngestionService:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider
        self.pdf_service = PDFService()


    async def process_book(self, book_id: int):

        print(f"Processing book {book_id}")

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Book).where(Book.id == book_id)
            )

            book = result.scalar_one()

            text = self.pdf_service.extract_text(book.file_path)
            print("Text extracted")

            if not text.strip():
                print("No text extracted")
                return

            chunks = splitText(text)
            partial_summaries = []

            for chunk in chunks:
                print("Summarizing chunk...")
                summary_part = await self.llm_provider.summarize(chunk)
                partial_summaries.append(summary_part)

            combined_text = "\n".join(partial_summaries)

            print("Creating final summary...")
            final_summary = await self.llm_provider.summarize(
                f"Create a final concise summary:\n{combined_text}"
            )

            print("Final summary:", final_summary)

            book.summary = final_summary
            await db.flush()
            await db.refresh(book)

            await db.commit()

            print("Saved summary length:", len(book.summary or "EMPTY"))

        print("Ingestion completed")
