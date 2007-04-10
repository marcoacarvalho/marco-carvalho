#!/usr/bin/env python
#**** cores.py ****

import sys

for frente in xrange(8):
       for bold in '', ";1":
               for fundo in xrange(8):
                       seq="4%d;3%d%s" % (fundo, frente, bold)
                       saida = "\033[%sm %s" % (seq, seq.ljust(8))
                       sys.stdout.write(saida)
               sys.stdout.write("\033[0m\n")
