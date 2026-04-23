import pymysql
from tkinter import *
from tkinter import messagebox

class janelaLogin():
    def VerificarLogin(self):
        autenticado = False
        usuarioMaster = False

        try:
            conexao = pymysql.connect(

              host = "localhost",
              user = "root",
              password = "",
              db = "erp",
              charset = "utf8mb4",
              cursorclass = pymysql.cursors.DictCursor

            )
        except:
            print('ERRO ***')
        usuario = self.login.get()
        senha = self.senha.get()

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('erro ao fazer consulta')

        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            messagebox.showinfo('login', 'Email ou senha incorretos')

        if autenticado:
            self.root.destroy()
            if usuarioMaster:
                messagebox.showinfo('login', 'AUTENTICADO')


    def __init__(self):
        self.root = Tk()
        self.root.title('login')
        Label(self.root, text='Faça seu login').grid(row=0, column=0, columnspan=2)

        Label(self.root, text='Usuario').grid(row=1, column=0)

        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=5, pady=5)

        Label(self.root, text='senha').grid(row=2, column=0)

        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)

        Button(self.root, text='Login', bg='green3', width=10, command=self.VerificarLogin).grid(row=3, column=0, padx=5, pady=5)

        Button(self.root, text='Cadastar', bg='orange3', width=10).grid(row=3, column=1, padx=5, pady=5)

        Button(self.root, text='Visualisar cadastros', bg='white').grid(row=4, column=0, columnspan=2)

        self.root.mainloop()

janelaLogin()