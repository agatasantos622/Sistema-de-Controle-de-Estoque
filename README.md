📦 Sistema de Controle de Estoque

Projeto acadêmico desenvolvido para aprendizado de Python, interface gráfica e banco de dados.

O sistema permite cadastrar produtos, registrar movimentações de entrada e saída, acompanhar o histórico das movimentações e gerenciar usuários do sistema.

🎯 Objetivo do Projeto

O objetivo deste projeto é aplicar conceitos de programação em Python, desenvolvimento de interface gráfica e integração com banco de dados para criar um sistema simples de controle de estoque.

🛠 Tecnologias Utilizadas

- Python 3
- Tkinter (Interface gráfica)
- MySQL (Banco de dados)
- MySQL Connector Python
- Visual Studio Code

📋 Funcionalidades do Sistema

O sistema possui as seguintes funcionalidades:

- Login de usuários
- Cadastro de produtos
- Listagem de produtos
- Registro de movimentações de entrada e saída
- Histórico de movimentações
- Dashboard com informações do estoque
- Alerta de produtos com estoque baixo
- Cadastro e gerenciamento de usuários
- Controle de perfil (Administrador e Usuário comum)

🗂 Estrutura do Projeto

CONTROLE DE ESTOQUE/
- database/
    - conexao.py
    - DB_Controle_Estoque.sql
- interface/
    - tela_login.py
    - tela_menu.py
    - tela_produtos.py
    - tela_movimentacao.py
    - tela_historico.py
    - tela_usuarios.py
- main.py

🗄 Banco de Dados

O sistema utiliza um banco de dados MySQL chamado:

controle_estoque

Ele possui três tabelas principais:
- usuarios: Armazena os usuários do sistema
- produtos: Armazena os produtos cadastrados
- movimentacoes: Registra todas as movimentações de entrada e saída de produtos

▶ Como Executar o Sistema

- Instalar o MySQL
- Criar o banco de dados executando o script DB_Controle_Estoque.sql
- Instalar a biblioteca de conexão com o banco: pip install mysql-connector-python
- Executar o sistema com o comando: python main.py

👩‍💻 Autora

Ágata Oliveira
- Projeto desenvolvido para a disciplina Development with Python.
