import wx
from src.utils.appState import state

class MainView(wx.Frame):
    def __init__(self):
        """
        Inicializa a janela principal da aplicação.
        """
        super().__init__(None, title="KBingo - Tela Principal", size=(600, 400))
        self.panel = wx.Panel(self)
        self.Center()

        # Layout principal
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Bem-vindo e papel do usuário
        welcomeLabel = wx.StaticText(
            self.panel,
            label=f"Bem-vindo, {state.currentUser}! ({'Administrador' if state.currentRole == 'admin' else 'Operador'})",
            style=wx.ALIGN_CENTER
        )
        welcomeLabel.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        mainSizer.Add(welcomeLabel, 0, wx.ALL | wx.EXPAND, 10)

        # Botões para funcionalidades
        manageUsersButton = wx.Button(self.panel, label="Gerenciar Usuários")
        manageUsersButton.Bind(wx.EVT_BUTTON, self.onManageUsers)
        manageUsersButton.Enable(state.currentRole == "admin")  # Apenas admin pode acessar
        mainSizer.Add(manageUsersButton, 0, wx.ALL | wx.CENTER, 10)

        manageBingoButton = wx.Button(self.panel, label="Gerenciar Bingos")
        manageBingoButton.Bind(wx.EVT_BUTTON, self.onManageBingo)
        mainSizer.Add(manageBingoButton, 0, wx.ALL | wx.CENTER, 10)

        logoutButton = wx.Button(self.panel, label="Sair")
        logoutButton.Bind(wx.EVT_BUTTON, self.onLogout)
        mainSizer.Add(logoutButton, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(mainSizer)
        self.Show()

    def onManageUsers(self, event):
        """
        Abre a tela de gerenciamento de usuários.
        """
        wx.MessageBox("Funcionalidade de gerenciamento de usuários ainda não implementada.", "Aviso", wx.OK | wx.ICON_INFORMATION)

    def onManageBingo(self, event):
        """
        Abre a tela de gerenciamento de bingos.
        """
        wx.MessageBox("Funcionalidade de gerenciamento de bingos ainda não implementada.", "Aviso", wx.OK | wx.ICON_INFORMATION)

    def onLogout(self, event):
        """
        Realiza logout e retorna para a tela de login.
        """
        wx.MessageBox("Logout realizado com sucesso!", "Logout", wx.OK | wx.ICON_INFORMATION)
        self.Destroy()

        # Retorna à tela de login
        from src.views.loginView import LoginView
        LoginView()
