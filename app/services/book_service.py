from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.book import Book

class BookService:
    def __init__(self, storage):
        self.storage = storage

    async def create_Book(self,db:AsyncSession,title, file, user_id):
        path = await self.storage.save(file, file.filename)

        book = Book(
            title = title,
            file_path = path,
            owner_id = user_id,

        )

        db.add(book)
        await db.commit()
        await db.refresh(book)

        return book