#!/bin/env/python

import scapy.all as scapy
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_brodcast_request = brodcast/arp_request
    answered = scapy.srp(arp_brodcast_request, timeout=1)[0]
	for elements in answered:
		print(elements[1].hwsrc)
		print(elements[1].psrc)
		print("-------------------------------------------")
	
scan("172.16.93.2")
