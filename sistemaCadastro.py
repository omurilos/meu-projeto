import pymysql
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox


conexao = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db="cadastro",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
)


class telaCadastro:
 
   
    def __init__(self):
        self.pai = Tk()
        self.pai.title("Tela Inicio")
        self.pai.geometry('550x250')
        self.pai.configure(bg='#2c3e50')

        Label(self.pai, text='CADASTRO', bg="#CA6913", fg='white').grid(row=0, column=2, columnspan=2, pady=15)
                    
                    
        Label(self.pai, text='Nome', bg="#E67E22", fg='white').grid(row=3, padx=15, pady=5 )
        self.nome = Entry(self.pai, width=30)
        self.nome.grid(row=3, column=3)

        Label(self.pai, text='Data de Nascimento', bg="#E67E22", fg='white').grid(row=4, padx=15, pady=5)
        self.idade = Entry(self.pai, width=30)
        self.idade.grid(row=4, column=3)

        Label(self.pai, text='E-mail', bg="#E67E22", fg='white').grid(row=5, padx=15, pady=5)
        self.email = Entry(self.pai, width=30)
        self.email.grid(row=5, column=3)

        Label(self.pai, text='Senha', bg="#E67E22", fg='white').grid(row=6, padx=15, pady=5)
        self.senha = Entry(self.pai, width=30, show='*')
        self.senha.grid(row=6, column=3)


        Label(self.pai, text='Telefone', bg="#E67E22", fg='white').grid(row=7, padx=15, pady=5)
        self.telefone = Entry(self.pai, width=30)
        self.telefone.grid(row=7, column=3)

            

        Button(self.pai, text='CADASTRAR', width=25, fg='white', bg="#006912", command=self.cadastrar).grid(row=4, column=4, padx=20)

        Label(self.pai, text='Já possui um cadastro?', bg='#2c3e50', fg="#FFFFFF" ).grid(row=6, column=4)
        Button(self.pai, text='LOGIN', width=25, fg='white', bg="#0e4985", command=self.entrar).grid(row=7, column=4, padx=20)

        self.pai.mainloop()

    def cadastrar (self):
        nome = self.nome.get()
        idade = self.idade.get()
        email = self.email.get()
        senha = self.senha.get()
        telefone = self.telefone.get()

        try:
            with conexao.cursor() as cursor:
                sql = 'INSERT INTO usuarios (nome, idade, email, senha, telefone) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(sql, (nome, idade, email, senha, telefone))
                conexao.commit()
                messagebox.showinfo("Sucesso", "Usuario cadastrado!")
                
        except Exception as e:
            print(f'Não foi possível cadastrar: {e}')

    def entrar(self):
       telaentrada(self.pai)
        
class telaentrada:  

    def __init__(self, root_pai):
        self.entra = Toplevel(root_pai)
        self.entra.title('Tela do Usuario')
        self.entra.configure(bg='#2c3e50')
        self.entra.geometry('430x250')

        Label(self.entra, text='LOGIN', bg='#E67E22', fg='white').grid(row=0, column=0, columnspan=2, padx= 20, pady=20)

        Label(self.entra, text='Email',bg='#2c3e50', fg='white').grid(row=1, column=0, pady=30)
        self.email = Entry(self.entra, width=25)
        self.email.grid(row=1, column=1)

        Label(self.entra, text='Senha', bg='#2c3e50', fg='white').grid(row=2, column=0)
        self.senha = Entry(self.entra, width=25, show='*')
        self.senha.grid(row=2, column=1)

        Button(self.entra, text='ENTRAR', width=20, fg='white', bg="#0e4985", command=self.logar).grid(row=3, column=0, padx=30, pady=40)
        Button(self.entra, text='VOLTAR', width=20, bg='red', fg='white', command=self.voltar).grid(row=3, column=1)

    def voltar(self):
        self.entra.destroy()

    def logar(self):
        email = self.email.get()
        senha = self.senha.get()
        
        try:
            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = 'select * from usuarios where email = %s and senha = %s '
                cursor.execute(sql, (email, senha))

                usuario_encontrado = cursor.fetchone()
                    
                if usuario_encontrado:
                    tipo = usuario_encontrado['tipo_usuario']   
                
                    if tipo == 'Comum':
                        self.entra.withdraw()
                        messagebox.showinfo('Logado', 'Bem-vindo Usuário!')
                        self.comum()

                    elif tipo == 'Admin':
                        self.entra.withdraw()
                        messagebox.showinfo('Logado', 'Bem-vindo Administrador!')
                        self.admin()
                
                else:
                    messagebox.showerror('Erro', 'E-mail ou senha inválidos.')
                        
        except Exception as e:
            print(f'ERRO NO LOGIN: {e}')

        
    def comum(self):
            telaComum(self.entra)

    def admin(self):
            telaAdmin(self.entra)


