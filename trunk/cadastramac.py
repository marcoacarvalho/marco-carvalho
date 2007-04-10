import string
from macaddress_db import *

def processamac(macaddress):

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        return macaddress
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
        return macaddress
    else:
        raise ValueError('Formato incorreto do MAC Address')

def gslice(seq, step=1):
     for i in xrange(0, len(seq), step):
             yield seq[i : i+step]

local = string.upper(raw_input("Local (OFM/UNIBRATEC): "))
for i in Host.select(Host.q.Local==local):
    print i.Host_IP

mac = testamac(string.upper(raw_input("MAC ADDRESS (xx:xx:xx:xx:xx:xx): ")))
ip = raw_input ("IP (xx.xx.xx.xx): ")
mac2 = ':'.join(gslice(mac,2))
print "%s %s %s" % (mac2, ip, local)

#Host(HostName = ip, MacAddress = mac, Host_IP = ip, Local = local)
