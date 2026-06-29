import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import engine, Base, SessionLocal
from app.db import crud

def init_database():
    print("Создаем таблицы в базе данных...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not crud.get_categories(db):
            print("Заполняем базу тестовыми данными...")

            cat_python = crud.create_category(db, title="Программирование на Python")
            cat_databases = crud.create_category(db, title="Базы данных")

            crud.create_book(db, title="Python для чайников", price=1200.0, category_id=cat_python.id, description="Краткое и простое пособие для изучения языка")
            crud.create_book(db, title="Python для продвинутых", price=850.0, category_id=cat_python.id, description="Пособие для продвинутых пользователей Python")

            crud.create_book(db, title="Проектирование БД", price=950.0, category_id=cat_databases.id, description="Все про нормальные формы и SQL")
            crud.create_book(db, title="PostgreSQL изнутри", price=1500.0, category_id=cat_databases.id, description="Глубокое погружение в работу движка")
            
            print("База успешно заполнена!")
        else:
            print("База данных уже содержит данные.")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()