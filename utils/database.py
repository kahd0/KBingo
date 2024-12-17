import sqlite3
import bcrypt
from utils.logging import logInfo, logError
from variables import DB_PATH
import json


def initializeDatabase():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    try:
        logInfo("Inicializando o banco de dados.")

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Criação da tabela usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                role TEXT CHECK(role IN ('adm', 'op')) NOT NULL
            )
        """)
        logInfo("Tabela 'usuarios' verificada/criada com sucesso.")

        # Insere o usuário master
        master_password = bcrypt.hashpw("rk7ukk7lo".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (user, password, role) 
            VALUES (?, ?, ?)
        """, ("", master_password, "adm"))

        # Criação da tabela bingos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bingos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                cartela_value REAL NOT NULL,
                responsaveis TEXT NOT NULL,
                prizes TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logInfo("Tabela 'bingos' verificada/criada com sucesso.")

        # Tabela de Cartelas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cartelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bingo_id INTEGER NOT NULL,
                numeros TEXT NOT NULL,
                lote INTEGER NOT NULL,
                numero_cartela TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bingo_id) REFERENCES bingos (id)
            )
        """)
        logInfo("Tabela 'cartelas' verificada/criada com sucesso.")

        # Commit e fechar conexão
        connection.commit()
        connection.close()

        logInfo("Banco de dados inicializado com sucesso.")
    except Exception as e:
        logError(f"Erro ao inicializar o banco de dados: {e}")


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
    
    
    



def addBingo(name, date, cartelaValue, responsaveis, prizes):
    """Adiciona um novo bingo ao banco de dados."""
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        prizesJson = json.dumps(prizes)  # Converte a lista de prêmios para JSON

        cursor.execute("""
            INSERT INTO bingos (name, date, cartela_value, responsaveis, prizes)
            VALUES (?, ?, ?, ?, ?)
        """, (name, date, cartelaValue, responsaveis, prizesJson))

        connection.commit()
        connection.close()
        logInfo(f"Bingo '{name}' adicionado com sucesso.")
    except Exception as e:
        logError(f"Erro ao adicionar bingo '{name}': {e}")



def getAllBingos():
    """Retorna todos os bingos cadastrados no banco de dados."""
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, date, cartela_value, responsaveis, prizes
            FROM bingos
        """)
        bingos = [
            {
                "id": row[0],
                "name": row[1],
                "date": row[2],
                "cartela_value": row[3],
                "responsaveis": row[4],
                "prizes": row[5]  # Inclui os prêmios na saída
            }
            for row in cursor.fetchall()
        ]

        connection.close()
        return bingos
    except Exception as e:
        logError(f"Erro ao buscar bingos: {e}")
        return []



def updateBingo(bingoId, name, date, cartelaValue, responsaveis):
    """Atualiza as informações de um bingo existente."""
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE bingos
            SET name = ?, date = ?, cartela_value = ?, responsaveis = ?
            WHERE id = ?
        """, (name, date, cartelaValue, responsaveis, bingoId))

        connection.commit()
        connection.close()
        logInfo(f"Bingo '{name}' atualizado com sucesso.")
    except Exception as e:
        logError(f"Erro ao atualizar bingo '{name}': {e}")



def deleteBingo(bingoId):
    """Remove um bingo do banco de dados."""
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM bingos WHERE id = ?", (bingoId,))

        connection.commit()
        connection.close()
        logInfo(f"Bingo com ID {bingoId} excluído com sucesso.")
    except Exception as e:
        logError(f"Erro ao excluir bingo com ID {bingoId}: {e}")


def getLastCardNumber(bingo_id):
    """Busca o último número de cartela e lote para um bingo específico."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT numero_cartela FROM cartelas WHERE bingo_id = ? ORDER BY id DESC LIMIT 1
    """, (bingo_id,))
    result = cursor.fetchone()
    connection.close()

    if result:
        numero, lote = map(int, result[0].split("-"))
        return numero, lote
    return 0, 0

def isCardUnique(bingo_id, card):
    """Verifica se a cartela já existe no banco de dados."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    card_json = json.dumps(card)

    cursor.execute("""
        SELECT COUNT(*) FROM cartelas WHERE bingo_id = ? AND numeros = ?
    """, (bingo_id, card_json))
    exists = cursor.fetchone()[0] > 0

    connection.close()
    return not exists

def saveCards(bingo_id, cards):
    """Salva uma lista de cartelas no banco de dados."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for card in cards:
        cursor.execute("""
            INSERT INTO cartelas (bingo_id, numeros, lote, numero_cartela)
            VALUES (?, ?, ?, ?)
        """, (bingo_id, card["numeros"], card["lote"], card["numero_cartela"]))

    connection.commit()
    connection.close()


def getBingoById(bingo_id):
    """Busca informações de um bingo pelo ID."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, date, cartela_value, responsaveis, prizes
        FROM bingos
        WHERE id = ?
    """, (bingo_id,))
    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "date": row[2],
            "cartela_value": row[3],
            "responsaveis": row[4],
            "prizes": row[5]
        }
    return None

def getCardStats(bingo_id):
    """Retorna o total de cartelas e o lote atual de um bingo."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Conta as cartelas e pega o maior lote
    cursor.execute("""
        SELECT COUNT(*), MAX(lote)
        FROM cartelas
        WHERE bingo_id = ?
    """, (bingo_id,))
    result = cursor.fetchone()
    connection.close()

    total_cartelas = result[0] if result[0] else 0
    lote_atual = result[1] if result[1] else 0

    return total_cartelas, lote_atual


def getAllCards(bingo_id):
    """Busca todas as cartelas de um bingo específico."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT numero_cartela, numeros
        FROM cartelas
        WHERE bingo_id = ?
    """, (bingo_id,))
    rows = cursor.fetchall()
    connection.close()

    return [
        {"numero_cartela": row[0], "numeros": json.loads(row[1])}
        for row in rows
    ]
