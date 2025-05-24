import sqlite3
import os

DB_USERS = os.path.join("data", "users.db")
DB_ITEMS = os.path.join("data", "itens.db")

# Para simplificar, vamos usar um único banco com 3 tabelas
DB_PATH = os.path.join("data", "compra_facil.db")

TYPES = ["Eletrônicos", "Roupas", "Livros", "Brinquedos"]  # sem "Alimentos"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(item_id) REFERENCES items(id)
    )
    """)

    conn.commit()
    conn.close()

def add_user(nome):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (nome) VALUES (?)", (nome,))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Usuário já existe, buscar ID
        cursor.execute("SELECT id FROM users WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        user_id = row["id"] if row else None
    conn.close()
    return user_id

def list_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM users ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "nome": row["nome"]} for row in rows]

def remove_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def add_item(nome, tipo):
    if tipo not in TYPES:
        raise ValueError("Tipo inválido")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (nome, tipo) VALUES (?, ?)", (nome, tipo))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id

def list_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, tipo FROM items ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "nome": row["nome"], "tipo": row["tipo"]} for row in rows]

def remove_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def add_purchase(user_id, item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO purchases (user_id, item_id) VALUES (?, ?)", (user_id, item_id))
    conn.commit()
    conn.close()

def recommend_for_user(user_id, max_recommendations=5):
    """
    Recomenda itens com base no histórico de compras do usuário:
    - Recomenda itens do mesmo tipo dos que o usuário comprou
    - Que ele ainda não comprou
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Itens comprados pelo usuário
    cursor.execute("""
    SELECT items.tipo FROM purchases
    JOIN items ON purchases.item_id = items.id
    WHERE purchases.user_id = ?
    """, (user_id,))
    tipos_comprados = {row["tipo"] for row in cursor.fetchall()}

    if not tipos_comprados:
        # Se não comprou nada, recomendar itens mais populares (mais comprados no geral)
        cursor.execute("""
        SELECT items.id, items.nome, items.tipo, COUNT(purchases.id) as freq
        FROM items LEFT JOIN purchases ON items.id = purchases.item_id
        GROUP BY items.id
        ORDER BY freq DESC
        LIMIT ?
        """, (max_recommendations,))
        recs = cursor.fetchall()
    else:
        # Recomendamos itens do mesmo tipo que ele comprou e que ainda não comprou
        cursor.execute("""
        SELECT id, nome, tipo FROM items
        WHERE tipo IN ({seq})
        AND id NOT IN (
            SELECT item_id FROM purchases WHERE user_id = ?
        )
        LIMIT ?
        """.format(seq=','.join(['?']*len(tipos_comprados))),
        (*tipos_comprados, user_id, max_recommendations))
        recs = cursor.fetchall()

    conn.close()
    return [{"id": row["id"], "nome": row["nome"], "tipo": row["tipo"]} for row in recs]

def init_test_data():
    create_tables()
    # Inserir dados de teste só se não tiver nenhum usuário
    if not list_users():
        add_user("Alice")
        add_user("Bob")
    if not list_items():
        add_item("Smartphone", "Eletrônicos")
        add_item("Notebook", "Eletrônicos")
        add_item("Camiseta", "Roupas")
        add_item("Calça Jeans", "Roupas")
        add_item("Livro Python", "Livros")
        add_item("Quebra-cabeça", "Brinquedos")
