import sqlite3
from variables import DB_PATH
import bcrypt
from utils.logging import logInfo, logError



def initializeDatabase():
    
    try:
        logInfo("Inicializando o banco de dados.")


        """Cria a tabela usuarios se não existir e insere dados iniciais."""
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Criação da tabela usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                role TEXT CHECK(role IN ('adm', 'op')) NOT NULL
            )
        ''')

        # Hash das senhas padrão
        adminPasswordHash = hashPassword("1234")
        operadorPasswordHash = hashPassword("5678")

        # Inserção de usuários padrões (caso não existam)
        cursor.execute("INSERT OR IGNORE INTO usuarios (user, password, role) VALUES (?, ?, ?)",
                    ("admin", adminPasswordHash, "adm"))
        cursor.execute("INSERT OR IGNORE INTO usuarios (user, password, role) VALUES (?, ?, ?)",
                    ("operador", operadorPasswordHash, "op"))

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
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def checkPassword(password, hashedPassword):
    """Verifica se a senha corresponde ao hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashedPassword)
