from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year_published = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="books")
