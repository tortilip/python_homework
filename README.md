### 1. Установка программных зависимостей
Установка необходимых внешних библиотек и бинарного драйвера СУБД (`psycopg2-binary`) в целевую среду выполнения:
```bash
pip install fastapi uvicorn sqlalchemy pydantic psycopg2-binary --break-system-packages