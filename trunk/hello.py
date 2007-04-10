#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# hello.py
#

from Tkinter import *                  # importa o módulo que contém as classes de GUI
import sys                             # classes do sistema

def principal():                       # função principal do programa
   raiz = Tk()                         # cria o widget principal
   botao = Button(raiz)                # cria um botão como filho do widget principal
   botao['text'] = 'Olá mundo!'        # Texto do botão
   botao['command'] = sai              # quando clicado sai (veja abaixo)
   botao.pack()
   raiz.mainloop()                     # loop principal que gerencia os eventos

def sai():
   sys.exit(0)                         # sai sem erro.

principal()                            # executa principal
