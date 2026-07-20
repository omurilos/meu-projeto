import pymysql
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import customtkinter as ctk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class telainico:
  def __init__(self):

        self.pai = ctk.CTk()
        
        self.pai.title('')
        self.pai.geometry('1300x600')
        self.pai.configure(fg_color="#FFFFFF")
        self.pai.resizable(False, False)

         #menu

        frame_menu = ctk.CTkFrame(self.pai, fg_color="#D1CECE", corner_radius=15)
        frame_menu.pack(side=LEFT, fill=Y, padx=3, pady=10)

        ctk.CTkLabel(frame_menu, text='🌱 Monitoramento \n de Doenças', bg_color="#D1CECE", text_color='#383434', width=16, font=('Arial', 18, 'bold')).pack( padx=10, pady=30)

        ctk.CTkButton(frame_menu, text='Tratamentos', fg_color='#F05933', text_color='white', width=15, font=('Arial', 20, 'bold')).pack(padx=10, pady=10)
        ctk.CTkButton(frame_menu, text='Ocorrências', fg_color='#F05933', text_color='white', width=15, font=('Arial', 20, 'bold')).pack(padx=10, pady=10)
        ctk.CTkButton(frame_menu, text='Inspeções', fg_color='#F05933', text_color='white',width=15, font=('Arial', 20, 'bold')).pack(padx=10, pady=10)
        ctk.CTkButton(frame_menu, text='Relatórios', fg_color='#F05933', text_color='white', width=15, font=('Arial', 20, 'bold')).pack(padx=10, pady=10)
        ctk.CTkButton(frame_menu, text='Talhões', fg_color='#F05933', text_color='white', width=15, font=('Arial', 20, 'bold')).pack( padx=10, pady=10)
        ctk.CTkButton(frame_menu, text='Sair', fg_color="#F03333", text_color='white', command=self.fechar, width=6, font=('Arial', 18, 'bold')).pack(padx=10, pady=25)
  
         #dashboard

        frame_dash = ctk.CTkFrame(self.pai, fg_color='#D1CECE', corner_radius=15)
        frame_dash.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame_dash, text='Dashboard', text_color='#383434', font=('Arial', 25, 'bold')).grid(column=0, row=0, padx=20, pady=20, sticky="w")

        ctk.CTkLabel(frame_dash, text='Ocorrências \n \n 5', text_color='#F05933', font=('Arial', 20, 'bold')).grid(column=0, row=1, padx=70, pady=20, sticky="w")
        ctk.CTkLabel(frame_dash, text='Talhões \n \n 7', text_color='#F05933', font=('Arial', 20, 'bold')).grid(column=1, row=1, padx=70, pady=20, sticky="w")
        ctk.CTkLabel(frame_dash, text='Tratamentos \n \n 2', text_color='#F05933', font=('Arial', 20, 'bold')).grid(column=2, row=1, padx=70, pady=20, sticky="w")


          #tabela 

        frame_tabela = LabelFrame(self.pai, text='' , fg="green", padx=10, pady=10)
        frame_tabela.pack(fill=BOTH, expand=True, pady=10)

        colunas = ('talhao', 'doenca', 'gravidade')
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show='headings')

        tabela.heading('talhao', text='Talhão')
        tabela.heading('doenca', text='Doença')
        tabela.heading('gravidade', text='Gravidade')
        
        tabela.column('talhao', width=100)
        tabela.column('doenca', width=100)
        tabela.column('gravidade', width=150)

        tabela.pack(fill=BOTH, expand=True)


          # matplotlib

        frame = ctk.CTkFrame(frame_dash)
        frame.grid(row=2, column=0, columnspan=3, padx=50, pady=20, sticky="nsew")

        fig = Figure(figsize=(5, 4), dpi=70)
        fig.patch.set_facecolor("#D1CECE")
        ax = fig.add_subplot(111)

       
        meses = ["Jan", "Fev", "Mar", "Abr"]
        casos = [10, 18, 8, 15]

        ax.plot(meses, casos, color="#F05933", linewidth=3, marker="o", markersize=8)
        ax.set_title("Casos de Doenças")
        ax.set_ylabel("Quantidade")
        ax.set_facecolor("#D1CECE")
        

       
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


        #novas ocorrênciaas

        ctk.CTkButton(frame_dash, text='Adicionar ocorrência +', fg_color="#F03333", text_color='white', command=self.novaocorrencias, width=8, font=('Arial', 20, 'bold')).grid(row=3, column=0, columnspan=3, pady=20)


        self.pai.mainloop()


  def novaocorrencias(self):
        ocorrencias(self.pai)


  def fechar(self):
        self.pai.destroy()




class ocorrencias:
     
     def __init__(self, root_pai):
          
          self.filho = ctk.CTkToplevel(root_pai)
          self.filho.title('+ Ocorrências')
          self.filho.configure(fg_color='white')
          self.filho.geometry('500x800')
          self.filho.resizable(False, False)

          self.filho.transient(root_pai)   
          self.filho.lift()                
          self.filho.focus_force()



          frame_cabecalho = ctk.CTkFrame(self.filho, fg_color="#D1CECE", corner_radius=15)
          frame_cabecalho.pack(side=LEFT, fill=Y, padx=3, pady=10)

          ctk.CTkLabel(frame_cabecalho, text='Nova Ocorrência', bg_color="#D1CECE", text_color='#383434', width=16, font=('Arial', 18, 'bold')).pack( padx=10, pady=10)
  

         

telainico()