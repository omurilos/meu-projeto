import pymysql
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox

def conectar():
     return pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db="cadastro",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
)


class telaCadastro:
 
  def cadastrar(pai):
         nome = pai.nome.get()
         idade = pai.idade.get()
         email = pai.email.get()
         senha = pai.senha.get()
         telefone = pai.telefone.get()


         try:
               with conexao.cursor() as cursor:
                  sql = 'insert into usuarios(nome, idade, email, senha, telefone) values (%s, %s, %s, %s, %s)'
                  cursor.execute(sql,(nome, idade, email, senha, telefone))
                  conexao.commit()
                  messagebox.showinfo("Sucesso, Você foi cadastrado")
         except Exception as e:
            print(f'Não foi possivel{e}') 


  
   pai = Tk()
   pai.title('Inicio')
   pai.geometry('500x250')
   pai.configure(bg='#2c3e50')

   Label(pai, text='CADASTRO', bg="#CA6913", fg='white').grid(row=0, column=3, columnspan=2, pady=15)
            
            
   Label(pai, text='Nome', bg="#E67E22", fg='white').grid(row=3, padx=15, pady=5 )
   nome = Entry(pai, width=30).grid(row=3, column=3)

   Label(pai, text='Idade', bg="#E67E22", fg='white').grid(row=4, padx=15, pady=5)
   idade = Entry(pai, width=30).grid(row=4, column=3)

   Label(pai, text='E-mail', bg="#E67E22", fg='white').grid(row=5, padx=15, pady=5)
   email = Entry(pai, width=30).grid(row=5, column=3)

   Label(pai, text='Senha', bg="#E67E22", fg='white').grid(row=6, padx=15, pady=5)
   senha = Entry(pai, width=30, show='*').grid(row=6, column=3)
   Label(pai, text='Telefone', bg="#E67E22", fg='white').grid(row=7, padx=15, pady=5)
   telefone = Entry(pai, width=30).grid(row=7, column=3)

            

   Button(pai, text='CADASTRAR', width=25, fg='white', bg="#006912", command=lambda: cadastrar(pai)).grid(row=4, column=4, padx=20)

   Label(pai, text='Já possui um cadastro?', bg='#2c3e50', fg="#FFFFFF" ).grid(row=6, column=4)
   Button(pai, text='ENTRAR', width=25, fg='white', bg="#0e4985").grid(row=7, column=4, padx=20)

   pai.mainloop()






       

   
       