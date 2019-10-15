#!/usr/bin/env python3
#snmp_discover.py

from processing import Process, Queue, Pool
import time
import subprocess
import sys
from snmp import Snmp

q = Queue()
oq = Queue()
#ips = IP("10.0.1.0/24")
ips = ["192.19.101.250", "192.19.101.251", "192.19.101.252","192.19.101.253","192.168.1.1"]
num_workers = 10

class HostRecord(object):
    """Record for Hosts"""
    def __init__(self, ip=None, mac=None, snmp_response=None):
        self.ip = ip
        self.mac = mac
        self.snmp_response = snmp_response
    
    def __repr__(self):
        return "[Host Record('%s','%s','%s')]" % (self.ip,self.mac,self.snmp_response)
    
def f(i,q,oq):
    while True:
        time.sleep(.1)
        if q.empty():
            sys.exit()
            print(f"Process Number: {i} Exit" )
        ip = q.get()
        print "Process Number: %s" % i
        ret = subprocess.call("ping -c 1 %s" % ip,shell=True,stdout=open('/dev/null', 'w'),stderr=subprocess.STDOUT)
        if ret == 0:
            print (f"{ip}: is alive")
            oq.put(ip)
        else:
            print (f"Process Number: {i} didn’t find a response for {ip}")
            pass
    
def snmp_query(i,out):
    while True:
        time.sleep(.1)
        if out.empty():
            sys.exit()
            print "Process Number: %s" % i
        ipaddr = out.get()
        s = Snmp()
        h = HostRecord()
        h.ip = ipaddr
        h.snmp_response = s.query()
        print h
        return h

try:
    q.putmany(ips)
finally:
    for i in range(num_workers):
        p = Process(target=f, args=[i,q,oq])
        p.start()
    
    for i in range(num_workers):
        pp = Process(target=snmp_query, args=[i,oq])
        pp.start()

print "main process joins on queue"
p.join()
#while not oq.empty():
#
print “Validated", oq.get()
print "Main Program finished"