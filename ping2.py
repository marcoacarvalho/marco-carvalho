#!/usr/bin/python
import os
import re
import time
import sys
from threading import Thread

class ping(Thread):
    def __init__ (self,ip):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
    def run(self):
        pingseq = os.popen("ping -q -c2 "+self.ip,"r")
        while 1:
            line = pingseq.readline()
            if not line: break
result = re.findall(ping.getstatus,line)
if result:
    self.status = int(result[0])
ping.getstatus = re.compile(r"(\d) received")
output = ("Not responding","Partial Response","Responding")

print time.ctime()

pinglist = []

for host in range(60,70):
    ip = "200.172.171."+str(host)
    current = ping(ip)
    pinglist.append(current)
    current.start()

for pingle in pinglist:
    pingle.join()
    print "Status from ",pingle.ip,"is",output[pingle.status]

print time.ctime()
