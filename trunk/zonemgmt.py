#!/usr/bin/env python
import dns.zone
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *

domain = "example.com"
print "Getting zone object for domain", domain
zone_file = "/etc/bind/databases/db.%s" % domain

try:
    zone = dns.zone.from_file(zone_file, domain)
    print "Zone origin:", zone.origin
    for name, node in zone.nodes.items():
        rdatasets = node.rdatasets
        print "\n**** BEGIN NODE ****" 
        print "node name:", name
        for rdataset in rdatasets:
            print "--- BEGIN RDATASET ---"
            print "rdataset string representation:", rdataset
            print "rdataset rdclass:", rdataset.rdclass
            print "rdataset rdtype:", rdataset.rdtype
            print "rdataset ttl:", rdataset.ttl
            print "rdataset has following rdata:"
            for rdata in rdataset:
                print "-- BEGIN RDATA --"
                print "rdata string representation:", rdata
                #print type(rdata)
                #print dir(rdata)
                if rdataset.rdtype == SOA:
                    print "** SOA-specific rdata **"
                    print "expire:", rdata.expire
                    print "minimum:", rdata.minimum
                    print "mname:", rdata.mname
                    print "refresh:", rdata.refresh
                    print "retry:", rdata.retry
                    print "rname:", rdata.rname
                    print "serial:", rdata.serial
                if rdataset.rdtype == MX:
                    print "** MX-specific rdata **"
                    print "exchange:", rdata.exchange
                    print "preference:", rdata.preference
                if rdataset.rdtype == NS:
                    print "** NS-specific rdata **"
                    print "target:", rdata.target
                if rdataset.rdtype == CNAME:
                    print "** CNAME-specific rdata **"
                    print "target:", rdata.target
                if rdataset.rdtype == A:
                    print "** A-specific rdata **"
                    print "address:", rdata.address

    print "\n*****Modifying zone*****\n"

    for (name, ttl, rdata) in zone.iterate_rdatas(SOA):
        serial = rdata.serial
        new_serial = serial + 1
        print "Changing SOA serial from %d to %d" %(serial, new_serial)
        rdata.serial = new_serial
        
    A_change = "www"
    new_IP = "10.1.1.10"
    print "Changing A record for", A_change, "to", new_IP
    rdataset = zone.find_rdataset(A_change, rdtype=A)
    for rdata in rdataset:
        rdata.address = new_IP

    rdataset = zone.find_rdataset("@", rdtype=NS)
    new_ttl = rdataset.ttl / 2
    print "Changing TTL for NS records to", new_ttl
    rdataset.ttl = new_ttl

    node_delete = "www2"
    print "Deleting node", node_delete
    zone.delete_node(node_delete)

    A_add = "www4"
    print "Adding record of type A:", A_add
    rdataset = zone.find_rdataset(A_add, rdtype=A, create=True)
    rdata = dns.rdtypes.IN.A.A(IN, A, address="10.1.1.10")
    rdataset.add(rdata, ttl=86400)

    CNAME_add = "www3_alias"
    target = dns.name.Name(("www3",))
    print "Adding record of type CNAME:", CNAME_add
    rdataset = zone.find_rdataset(CNAME_add, rdtype=CNAME, create=True)
    rdata = dns.rdtypes.ANY.CNAME.CNAME(IN, CNAME, target)
    rdataset.add(rdata, ttl=86400)

    A_add = "ns3"
    print "Adding record of type A:", A_add
    rdataset = zone.find_rdataset(A_add, rdtype=A, create=True)
    rdata = dns.rdtypes.IN.A.A(IN, A, address="10.1.1.10")
    rdataset.add(rdata, ttl=86400)

    NS_add = "@"
    target = dns.name.Name(("ns3",))
    print "Adding record of type NS:", NS_add
    rdataset = zone.find_rdataset(NS_add, rdtype=NS, create=True)
    rdata = dns.rdtypes.ANY.NS.NS(IN, NS, target)
    rdataset.add(rdata, ttl=86400)


    MX_add = "@"
    exchange = dns.name.Name(("mail4",))
    preference = 30
    print "Adding record of type MX:", MX_add
    rdataset = zone.find_rdataset(MX_add, rdtype=MX, create=True)
    rdata = dns.rdtypes.ANY.MX.MX(IN, MX, preference, exchange)
    rdataset.add(rdata, ttl=86400)

    new_zone_file = "/etc/bind/databases/db.%s" % domain
    print "Writing modified zone to file %s" % new_zone_file
    zone.to_file(new_zone_file)

    print "\nALL 'IN' RECORDS EXCEPT 'SOA' and 'TXT':"
    for name, node in zone.nodes.items():
        rdatasets = node.rdatasets
        for rdataset in rdatasets:
            if rdataset.rdclass != IN or rdataset.rdtype in [SOA, TXT]:
                continue
            print name, rdataset

    print "\nGET_RDATASET('A'):"
    for name, node in zone.nodes.items():
        rdataset = node.get_rdataset(rdclass=IN, rdtype=A)
        if not rdataset:
            continue
        for rdataset in rdataset:
            print name, rdataset

    print "\nITERATE_RDATAS('A'):"
    for (name, ttl, rdata) in zone.iterate_rdatas('A'):
        print name, ttl, rdata

    print "\nITERATE_RDATAS('MX'):"
    for (name, ttl, rdata) in zone.iterate_rdatas('MX'):
        print name, ttl, rdata

    print "\nITERATE_RDATAS('CNAME'):"
    for (name, ttl, rdata) in zone.iterate_rdatas('CNAME'):
        print name, ttl, rdata

except DNSException, e:
    print e.__class__, e

