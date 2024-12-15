from src.utils.database import get_user
import bcrypt

def authenticate(username, password):
    """
    Autentica o usuário verificando a senha com hash bcrypt.
    """
    user = get_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return True, user[2]  # Retorna True e o role do usuário
    return False, None
