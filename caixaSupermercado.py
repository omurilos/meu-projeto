import pymysql
from tkinter import *
 
from tkinter import messagebox


def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="erp",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


class MenuSistema:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Estoque")

        Label(self.root, text="MENU PRINCIPAL").pack(pady=10)

        Button(self.root, text="Cadastrar Produto",
               width=20, command=self.cadastrar).pack(pady=5)

        Button(self.root, text="Visualizar Estoque",
               width=20, command=self.visualizar).pack(pady=5)

        Button(self.root, text="Excluir Produto",
               width=20, command=self.excluir).pack(pady=5)
        
    def excluir(self):
        excluirProduto(self.root)

    def cadastrar(self):
        TelaCadastro(self.root)

    def visualizar(self):
        visualizarProduto(self.root)

class visualizarProduto:


    def __init__(self, root_pai):
        self.janela = Toplevel(root_pai)
        self.janela.title("Visualizar Produtos")

        Label(self.janela, text="Lista de Produtos").pack()

        self.lista = Listbox(self.janela, width=50)
        self.lista.pack()

        self.carregar_produtos()

    def carregar_produtos(self):
        try:
            con = conectar()
            cursor = con.cursor()

            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()

        except Exception as e:
            Label(self.janela, text=f"Erro: {e}").pack()
            return

        if len(produtos) == 0:
            self.lista.insert(END, "Nenhum produto encontrado")
            return

        for produto in produtos:
            texto = f"ID: {produto[0]} | Nome: {produto[1]} | Preço: {produto[2]}"
            self.lista.insert(END, texto)
       

class excluirProduto:

    def __init__(self, root_pai):
       self.janela = Toplevel(root_pai)
       self.janela.title("Ecluir Produto")

       Label(self.janela, text='Nome do produto').grid(row=0, column=0)

       self.nome = Entry(self.janela)
       self.nome.grid(row=0, column=1)

       Button(self.janela, text="Excluir",
               command=self.excluir).grid(row=1, column=0, columnspan=2)
       
       
    def excluir(self):
        produto = self.nome.get()

        con = conectar()
        cursor = con.cursor()

        sql = "DELETE FROM produtos WHERE nome = %s"
        cursor.execute(sql, (produto,))
        con.commit()

        messagebox.showinfo("Sucesso", "Produto excluido")
        self.janela.destroy()


class TelaCadastro:

    def __init__(self, root_pai):
        self.janela = Toplevel(root_pai)
        self.janela.title("Cadastro de Produto")

        Label(self.janela, text='Nome do produto').grid(row=0, column=0)

        self.nome = Entry(self.janela)
        self.nome.grid(row=0, column=1)

        Button(self.janela, text="Salvar",
               command=self.salvar).grid(row=1, column=0, columnspan=2)

    def salvar(self):
        produto = self.nome.get()

        con = conectar()
        cursor = con.cursor()

        sql = "INSERT INTO produtos (nome) VALUES (%s)"
        cursor.execute(sql, (produto,))
        con.commit()

        messagebox.showinfo("Sucesso", "Produto cadastrado!")
        self.janela.destroy()


class JanelaLogin:

    def __init__(self):
        self.root = Tk()
        self.root.title('Login')

        Label(self.root, text='Usuário').grid(row=0, column=0, padx=40, pady=20)
        self.login = Entry(self.root)
        self.login.grid(row=0, column=1, padx=20, pady=20)

        Label(self.root, text='Senha').grid(row=1, column=0, padx=40, pady=20 )
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=1, column=1, padx=20, pady=20)

        Button(self.root, text='ENTRAR',
               command=self.verificar_login).grid(row=3, column=0, columnspan=2, pady=20)

        self.root.mainloop()

    
    def verificar_login(self):
        usuario = self.login.get()
        senha = self.senha.get()

        con = conectar()
        cursor = con.cursor()

        sql = "SELECT * FROM cadastros WHERE nome=%s AND senha=%s"
        cursor.execute(sql, (usuario, senha))

        if cursor.fetchone():
            messagebox.showinfo("Login", "Sucesso!")

            
            self.root.withdraw()

        
            nova_janela = Toplevel(self.root)
            MenuSistema(nova_janela)

        else:
            messagebox.showerror("Erro", "Login inválido")
    


JanelaLogin()
