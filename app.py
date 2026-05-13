from flask import Flask, request, render_template_string, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <title>Simple User App</title>
    </head>
    <body>
        <h1>Simple User Management App</h1>

        <form method="POST" action="/add">
            <input type="text" name="name" placeholder="Enter user name" required>
            <button type="submit">Add User</button>
        </form>

        <h2>Users List</h2>
        <ul>
            {% for user in users %}
                <li>{{ user[0] }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)