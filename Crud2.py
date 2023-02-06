import tkinter as tk
from tkinter import ttk
import re
import pymysql



class APP(tk.Tk):
#TITULO E JANELA
    def __init__(self):
        super().__init__()
        self.title("VEÍCULOS")
        self.configure(background='#abdbe3')
        self.varResultado = tk.StringVar(self)
        self.lblResultado = tk.Label(
            self,textvariable= self.varResultado,
            font=("Arial",18),
            background='#36291c',

        )
        self.lblResultado.grid(row=0,column=0,columnspan=3,padx=100,pady=10,sticky="ewns")

#INFORMAÇÕES
        self.lblProprietario= ttk.Label(
            self, text= "PROPRIETÁRIO",
            font=("Arial",18,'bold'),
        )
        self.lblProprietario.grid(row=1,column=0,sticky='w',pady=5,padx=20)

        self.lblCpf = ttk.Label(
            self, text="CPF",
            font=("Arial", 18, 'bold'),
        )
        self.lblCpf.grid(row=2, column=0, sticky='w', pady=5, padx=20)

        self.lblPlaca = ttk.Label(
            self, text="PLACA",
            font=("Arial", 18, 'bold'),
        )
        self.lblPlaca.grid(row=3, column=0, sticky='w', pady=5, padx=20)

        self.lblModelo = ttk.Label(
            self, text="MODELO",
            font=("Arial", 18, 'bold'),
        )
        self.lblModelo.grid(row=4, column=0, sticky='w', pady=5, padx=20)

        self.lblAno = ttk.Label(
            self, text="ANO",
            font=("Arial", 18, 'bold'),
        )
        self.lblAno.grid(row=5, column=0, sticky='w', pady=5, padx=20)
#INPUT
        self.varnome = tk.StringVar(self)
        self.txtProprietario = ttk.Entry(
            self,textvariable=self.varnome,
            font=("Arial",18)
        )
        self.txtProprietario.grid(row=1,column=2,sticky='we',pady=5,padx=20)

        self.varCpf = tk.StringVar(self)
        self.txtCpf = ttk.Entry(
            self,textvariable=self.varCpf,
            font=("Arial",18)
        )
        self.txtCpf.grid(row=2,column=2,sticky='we',pady=5,padx=20)

        self.varPlaca = tk.StringVar(self)
        self.txtPlaca = ttk.Entry(
            self,textvariable=self.varPlaca,
            font=("Arial",18),
        )
        self.txtPlaca.grid(row=3,column=2,sticky='we',pady=5,padx=20)

        self.varModelo = tk.StringVar(self)
        self.txtModelo = ttk.Entry(
            self,textvariable=self.varModelo,
            font=("Arial",18)
        )
        self.txtModelo.grid(row=4,column=2,sticky='we',pady=5,padx=20)

        self.varAno = tk.StringVar(self)
        self.txtAno = ttk.Entry(
            self,textvariable=self.varAno,
            font=("Arial",18)
        )
        self.txtAno.grid(row=5,column=2,sticky='we',pady=5,padx=20)
#LISTA DE RESULTADOS
#CHAMADA DE POSIONAMENTO DA LISTA DE CLIENTES
        self.frameLista = ttk.Frame(self)
        self.frameLista.grid(row=6,column=0,columnspan=3,rowspan=4,sticky='nwes',padx=20,pady=10)

        self.txtLista = ttk.Treeview(
            self.frameLista, columns=("Proprietário","Cpf","Placa","Modelo","Ano"),
            show="headings", height=15
        )
        self.txtLista.heading('Proprietário', text='Proprietário')
        self.txtLista.heading("Cpf",text="Cpf")
        self.txtLista.heading("Placa",text="Placa")
        self.txtLista.heading("Modelo",text="Modelo")
        self.txtLista.heading("Ano",text="Ano")


        def item_selected(event):
            for selected_item in self.txtLista.selection():
                item = self.txtLista.item(selected_item)
                record = item['values']
                self.varnome.set(record[0])
                self.varCpf.set(record[1])
                self.varPlaca.set(record[2])
                self.varModelo.set(record[3])
                self.varAno.set(record[4])
        self.txtLista.bind('<<TreeviewSelect>>', item_selected)

        self.txtLista.grid(row=0, column=0, sticky="nwes")

        scrollbar = ttk.Scrollbar(
            self.frameLista, orient=tk.VERTICAL,
            command=self.txtLista.yview)

        scrollbar.grid(row=0, column=1, sticky='ns')
