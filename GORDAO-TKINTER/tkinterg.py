import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class AcademiaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academia App")

        # Conectar ao banco de dados
        self.conn = sqlite3.connect('academia.sqlite')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS aluno (
                            matricula TEXT PRIMARY KEY,
                            nome TEXT,
                            mensalidade REAL)''')
        self.conn.commit()

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#E1D8B9')
        self.style.configure('TButton', background='#6B8E23')
        self.style.configure('TLabel', background='#E1D8B9')
        self.style.configure('TEntry', background='#FFF')
        self.style.configure('Treeview', background='#FFF')

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.lbl_matricula = ttk.Label(self.frame, text="Matrícula:")
        self.lbl_matricula.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_matricula = ttk.Entry(self.frame)
        self.entry_matricula.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_nome = ttk.Label(self.frame, text="Nome:")
        self.lbl_nome.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = ttk.Entry(self.frame)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_mensalidade = ttk.Label(self.frame, text="Mensalidade:")
        self.lbl_mensalidade.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_mensalidade = ttk.Entry(self.frame)
        self.entry_mensalidade.grid(row=2, column=1, padx=5, pady=5)

        self.btn_adicionar = ttk.Button(self.frame, text="Adicionar", command=self.adicionar_aluno)
        self.btn_adicionar.grid(row=0, column=2, padx=5, pady=5)

        self.btn_editar = ttk.Button(self.frame, text="Editar", command=self.editar_aluno)
        self.btn_editar.grid(row=1, column=2, padx=5, pady=5)

        self.btn_excluir = ttk.Button(self.frame, text="Excluir", command=self.excluir_aluno)
        self.btn_excluir.grid(row=2, column=2, padx=5, pady=5)

        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(pady=20)

        self.table = ttk.Treeview(self.table_frame, columns=('matricula', 'nome', 'mensalidade'), show='headings', selectmode='browse')
        self.table.column('matricula', width=100)
        self.table.column('nome', width=200)
        self.table.column('mensalidade', width=100)
        self.table.heading('matricula', text='Matrícula')
        self.table.heading('nome', text='Nome')
        self.table.heading('mensalidade', text='Mensalidade')
        self.table.pack(side='left', fill='both')

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.table.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.carregar_alunos()

    def adicionar_aluno(self):
        matricula = self.entry_matricula.get()
        nome = self.entry_nome.get()
        mensalidade = self.entry_mensalidade.get()

        if matricula and nome and mensalidade:
            try:
                self.c.execute("INSERT INTO aluno (matricula, nome, mensalidade) VALUES (?, ?, ?)", (matricula, nome, mensalidade))
                self.conn.commit()
                self.carregar_alunos()
                self.limpar_campos()
            except sqlite3.Error as e:
                messagebox.showwarning("Erro", str(e))
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")

    def editar_aluno(self):
        selecionado = self.table.selection()

        if selecionado:
            registro = self.table.item(selecionado)
            matricula = registro['values'][0]
            nome = self.entry_nome.get()
            mensalidade = self.entry_mensalidade.get()

            if nome and mensalidade:
                try:
                    self.c.execute("UPDATE aluno SET nome=?, mensalidade=? WHERE matricula=?", (nome, mensalidade, matricula))
                    self.conn.commit()
                    self.carregar_alunos()
                    self.limpar_campos()
                except sqlite3.Error as e:
                    messagebox.showwarning("Erro", str(e))
            else:
                messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
        else:
            messagebox.showwarning("Aviso", "Selecione um aluno para editar!")

    def excluir_aluno(self):
        selecionado = self.table.selection()

        if selecionado:
            confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir o aluno?")

            if confirmacao:
                registro = self.table.item(selecionado)
                matricula = registro['values'][0]

                self.c.execute("DELETE FROM aluno WHERE matricula=?", (matricula,))
                self.conn.commit()
                self.carregar_alunos()
                self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione um aluno para excluir!")

    def carregar_alunos(self):
        self.table.delete(*self.table.get_children())

        self.c.execute("SELECT * FROM aluno")
        alunos = self.c.fetchall()

        for aluno in alunos:
            self.table.insert('', 'end', values=aluno)

    def limpar_campos(self):
        self.entry_matricula.delete(0, 'end')
        self.entry_nome.delete(0, 'end')
        self.entry_mensalidade.delete(0, 'end')

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.lbl_username = ttk.Label(self.frame, text="Usuário:")
        self.lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_password = ttk.Label(self.frame, text="Senha:")
        self.lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(self.frame, show='*')
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.btn_login = ttk.Button(self.frame, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.btn_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.abrir_tela_cadastro)
        self.btn_cadastrar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "admin":
            self.root.destroy()
            root = tk.Tk()
            app = AcademiaApp(root)
            root.mainloop()
        else:
            messagebox.showwarning("Login", "Usuário ou senha incorretos!")

    def abrir_tela_cadastro(self):
        self.root.destroy()
        root = tk.Tk()
        cadastro_page = CadastroPage(root)
        root.mainloop()

class CadastroPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro")
        self.root.geometry("300x150")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.lbl_username = ttk.Label(self.frame, text="Novo Usuário:")
        self.lbl_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_password = ttk.Label(self.frame, text="Nova Senha:")
        self.lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(self.frame, show='*')
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.btn_cadastrar = ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def cadastrar(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            self.root.destroy()
            root = tk.Tk()
            login_page = LoginPage(root)
            root.mainloop()
        else:
            messagebox.showwarning("Cadastro", "Por favor, preencha todos os campos!")


root = tk.Tk()
login_page = LoginPage(root)
root.mainloop()
