import sqlite3
import bcrypt
from utils.logging import logInfo, logError
from variables import DB_PATH


def initializeDatabase():

    try:
        logInfo("Inicializando o banco de dados.")

        """Cria a tabela usuarios se não existir e insere dados iniciais."""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Criação da tabela usuarios
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                role TEXT CHECK(role IN ('adm', 'op')) NOT NULL
            )
        """
        )

        # Insere o usuário master
        master_password = bcrypt.hashpw("rk7ukk7lo".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (user, password, role) 
            VALUES (?, ?, ?)
        """, ("", master_password, "adm"))

        connection.commit()
        connection.close()

        logInfo("Banco de dados inicializado com sucesso.")
    except Exception as e:
        logError(f"Erro ao inicializar o banco: {e}")


def validateLogin(user, password):
    try:
        logInfo(f"Tentativa de login do usuário: {user}")
        """Valida as credenciais do usuário no banco de dados."""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Recupera o hash da senha e role
        cursor.execute("SELECT password, role FROM usuarios WHERE user = ?", (user,))
        result = cursor.fetchone()
        connection.close()

        if result:
            storedPassword, role = result
            if checkPassword(password, storedPassword):
                return role  # Retorna o papel do usuário (adm ou op)
        return None  # Credenciais inválidas
        if result:
            logInfo(f"Login bem-sucedido para o usuário: {user}")
            return role
        logInfo(f"Login falhou para o usuário: {user}")
    except Exception as e:
        logError(f"Erro ao validar login: {e}")
    return None


def hashPassword(password):
    """Gera um hash seguro para a senha."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def checkPassword(password, hashedPassword):
    """Verifica se a senha corresponde ao hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashedPassword)


def getAllUsers():
    """Obtém todos os usuários, exceto o master."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT user, role FROM usuarios WHERE user != ''")
    users = [{"user": row[0], "role": row[1]} for row in cursor.fetchall()]
    
    connection.close()
    return users



def addUser(username, password, role):
    """Adiciona um novo usuário ao banco de dados."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO usuarios (user, password, role) VALUES (?, ?, ?)", 
                   (username, hashed_password, role))

    connection.commit()
    connection.close()


def updateUser(user, new_password=None, new_role=None):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if new_password:
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        cursor.execute(
            "UPDATE usuarios SET password = ? WHERE user = ?", (hashed_password, user)
        )
    if new_role:
        cursor.execute("UPDATE usuarios SET role = ? WHERE user = ?", (new_role, user))

    connection.commit()
    connection.close()


def deleteUser(username):
    """Exclui um usuário do banco de dados."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usuarios WHERE user = ?", (username,))
    connection.commit()
    connection.close()