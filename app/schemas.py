from pydantic import BaseModel
from typing import Optional

# ================= CATEGORY SCHEMAS =================

# Базовые поля для категории
class CategoryBase(BaseModel):
    title: str

# Схема для создания/обновления категории
class CategoryCreate(CategoryBase):
    pass

# Схема ответа API (возвращается клиенту)
class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True  # Позволяет работать с объектами SQLAlchemy


# ================= BOOK SCHEMAS =================

# Базовые поля для книги
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: int

# Схема для создания/обновления книги
class BookCreate(BookBase):
    pass

# Схема ответа API
class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True