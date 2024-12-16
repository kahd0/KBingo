from views.mainView import MainView
from utils.database import initializeDatabase
from settings import loadTheme
import customtkinter as ctk
from variables import ICON_PATH

if __name__ == "__main__":
    initializeDatabase()
    ctk.set_appearance_mode(loadTheme())
    app = MainView()
    app.wm_iconbitmap(ICON_PATH)  # Define o ícone da janela
    app.mainloop()
