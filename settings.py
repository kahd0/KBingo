import customtkinter as ctk


# Configuração de tema
def configureTheme():
    ctk.set_appearance_mode("System")  # "Dark", "Light", "System"
    ctk.set_default_color_theme("blue")  # "blue", "dark-blue", "green"


# Configuração de Fonte Padrão
FONT_TITLE = ("Arial", 16)
FONT_NORMAL = ("Arial", 14)
FONT_SMALL = ("Arial", 12)


LOG_LEVEL = "INFO"  # Alterar para "DEBUG", "ERROR", etc.
