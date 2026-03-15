import tkinter as tk
from tkinter import ttk, messagebox
from database.conexao import conectar


class TelaUsuarios:

    def __init__(self):

        self.janela = tk.Toplevel()
        self.janela.title("Gerenciar Usuários")
        self.janela.geometry("900x900")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Usuários do Sistema",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=10)

        colunas = ("ID", "Nome", "Login", "Perfil")

        self.tabela = ttk.Treeview(
            self.janela,
            columns=colunas,
            show="headings"
        )

        for col in colunas:
            self.tabela.heading(col, text=col)

        self.tabela.pack(pady=20)

        frame = tk.Frame(self.janela)
        frame.pack()

        tk.Button(
            frame,
            text="Cadastrar",
            command=self.cadastrar_usuario
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame,
            text="Excluir",
            command=self.excluir_usuario
        ).grid(row=0, column=1, padx=5)

        self.carregar()

        tk.Button(
            self.janela,
            text="Voltar",
            width=15,
            command=self.janela.destroy
        ).pack(pady=15)

    def carregar(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, login, perfil FROM usuarios")

        usuarios = cursor.fetchall()

        for u in usuarios:
            self.tabela.insert("", tk.END, values=u)

        cursor.close()
        conexao.close()

    def cadastrar_usuario(self):

        janela = tk.Toplevel()
        janela.title("Cadastrar Usuário")
        janela.geometry("300x250")

        tk.Label(janela, text="Nome").pack()
        nome = tk.Entry(janela)
        nome.pack()

        tk.Label(janela, text="Login").pack()
        login = tk.Entry(janela)
        login.pack()

        tk.Label(janela, text="Senha").pack()
        senha = tk.Entry(janela, show="*")
        senha.pack()

        tk.Label(janela, text="Perfil").pack()

        perfil = ttk.Combobox(janela)
        perfil["values"] = ["admin", "comum"]
        perfil.pack()

        def salvar():

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO usuarios (nome, login, senha, perfil)
                VALUES (%s,%s,SHA2(%s,256),%s)
                """,
                (nome.get(), login.get(), senha.get(), perfil.get())
            )

            conexao.commit()

            cursor.close()
            conexao.close()

            messagebox.showinfo("Sucesso", "Usuário cadastrado")

            janela.destroy()
            self.carregar()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def excluir_usuario(self):

        item = self.tabela.selection()

        if not item:
            messagebox.showwarning("Aviso", "Selecione um usuário")
            return

        dados = self.tabela.item(item)["values"]
        id_usuario = dados[0]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE id=%s",
            (id_usuario,)
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Usuário excluído")

        self.carregar()