import customtkinter as ctk
from utils.helpers import centralizeWindow
from settings import FONT_NORMAL, FONT_TITLE
from utils.logging import logInfo, logError
from variables import LOGO_PATH, ICON_PATH
from PIL import Image
from utils.database import validateLogin



class LoginView(ctk.CTkToplevel):
    def __init__(self, mainView):
        super().__init__()
        self.mainView = mainView
        self.title("Login")
        centralizeWindow(self, 400, 400)
        self.resizable(False, False)

        # Aplicar ícone
        try:
            self.wm_iconbitmap(ICON_PATH)  # Define o ícone
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Torna a janela modal
        self.transient(mainView)
        self.grab_set()

        self.createWidgets()

    def createWidgets(self):
        # Logo
        try:
            self.logoImage = ctk.CTkImage(dark_image=Image.open(LOGO_PATH), size=(150, 150))
            self.logoLabel = ctk.CTkLabel(self, image=self.logoImage, text="")
            self.logoLabel.pack(pady=20)
        except Exception as e:
            print(f"Erro ao carregar a logo: {e}")

        # Título
        self.labelTitle = ctk.CTkLabel(self, text="Faça Login", font=FONT_TITLE)
        self.labelTitle.pack(pady=10)

        # Campo de Usuário
        self.entryUser = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entryUser.pack(pady=5, padx=50)
        self.entryUser.bind("<Return>", lambda event: self.entryPassword.focus())  # Move foco

        # Campo de Senha
        self.entryPassword = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entryPassword.pack(pady=5, padx=50)
        self.entryPassword.bind("<Return>", self.performLoginEvent)  # Chama performLogin ao pressionar Enter

        # Botão de Login
        self.loginButton = ctk.CTkButton(self, text="Entrar", command=self.performLogin)
        self.loginButton.pack(pady=20)

        # Mensagem de Erro
        self.errorLabel = ctk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack(pady=5)

    def performLoginEvent(self, event=None):
        """Função de evento para chamar performLogin."""
        self.performLogin()


    def performLogin(self):
        """Função que valida o login."""
        user = self.entryUser.get()
        password = self.entryPassword.get()

        role = validateLogin(user, password)  # Valida credenciais com segurança
        if role:
            logInfo(f"Login bem-sucedido para {user} com papel {role}.")
            self.mainView.updateAfterLogin(user, role)  # Passa o papel do usuário
            self.destroy()
        else:
            logError(f"Tentativa de login falhou para o usuário: {user}")
            self.errorLabel.configure(text="Usuário ou senha inválidos.", text_color="red")
