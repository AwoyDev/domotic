import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(mail_content: str):
  receiver_address = 'email'
  sender_address = 'email'
  sender_pass = 'password'
  mail_content = " "
  message = MIMEMultipart()
  message['From'] = sender_address
  message['To'] = receiver_address
  message['Subject'] = 'Raspberry alarme de sécurité'  
  message.attach(MIMEText(mail_content, 'plain'))
  session = smtplib.SMTP('smtp.gmail.com', 587) 
  session.starttls() 
  session.login(sender_address, sender_pass) 
  text = message.as_string()
  session.sendmail(sender_address, receiver_address, text)
  session.quit()

GPIO.setmode(GPIO.BCM)
GPIO_PIR = 7
GPIO.setup(GPIO_PIR,GPIO.IN)

Current_State  = 0
Previous_State = 0

try:
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0    
    send_email(mail_content = "L'alarme vient d'être activé 🚨")
  while True :
    Current_State = GPIO.input(GPIO_PIR)
    if Current_State==1 and Previous_State==0:
      send_email(mail_content = "Un mouvement vient d'être détecté 🚨")
      Previous_State=1
      time.sleep(0.01)      
      
except KeyboardInterrupt:
    send_email(mail_content = "L'alarme vient d'être désactivé 🚨")
    GPIO.cleanup()