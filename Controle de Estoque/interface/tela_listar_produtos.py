import tkinter as tk
from tkinter import ttk, messagebox
from database.conexao import conectar


class TelaListarProdutos:

    def __init__(self):

        self.janela = tk.Toplevel()
        self.janela.title("Lista de Produtos")
        self.janela.geometry("800x500")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Produtos Cadastrados",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=10)

        # FRAME PRINCIPAL
        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # FRAME DA TABELA
        frame_tabela = tk.Frame(frame_principal)
        frame_tabela.pack(side="left", fill="both", expand=True)

        # FRAME DOS BOTÕES
        frame_botoes = tk.Frame(frame_principal)
        frame_botoes.pack(side="right", padx=10)

        colunas = ("ID", "Nome", "Quantidade", "Estoque mínimo")

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings"
        )

        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Quantidade", text="Quantidade")
        self.tabela.heading("Estoque mínimo", text="Estoque mínimo")

        self.tabela.column("ID", width=60)
        self.tabela.column("Nome", width=220)
        self.tabela.column("Quantidade", width=120)
        self.tabela.column("Estoque mínimo", width=120)

        self.tabela.pack(side="left", fill="both", expand=True)

        # SCROLLBAR
        scrollbar = tk.Scrollbar(frame_tabela)
        scrollbar.pack(side="right", fill="y")

        self.tabela.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tabela.yview)

        # COR PARA ESTOQUE BAIXO
        self.tabela.tag_configure("baixo", background="#ffcccc")

        # BOTÕES

        tk.Button(
            frame_botoes,
            text="Atualizar",
            width=15,
            command=self.carregar_produtos
        ).pack(pady=5)

        tk.Button(
            frame_botoes,
            text="Excluir",
            width=15,
            command=self.excluir_produto
        ).pack(pady=5)

        tk.Button(
            frame_botoes,
            text="Voltar",
            width=15,
            command=self.janela.destroy
        ).pack(pady=20)

        self.carregar_produtos()

    def carregar_produtos(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()

        # CONSULTA COM ORDENAÇÃO
        cursor.execute(
            """
            SELECT id, nome, quantidade, estoque_minimo
            FROM produtos
            ORDER BY nome
            """
        )

        produtos = cursor.fetchall()

        for p in produtos:

            if p[2] <= p[3]:
                self.tabela.insert("", tk.END, values=p, tags=("baixo",))
            else:
                self.tabela.insert("", tk.END, values=p)

        cursor.close()
        conexao.close()

    def excluir_produto(self):

        item = self.tabela.selection()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto")
            return

        dados = self.tabela.item(item)["values"]
        id_produto = dados[0]

        confirmar = messagebox.askyesno(
            "Excluir",
            "Deseja excluir o produto?"
        )

        if not confirmar:
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM produtos WHERE id=%s",
            (id_produto,)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        self.carregar_produtos()