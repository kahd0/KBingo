import sqlite3
import logging
from src.variables import DB_PATH

def init_db():
    """
    Inicializa o banco de dados SQLite.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
                """
            )
            conn.commit()
        logging.info(f"Banco de dados inicializado: {DB_PATH}")
    except sqlite3.Error as e:
        logging.error(f"Erro ao inicializar banco de dados: {e}")

def get_user(username):
    """
    Recupera um usuário pelo nome.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password, role FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Erro ao buscar usuário {username}: {e}")
        return None
