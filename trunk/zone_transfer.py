#!/usr/bin/env python
import dns.resolver
import dns.query
import dns.zone
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *

domain = "dnspython.org"
print "Getting NS records for", domain
answers = dns.resolver.query(domain, 'NS')
ns = []
for rdata in answers:
    n = str(rdata)
    print "Found name server:", n
    ns.append(n)

for n in ns:
    print "\nTrying a zone transfer for %s from name server %s" % (domain, n)
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(n, domain))

        print "\nALL RECORDS:"
        for name, node in zone.nodes.items():
            rdataset = node.rdatasets
            for record in rdataset:
                print name, record

        print "\nALL 'IN' RECORDS EXCEPT 'SOA' and 'TXT':"
        for name, node in zone.nodes.items():
            rdataset = node.rdatasets
            for record in rdataset:
                if record.rdclass != IN or record.rdtype in [SOA, TXT]:
                    continue
                print name, record

        print "\nITERATING THROUGH 'A' RECORDS:"
        for (name, ttl, rdata) in zone.iterate_rdatas('A'):
            print name, ttl, rdata

        print "\nITERATING THROUGH 'MX' RECORDS:"
        for (name, ttl, rdata) in zone.iterate_rdatas('MX'):
            print name, ttl, rdata


        break
    except DNSException, e:
        print e.__class__, e

