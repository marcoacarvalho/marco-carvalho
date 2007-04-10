import sys
for seq in xrange(1, 10):
     saida = '\033[G\033[@#\033[11G\033[0K%d' % (seq)
     sys.stdout.write(saida)
print ''
