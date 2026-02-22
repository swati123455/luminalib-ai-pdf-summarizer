from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.auth_dependencies import get_current_user
from app.infrastructure.storage.local_storage import LocalStorage
from app.services.book_service import BookService
from app.domain.models.user import User
from app.services.ingestion_service import IngestionService
from app.services.llm_provider import LLMProvider

router = APIRouter(prefix="/books", tags=["Books"])

llm_provider = LLMProvider()
ingestion = IngestionService(llm_provider)

storage = LocalStorage()
service = BookService(storage)

@router.post("/")
async def upload_book(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    book = await service.create_Book(
        db,
        title,
        file,
        current_user.id,
    )

    background_tasks.add_task(
        ingestion.process_book,
        book.id,
    )
    return book

