import customtkinter as ctk
import logging
import os

# Configuração de tema
def configureTheme():
    ctk.set_appearance_mode("System")  # "Dark", "Light", "System"
    ctk.set_default_color_theme("blue")  # "blue", "dark-blue", "green"

# Configuração de Logs
LOG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def logInfo(message):
    logging.info(message)

def logError(message):
    logging.error(message)
