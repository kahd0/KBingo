# settings.py
import customtkinter as ctk
import json, os
from variables import CONFIG_FILE
from utils.logging import logInfo, logError

def configureTheme():
    """Define a configuração inicial do tema."""
    ctk.set_appearance_mode("System")  # Tema inicial
    ctk.set_default_color_theme("blue")  # Cor padrão

def saveTheme(theme):
    """Salva o tema selecionado no arquivo de configuração."""
    try:
        config_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(config_dir):  # Garante que o diretório existe
            os.makedirs(config_dir)

        with open(CONFIG_FILE, "w") as config:
            json.dump({"theme": theme}, config)
        logInfo(f"Tema '{theme}' salvo com sucesso.")
    except Exception as e:
        logError(f"Erro ao criar/salvar config.json: {e}")




def loadTheme():
    """Carrega o tema do arquivo de configuração."""
    try:
        if os.path.exists(CONFIG_FILE):  # Verifica se o arquivo existe
            with open(CONFIG_FILE, "r") as config:
                return json.load(config).get("theme", "system")  # Retorna o tema salvo
    except Exception as e:
        logError(f"Erro ao carregar config.json: {e}")
    return "system"  # Retorna o padrão




# Configuração de Fonte Padrão
FONT_TITLE = ("Arial", 16)
FONT_NORMAL = ("Arial", 14)
FONT_SMALL = ("Arial", 12)
