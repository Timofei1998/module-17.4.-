from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from typing import Annotated
from backend.db_depends import get_db
from backend.models import User
from backend.schemas import CreateUser, UpdateUser

router = APIRouter()
@router.get("/")
def all_users(db: Annotated[Session, Depends(get_db)]):
    query = select(User)
    result = db.scalars(query).all()
    return result

@router.get("/{user_id}")
def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    user = db.scalars(query).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create")
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    # Проверка на существующего пользователя
    query = select(User).where(User.username == user.username)
    existing_user = db.scalars(query).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    slug = slugify(user.username)
    stmt = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update/{user_id}")
def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    existing_user = db.scalars(query).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    stmt = update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(existing_user.username)
    )
    db.execute(stmt)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    existing_user = db.scalars(query).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
