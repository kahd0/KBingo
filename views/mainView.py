import customtkinter as ctk
from views.loginView import LoginView
from settings import configureTheme, FONT_NORMAL, FONT_TITLE, FONT_SMALL
from utils.helpers import centralizeWindow
from utils.logging import logInfo, logError
from controllers.userController import UserController




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
        self.infoLabel = ctk.CTkLabel(self, text="Aguardando Login...", font=FONT_NORMAL)
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
        #self.infoLabel = ctk.CTkLabel(self, text=f"Bem-vindo, {userName} ({role.upper()})!", font=FONT_TITLE)
        #self.infoLabel.pack(pady=20)

        if role == "adm":
            self.createAdminContent()
        elif role == "op":
            self.createOperatorContent()
        else:
            self.infoLabel.configure(text="Acesso não permitido.")

    def createAdminContent(self):
        # Menu Lateral
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.labelMenu = ctk.CTkLabel(self.sidebar, text="Menu", font=FONT_TITLE)
        self.labelMenu.pack(pady=10)

        self.btnSelectBingo = ctk.CTkButton(self.sidebar, text="Selecionar Bingo", command=self.onSelectBingo)
        self.btnSelectBingo.pack(pady=5)

        self.labelSelectedBingo = ctk.CTkLabel(self.sidebar, text="Nenhum bingo selecionado", font=FONT_SMALL)
        self.labelSelectedBingo.pack(pady=2)

        self.btnBingos = ctk.CTkButton(self.sidebar, text="Gerenciar Bingos", command=self.onManageBingos)
        self.btnBingos.pack(pady=5)

        self.btnStartGame = ctk.CTkButton(self.sidebar, text="Iniciar Partida", command=self.onStartGame, fg_color="red", hover_color="darkred")
        self.btnStartGame.pack(pady=5)
        self.btnStartGame.pack_forget()  # Esconde o botão inicialmente

        self.btnReports = ctk.CTkButton(self.sidebar, text="Relatórios", command=self.onReports)
        self.btnReports.pack(pady=5)

        self.btnSettings = ctk.CTkButton(self.sidebar, text="Configurações", command=self.onSettings)
        self.btnSettings.pack(pady=5)

        self.btnUsers = ctk.CTkButton(self.sidebar, text="Gerenciar Usuários", command=self.onManageUsers)
        self.btnUsers.pack(pady=5)


        # Área Principal
        self.mainArea = ctk.CTkFrame(self, corner_radius=10)
        self.mainArea.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.labelMain = ctk.CTkLabel(self.mainArea, text="Bem-vindo, Administrador!", font=FONT_TITLE)
        self.labelMain.pack(pady=20)

        self.labelDescription = ctk.CTkLabel(
            self.mainArea,
            text="Selecione uma opção no menu para começar.",
            font=FONT_NORMAL
        )
        self.labelDescription.pack(pady=10)


    def createOperatorContent(self):
        # Conteúdo específico para operadores
        self.operatorLabel = ctk.CTkLabel(self, text="Área de Operador (Acesso Limitado)", font=FONT_NORMAL)
        self.operatorLabel.pack(pady=10)

        self.exitButton = ctk.CTkButton(self, text="Sair", command=self.closeApp)
        self.exitButton.pack(pady=20)


    def closeApp(self):
        self.destroy()


    def onManageUsers(self):
        # Limpa o conteúdo principal
        for widget in self.mainArea.winfo_children():
            widget.destroy()

        # Carrega o Gerenciamento de Usuários
        self.userController = UserController(self.mainArea)
        self.userController.pack(fill="both", expand=True)


    def onManageBingos(self):
        print("Gerenciar Bingos - Em Desenvolvimento")

    def onSelectBingo(self):
        # Simula a seleção de um bingo (futuramente, isso pode ser substituído por um dialog ou combobox)
        selectedBingo = "Bingo da Festa Junina"  # Exemplo de bingo selecionado
        self.labelSelectedBingo.configure(text=f"{selectedBingo}")
        
        # Exibe o botão "Iniciar Partida" após o bingo ser selecionado
        self.btnStartGame.pack(pady=5)

    def onStartGame(self):
        print("Iniciar Partida - Em Desenvolvimento")

    def onSettings(self):
        print("Configurações - Em Desenvolvimento")

    def onReports(self):
        print("Relatórios - Em Desenvolvimento")
