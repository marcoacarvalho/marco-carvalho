from Tkinter import *
from time import localtime
import math

class Relogiodigital:
   def __init__(self,raiz):
       self.canvas=Canvas(raiz, width=100, height=100,
                          bg='dodgerblue',highlightthickness=0)
       self.canvas.pack()
       #self.mostrar=Button(self.canvas,command=self.mostra())
       #self.mostrar2=Button(self.canvas,command=self.mostra2())
       #self.mostrar3=Button(self.canvas,command=self.mostra3())
       self.texto=self.canvas.create_text
       self.canvas.create_oval(4,4,73,73, fill='black')
       #self.canvas.create_oval(37,37,43,43, fill='white')
       self.fonte=('verdana','7')
       self.texto(40,10, text='12',font=self.fonte, fill='white')
       self.texto(55,15, text='1',font=self.fonte, fill='white')
       self.texto(65,25, text='2',font=self.fonte, fill='white')
       self.texto(65,40, text='3',font=self.fonte, fill='white')
       self.texto(63,52, text='4',font=self.fonte, fill='white')

       self.texto(55,63, text='5',font=self.fonte, fill='white')
       self.texto(40,65, text='6',font=self.fonte, fill='white')
       self.texto(26,64, text='7',font=self.fonte, fill='white')
       self.texto(16,52, text='8',font=self.fonte, fill='white')
       self.texto(13,40, text='9',font=self.fonte, fill='white')
       self.texto(13,26, text='10',font=self.fonte, fill='white')
       self.texto(25,15, text='11',font=self.fonte, fill='white')

       self.canvas.create_line(0, 0, 0, 0, tag='s', fill='yellow')
       self.canvas.create_line(0, 0, 0, 0, tag='m', fill='green')
       self.canvas.create_line(0, 0, 0, 0, tag='h', fill='magenta')

       self.mostra()

   def mostra(self):
       hora, min, seg = localtime()[3:6]
#       print hora
       # desenha segundo
       #angulo do ponteiro, em radianos
       r = math.radians((360/60*seg) - 90)

       x = int(40+(math.cos(r)*20))
       y = int(40+(math.sin(r)*20))
#       print x, y

       self.canvas.coords('s', 40, 40, x, y)

       # desenha minuto
       r = math.radians((360/60*min) - 90)

       x = int(40+(math.cos(r)*20))
       y = int(40+(math.sin(r)*20))
#       print x, y

       self.canvas.coords('m', 40, 40, x, y)

       #desenha hora
       r = math.radians((360/12*hora) - 90)

       x = int(40+(math.cos(r)*20))
       y = int(40+(math.sin(r)*20))
#       print x, y

       self.canvas.coords('h', 40, 40, x, y)

       #agenda self.mostra para execucao daqui a 100 ms
       self.canvas.after(100,self.mostra)


instancia=Tk()
Relogiodigital(instancia)
instancia.mainloop()
