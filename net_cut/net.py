#! /usr/bin/env/ python

import netfilterqueue as nf

def process_packet(packet):
	print(packet)
	packet.drop()
	
queue = nf.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