class telaComum:  

    def __init__(self, root_pai):
        self.entra = Toplevel(root_pai)
        self.entra.title('Tela Inicio')
        self.entra.configure(bg='#2c3e50')
        self.entra.geometry('550x250')
                            
class telaAdmin:  

    def __init__(self, root_pai):
        self.admin = Toplevel(root_pai)
        self.admin.title('Tela Admin')
        self.admin.configure(bg='#2c3e50')
        self.admin.geometry('700x600') 

        frame_pesquisa = Frame(self.admin, bg='#2c3e50' )
        frame_pesquisa.pack(fill=X, padx=15,pady=15)

        Label(frame_pesquisa, text='PESQUISAR POR ID', bg='#2c3e50', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        
        self.input_pesquisa = Entry(frame_pesquisa, width=10)
        self.input_pesquisa.grid(row=0, column=1, padx=5)

        btn_pesquisar = Button(frame_pesquisa, text='PESQUISAR', command=self.pesquisar, bg='#0e4985', fg='white')
        btn_pesquisar.grid(row=0, column=2, padx=5)

        frame_tabela = LabelFrame(self.admin, text="LISTA DE USUÁRIOS ", fg="green", bg='#2c3e50', font=('Arial', 10, 'bold'), padx=10, pady=10)
        frame_tabela.pack(fill=BOTH, expand=True, pady=10)

        colunas = ("id", "nome", 'idade', "email", "senha", 'telefone', 'data_cadastro' )

        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")


        self.tabela.heading("id", text="Id")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.heading("email", text="Email")
        self.tabela.heading("senha", text="Senha")
        self.tabela.heading("telefone", text="Telefone")
        self.tabela.heading("data_cadastro", text="Data e Hora")

        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("nome", width=120)
        self.tabela.column("idade", width=60)
        self.tabela.column("email", width=150)
        self.tabela.column("senha", width=90)
        self.tabela.column("telefone", width=110)
        self.tabela.column("data_cadastro",  width=120)

        scroll_y = Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll_y.set)

        self.tabela.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_y.pack(side=RIGHT, fill=Y)          
       
        self.tabela.bind("<Double-1>", self.abrir_detalhes)
        self.carregar_info()

    def abrir_detalhes(self, event):
        janeladetalhes(self.tabela)



    def pesquisar(self):
        id = self.input_pesquisa.get()

        if not id:
            self.carregar_info()
            return

        try:
            with conexao.cursor() as cursor:
                sql = 'SELECT id, nome, idade, email, senha, telefone, data_cadastro FROM usuarios WHERE id = %s'
                cursor.execute(sql, (id))

                usuario = cursor.fetchone()

                for item in self.tabela.get_children():
                    self.tabela.delete(item)

                if usuario:
                    self.tabela.insert("", "end", values=(
                        usuario['id'],
                        usuario['nome'],
                        usuario['idade'],
                        usuario['email'],
                        usuario['senha'],
                        usuario['telefone'],
                        usuario['data_cadastro']
                    ))
                else:
                    messagebox.showwarning("Aviso", "Nenhum usuário encontrado com este ID.")

        except Exception as e:
            print(f'ERRO AO PESQUISAR: {e}')

    def carregar_info(self):

       
        for item in self.tabela.get_children():
            self.tabela.delete(item) 

        try:
            with conexao.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = 'SELECT id, nome, idade, email, senha, telefone, data_cadastro FROM usuarios'
                cursor.execute(sql) 

                todos_usuarios = cursor.fetchall()

                for usuario in todos_usuarios:
                    self.tabela.insert("", "end", values=(
                        usuario['id'],
                        usuario['nome'],
                        usuario['idade'],
                        usuario['email'],
                        usuario['senha'],
                        usuario['telefone'],
                        usuario['data_cadastro']
                    ))

        except Exception as e:
            print(f'ERRO AO CARREGAR DADOS NA TABELA: {e}')