#BOTÕES
        self.btnConectar = ttk.Button(
            self,text= "CONECTAR",
            command=self.btnConectar_Click
        )
        self.btnConectar.grid(row=0,column=3,sticky="nwes",pady=5,padx=20,ipadx=20)

        self.btnCriarTabela = ttk.Button(
            self, text="CRIAR TABELA",
            command=self.btnCriarTabela_Click
        )
        self.btnCriarTabela.grid(row=1, column=3, sticky="nwes", pady=5, padx=20, ipadx=20)

        self.btnCreate = ttk.Button(
            self, text="CREATE",
            command=self.btnCreate_Click
        )
        self.btnCreate.grid(row=2, column=3, sticky="nwes", pady=5, padx=20, ipadx=20)

        self.btnRead = ttk.Button(
            self,text= "READ",
            command=self.btnRead_Click
        )
        self.btnRead.grid(row=3,column=3,sticky="nwes",pady=5,padx=20,ipadx=20)

        self.Update = ttk.Button(
            self,text="UPDATE",
            command=self.btnUpdate_Click
        )
        self.Update.grid(row=4,column=3,sticky="nwes",pady=5,padx=20,ipadx=20)

        self.btnDelete=ttk.Button(
            self,text="DELETE",
            command=self.btnDelete_Click
        )
        self.btnDelete.grid(row=5,column=3,sticky="nwes",pady=5,padx=20,ipadx=20)

