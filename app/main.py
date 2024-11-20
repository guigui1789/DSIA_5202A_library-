from fastapi import FastAPI, Depends, HTTPException, APIRouter, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List 

from .auth import verify_password, create_access_token, get_password_hash, authenticate_user, get_current_user, fake_users_db
from .database.database import SessionLocal, engine, Base
from .models.user import User
from .models.book import Book
from .schemas.user_schema import UserCreate, User as UserSchema
from .schemas.book_schema import BookCreate, Book

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Création des tables
Base.metadata.create_all(bind=engine)

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@app.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

@app.get("/protected-endpoint")
def read_protected(token: str = Depends(oauth2_scheme)):
    return {"message": "You are authorized", "token": token}
