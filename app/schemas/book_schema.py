from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    year_published: int

class BookCreate(BookBase):
    pass

class BookSchema(BookBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
