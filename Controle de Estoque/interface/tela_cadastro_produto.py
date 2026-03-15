import tkinter as tk
from tkinter import messagebox
from database.conexao import conectar


class TelaCadastroProduto:

    def __init__(self):

        self.janela = tk.Toplevel()
        self.janela.title("Cadastrar Produto")
        self.janela.geometry("700x600")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Cadastro de Produto",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)

        # NOME

        tk.Label(self.janela, text="Nome do Produto").pack()
        self.nome = tk.Entry(self.janela, width=30)
        self.nome.pack(pady=5)

        # DESCRIÇÃO

        tk.Label(self.janela, text="Descrição").pack()
        self.descricao = tk.Entry(self.janela, width=30)
        self.descricao.pack(pady=5)

        # QUANTIDADE

        tk.Label(self.janela, text="Quantidade").pack()
        self.quantidade = tk.Entry(self.janela, width=30)
        self.quantidade.pack(pady=5)

        # ESTOQUE MÍNIMO

        tk.Label(self.janela, text="Estoque mínimo").pack()
        self.estoque_minimo = tk.Entry(self.janela, width=30)
        self.estoque_minimo.pack(pady=5)

        # BOTÃO SALVAR

        botao_salvar = tk.Button(
            self.janela,
            text="Salvar",
            width=20,
            command=self.salvar
        )
        botao_salvar.pack(pady=10)

        # BOTÃO VOLTAR

        botao_voltar = tk.Button(
            self.janela,
            text="Voltar",
            width=20,
            command=self.janela.destroy
        )
        botao_voltar.pack()

    def salvar(self):

        nome = self.nome.get()
        descricao = self.descricao.get()
        quantidade = self.quantidade.get()
        estoque_minimo = self.estoque_minimo.get()

        # VALIDAÇÕES

        if nome == "":
            messagebox.showwarning("Erro", "Informe o nome do produto")
            return

        if quantidade == "":
            messagebox.showwarning("Erro", "Informe a quantidade")
            return

        if estoque_minimo == "":
            messagebox.showwarning("Erro", "Informe o estoque mínimo")
            return

        # VALIDAR NÚMEROS

        try:
            quantidade = int(quantidade)
            estoque_minimo = int(estoque_minimo)
        except ValueError:
            messagebox.showwarning(
                "Erro",
                "Quantidade e estoque mínimo devem ser números"
            )
            return

        # INSERIR NO BANCO

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO produtos
            (nome, descricao, quantidade, estoque_minimo)
            VALUES (%s,%s,%s,%s)
            """,
            (nome, descricao, quantidade, estoque_minimo)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")

        self.janela.destroy()