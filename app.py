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
        <title>User Management App</title>
        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f3f4f6;
                color: #111827;
            }

            .layout {
                display: flex;
                min-height: 100vh;
            }

            .sidebar {
                width: 240px;
                background-color: #111827;
                color: white;
                padding: 25px 20px;
            }

            .logo {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 35px;
            }

            .menu-item {
                padding: 12px 14px;
                border-radius: 8px;
                margin-bottom: 10px;
                background-color: #1f2937;
                font-size: 15px;
            }

            .main {
                flex: 1;
                padding: 30px 40px;
            }

            .topbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }

            .topbar h1 {
                margin: 0;
                font-size: 30px;
                color: #111827;
            }

            .admin-box {
                background-color: white;
                padding: 12px 18px;
                border-radius: 10px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
                color: #374151;
            }

            .dashboard-cards {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }

            .stat-card {
                background-color: white;
                padding: 24px;
                border-radius: 14px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.07);
            }

            .stat-title {
                color: #6b7280;
                font-size: 14px;
                margin-bottom: 10px;
            }

            .stat-value {
                font-size: 32px;
                font-weight: bold;
                color: #2563eb;
            }

            .content-grid {
                display: grid;
                grid-template-columns: 1fr;
                gap: 25px;
            }

            .card {
                background-color: white;
                padding: 28px;
                border-radius: 14px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.07);
            }

            .card h2 {
                margin-top: 0;
                margin-bottom: 8px;
                font-size: 22px;
            }

            .card p {
                color: #6b7280;
                margin-bottom: 22px;
            }

            form {
                display: flex;
                gap: 12px;
            }

            input[type="text"] {
                flex: 1;
                padding: 13px 14px;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                font-size: 15px;
                outline: none;
            }

            input[type="text"]:focus {
                border-color: #2563eb;
            }

            button {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 13px 22px;
                border-radius: 10px;
                font-size: 15px;
                cursor: pointer;
            }

            button:hover {
                background-color: #1d4ed8;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 18px;
            }

            th {
                background-color: #f9fafb;
                color: #374151;
                font-size: 14px;
            }

            th, td {
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
            }

            tr:hover {
                background-color: #f9fafb;
            }

            .badge {
                background-color: #dcfce7;
                color: #166534;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: bold;
            }

            .empty {
                text-align: center;
                color: #6b7280;
                padding: 30px;
            }
        </style>
    </head>
    <body>

        <div class="layout">

            <div class="sidebar">
                <div class="logo">UserPanel</div>
                <div class="menu-item">Dashboard</div>
                <div class="menu-item">Users</div>
                <div class="menu-item">Reports</div>
                <div class="menu-item">Settings</div>
            </div>

            <div class="main">

                <div class="topbar">
                    <h1>User Management App</h1>
                    <div class="admin-box">Admin Panel</div>
                </div>

                <div class="dashboard-cards">
                    <div class="stat-card">
                        <div class="stat-title">Total Users</div>
                        <div class="stat-value">{{ users|length }}</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-title">Active Status</div>
                        <div class="stat-value">Live</div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-title">Database</div>
                        <div class="stat-value">SQLite</div>
                    </div>
                </div>

                <div class="content-grid">

                    <div class="card">
                        <h2>Add New User</h2>
                        <p>Enter a user name to add it into the application database.</p>

                        <form method="POST" action="/add">
                            <input type="text" name="name" placeholder="Enter user name" required>
                            <button type="submit">Add User</button>
                        </form>
                    </div>

                    <div class="card">
                        <h2>Users List</h2>
                        <p>All users stored in the database are displayed below.</p>

                        {% if users %}
                            <table>
                                <tr>
                                    <th>#</th>
                                    <th>User Name</th>
                                    <th>Status</th>
                                </tr>

                                {% for user in users %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td>{{ user[0] }}</td>
                                        <td><span class="badge">Active</span></td>
                                    </tr>
                                {% endfor %}
                            </table>
                        {% else %}
                            <div class="empty">
                                No users added yet.
                            </div>
                        {% endif %}
                    </div>

                </div>

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