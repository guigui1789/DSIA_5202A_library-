from fastapi import FastAPI, Depends, HTTPException, APIRouter, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List 
from jose import JWTError
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .auth import verify_password, create_access_token, get_password_hash, authenticate_user, get_current_user, fake_users_db
from .database.database import SessionLocal, engine, Base, get_db
from .models.user import User
from .models.book import Book as BookModel
from .schemas.user_schema import UserCreate, User as UserSchema
from .schemas.book_schema import BookCreate, BookSchema

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
async def read_protected_endpoint(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated. Please provide a valid token."
        )
    return {"message": "You are authorized"}

@app.get("/admin/")
async def admin_endpoint(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Access forbidden. You do not have the required permissions."
        )
    return {"message": "Welcome, admin!"}

@app.get("/books/{book_id}", response_model=BookSchema)
async def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Book with ID {book_id} not found."
        )
    return book

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, 
                detail="Invalid token. Username not found."
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=401, 
            detail="Invalid token."
        )
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="User not found."
        )
    return user

# GET all books
@app.get("/books/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(BookModel).offset(skip).limit(limit).all()
    return books

# GET a single book by ID
@app.get("/books/{book_id}", response_model=BookSchema)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# POST a new book
@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BookModel(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# DELETE a book
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
