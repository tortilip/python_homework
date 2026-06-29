from sqlalchemy.orm import Session
from app.db import models
from app import schemas

def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(title=category.title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_data: schemas.CategoryCreate):
    db_category = get_category(db, category_id)
    if db_category:
        db_category.title = category_data.title
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

def get_books(db: Session, category_id: int = None):
    query = db.query(models.Book)
    if category_id:
        query = query.filter(models.Book.category_id == category_id)
    return query.all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_data: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in book_data.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False