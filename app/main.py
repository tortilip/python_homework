import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("ПОЛУЧЕНИЕ ДАННЫХ ИЗ БАЗЫ ДАННЫХ ПОСТГРЕС")
        print("=" * 50)

        categories = crud.get_categories(db)
        
        for category in categories:
            print(f"\nКатегория: {category.title} (ID: {category.id})")
            print("-" * 30)
            
            if category.books:
                for book in category.books:
                    print(f"  - Книга: {book.title}")
                    print(f"    Цена: {book.price} руб.")
                    print(f"    Описание: {book.description}")
                    print(f"    Ссылка: '{book.url}'")
            else:
                print("  (В этой категории пока нет книг)")
                
        print("\n" + "=" * 50)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()