from pydantic import BaseModel

class BookCreate(BaseModel):
    title:str

class BookResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True
