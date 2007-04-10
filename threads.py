import subprocess as sp

x = sp.Popen("console")
print "Pid do subprocesso 1: %d" % x.pid
x = sp.Popen("console")
print "Pid do subprocesso 2: %d" % x.pid
x = sp.Popen("console")
print "Pid do subprocesso 3: %d" % x.pid
raw_input()
print "Implementacao com threads"

