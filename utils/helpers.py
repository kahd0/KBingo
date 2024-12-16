def centralizeWindow(window, width, height):
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth - width) // 2
    y = (screenHeight - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def centralizeWindowRelative(parent, window, width, height):
    """
    Centraliza uma janela em relação à posição da janela pai (parent).
    :param parent: A janela pai (ex: mainView).
    :param window: A janela que será centralizada (ex: CTkToplevel).
    :param width: Largura da janela.
    :param height: Altura da janela.
    """
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    pos_x = parent_x + (parent_width // 2) - (width // 2)
    pos_y = parent_y + (parent_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")


current_user = None

def setCurrentUser(user):
    """Define o usuário atualmente logado."""
    global current_user
    current_user = user

def getCurrentUser():
    """Obtém o usuário atualmente logado."""
    return current_user