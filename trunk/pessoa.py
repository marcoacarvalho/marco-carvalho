class Pessoa:
   def __init__(self, codigo, nome, endereco, telefone):
       self.codigo = codigo
       self.nome = nome
       self.endereco = endereco
       self.telefone = telefone

   def read(self):
       self.codigo = raw_input("Codigo: ")
       self.nome = raw_input("Nome: ")
       self.endereco = raw_input("Endereco: ")
       self.telefone = raw_input("Telefone: ")

   def write(self):
       print "[%s] %s" % (self.codigo, self.nome)
       print "End.: %s" % self.endereco
       print "Fone: %s" % self.telefone

