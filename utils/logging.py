# logging.py
import logging
import os
from variables import LOG_DIR, LOG_LEVEL  # Importa LOG_LEVEL daqui

# Configuração de Logs
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL.upper(), "INFO"),  # Define o nível dinamicamente
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def logInfo(message):
    logging.info(message)

def logError(message):
    logging.error(message)
