import sqlite3
import os

DB_PATH = os.path.join("data", "itens.db")
TYPES = ["Eletrônicos", "Roupas", "Livros", "Cosméticos", "Alimentos"]

def init_item_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS itens
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, tipo TEXT)''')
    conn.commit()
    conn.close()

def add_item(nome, tipo):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO itens (nome, tipo) VALUES (?, ?)", (nome, tipo))
    conn.commit()
    conn.close()

def remove_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def list_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM itens")
    items = c.fetchall()
    conn.close()
    return items
