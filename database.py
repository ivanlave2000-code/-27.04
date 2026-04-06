import sqlite3
from flask import Flask, g
import flask

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
    """Функція підключення до бази даних"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)  # Підключаємось до SQLite
    return g.db  # Повертаємо з'єднання


@app.teardown_appcontext
def close_db(exception):
    """Функція, яка закриває підключення до бази після завершення запиту"""
    db = g.pop('db', None)  # Видаляємо підключення з глобального контексту g
    if db is not None:
        db.close()  # Закриваємо з'єднання



def create_table():
    """Функція для створення таблиці users"""
    db = get_db()  # Отримуємо з'єднання з базою
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')  # Виконуємо SQL-запит на створення таблиці
    db.commit()  # Зберігаємо зміни



if __name__ == "__main__":
    with app.app_context():
        create_table()  # Створюємо таблицю перед запуском сервера
    app.run(debug=True)