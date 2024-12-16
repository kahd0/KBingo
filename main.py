from views.mainView import MainView
from utils.database import initializeDatabase

if __name__ == "__main__":
    initializeDatabase()  # Inicializa o banco de dados
    app = MainView()
    app.mainloop()
