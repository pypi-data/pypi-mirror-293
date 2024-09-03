import tkinter as tk
from tkinter import messagebox
from .db_utils import buscar_planilha

def submit(entry_query, entry_banco, entry_servidor, entry_senha, entry_usuario, entry_nome_planilha):
    query = entry_query.get()
    banco = entry_banco.get()
    servidor = entry_servidor.get()
    senha = entry_senha.get()
    usuario = entry_usuario.get()
    nome_planilha = entry_nome_planilha.get()

    if not all([query, banco, servidor, senha, usuario, nome_planilha]):
        messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
        return

    buscar_planilha(query, banco, servidor, senha, usuario, nome_planilha)

def run():
    root = tk.Tk()
    root.title("Consulta ao Banco de Dados")

    tk.Label(root, text="Consulta SQL:").grid(row=0, column=0)
    entry_query = tk.Entry(root, width=50)
    entry_query.grid(row=0, column=1)

    tk.Label(root, text="Banco de Dados:").grid(row=1, column=0)
    entry_banco = tk.Entry(root, width=50)
    entry_banco.grid(row=1, column=1)

    tk.Label(root, text="Servidor:").grid(row=2, column=0)
    entry_servidor = tk.Entry(root, width=50)
    entry_servidor.grid(row=2, column=1)

    tk.Label(root, text="Usuário:").grid(row=3, column=0)
    entry_usuario = tk.Entry(root, width=50)
    entry_usuario.grid(row=3, column=1)

    tk.Label(root, text="Senha:").grid(row=4, column=0)
    entry_senha = tk.Entry(root, show='*', width=50)
    entry_senha.grid(row=4, column=1)

    tk.Label(root, text="Nome da Planilha:").grid(row=5, column=0)
    entry_nome_planilha = tk.Entry(root, width=50)
    entry_nome_planilha.grid(row=5, column=1)

    btn_submit = tk.Button(
        root,
        text="Buscar Planilha",
        command=lambda: submit(entry_query, entry_banco, entry_servidor, entry_senha, entry_usuario, entry_nome_planilha)
    )
    btn_submit.grid(row=6, columnspan=2)

    root.mainloop()

