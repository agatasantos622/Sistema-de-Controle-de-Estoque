import tkinter as tk
from tkinter import messagebox
from database.conexao import conectar
from interface.tela_menu import TelaMenu


class TelaLogin:

    def __init__(self):

        self.janela = tk.Tk()
        self.janela.title("Login - Controle de Estoque")
        self.janela.geometry("700x600")
        self.janela.resizable(False, False)

        titulo = tk.Label(self.janela, text="Login", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        tk.Label(self.janela, text="Usuário").pack()
        self.entry_login = tk.Entry(self.janela)
        self.entry_login.pack(pady=5)

        tk.Label(self.janela, text="Senha").pack()
        self.entry_senha = tk.Entry(self.janela, show="*")
        self.entry_senha.pack(pady=5)

        botao_login = tk.Button(
            self.janela,
            text="Entrar",
            width=20,
            command=self.fazer_login
        )
        botao_login.pack(pady=20)

        self.janela.mainloop()

    def fazer_login(self):

        login = self.entry_login.get()
        senha = self.entry_senha.get()

        conexao = conectar()
        cursor = conexao.cursor()

        query = """
        SELECT id, nome, perfil
        FROM usuarios
        WHERE login = %s AND senha = SHA2(%s,256)
        """

        cursor.execute(query, (login, senha))
        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if usuario:
            messagebox.showinfo("Sucesso", "Login realizado!")

            self.janela.destroy()

            usuario_id = usuario[0]
            TelaMenu(usuario_id)

        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")