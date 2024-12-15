import os

# Caminho correto do banco de dados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
