import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets/images/logo.png")
DB_PATH = os.path.join(BASE_DIR, "assets/data/app.db")
LOG_DIR = os.path.join(BASE_DIR, "logs")
CONFIG_FILE = os.path.join(BASE_DIR, "assets", "data", "config.json")
LOG_LEVEL = "INFO"  # Alterar para "DEBUG", "ERROR", etc.
ICON_PATH = os.path.join("assets", "images", "logo.ico")
THEME_PATH = os.path.join("assets", "data", "config.json")