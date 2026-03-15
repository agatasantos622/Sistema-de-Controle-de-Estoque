import tkinter as tk
from database.conexao import conectar


class TelaHistorico:

    def __init__(self):

        self.janela = tk.Toplevel()
        self.janela.title("Histórico de Movimentações")
        self.janela.geometry("700x600")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Histórico de Movimentações",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=10)

        self.lista = tk.Listbox(self.janela, width=100)
        self.lista.pack(pady=20)

        self.carregar()

    def carregar(self):

        conexao = conectar()
        cursor = conexao.cursor()

        query = """
        SELECT
        m.id,
        p.nome,
        m.tipo,
        m.quantidade,
        m.data_movimentacao,
        u.nome
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        LEFT JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.data_movimentacao DESC
        """

        cursor.execute(query)

        movimentacoes = cursor.fetchall()

        for m in movimentacoes:

            texto = f"ID:{m[0]} | Produto:{m[1]} | Tipo:{m[2]} | Quantidade:{m[3]} | Data:{m[4]} | Usuário:{m[5]}"
            self.lista.insert(tk.END, texto)

        cursor.close()
        conexao.close()

        tk.Button(
            self.janela,
            text="Voltar",
            width=15,
            command=self.janela.destroy
        ).pack(pady=15)