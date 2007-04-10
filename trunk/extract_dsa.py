#!/bin/env python
# -*- coding: latin-1 -*-

# Copyright (c)2006 Marco Carvalho (macs) <marcocarvalho89@yahoo.com.br>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; the version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License with
# the Debian GNU/Linux distribution in file /usr/share/common-licenses/GPL;
# if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA  02111-1307  USA
#
# On Debian systems, the complete text of the GNU General Public
# License, version 2, can be found in /usr/share/common-licenses/GPL-2.
#
#File: extract_dsa.py
#Version: 0.2

"""
extract_dsa.py

Extrai o conteudo da pagina HTML de avisos de seguranca
Debian (DSAs) e gera um template de e-mail para o mutt.

Uso: extract_dsa.py <numero_da_dsa> > arquivo_template.
     ex: extract_dsa 960 > dsa_960.txt

Apos gerar o template carregue-o com:
~$ mutt -H arquivo_template
"""
import sys
import urllib
import sgmllib
import re

dsa_regex = re.compile(r"(DSA-\d+-\d+\s+.+\s+--\s+.+)")
cve_regex = re.compile(r"(CVE-\d+-\d+)")
dsa_data = re.compile(r"(?P<dd>..)/(?P<mm>..)/(?P<aaaa>....)")
Meses = ('Janeiro',	\
		'Fevereiro',	\
		'Março',		\
		'Abril',		\
		'Maio',		\
		'Junho',		\
		'Julho',		\
		'Agosto',	\
		'Setembro',	\
		'Outubro',	\
		'Novembro',	\
		'Dezembro')
class DsaParser(sgmllib.SGMLParser):

	inside_text = False
	text = ''
	matches = []
	cve = []
	last_item = ''
	lista = []

	def start_div(self, attrs):
		for attr, value in attrs:
			if value == "inner":
				self.inside_text = True

	def end_div(self):
		self.inside_text = False

	def handle_data(self, data):
		if self.inside_text and data:
			m = dsa_regex.match(data)
			if m is not None:
				self.matches.extend(m.groups())
				self.dsa_string = self.matches[0].split(' ',3)
			m = cve_regex.match(data)
			if m is not None:
				self.cve.extend(m.groups())
				self.lista = uniq(self.cve)
			m = dsa_data.search(data)
			if m is not None:
				self.dia = m.group('dd')
				self.mes = Meses[int(m.group('mm'))-1]
				self.ano = m.group('aaaa')
			self.text = self.text + data

def uniq(l):
	res = []
	for x in l:
		if x not in res:
			res.append(x)
	return res

def main():
	for url in sys.argv[1:]:
		try:
			myurl = "http://www.us.debian.org/security/2006/dsa-%s.pt.html" % url
			file = open(myurl)
		except IOError:
			file = urllib.urlopen(myurl)
		cve_items = ''
		links = ''
		p = DsaParser()
		p.feed(file.read())
		p.close()
		dsa = p.dsa_string[0]
		package = p.dsa_string[1]
		issue = p.dsa_string[3]
		if p.lista:
			for item, obj in enumerate(p.lista):
				cve_items = cve_items + "[" + str(item+3) + "]" + obj + ", "
		links = links + str(item+3) + ".http://cve.mitre.org/cgi-bin/cvename.cgi?name=" + obj + "\n"
		else:
		cve_items = "Nenhuma outra base de dados externas de referências de segurança está disponível atualmente."
		text = ''
		lines = p.text.splitlines()
		for item in lines[14:]:
			text = text + item + "\n"

        header="""To: debian-news-portuguese@lists.debian.org
Cc:
Bcc:
Subject: [SEGURANCA][%s] %s (%s)
Reply-To: debian-user-portuguese@lists.debian.org
--------------------------------------------------------------------------
Alerta de Segurança Debian %s                  security@debian.org
http://www.debian.org/security/%s/dsa-%s
%s de %s de %s                 http://www.debian.org/security/faq
--------------------------------------------------------------------------
Essa é uma tradução do DSA (Debian Security Advisory - Alerta de Segurança
Debian) que é enviado para a lista [1]debian-security-announce e, por esse
motivo, há um atraso entre o anúncio original em inglês e esta tradução.
Caso queira receber os alertas em inglês, [2]inscreva-se na lista.

1.http://lists.debian.org/debian-security-announce
2. Envie um e-mail para debian-security-announce-request@lists.debian.org
   e coloque no campo assunto a palavra \"subscribe\".
--------------------------------------------------------------------------
Vulnerabilidade  : %s
CVE ID           : %s
""" % (dsa,package,issue,dsa,p.ano,url,p.dia,p.mes,p.ano,issue,cve_items)

        footer="""
%s
--

        Marco Carvalho (macs) <marcocarvalho89@yahoo.com.br>
 *******************************************************************
   .''`.   Debian Weekly News: <http://www.debian.org/News/weekly>
  : :'  :  Debian BR.........: <http://debianbrasil.org>
  `. `'`        Equipe de Imprensa e Traduções do Debian-BR
    `-                 O que você quer saber hoje?
""" % (links)

        print header
        print text
        print footer
        file.close

if __name__ == "__main__":
    main()