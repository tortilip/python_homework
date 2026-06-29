from sqlalchemy.orm import Session
from app.db import models


def create_category(db: Session, title: str):
    """Создать новую категорию"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    """Получить все категории"""
    return db.query(models.Category).all()



def create_book(db: Session, title: str, price: float, category_id: int, description: str = None, url: str = ""):
    """Создать новую книгу"""
    db_book = models.Book(
        title=title,
        price=price,
        category_id=category_id,
        description=description,
        url=url
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    """Получить все книги"""
    return db.query(models.Book).all()