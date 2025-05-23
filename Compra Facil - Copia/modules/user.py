import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

def init_user_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS compras
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, tipo TEXT)''')
    conn.commit()
    conn.close()

def add_user(nome):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def remove_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM compras WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def list_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

def add_purchase(user_id, tipo):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO compras (user_id, tipo) VALUES (?, ?)", (user_id, tipo))
    conn.commit()
    conn.close()

def get_user_purchases(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT tipo FROM compras WHERE user_id = ?", (user_id,))
    purchases = c.fetchall()
    conn.close()
    return [p[0] for p in purchases]