#CONECTAR AO BANCO DE DADOS
    def btnConectar_Click(self):
        try:
            conexao = pymysql.connect(
                host="localhost",
                database="carros",
                user="root",
                password="dvd2501920506"
            )
            mycursor = conexao.cursor()
            sql = "CREATE DATABASE IF NOT EXISTS carros"
            mycursor.execute(sql)
            self.varResultado.set("     Conexão criada com sucesso!!")
            self.lblResultado.configure(background="#3cb371")
        except:
            self.varResultado.set("Erro ao criar conexão!!")
            self.lblResultado.configure(background="#ff6347")
    def btnCriarTabela_Click(self):
        try:
            conexao = pymysql.connect(
                host="localhost",
                database="carros",
                user="root",
                password="dvd2501920506"
            )
            mycursor = conexao.cursor()
            sql = "CREATE TABLE IF NOT EXISTS carros1(nome VARCHAR(55) NOT NULL,Cpf VARCHAR(55) NOT NULL UNIQUE,Placa VARCHAR(55) NOT NULL,Modelo VARCHAR(55) NOT NULL,Ano VARCHAR(55) NOT NULL,PRIMARY KEY (nome))"
            mycursor.execute(sql)
            self.varResultado.set("Tabela Criada com Sucesso")
            self.lblResultado.configure(background="#ff6347")
        except:
            self.varResultado.set("Erro ao Criar Tabela")
            self.lblResultado.configure(background="#ff6347")

    def btnCreate_Click(self):
        nome = self.varnome.get().strip()
        Cpf = self.varCpf.get().strip()
        Placa = self.varPlaca.get().strip()
        Modelo = self.varModelo.get().strip()
        Ano = self.varAno.get().strip()

        renome = re.fullmatch(r"\b[A-Za-z ]+\b",nome)
        reCpf = re.fullmatch(r"\d{3}\.\d{3}\.\d{3}\-\d{2}", Cpf)
        rePlaca = re.fullmatch(r'^[A-Z]{3}\d{4}$', Placa)
        reModelo = re.fullmatch(r'\b[A-Za-z ]+\b',Modelo)
        reANO = re.fullmatch(r'\d{4}',Ano)

        if renome is None:
            self.varResultado.set("O campo Proprietário é obrigatório.")
            self.lblResultado.configure(background="#3cb371")
            self.txtProprietario.focus()
        elif reCpf is None:
            self.varResultado.set("INSIRA UM CPF VÁLIDO")
            self.lblResultado.configure(background="#3cb371")
            self.txtCpf.focus()
        elif rePlaca is None:
            self.varResultado.set("DIGITE CORRETAMENTE")
            self.lblResultado.configure(background="#3cb371")
            self.txtPlaca.focus()
        elif reModelo is None:
            self.varResultado.set("DIGITE UM MODELO VÁLIDO")
            self.lblResultado.configure(background="#3cb371")
            self.txtModelo.focus()
        elif reANO is None:
            self.varResultado.set("DIGITE UM ANO VÁLIDO")
            self.lblResultado.configure(background="#3cb371")
            self.txtAno.focus()
        else:
            try:
                conexao = pymysql.connect(
                    host="localhost",
                    database="carros",
                    user="root",
                    password="dvd2501920506"
                )

                mycursor = conexao.cursor()
                sql = "INSERT INTO carros1(nome,Cpf,Placa,Modelo,Ano) VALUES (%s,%s,%s,%s,%s)"
                val = (nome,Cpf,Placa,Modelo,Ano)
                mycursor.execute(sql, val)
                conexao.commit()

                self.varResultado.set(str(mycursor.rowcount) + " registro(s) inserido(s).")
                self.lblResultado.configure(background="#3cb371")
                self.varnome.set("")
                self.varCpf.set("")
                self.varPlaca.set("")
                self.varModelo.set("")
                self.varAno.set("")
                self.txtProprietario.focus()
            except:
                self.varResultado.set("Erro ao inserir novo registro.")
                self.lblResultado.configure(background="#FF9999")

    def btnRead_Click(self):
        self.txtLista.delete(*self.txtLista.get_children())

        try:

            conexao = pymysql.connect(
                host="localhost",
                database="carros",
                user="root",
                password="dvd2501920506"
            )

            mycursor = conexao.cursor()
            sql = "SELECT * FROM carros1 ORDER BY nome ASC"
            mycursor.execute(sql)

            if self.varnome.get() != "":
                sql = "SELECT * FROM carros1 WHERE nome LIKE %s"
                val = (self.varnome.get(),)
                mycursor.execute(sql, val)
            elif self.varCpf.get() != "":
                sql = "SELECT * FROM carros1 WHERE Cpf LIKE %s"
                val = (self.varCpf.get(),)
                mycursor.execute(sql, val)
            elif self.varPlaca.get() != "":
                sql = "SELECT * FROM carros1 WHERE Placa LIKE %s"
                val = (self.varPlaca.get(),)
                mycursor.execute(sql,val)
            elif self.varModelo.get() != "":
                sql = "SELECT * FROM carros1 WHERE Modelo LIKE %s"
                val = (self.varModelo.get(),)
                mycursor.execute(sql,val)
            elif self.varAno.get() != "":
                sql = "SELECT * FROM carros1 WHERE Ano LIKE %s"
                val = (self.varAno.get(),)
                mycursor.execute(sql,val)
            myresult = mycursor.fetchall()

            for contato in myresult:
                self.txtLista.insert('', tk.END, values=contato)

            self.varResultado.set("Lista gerada com sucesso")
            self.lblResultado.configure(background="#3cb371")
            self.txtProprietario.focus()
        except:
            self.varResultado.set("Erro ao buscar registros.")
            self.lblResultado.configure(background="#FF9999")


    def btnUpdate_Click(self):
        nome = self.varnome.get().strip()
        Cpf = self.varCpf.get().strip()
        Placa = self.varPlaca.get().strip()
        Modelo = self.varModelo.get().strip()
        Ano = self.varAno.get().strip()

        renome = re.fullmatch(r"\b[A-Za-z ]+\b", nome)
        reCpf = re.fullmatch(r"\d{3}\.\d{3}\.\d{3}\-\d{2}", Cpf)
        rePlaca = re.fullmatch(r'^[A-Z]{3}\d{4}$',Placa)
        reModelo = re.fullmatch(r'\b[A-Za-z ]+\b',Modelo)
        reAno = re.fullmatch(r'\d{4}', Ano)

        if len(self.txtLista.selection()) < 1:
            self.varResultado.set("Selecione um registro para editar.")
            self.lblResultado.configure(background="#FF9999")
            self.txtProprietario.focus()
            return
        try:
            registro = self.txtLista.selection()[0]
            dadosRegistro = self.txtLista.item(registro)
            proprietarioRegistro = dadosRegistro["values"][0]
            cpfRegistro = dadosRegistro["values"][1]
            placaRegistro = dadosRegistro["values"][2]
            modeloRegistro = dadosRegistro["values"][3]
            anoRegistro = dadosRegistro["values"][4]

            conexao = pymysql.connect(
                host="localhost",
                database="carros",
                user="root",
                password="dvd2501920506"
            )
            mycursor = conexao.cursor()
            sql = "UPDATE carros1 SET nome = %s, Cpf = %s,Placa = %s,Modelo = %s,Ano = %s WHERE nome = %s AND Cpf = %s AND Placa = %s AND Modelo = %s AND ano = %s"
            val = (nome,Cpf,Placa,Modelo,Ano,proprietarioRegistro,cpfRegistro,placaRegistro,modeloRegistro,anoRegistro)
            mycursor.execute(sql, val)
            conexao.commit()
            self.varnome.set("")
            self.varCpf.set("")
            self.varPlaca.set("")
            self.varModelo.set("")
            self.varAno.set("")

            self.btnUpdate_Click()
            self.varResultado.set("Registro alterado com sucesso!!")
            self.lblResultado.configure(background="#3cb371")
        except:
                self.varResultado.set("Erro ao excluir registro.")
                self.lblResultado.configure(background="#FF9999")

    def btnDelete_Click(self):
        nome = self.varnome.get().strip()
        Cpf = self.varCpf.get().strip()
        Placa = self.varPlaca.get().strip()
        Modelo = self.varModelo.get().strip()
        Ano = self.varAno.get().strip()

        if nome == "" or Cpf == "" or Placa == "" or Modelo == "" or Ano == "":
            self.varResultado.set("Selecione um registro para excluir.")
            self.lblResultado.configure(background="#FF9999")
            self.lblProprietario.focus()
        else:
                try:
                    conexao = pymysql.connect(
                    host="localhost",
                    database="carros",
                    user="root",
                    password="dvd2501920506"

                )
                    mycursor = conexao.cursor()
                    sql = "DELETE FROM carros1 WHERE nome = %s AND Cpf = %s AND Placa = %s AND Modelo = %s AND Ano = %s"
                    val = (nome, Cpf, Placa, Modelo, Ano)
                    mycursor.execute(sql,val)
                    conexao.commit()

                    self.varnome.set("")
                    self.varCpf.set("")
                    self.varPlaca.set("")
                    self.varModelo.set("")
                    self.varAno.set("")

                    self.btnDelete_Click()
                    self.varResultado.set("DELETADO COM SUCESSO")
                    self.lblResultado.configure(background="#FF9999")

                except:
                    self.varResultado.set("Erro ao excluir registro.")
                    self.lblResultado.configure(background="#FF9999")
if __name__ == "__main__":
    app = APP()
    app.mainloop()
