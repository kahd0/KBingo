import customtkinter as ctk
from utils.logging import logInfo, logError
from settings import saveTheme, FONT_TITLE, FONT_NORMAL
import tkinter.messagebox as messagebox



class ConfigController(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título
        self.labelTitle = ctk.CTkLabel(self, text="Configurações", font=FONT_TITLE)
        self.labelTitle.pack(pady=10)

        # Opção: Escolher Tema
        self.labelTheme = ctk.CTkLabel(self, text="Tema:", font=FONT_NORMAL)
        self.labelTheme.pack(pady=5)

        self.comboTheme = ctk.CTkComboBox(
            self, values=["System", "Light", "Dark"], command=self.applyTheme
        )
        self.comboTheme.set(ctk.get_appearance_mode().capitalize())  # Define o tema atual como padrão
        self.comboTheme.pack(pady=5)


        # Espaço reservado para outras configurações futuras
        self.labelPlaceholder = ctk.CTkLabel(self, text="Mais opções em breve...", font=FONT_NORMAL)
        self.labelPlaceholder.pack(pady=20)

    def applyTheme(self, selectedTheme):
        """Aplica o tema selecionado e salva a configuração."""
        try:
            ctk.set_appearance_mode(selectedTheme.lower())  # Aplica o tema
            saveTheme(selectedTheme.lower())  # Salva o tema no arquivo de configuração
            logInfo(f"Tema alterado para '{selectedTheme}'.")
        except Exception as e:
            logError(f"Erro ao alterar tema: {e}")
            messagebox.showerror("Erro", f"Não foi possível alterar o tema: {e}")
