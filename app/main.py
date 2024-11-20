from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database.database import SessionLocal, engine, Base
from .models.user import User
from .schemas.user_schema import UserCreate, User as UserSchema

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"Hello": "World"}


