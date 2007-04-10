# -*- encoding: iso8859-1 -*-
ass_padrao = open('assinatura_padrao.html', 'r').read()

pasta_armazenamento = ''

dic = {}
dic['nome'] = raw_input('Entre com o nome completo da pessoa: ')
dic['tel'] = raw_input('Entre com o telefone da pessoa (Ex: 55 71 2525 2525): ')
dic['cel'] = raw_input('Entre com o celular da pessoa (Ex: 55 71 2525 2525): ')
dic['fax'] = raw_input('Entre com o fax da pessoa (Ex: 55 71 2525 2525): ')
dic['skype'] = raw_input('Entre com o skype da pessoa (Ex: 71 2525 2525): ')
dic['nome_email'] = raw_input('Entre com o nome do e-mail (nome que vem antes de @email.com.br): ')

for i in dic.keys():
   ass_padrao = ass_padrao.replace('%('+i+')', dic[i])

endereco_arquivo = pasta_armazenamento + dic['nome_email'] + '.html'

fp = open(endereco_arquivo, 'w')
fp.write(unicode(ass_padrao, 'iso8859-1'))
fp.close()

print "\n" * 2
print "Assinatura criada em: %s" % (endereco_arquivo)


raw_input("Aperte ENTER para sair.")
