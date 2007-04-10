#!/bin/env python
import string
for letra in ["0","1","2","3","4","5","6","7"]:
    for bold in ['',';1']:
        for fundo in ["0","1","2","3","4","5","6","7"]:
            seq="4"+fundo+";3"+letra
            saida = "\033["+seq+bold+"m"+string.center(seq+bold,8)+"\033[m"
            print "%s" % saida,
        print
