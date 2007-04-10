import os
import random

def random_floats(lst_size):
   return [ random.random() for i in xrange(lst_size) ]

n = 1000000
l = random_floats(n)

def c():
   from ckth import kth as c_kth
   c_kth(l, n//2)
   os.system('pmap -d %s | tail -n 1' % os.getpid())

def py():
   from kth import kth as py_kth
   py_kth(l, n//2)
   os.system('pmap -d %s | tail -n 1' % os.getpid())

def psyco():
   from kth import kth as py_kth
   from psyco import proxy
   psyco_kth = proxy(py_kth)
   psyco_kth(l, n//2)
   os.system('pmap -d %s | tail -n 1' % os.getpid())

def nothing():
   os.system('pmap -d %s | tail -n 1' % os.getpid())
