# -*- coding: cp1252 -*-

import Tkinter; Tk = Tkinter
import tkMessageBox

class App(Tk.Frame):
#cria o Frame e seta as variáveis do jogo
    def __init__(self, master = None):
        Tk.Frame.__init__ (self, master)

        self.varA = Tk.IntVar()
        self.varB = Tk.IntVar()
        self.varC = Tk.IntVar()
        self.varD = Tk.IntVar()
        self.varE = Tk.IntVar()
        self.varF = Tk.IntVar()

# carrega as imagens 

    def criaImagens(self):
        self.__image_runner1__ = Tk.PhotoImage('runner1',file="1.gif")
        self.__image_runner2__ = Tk.PhotoImage('runner2',file="2.gif")
        self.__image_runner3__ = Tk.PhotoImage('runner3',file="3.gif")
        self.__image_runner4__ = Tk.PhotoImage('runner4',file="4.gif")
        self.__image_runner5__ = Tk.PhotoImage('runner5',file="5.gif")
        self.__image_runner6__ = Tk.PhotoImage('runner6',file="6.gif")

# seta onde as imagens devem ser carregadas

        self.img_1 = Tk.Label (self,  {'image' : 'runner1'})
        self.img_2 = Tk.Label (self,  {'image' : 'runner2'})
        self.img_3 = Tk.Label (self,  {'image' : 'runner3'})
        self.img_4 = Tk.Label (self,  {'image' : 'runner4'})
        self.img_5 = Tk.Label (self,  {'image' : 'runner5'})
        self.img_6 = Tk.Label (self,  {'image' : 'runner6'})

#cria as caixas de checagem atribuindo a variável usada

    def criaCheck(self):
        self.a = Tk.Checkbutton(self, variable=self.varA)
        self.b = Tk.Checkbutton(self, variable=self.varB)
        self.c = Tk.Checkbutton(self, variable=self.varC)
        self.d = Tk.Checkbutton(self, variable=self.varD)
        self.e = Tk.Checkbutton(self, variable=self.varE)
        self.f = Tk.Checkbutton(self, variable=self.varF)

#cria os botões  

    def criaBot(self):
        self.btOK=Tk.Button(self, text = "Resultado", command=self.btOK)
        self.btSAIR=Tk.Button(self, text = "Sair", command=self.btSAIR)

#configura as linhas e colunas do frame, que serão usadas para carregar as imagens, botões e caixas de checagem

    def configuraFrame(self):
        self.rowconfigure (1, {'weight' : 1, 'minsize' : 30})
        self.rowconfigure (2, {'weight' : 0, 'minsize' : 30})
        self.rowconfigure (3, {'weight' : 0, 'minsize' : 30})
        self.rowconfigure (4, {'weight' : 0, 'minsize' : 30})
        self.columnconfigure (1, {'weight' : 0, 'minsize' : 30})
        self.columnconfigure (2, {'weight' : 0, 'minsize' : 30})
        self.columnconfigure (3, {'weight' : 0, 'minsize' : 30})
        self.columnconfigure (4, {'weight' : 0, 'minsize' : 30})
        self.columnconfigure (5, {'weight' : 0, 'minsize' : 30})

#coloca o objeto(caixas, botões e imagens) em suas posições na tela (coluna x linha)

    def posicionaObjetos(self):
        self.img_1.grid({
              'in' : self,
              'column' : '1',
              'row' : '1',
              'sticky' : ''
              })

        self.img_2.grid({
              'in' : self,
              'column' : '2',
              'row' : '1',
              'sticky' : ''
              })

        self.img_3.grid({
              'in' : self,
              'column' : '3',
              'row' : '1',
              'sticky' : ''
              })

        self.img_4.grid({
              'in' : self,
              'column' : '1',
              'row' : '3',
              'sticky' : ''
              })

        self.img_5.grid({
              'in' : self,
              'column' : '2',
              'row' : '3',
              'sticky' : ''
              })

        self.img_6.grid({
              'in' : self,
              'column' : '3',
              'row' : '3',
              'sticky' : ''
              })

        self.a.grid({
              'in' : self,
              'column' : '1',
              'row' : '2',
              'sticky' : ''
              })

        self.b.grid({
              'in' : self,
              'column' : '2',
              'row' : '2',
              'sticky' : ''
              })

        self.c.grid({
              'in' : self,
              'column' : '3',
              'row' : '2',
              'sticky' : ''
              })

        self.d.grid({
              'in' : self,
              'column' : '1',
              'row' : '4',
              'sticky' : ''
              })

        self.e.grid({
              'in' : self,
              'column' : '2',
              'row' : '4',
              'sticky' : ''
              })

        self.f.grid({
              'in' : self,
              'column' : '3',
              'row' : '4',
              'sticky' : ''
              })

        self.btOK.grid({
              'in' : self,
              'column' : '2',
              'row' : '5',
              'sticky' : ''
              })
        self.btSAIR.grid({
              'in' : self,
              'column' : '3',
              'row' : '5',
              'sticky' : ''
              })
#cria a função de retorno das variáveis das checkbox

    def pegarA(self):
        return self.varA.get()

    def pegarB(self):
        return self.varB.get()

    def pegarC(self):
        return self.varC.get()

    def pegarD(self):
        return self.varD.get()

    def pegarE(self):
        return self.varE.get()

    def pegarF(self):
        return self.varF.get()

#desenha a tela    

    def mostraFrame(self, **packOptions):
        self.pack(packOptions)


    def setres(self,res):
        self.res = res

#define as funções do botão sair (fechar o jogo)

    def btSAIR(self):
        self.master.destroy()
        self.destroy()

#define as funções do botão OK (pegar o valor das variáveis)

    def btOK(self):
        self.res.calcula(self)
        self.varA.set(0)
        self.varB.set(0)
        self.varC.set(0)
        self.varD.set(0)
        self.varE.set(0)
        self.varF.set(0)


#faz o calculo do número pensado, seguindo a lógica que se a primeira checkbox for selecionada o valor será 1, a segunda será 2, a terceira será 4, a quarta será 8, a quinta 16 e sexta 32. Pois a soma dos variáveis onde o número pensado aparece utiliza-se desta regra para dar a resposta ao usuário

class Resultado(Tk.Frame):
    def calcula(self,app):
        self.x = 0
        if app.pegarA() == 1:
            self.x+= 1
        if app.pegarB() == 1:
            self.x+= 2
        if app.pegarC() == 1:
            self.x+= 4
        if app.pegarD() == 1:
            self.x+= 8
        if app.pegarE() == 1:
            self.x+= 16
        if app.pegarF() == 1:
            self.x+= 32

        res = self.montaTela()
        return res
#cria a tela do resultado

    def montaTela(self, master2=None):

        if self.x <= 0:
            res = tkMessageBox.showinfo("RESULTADO ", "Você não pensou em nenhum número")
        elif self.x > 60:
            res = tkMessageBox.showinfo("RESULTADO ", "Por favor pense em números de 1 a 60")
        else:
            res = tkMessageBox.showinfo("RESULTADO ", "Você pensou no número: "+str(self.x))

        return res

    def btSAIR(self):
        self.master2.destroy()
#cria o aplicativo propriamente dito        
def inicia():
    app = App()
    res = Resultado()

    app.setres(res)
    app.criaImagens()
    app.criaCheck()
    app.criaBot()
    app.configuraFrame()
    app.posicionaObjetos()
    app.mostraFrame(fill = 'both', expand = 1)

    app.mainloop ()


if __name__ == '__main__':
    inicia()
