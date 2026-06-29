from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import db, models, crud
from app import schemas

app = FastAPI(
    title="Book and Category API",
    description="API для управления книгами и категориями",
    version="1.0.0"
)

def get_db_session():
    db_gen = db.get_db()
    try:
        yield next(db_gen)
    except StopIteration:
        pass

@app.get("/health", tags=["Health"])
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok", "message": "Service is alive and kicking"}


@app.get("/categories", response_model=List[schemas.CategoryResponse], tags=["Categories"])
def read_categories(db_session: Session = Depends(get_db_session)):
    """Получить список всех категорий"""
    return crud.get_categories(db_session)

@app.get("/categories/{category_id}", response_model=schemas.CategoryResponse, tags=["Categories"])
def read_category(category_id: int, db_session: Session = Depends(get_db_session)):
    """Получить категорию по её ID"""
    db_category = crud.get_category(db_session, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.post("/categories", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db_session: Session = Depends(get_db_session)):
    """Создать новую категорию"""
    return crud.create_category(db_session, category)

@app.put("/categories/{category_id}", response_model=schemas.CategoryResponse, tags=["Categories"])
def update_category(category_id: int, category: schemas.CategoryCreate, db_session: Session = Depends(get_db_session)):
    """Обновить существующую категорию"""
    db_category = crud.update_category(db_session, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int, db_session: Session = Depends(get_db_session)):
    """Удалить категорию"""
    success = crud.delete_category(db_session, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}


@app.get("/books", response_model=List[schemas.BookResponse], tags=["Books"])
def read_books(category_id: Optional[int] = None, db_session: Session = Depends(get_db_session)):
    """Получить список книг (с возможностью фильтрации по category_id)"""
    return crud.get_books(db_session, category_id=category_id)

@app.get("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def read_book(book_id: int, db_session: Session = Depends(get_db_session)):
    """Получить книгу по её ID"""
    db_book = crud.get_book(db_session, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(book: schemas.BookCreate, db_session: Session = Depends(get_db_session)):
    """Создать книгу (с валидацией существования категории)"""
    db_category = crud.get_category(db_session, book.category_id)
    if not db_category:
        raise HTTPException(status_code=400, detail="Category with this ID does not exist")
    return crud.create_book(db_session, book)

@app.put("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def update_book(book_id: int, book: schemas.BookCreate, db_session: Session = Depends(get_db_session)):
    """Обновить данные книги"""
    db_category = crud.get_category(db_session, book.category_id)
    if not db_category:
        raise HTTPException(status_code=400, detail="Category with this ID does not exist")
        
    db_book = crud.update_book(db_session, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db_session: Session = Depends(get_db_session)):
    """Удалить книгу"""
    success = crud.delete_book(db_session, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}