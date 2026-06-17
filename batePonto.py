import pymysql
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import time


conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='batePonto',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
)



 
class teladePonto:  

 

    def __init__(self):
        self.mae = Tk()
        self.mae.title('Totem de Ponto')
        self.mae.geometry('500x800')
        self.mae.configure(bg='#224E08')

       
        self.label_relogio = Label(self.mae, text='', font=('Arial', 30, 'bold'), fg='white', bg='#224E08')
        self.label_relogio.pack(pady=40)

        
        Label(self.mae, text='BATER PONTO', bg='#224E08', fg='#FFFFFF', font=('Arial', 24, 'bold')).pack(pady=20)

        
        self.campo_matricula = Entry(self.mae, width=15, bg='#2D7503', fg='white', font=('Arial', 20), justify='center')
        self.campo_matricula.pack(pady=20, ipady=5)

        self.atualizar_relogio()
            
        
        frame_teclado = Frame(self.mae, bg='#224E08') 
        frame_teclado.pack(pady=10)

        
        config_botao = {'font': ('Arial', 18, 'bold'), 'width': 5, 'height': 2, 'bg': '#B8BEB5'}

        
        Button(frame_teclado, text='1', **config_botao, command=lambda: self.digitar('1')).grid(row=0, column=0, padx=5, pady=5)
        Button(frame_teclado, text='2', **config_botao, command=lambda: self.digitar('2')).grid(row=0, column=1, padx=5, pady=5)
        Button(frame_teclado, text='3', **config_botao, command=lambda: self.digitar('3')).grid(row=0, column=2, padx=5, pady=5)

        
        Button(frame_teclado, text='4', **config_botao, command=lambda: self.digitar('4')).grid(row=1, column=0, padx=5, pady=5)
        Button(frame_teclado, text='5', **config_botao, command=lambda: self.digitar('5')).grid(row=1, column=1, padx=5, pady=5)
        Button(frame_teclado, text='6', **config_botao, command=lambda: self.digitar('6')).grid(row=1, column=2, padx=5, pady=5)

        
        Button(frame_teclado, text='7', **config_botao, command=lambda: self.digitar('7')).grid(row=2, column=0, padx=5, pady=5)
        Button(frame_teclado, text='8', **config_botao, command=lambda: self.digitar('8')).grid(row=2, column=1, padx=5, pady=5)
        Button(frame_teclado, text='9', **config_botao, command=lambda: self.digitar('9')).grid(row=2, column=2, padx=5, pady=5)

        
        Button(frame_teclado, text='Corrigir', font=('Arial', 12, 'bold'), width=7, height=3, bg='#ff6347', fg='white', command=self.limpar).grid(row=3, column=0, padx=5, pady=5)
        Button(frame_teclado, text='0', **config_botao, command=lambda: self.digitar('0')).grid(row=3, column=1, padx=5, pady=5)

        
        self.btn_confirmar = Button(self.mae, text='CONFIRMAR PONTO', font=('Arial', 16, 'bold'), bg='green', fg='white', width=25, command=self.processar_ponto)
        self.btn_confirmar.pack(pady=30, ipady=8)
        
        
        self.mae.mainloop()

    
    def digitar(self, numero):
        self.campo_matricula.insert(END, numero)

    
    def limpar(self):
        self.campo_matricula.delete(0, END)

    def atualizar_relogio(self):
        try:
            hora_atual = time.strftime("%H:%M:%S")
            self.label_relogio.config(text=hora_atual)
            self.mae.after(1000, self.atualizar_relogio)
        except TclError:
            pass

    
    def processar_ponto(self):
         matricula = self.campo_matricula.get()
         
         try:
             with conexao.cursor() as cursor:
                 sql = 'select id, nome from funcionarios where matricula = %s'
                 cursor.execute(sql, (matricula,))

                 funcionario = cursor.fetchone()

                 if funcionario:
                    self.confirmar(funcionario)
                 else:
                        messagebox.showerror('Erro, Funcionario não encontrado')

         except Exception as e:
             print(f'ERRO em {e}')

    def confirmar(self, funcionario):
        self.filha = Toplevel(self.mae)
        self.filha.title('Totem de Ponto')
        self.filha.geometry('400x200')
        self.filha.configure(bg='#224E08')

        
        id_fun = funcionario['id']
        nome_fun = funcionario['nome']

        Label(self.filha, text=nome_fun , font=('Arial', 20, 'bold'), bg='#224E08', fg='white').pack(padx=20, pady=30)

        Button(self.filha, text='CONFIRMAR', font=('Arial', 12, 'bold'), width=15,  bg='#ff6347', fg='white', command=lambda: self.salvar_ponto(id_fun)).pack(padx=20, pady=10)
        Button(self.filha, text='CANCELAR', font=('Arial', 12, 'bold', ), width=15, bg='#BD0000', fg='white', command=self.fechar).pack(padx=20, pady=10)
    
    def salvar_ponto(self, id_funcionario):

        try:
            with conexao.cursor() as cursor:
                sql_1 = '''select tipo from registro_ponto where id_funcionario = %s order by data_hora desc limit 1'''
                cursor.execute(sql_1,(id_funcionario,)) 

                ultimo_registro = cursor.fetchone()


                if ultimo_registro is None:
                    tipo_atual = 'Entrada'
                elif ultimo_registro['tipo'] == 'Saída':
                    tipo_atual = 'Entrada'
                else:
                    tipo_atual = 'Saida'

                sql_insert = '''
                    INSERT INTO registro_ponto (id_funcionario, data_hora, tipo) 
                    VALUES (%s, NOW(), %s)

                '''
                cursor.execute(sql_insert, (id_funcionario, tipo_atual))
                conexao.commit()

                messagebox.showinfo('Sucesso', f'Ponto de {tipo_atual} registrado com sucesso!')
                self.filha.destroy()
                self.campo_matricula.delete(0, END)


        except Exception as e:
            print(f'ERRO ao salvar ponto: {e}')   
            messagebox.showerror('Erro', 'Não foi possível registrar o ponto no banco de dados.')


    def fechar(self):

        self.filha.destroy()


app = teladePonto()


    
            



      

