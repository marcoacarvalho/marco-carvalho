from threading import Thread

class conta(Thread):
   def run(self):
       for i in range(10):
           print i
x = conta().start()
y = conta().start()
z = conta().start()
