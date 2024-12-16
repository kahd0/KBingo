import customtkinter as ctk
from views.loginView import LoginView
from settings import configureTheme
from utils.helpers import centralizeWindow


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KBingo - Gerenciador de Bingos")
        centralizeWindow(self, 800, 600)

        # Configuração do tema
        configureTheme()

        # Bloqueia a janela até que o login seja concluído
        self.createWidgets()
        self.openLoginView()

    def createWidgets(self):
        # Exibe uma mensagem inicial enquanto aguarda o login
        self.infoLabel = ctk.CTkLabel(self, text="Aguardando Login...", font=("Arial", 14))
        self.infoLabel.pack(pady=100)
        
        # Botão para abrir a tela de login
        self.loginButton = ctk.CTkButton(self, text="Fazer Login", command=self.openLoginView)
        self.loginButton.pack(pady=10)

    def openLoginView(self):
        # Abre o LoginView como modal
        self.loginWindow = LoginView(self)
        self.wait_window(self.loginWindow)  # Bloqueia MainView até que LoginView seja fechado

    def updateAfterLogin(self, userName, role):
        # Remove a mensagem e o botão de login
        if hasattr(self, 'infoLabel'):
            self.infoLabel.destroy()
        if hasattr(self, 'loginButton'):
            self.loginButton.destroy()

        # Atualiza a interface com base no papel do usuário
        self.infoLabel = ctk.CTkLabel(self, text=f"Bem-vindo, {userName} ({role.upper()})!", font=("Arial", 16))
        self.infoLabel.pack(pady=20)

        if role == "adm":
            self.createAdminContent()
        elif role == "op":
            self.createOperatorContent()
        else:
            self.infoLabel.configure(text="Acesso não permitido.")

    def createAdminContent(self):
        # Conteúdo específico para administradores
        self.adminLabel = ctk.CTkLabel(self, text="Área de Administrador", font=("Arial", 14))
        self.adminLabel.pack(pady=10)

        self.exitButton = ctk.CTkButton(self, text="Sair", command=self.closeApp)
        self.exitButton.pack(pady=20)

    def createOperatorContent(self):
        # Conteúdo específico para operadores
        self.operatorLabel = ctk.CTkLabel(self, text="Área de Operador (Acesso Limitado)", font=("Arial", 14))
        self.operatorLabel.pack(pady=10)

        self.exitButton = ctk.CTkButton(self, text="Sair", command=self.closeApp)
        self.exitButton.pack(pady=20)


    def closeApp(self):
        self.destroy()
