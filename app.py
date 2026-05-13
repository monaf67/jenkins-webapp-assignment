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
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple User Management App</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f4f7fb;
                color: #222;
            }

            .navbar {
                background-color: #1f2937;
                color: white;
                padding: 18px 40px;
                font-size: 22px;
                font-weight: bold;
            }

            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }

            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                margin-bottom: 25px;
            }

            h1 {
                margin-top: 0;
                color: #1f2937;
            }

            .subtitle {
                color: #6b7280;
                margin-bottom: 25px;
            }

            form {
                display: flex;
                gap: 10px;
            }

            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 15px;
            }

            button {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 15px;
                cursor: pointer;
            }

            button:hover {
                background-color: #1d4ed8;
            }

            .stats {
                display: flex;
                gap: 20px;
                margin-bottom: 25px;
            }

            .stat-box {
                flex: 1;
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                text-align: center;
            }

            .stat-number {
                font-size: 32px;
                font-weight: bold;
                color: #2563eb;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }

            th, td {
                padding: 14px;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
            }

            th {
                background-color: #f9fafb;
                color: #374151;
            }

            .empty {
                text-align: center;
                color: #6b7280;
                padding: 20px;
            }

            .footer {
                text-align: center;
                color: #6b7280;
                margin-top: 30px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>

        <div class="navbar">
            User Management Dashboard
        </div>

        <div class="container">

            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{{ users|length }}</div>
                    <div>Total Users</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">CI/CD</div>
                    <div>Jenkins Deployment</div>
                </div>
            </div>

            <div class="card">
                <h1>Simple User Management App</h1>
                <p class="subtitle">
                    Add users and store their information using a database-backed Flask web application.
                </p>

                <form method="POST" action="/add">
                    <input type="text" name="name" placeholder="Enter user name" required>
                    <button type="submit">Add User</button>
                </form>
            </div>

            <div class="card">
                <h2>Users List</h2>

                {% if users %}
                    <table>
                        <tr>
                            <th>#</th>
                            <th>User Name</th>
                        </tr>

                        {% for user in users %}
                            <tr>
                                <td>{{ loop.index }}</td>
                                <td>{{ user[0] }}</td>
                            </tr>
                        {% endfor %}
                    </table>
                {% else %}
                    <div class="empty">
                        No users added yet.
                    </div>
                {% endif %}
            </div>

            <div class="footer">
                Flask + SQLite + Docker + Jenkins CI/CD Pipeline
            </div>

        </div>

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