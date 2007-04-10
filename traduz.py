#!/bin/env python
# -*- coding: latin-1 -*-

import re, sys

orig_path = "/home/marco/DWN/webwml/english/security"
dest_path = "/home/marco/teste"
year = "2006"
tabela = {
    '([^ ]*) creates a temporary file': '\\1 cria um arquivo temporário',
    'identifies the following problems:': 'identificou os seguintes problemas:',
    'programming error':'erro de programação',
    }

def traduz(srcfile, dstfile):
    f = open (srcfile)
    g = open (dstfile,'w')
    texto = f.read()
    for expr, subst in tabela.iteritems():
        texto = re.sub(expr, subst, texto)
    g.write(texto)

if __name__ == '__main__':

    num_dsa = raw_input("Informe o no. da DSA: ")
    arquivoin = "%s/%s/dsa-%s.wml" % (orig_path,year,num_dsa)
    arquivoout = "%s/%s/dsa-%s.wml" % (dest_path,year,num_dsa)

    traduz(arquivoin, arquivoout)

