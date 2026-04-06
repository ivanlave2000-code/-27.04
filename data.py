import sqlite3

from flask import app, g, render_template, request


DATABASE = "data.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            name TEXT,
                            email TEXT UNIQUE,
                            password TEXT,
                            country TEXT,
                            phone TEXT)""")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/register", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        nickname = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Users (name, password, email, phone) VALUES (?, ?, ?, ?)",
            (nickname, password, email, phone),
        )

        return render_template("register.html")
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)