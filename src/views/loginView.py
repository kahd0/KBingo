import wx
from src.controllers.userController import authenticate
from src.utils.appState import state
from src.variables import LOGO_PATH
import os
from src.views.mainView import MainView

class LoginView(wx.Frame):
    def __init__(self):
        # Adiciona o estilo wx.DEFAULT_FRAME_STYLE sem wx.RESIZE_BORDER
        super().__init__(None, title="Login KBingo", size=(400, 400), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self)
        self.Center()

        # Layout principal
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Carregar e exibir a logo
        if os.path.exists(LOGO_PATH):
            try:
                image = wx.Image(LOGO_PATH, wx.BITMAP_TYPE_ANY).Scale(150, 150)  # Redimensiona para 150x150
                bitmap = wx.Bitmap(image)
                logo = wx.StaticBitmap(self.panel, bitmap=bitmap)
                mainSizer.Add(logo, 0, wx.ALL | wx.CENTER, 20)
            except Exception as e:
                print(f"Erro ao carregar a logo: {e}")
        else:
            print(f"Logo não encontrada no caminho: {LOGO_PATH}")

        # Campos de entrada
        self.usernameEntry = wx.TextCtrl(self.panel, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.usernameEntry.SetHint("Usuário")
        mainSizer.Add(self.usernameEntry, 0, wx.ALL | wx.CENTER, 10)
        self.usernameEntry.Bind(wx.EVT_TEXT_ENTER, self.onLogin)  # Evento Enter

        self.passwordEntry = wx.TextCtrl(self.panel, size=(200, -1), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.passwordEntry.SetHint("Senha")
        mainSizer.Add(self.passwordEntry, 0, wx.ALL | wx.CENTER, 10)
        self.passwordEntry.Bind(wx.EVT_TEXT_ENTER, self.onLogin)  # Evento Enter

        # Botão de Login
        loginButton = wx.Button(self.panel, label="Entrar")
        loginButton.Bind(wx.EVT_BUTTON, self.onLogin)
        mainSizer.Add(loginButton, 0, wx.ALL | wx.CENTER, 10)

        # Mensagem de erro
        self.errorMessage = wx.StaticText(self.panel, label="")
        self.errorMessage.SetForegroundColour(wx.RED)
        mainSizer.Add(self.errorMessage, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(mainSizer)
        self.Show()

    def onLogin(self, event):
        username = self.usernameEntry.GetValue()
        password = self.passwordEntry.GetValue()

        success, role = authenticate(username, password)
        if success:
            state.currentUser = username
            state.currentRole = role
            self.Destroy()
            MainView()
        else:
            self.errorMessage.SetLabel("Usuário ou senha inválidos.")
