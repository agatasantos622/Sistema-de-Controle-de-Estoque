import mysql.connector


def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Scarlet.2025",  # coloque sua senha do mysql se tiver
        database="controle_estoque"
    )

    return conexao