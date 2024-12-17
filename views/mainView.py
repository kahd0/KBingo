import customtkinter as ctk
from views.loginView import LoginView
from settings import FONT_NORMAL, FONT_TITLE, FONT_SMALL
from utils.helpers import centralizeWindow
from utils.logging import logInfo, logError
from tkinter import messagebox
from tkinter.simpledialog import askinteger
from controllers.userController import UserController
from controllers.configController import ConfigController
from controllers.bingoController import BingoController
from controllers.selectBingoController import SelectBingoController
from controllers.generateCardsController import GenerateCardsController




class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KBingo - Gerenciador de Bingos")
        centralizeWindow(self, 1200, 600)


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

        self.btnCreateCards = ctk.CTkButton(self.sidebar, text="Gerar Cartelas", command=self.onCreateCards, fg_color="red", hover_color="darkred")
        self.btnCreateCards.pack(pady=5)
        self.btnCreateCards.pack_forget()  # Esconde o botão inicialmente

        self.btnExportCards = ctk.CTkButton(self.sidebar, text="Exportar Cartelas", command=self.onExportCards, fg_color="red", hover_color="darkred")
        self.btnExportCards.pack(pady=5)
        self.btnExportCards.pack_forget()  # Esconde o botão inicialmente

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
        """Abre o Gerenciador de Bingos."""
        # Limpa o conteúdo principal
        for widget in self.mainArea.winfo_children():
            widget.destroy()

        # Carrega o Gerenciamento de Bingos
        self.bingoController = BingoController(self.mainArea)
        self.bingoController.pack(fill="both", expand=True)

    def onSelectBingo(self):
        def setSelectedBingo(bingoName):
            if bingoName:  # Verifica se um nome válido foi selecionado
                self.labelSelectedBingo.configure(text=f"{bingoName}")
                self.btnStartGame.pack(pady=5)  # Exibe o botão "Iniciar Partida"
                self.btnCreateCards.pack(pady=5)
                self.btnExportCards.pack(pady=5)

        # Limpa a área principal antes de abrir o modal
        for widget in self.mainArea.winfo_children():
            widget.destroy()

        # Título temporário na área principal
        self.labelMain = ctk.CTkLabel(self.mainArea, text="Carregando detalhes do Bingo...", font=FONT_TITLE)
        self.labelMain.pack(pady=20)

        # Abre o modal para seleção de bingo e passa a área principal para exibir detalhes
        SelectBingoController(self, callback=setSelectedBingo, displayArea=self.mainArea)


    def onStartGame(self):
        print("Iniciar Partida - Em Desenvolvimento")

    def onExportCards(self):
        print("Exportar Cartelas - Em Desenvolvimento")

    def onCreateCards(self):
        """Solicita ao usuário o número de cartelas e gera as cartelas."""
        bingo_id = self.getSelectedBingoId()
        if not bingo_id:
            messagebox.showerror("Erro", "Nenhum bingo selecionado!")
            return

        # Solicita o número de cartelas
        num_cartelas = askinteger("Número de Cartelas", "Quantas cartelas deseja gerar?", minvalue=1)
        if not num_cartelas:  # Se o usuário cancelar ou não inserir
            messagebox.showinfo("Aviso", "Operação cancelada.")
            return

        # Gera as cartelas
        controller = GenerateCardsController(bingo_id, num_cartelas)
        generated_cards = controller.saveGeneratedCards()

        if generated_cards:
            messagebox.showinfo("Sucesso", f"{len(generated_cards)} cartelas geradas com sucesso!")
            # Atualiza os detalhes do bingo após gerar cartelas
            self.refreshBingoDetails()
        else:
            messagebox.showerror("Erro", "Não foi possível gerar as cartelas.")



    def getSelectedBingoId(self):
        """Obtém o ID do bingo selecionado no banco de dados."""
        from utils.database import getAllBingos

        selectedBingoName = self.labelSelectedBingo.cget("text")  # Pega o texto do label
        if selectedBingoName == "Nenhum bingo selecionado":
            return None

        # Busca o ID do bingo no banco de dados
        allBingos = getAllBingos()
        for bingo in allBingos:
            if bingo["name"] == selectedBingoName:
                return bingo["id"]
        return None

    def refreshBingoDetails(self):
        """Atualiza os detalhes do bingo exibidos na área principal."""
        from controllers.selectBingoController import SelectBingoController
        from utils.database import getAllBingos

        selectedBingoName = self.labelSelectedBingo.cget("text")  # Pega o nome do bingo selecionado
        if selectedBingoName and selectedBingoName != "Nenhum bingo selecionado":
            # Busca todos os bingos
            allBingos = getAllBingos()
            # Chama diretamente o método estático para atualizar os detalhes
            SelectBingoController.displayBingoDetails(self.mainArea, selectedBingoName, allBingos)


    def onSettings(self):
        """Abre a interface de configurações."""
        # Limpa o conteúdo principal
        for widget in self.mainArea.winfo_children():
            widget.destroy()

        # Carrega as configurações
        self.configController = ConfigController(self.mainArea)
        self.configController.pack(fill="both", expand=True)

    def onReports(self):
        print("Relatórios - Em Desenvolvimento")
