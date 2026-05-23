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
                        self.comum()
                        messagebox.showinfo('Logado', 'Bem-vindo Usuário Comum!')
                        self.entra.destroy()

                    elif tipo == 'Admin':
                        self.admin()
                        messagebox.showinfo('Logado', 'Bem-vindo Administrador!')
                        self.entra.destroy()
                
                
                else:
                    messagebox.showerror('Erro', 'E-mail ou senha inválidos.')
                        
        except Exception as e:
            print(f'ERRO NO LOGIN: {e}')

        
        def comum(self):
            telaComum(self.pai)

        def admin(self):
            telaAdmin(self.pai)


class telaComum:  

    def __init__(self, root_pai):
        self.entra = Toplevel(root_pai)
        self.entra.title('Tela Inicio')
        self.entra.configure(bg='#2c3e50')
        self.entra.geometry('430x250')
                            
class telaAdmin:  

    def __init__(self, root_pai):
        self.entra = Toplevel(root_pai)
        self.entra.title('Tela Admin')
        self.entra.configure(bg='#2c3e50')
        self.entra.geometry('430x250')              
       

telaCadastro()




       

   
       