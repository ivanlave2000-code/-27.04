import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ticket_system_2026_fixed'

def get_db_connection():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'tickets_base.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Створюємо таблицю Користувачі
    cursor.execute('DROP TABLE IF EXISTS users') # Видаляємо стару версію для чистоти
    cursor.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)''')

    # 2. Створюємо таблицю Заходи (ТУТ Є PRICE)
    cursor.execute('DROP TABLE IF EXISTS events')
    cursor.execute('''CREATE TABLE events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        price REAL NOT NULL, 
                        location TEXT)''')

    # 3. Створюємо таблицю Квитки
    cursor.execute('DROP TABLE IF EXISTS tickets')
    cursor.execute('''CREATE TABLE tickets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        event_id INTEGER,
                        purchase_date DATE DEFAULT (date('now')),
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (event_id) REFERENCES events(id))''')

    # Наповнюємо даними
    cursor.executemany("INSERT INTO events (title, price, location) VALUES (?, ?, ?)", [
        ('Рок-концерт', 650.0, 'Київ'),
        ('IT-Конференція', 1200.0, 'Харків'),
        ('Футбольний матч', 350.0, 'Одеса')
    ])
    cursor.execute("INSERT INTO users (name) VALUES ('Гість')")
    
    conn.commit()
    conn.close()
    print("✅ База даних успішно створена з усіма стовпцями!")

def debug_tickets():
    conn = get_db_connection()
    # Запит, який об'єднує таблиці для звіту
    stats = conn.execute('''
        SELECT t.id, u.name, e.title, e.price 
        FROM tickets t
        JOIN users u ON t.user_id = u.id
        JOIN events e ON t.event_id = e.id
    ''').fetchall()
    
    print("\n🎟 --- СПИСОК ПРОДАНИХ КВИТКІВ ---")
    if not stats:
        print("Квитків ще не куплено.")
    for row in stats:
        print(f"Квиток №{row['id']} | {row['name']} купив квиток на '{row['title']}' за {row['price']} грн")
    conn.close()

@app.route('/')
def index():
    debug_tickets()
    conn = get_db_connection()
    all_events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return render_template('index.html', events=all_events)

@app.route('/buy/<int:event_id>', methods=['POST'])
def buy_ticket(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Купуємо від імені Гостя (ID=1)
    cursor.execute("INSERT INTO tickets (user_id, event_id) VALUES (?, ?)", (1, event_id))
    conn.commit()
    conn.close()
    print(f"✅ Квиток на подію #{event_id} успішно додано в базу!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)