import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login('tulu.gupta1234@gmail.com', 'hczbswsmltuhywdj')
server.sendmail('tulu.gupta1234@gmail.com', 'tulu.gupta1234@gmail.com', 'hello')
server.quit()