class janeladetalhes:
    def __init__(self, root_pai):
        self.admin = Toplevel(root_pai)
        self.admin.title('Editar')
        self.admin.configure(bg='#2c3e50')
        self.admin.geometry('850x200')

        frame_edita = Frame(self.admin, bg='#2c3e50' )
        frame_edita.pack(fill=X, padx=15,pady=15)

        Label(frame_edita, text='EDITAR', bg="#CA6913", fg='white').grid(row=0, column=2, columnspan=2, pady=15)
                    
                    
        Label(frame_edita, text='Nome', bg='#2c3e50', fg='white').grid(row=3, column=0, padx=15 )
        self.input_nome = Entry(frame_edita, width=30)
        self.input_nome.grid(row=3, column=1)

        Label(frame_edita, text='Data de Nascimento', bg='#2c3e50', fg='white').grid(row=3, column=2, padx=15)
        self.input_idade = Entry(frame_edita, width=30)
        self.input_idade.grid(row=3, column=3)

        Label(frame_edita, text='E-mail',bg='#2c3e50', fg='white').grid(row=3, column=4 )
        self.input_email = Entry(frame_edita, width=30)
        self.input_email.grid(row=3, column=5)

        Label(frame_edita, text='Senha',bg='#2c3e50', fg='white').grid(row=4, column=0 )
        self.input_senha = Entry(frame_edita, width=30, show='*')
        self.input_senha.grid(row=4, column=1)


        Label(frame_edita, text='Telefone', bg='#2c3e50', fg='white').grid(row=4, column=2 )
        self.input_telefone = Entry(frame_edita, width=30)
        self.input_telefone.grid(row=4, column=3)

        
        Label(frame_edita, text='Data e Hora', bg='#2c3e50', fg='white').grid(row=4, column=4)
        self.input_data = Entry(frame_edita, width=30)
        self.input_data.grid(row=4, column=5)

        btn_salvar = Button(frame_edita, text='SALVAR', command=self.salvar, bg='#0e4985', fg='white')
        btn_salvar.grid(row=5, column=2, columnspan=2, pady=15)

        btn_voltar = Button(frame_edita, text='VOLTAR', command=self.voltar, bg='red', fg='white')
        btn_voltar.grid(row=5, column=2, columnspan=2, pady=15)


        frame_tabela = LabelFrame(self.admin, text="INFORMAÇÕES ", fg="green", bg='#2c3e50', font=('Arial', 10, 'bold'), padx=10, pady=10)
        frame_tabela.pack(fill=BOTH, expand=True, pady=10)

        colunas = ("id", "nome", 'idade', "email", "senha", 'telefone', 'data_cadastro' )

        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")


        self.tabela.heading("id", text="Id")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.heading("email", text="Email")
        self.tabela.heading("senha", text="Senha")
        self.tabela.heading("telefone", text="Telefone")
        self.tabela.heading("data_cadastro", text="Data e Hora")

        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("nome", width=120)
        self.tabela.column("idade", width=60)
        self.tabela.column("email", width=150)
        self.tabela.column("senha", width=90)
        self.tabela.column("telefone", width=110)
        self.tabela.column("data_cadastro",  width=120)

        scroll_y = Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll_y.set)

        self.tabela.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_y.pack(side=RIGHT, fill=Y) 

        self.carregar_dados_especificos(self)

    def carregar_dados_especificos(self):
        
        try:
            with conexao.cursor() as cursor:
                sql = 'select id, nome, idade, email, senha, telefone, data_cadastro  FROM cadastro WHERE id = %s'
                cursor.execute(sql(id))

                todos_usuarios = cursor.fetchall()

                for usuario in todos_usuarios:
                    self.tabela.insert("", "end", values=(
                        usuario['id'],
                        usuario['nome'],
                        usuario['idade'],
                        usuario['email'],
                        usuario['senha'],
                        usuario['telefone'],
                        usuario['data_cadastro']
                    ))

        except Exception as e:
            print(f'ERRO AO CARREGAR DADOS NA TABELA: {e}')

    def voltar(self):
        self.admin.destroy()

    def salvar(self):
        nome = self.input_nome.get()
        idade = self.input_idade.get()
        email = self.input_email.get()
        senha = self.input_senha.get()
        telefone = self.input_telefone.get()
        data = self.input_data.get()

        try:
            with conexao.cursor() as cursor:
                sql = """
                            UPDATE cadastro 
                            SET nome = %s, idade = %s, email = %s, senha = %s, telefone = %s, data = %s 
                            WHERE id = %s
                            """
                cursor.execute(sql, (nome, idade, email, senha, telefone, data))
                conexao.commit()
        except Exception as e:
            print('ERRO AO ALTERAR: {e}')

telaCadastro()




       

   
       