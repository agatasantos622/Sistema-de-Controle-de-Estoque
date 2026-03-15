import tkinter as tk
from tkinter import messagebox
from database.conexao import conectar

from interface.tela_produtos import TelaProdutos
from interface.tela_movimentacao import TelaMovimentacao
from interface.tela_historico import TelaHistorico
from interface.tela_usuarios import TelaUsuarios


class TelaMenu:

    def __init__(self, usuario_id):

        self.usuario_id = usuario_id

        self.janela = tk.Tk()
        self.janela.title("Sistema de Controle de Estoque")
        self.janela.geometry("600x520")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Controle de Estoque",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        # BUSCAR NOME DO USUÁRIO
        nome_usuario = self.buscar_nome_usuario()

        label_usuario = tk.Label(
            self.janela,
            text=f"Usuário logado: {nome_usuario}",
            font=("Arial", 10)
        )
        label_usuario.pack(pady=5)

        # DASHBOARD

        frame_dashboard = tk.Frame(self.janela)
        frame_dashboard.pack(pady=10)

        self.lbl_total_produtos = tk.Label(frame_dashboard)
        self.lbl_total_produtos.pack()

        self.lbl_estoque_baixo = tk.Label(frame_dashboard)
        self.lbl_estoque_baixo.pack()

        self.lbl_movimentacoes = tk.Label(frame_dashboard)
        self.lbl_movimentacoes.pack()

        # BOTÃO ATUALIZAR DASHBOARD
        tk.Button(
            frame_dashboard,
            text="🔄 Atualizar Dashboard",
            width=20,
            command=self.carregar_dashboard
        ).pack(pady=5)

        self.carregar_dashboard()

        # BOTÕES

        tk.Button(
            self.janela,
            text="Produtos",
            width=25,
            height=2,
            command=self.abrir_produtos
        ).pack(pady=5)

        tk.Button(
            self.janela,
            text="Movimentações",
            width=25,
            height=2,
            command=self.abrir_movimentacao
        ).pack(pady=5)

        tk.Button(
            self.janela,
            text="Histórico de Movimentações",
            width=25,
            height=2,
            command=self.abrir_historico
        ).pack(pady=5)

        tk.Button(
            self.janela,
            text="Usuários",
            width=25,
            height=2,
            command=self.abrir_usuarios
        ).pack(pady=5)

        tk.Button(
            self.janela,
            text="Sair",
            width=25,
            height=2,
            command=self.sair
        ).pack(pady=15)

        self.verificar_estoque()

        self.janela.mainloop()

    # BUSCAR NOME DO USUÁRIO

    def buscar_nome_usuario(self):

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM usuarios WHERE id=%s",
            (self.usuario_id,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        if resultado:
            return resultado[0]
        else:
            return "Usuário"

    # DASHBOARD

    def carregar_dashboard(self):

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM produtos")
        total_produtos = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM produtos
            WHERE quantidade <= estoque_minimo
            """
        )
        estoque_baixo = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM movimentacoes")
        total_mov = cursor.fetchone()[0]

        cursor.close()
        conexao.close()

        self.lbl_total_produtos.config(
            text=f"Total de produtos cadastrados: {total_produtos}"
        )

        self.lbl_estoque_baixo.config(
            text=f"Produtos com estoque baixo: {estoque_baixo}"
        )

        self.lbl_movimentacoes.config(
            text=f"Total de movimentações: {total_mov}"
        )

    # ALERTA DE ESTOQUE

    def verificar_estoque(self):

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT nome, quantidade
            FROM produtos
            WHERE quantidade <= estoque_minimo
            """
        )

        produtos = cursor.fetchall()

        cursor.close()
        conexao.close()

        if produtos:

            mensagem = "⚠ Produtos com estoque baixo:\n\n"

            for p in produtos:
                mensagem += f"{p[0]} (Estoque: {p[1]})\n"

            messagebox.showwarning("Estoque baixo", mensagem)

    # ABRIR TELAS

    def abrir_produtos(self):
        TelaProdutos(self.usuario_id)

    def abrir_movimentacao(self):
        TelaMovimentacao(self.usuario_id)

    def abrir_historico(self):
        TelaHistorico()

    def abrir_usuarios(self):
        TelaUsuarios()

    # SAIR

    def sair(self):

        confirmar = messagebox.askyesno(
            "Sair do sistema",
            "Deseja realmente sair?"
        )

        if confirmar:
            self.janela.destroy()