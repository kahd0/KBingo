import os
import sys

# Configura o diretório base do projeto para os imports funcionarem
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import wx
from src.utils.database import init_db
from src.views.loginView import LoginView

def main():
    """
    Ponto de entrada principal da aplicação.
    """
    # Inicializa o banco de dados
    init_db()

    # Inicia a aplicação wxPython
    app = wx.App(False)
    LoginView()
    app.MainLoop()

if __name__ == "__main__":
    main()
