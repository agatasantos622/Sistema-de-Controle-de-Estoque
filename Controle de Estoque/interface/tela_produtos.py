import tkinter as tk
from interface.tela_cadastro_produto import TelaCadastroProduto
from interface.tela_listar_produtos import TelaListarProdutos


class TelaProdutos:

    def __init__(self, usuario_id):

        self.usuario_id = usuario_id

        self.janela = tk.Toplevel()
        self.janela.title("Produtos")
        self.janela.geometry("700x600")
        self.janela.resizable(False, False)

        titulo = tk.Label(
            self.janela,
            text="Gestão de Produtos",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=20)

        botao_cadastrar = tk.Button(
            self.janela,
            text="Cadastrar Produto",
            width=25,
            height=2,
            command=self.cadastrar
        )
        botao_cadastrar.pack(pady=10)

        botao_listar = tk.Button(
            self.janela,
            text="Listar Produtos",
            width=25,
            height=2,
            command=self.listar
        )
        botao_listar.pack(pady=10)

        botao_voltar = tk.Button(
            self.janela,
            text="Voltar",
            width=25,
            height=2,
            command=self.janela.destroy
        )
        botao_voltar.pack(pady=20)

    def cadastrar(self):
        TelaCadastroProduto()

    def listar(self):
        TelaListarProdutos()