import pymysql
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox


def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="agro_estoque",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


class MenuSistema:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Estoque")
        self.root.geometry("500x500")

        Label(self.root, text="MENU PRINCIPAL").pack(pady=20)

        Button(self.root, text="Cadastrar Produto", bg="green", fg="white",
               width=20, command=self.cadastrar).pack(padx=60, pady=50)

        Button(self.root, text="Visualizar Estoque",  bg="green", fg="white",
               width=20, command=self.visualizar).pack(padx=60, pady=50)

        Button(self.root, text="Excluir Produto", bg="green", fg="white",
               width=20, command=self.excluir).pack(padx=60, pady=50)

        Button(self.root, text="SAIR", bg="red", fg="white",
               width=10, command=self.root.destroy).pack(padx=60, pady=20 )
        
    
        
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
        self.janela.geometry("600x400")

        self.tree = ttk.Treeview(self.janela, 
                        columns=("id","nome", "preco", "quantidade"), 
                        show="headings")
        
        self.tree.heading("id", text="id")
        self.tree.heading("nome", text="nome")
        self.tree.heading("preco", text="preco")
        self.tree.heading("quantidade", text="quantidade")

        self.tree.column("id", width=50)
        self.tree.column("nome", width=150)
        self.tree.column("preco", width=100)
        self.tree.column("quantidade", width=100)

        Label(self.janela, text="Lista de Produtos").pack()

        self.tree.pack(fill=BOTH, expand=True)

        self.carregar_produtos()

    def carregar_produtos(self):
        try:
            con = conectar()
            cursor = con.cursor()

            cursor.execute("SELECT id, nome, preco, quantidade  FROM produtos")
            produtos = cursor.fetchall()

        except Exception as e:
            Label(self.janela, text=f"Erro: {e}").pack()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for produto in produtos:
            self.tree.insert("", END, values=(
                produto["id"],
                produto["nome"],
                produto["preco"], 
                produto["quantidade"]))   

class excluirProduto:

    def __init__(self, root_pai):
       self.janela = Toplevel(root_pai)
       self.janela.title("Ecluir Produto")
       self.janela.geometry("500x400")
    
       Label(self.janela, text='Nome do produto').grid(row=0, column=0, padx=60, pady=100)

       self.nome = Entry(self.janela)
       self.nome.grid(row=0, column=1, padx=60, pady=100)

       Button(self.janela, text="Excluir", bg="red", fg="white",
               command=self.excluir).grid(row=3, column=0, pady=20)
       
       Button(self.janela, text='Voltar', fg="red", 
              command=self.janela.destroy).grid(row=3, column=1, pady=20)

    def excluir(self):
        produtos = self.nome.get()

        con = conectar()
        cursor = con.cursor()

        sql = "DELETE FROM produtos WHERE nome = %s"
        cursor.execute(sql, (produtos,))

        con.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso, Produto não encontrado")
        else:
            messagebox.showinfo("Sucesso, Produto excluido")

        self.janela.destroy()


class TelaCadastro:

    def __init__(self, root_pai):
        self.janela = Toplevel(root_pai)
        self.janela.title("Cadastro de Produto")
        self.janela.geometry("500x500")

        Label(self.janela, text='Nome do produto').grid(row=0, column=0, padx=50, pady=50)
        self.nome = Entry(self.janela)
        self.nome.grid(row=0, column=1, padx=50, pady=50)

        Label(self.janela, text='Preço').grid(row=1, column=0, padx=50, pady=20)
        self.preco = Entry(self.janela)
        self.preco.grid(row=1, column=1, padx=50, pady=50)

        Label(self.janela, text='Quantidade').grid(row=2, column=0, padx=50, pady=50)
        self.quantidade = Entry(self.janela)
        self.quantidade.grid(row=2, column=1, padx=50, pady=50)

        Button(self.janela, text="Salvar", bg="green", fg="white",
               command=self.salvar).grid(row=4, column=0, padx=30, pady=20)
        Button(self.janela, text="Voltar", bg="red", fg="white",
               command=self.janela.destroy).grid(row=4, column=1, padx=30, pady=20)
     
    def salvar(self):
        nome = self.nome.get()
        preco = self.preco.get()
        quantidade = self.quantidade.get()

        con = conectar()
        cursor = con.cursor()

        sql = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, preco, quantidade))
        con.commit()

        cursor.close()
        con.close()

        messagebox.showinfo("Sucesso", "Produto cadastrado!")
        self.janela.destroy()


class JanelaLogin:

    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
        self.root.geometry("400x500")

        Label(self.root, text='Usuário').grid(row=0, column=0, padx=80, pady=90)
        self.login = Entry(self.root)
        self.login.grid(row=0, column=1, padx=10)

        Label(self.root, text='Senha').grid(row=1, column=0, padx=80, pady=20 )
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=1, column=1, padx=10)

        Button(self.root, text='ENTRAR', bg="green", fg="white",
               command=self.verificar_login).grid(row=2, column=0, pady=100)
        Button(self.root, text="SAIR", bg="red", fg="white",
               command=self.root.destroy).grid(row=2, column=1, pady=100)
        
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
