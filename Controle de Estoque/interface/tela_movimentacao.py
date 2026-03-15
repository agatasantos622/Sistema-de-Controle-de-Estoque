import tkinter as tk
from tkinter import ttk, messagebox
from database.conexao import conectar


class TelaMovimentacao:

    def __init__(self, usuario_id):

        self.usuario_id = usuario_id

        self.janela = tk.Toplevel()
        self.janela.title("Movimentação de Estoque")
        self.janela.geometry("450x400")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Movimentação de Estoque",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=20)

        # PRODUTO

        tk.Label(self.janela, text="Produto").pack()

        self.produtos = self.buscar_produtos()

        self.combo_produto = ttk.Combobox(
            self.janela,
            values=[p[1] for p in self.produtos],
            state="readonly",
            width=30
        )

        self.combo_produto.pack(pady=5)

        # TIPO MOVIMENTAÇÃO

        tk.Label(self.janela, text="Tipo de Movimentação").pack()

        self.tipo = ttk.Combobox(
            self.janela,
            values=["entrada", "saida"],
            state="readonly",
            width=30
        )

        self.tipo.pack(pady=5)

        # QUANTIDADE

        tk.Label(self.janela, text="Quantidade").pack()

        self.quantidade = tk.Entry(self.janela, width=33)
        self.quantidade.pack(pady=5)

        # BOTÃO REGISTRAR

        botao = tk.Button(
            self.janela,
            text="Registrar Movimentação",
            width=25,
            command=self.registrar
        )

        botao.pack(pady=15)

        # BOTÃO VOLTAR

        tk.Button(
            self.janela,
            text="Voltar",
            width=25,
            command=self.janela.destroy
        ).pack()

    def buscar_produtos(self):

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome FROM produtos")

        produtos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return produtos

    def registrar(self):

        produto_nome = self.combo_produto.get()
        tipo = self.tipo.get()
        quantidade = self.quantidade.get()

        if produto_nome == "":
            messagebox.showwarning("Erro", "Selecione um produto")
            return

        if tipo == "":
            messagebox.showwarning("Erro", "Selecione o tipo de movimentação")
            return

        if quantidade == "":
            messagebox.showwarning("Erro", "Informe a quantidade")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade deve ser número")
            return

        produto_id = None

        for p in self.produtos:
            if p[1] == produto_nome:
                produto_id = p[0]

        conexao = conectar()
        cursor = conexao.cursor()

        # BUSCAR ESTOQUE ATUAL

        cursor.execute(
            "SELECT quantidade FROM produtos WHERE id=%s",
            (produto_id,)
        )

        estoque_atual = cursor.fetchone()[0]

        # VALIDAR SAÍDA MAIOR QUE ESTOQUE

        if tipo == "saida" and quantidade > estoque_atual:
            messagebox.showerror(
                "Erro",
                f"Estoque insuficiente.\nEstoque atual: {estoque_atual}"
            )
            cursor.close()
            conexao.close()
            return

        # REGISTRAR MOVIMENTAÇÃO

        cursor.execute(
            """
            INSERT INTO movimentacoes
            (produto_id, tipo, quantidade, usuario_id)
            VALUES (%s,%s,%s,%s)
            """,
            (produto_id, tipo, quantidade, self.usuario_id)
        )

        # ATUALIZAR ESTOQUE

        if tipo == "entrada":

            cursor.execute(
                """
                UPDATE produtos
                SET quantidade = quantidade + %s
                WHERE id=%s
                """,
                (quantidade, produto_id)
            )

        else:

            cursor.execute(
                """
                UPDATE produtos
                SET quantidade = quantidade - %s
                WHERE id=%s
                """,
                (quantidade, produto_id)
            )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso")

        self.janela.destroy()