#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Autor:               Vinicius Rodrigues da Cunha Perallis
Data:                19/04/2006
                     20/04/2006
Projeto:             Calculadora Comercial 

Finalidade:          Calculadora que opera semelhante a calculadora
                     do windows, alem de conter uma caixa de 
                     texto que imita uma fita de impressão

Interpretador:       Python 2.4.1
Sistema Operacional: Linux, Windows

Email:perallis@rc.unesp.br


"""


#Importa todas funcoes do modulo Tkinter
from Tkinter import *


#Classe Principal que executa o aplicativo Calculadora
class Calculadora:

    def __init__(self,parent):
        self.myapp=parent
        self.myapp.title("Calculadora - Phy")
        #Cria o frame principa
        self.geral=Frame(self.myapp,bg="gray")
        self.geral.pack()


        """Cria os frames nescessarios para a disposição dos 
        widgets no programa"""

        """Cria os frames nescessarios para a disposição dos
        widgets no programa"""

        self.fexibir=Frame(self.geral,bg="gray")
        self.fzero=Frame(self.geral,bg="gray")
        self.fum=Frame(self.geral,bg="gray")
        self.fdois=Frame(self.geral,bg="gray")
        self.ftreis=Frame(self.geral,bg="gray")
        self.fquatro=Frame(self.geral,bg="gray")


        #Caixa de texto, que servirá para mostrar os numeros

        self.visor=Entry(self.fexibir,width=23,bg="white", \
                         fg="blue",justify="right")
        self.visor.insert(INSERT,0)

        """Frame geral: Escreve um titulo na primeira linha 
        do programa"""

        self.titulo=Label(self.geral,text="  CALCULADORA \
                          PYTHON  ",bg="gray",fg="black",
                          font= ('Helvetica','10','bold'))

        """ Insere a cixa de Texto que seá utilizada para 

        fazer a fita de impressão"""
        self.ffita=Frame(self.geral)
        self.ffita.pack(side="right",padx=15)
        self.sb=Scrollbar(self.ffita)

        self.fita=Text(self.ffita,width=23,height=13,\
                       bg="white",yscrollcommand=self.sb.set)
        self.sb["command"] = self.fita.yview
        self.fita.pack(side="left",padx=0)
        self.sb.pack(side="right",fill=Y)


        ## WIDGETS NO FRAME ZERO ########################### 

        #Botao para reiniciar a calculadora

        self.c=Button(self.fzero,text="C",bg="white",\
                      width=4,command=self.zera)

        #Label para organizar o programa

        self.space1=Label(self.fzero,bg="gray",\
                         text="                       ")
        #Botao igual 

        self.igual=Button(self.fzero,text="=",bg="white",\
                          width=4,command=lambda sin="": \
                          self.op(sin))

        #####################################################


        ## WIDGETS NO FRAME UM ##################
        self.sete=Button(self.fum,text="7",width=4,\
                         command=lambda n=7: \
                         self.write_visor(n))
        self.oito=Button(self.fum,text="8",width=4,\
                         command=lambda n=8: \
                         self.write_visor(n))
        self.nove=Button(self.fum,text="9",width=4,\
                         command=lambda n=9: \
                         self.write_visor(n))
        self.div=Button(self.fum,text="/",fg="red",\
                        width=4, command=lambda sin='/': \
                        self.op(sin))

        ######################################################

        ## WIDGETS NO FRAME DOIS #############################
        self.quatro=Button(self.fdois,text="4",width=4,\
                           command=lambda n=4: \
                           self.write_visor(n))
        self.cinco=Button(self.fdois,text="5",width=4,\
                          command=lambda n=5: \
                          self.write_visor(n))
        self.seis=Button(self.fdois,text="6",width=4,\
                         command=lambda n=6: \
                         self.write_visor(n))
        self.mult=Button(self.fdois,text="*",fg="red",\
                         width=4 ,command=lambda sin='*': \
                         self.op(sin))

        #######################################################



        ## WIDGETS NO FRAME TREIS #############################

        self.um=Button(self.ftreis,text="1",width=4,command= \
                      lambda n=1: self.write_visor(n) )
        self.dois=Button(self.ftreis,text="2",width=4,command= \
                         lambda n=2: self.write_visor(n))
        self.tres=Button(self.ftreis,text="3",width=4,command= \
                         lambda n=3: self.write_visor(n))
        self.menos=Button(self.ftreis,text="-",fg="red",\
                          width=4,command=lambda sin='-': \
                          self.op(sin) )

        #########################################################



        ## WIDGETS NO FRAME QUATRO###############################

        self.zero=Button(self.fquatro,text="0",width=4,command= \
                        lambda n=0: self.write_visor(n))
        self.virg=Button(self.fquatro,text=",",width=4,command=\
                        lambda n='.': self.write_visor(n))
        self.maismenos=Button(self.fquatro,fg="red",text="+/-",\
                              width=4, command=lambda n=-1: \
                              self.write_visor(n))
        self.mais=Button(self.fquatro,fg="red",text="+",\
                         width=4,command=lambda sin='+': \
                         self.op(sin))

       ###########################################################



        #Frame fgeral   
        self.titulo.pack()

        #Frame fexibir   
        self.fexibir.pack()

        self.visor.pack(ipadx="3")

        #Frame fzero  
        self.fzero.pack()

        self.c.pack(side=LEFT,fill=X,pady="5",padx="2")
        self.igual.pack(side=LEFT,fill=X,pady="5",padx="2")
        self.space1.pack()

        #Frame fum   
        self.fum.pack()

        self.sete.pack(side="left",padx=2,pady=2)
        self.oito.pack(side="left",padx=2,pady=2)
        self.nove.pack(side="left",padx=2,pady=2)
        self.div.pack(side="left",padx=2,pady=2)

        #Frame fdois   
        self.fdois.pack()
        self.seis.pack(side="left",padx=2,pady=2)
        self.cinco.pack(side="left",padx=2,pady=2)
        self.quatro.pack(side="left",padx=2,pady=2)
        self.mult.pack(side="left",padx=2,pady=2)

        #Frame ftreis 
        self.ftreis.pack()
        self.tres.pack(side="left",padx=2,pady=2)
        self.dois.pack(side="left",padx=2,pady=2)
        self.um.pack(side="left",padx=2,pady=2)
        self.menos.pack(side="left",padx=2,pady=2)

        #Frame fquatro   
        self.fquatro.pack()
        self.maismenos.pack(side="left",padx=2,pady=2)
        self.zero.pack(side="left",padx=2,pady=2)
        self.virg.pack(side="left",padx=2,pady=2)
        self.mais.pack(side="left",padx=2,pady=2)

        #  Variais da classe 
        self.z=0
        self.w=1
        self.atual=0
        self.i=0
        self.ty=0
        self.num=0
        self.prim=0
        self.h=0
        self.sa=0




    ###---Função para realizar as operações aritiméticas ------###

    def op(self,sin):
        if (self.w==0):
            self.num=float(self.visor.get())
            print self.num
            self.sinal=sin
            self.w=1
            self.z=1
            self.i=0
            self.ty=0
            self.divi=0
            if self.prim==0:
                self.ty=1

        else :
            if self.ty==0:
                self.atual=float(self.visor.get())

            if self.sa==1 and self.ty==1:
                self.num=float(self.visor.get())
                self.sa=0

            if self.sinal=='+':
                self.num=self.num + self.atual
            elif  self.sinal=='-':
                self.num=self.num - self.atual
            elif  self.sinal=='/' and self.ty!=1 and self.atual!=0:
                self.num=self.num / self.atual
            elif  self.sinal=='/' and self.atual==0 and self.ty!=1:
                self.visor.delete(0,END)
                self.visor.insert(INSERT,"Imposivel dividir")
                self.divi=1
                self.prim=1
            elif  self.sinal=='*' and self.ty!=1 and self.prim==1:
                self.num=self.num * self.atual

            if self.divi==0:
                self.visor.delete(0,END)
                self.visor.insert(END,self.num)
                self.prim=1
            if self.divi==0 and self.ty==0:
                self.fita.insert(INSERT,"\n"+self.sinal)
                self.fita.insert(INSERT,"\n"+str(self.atual))
                self.fita.insert(INSERT,"\n"+"=")
                self.fita.insert(INSERT,"\n"+str(self.num))


            self.atual=0
            self.ty=1
            self.i=0
            self.w=1
            self.z=1
            self.div=0
            self.sinal=sin
    ###---------------- Fim da funçõa aritmética op --------------###




    ###----- Função para escrever os numeros no visor ----------###  

    def write_visor(self,n):
        if (self.z==1) and n!=-1:
            if self.i==0:
                 self.visor.delete(0,END)

            self.visor.insert(INSERT,n)
            self.w=1
            self.z=1
            self.i=1
            self.ty=0
            self.prim=1



        elif self.z==0 and n!=-1:
            if self.i==0:
                self.visor.delete(0,END)
            self.visor.insert(INSERT,n)
            self.fita.insert(INSERT,n)
            self.w=0
            self.i=1
            self.ty=0
        if  n==-1:
            self.la=float(self.visor.get()) * (-1)
            self.visor.delete(0,END)
            self.visor.insert(END,self.la)
            self.fita.insert(INSERT,"\n"+"*(-1)")
            self.fita.insert(INSERT,"\n"+"=")
            self.fita.insert(INSERT,"\n"+str(self.la))
            self.sa=1

    ###--------------- Fim da funçõa write_visor --------------###



    ###------ Função para reiniciar a calculadora -------------###   

    def zera(self):
        self.num=0
        self.z=0
        self.w=1
        self.atual=0
        self.i=0
        self.ty=0
        self.prim=0
        self.visor.delete(0,END)
        self.visor.insert(INSERT,0)
        self.fita.delete('1.0','90.0')

    ###------------------ Fim da função zera---------------------### 




# root Intacia-se pela classe Tk() e inicia a aplicação       
root=Tk()
aplicativo=Calculadora(root)
root.mainloop()
