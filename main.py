import smtplib
import subprocess
from email.mime.text import MIMEText
import time
import os

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
SERVER_HOST = os.environ.get('SERVER_HOST')

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(msg)

def ping_server(host):
    try:
        # subprocess.check_output(['ping', host], universal_newlines=True)
        print(subprocess.check_output(['ping', host], universal_newlines=True))
        return True
    except subprocess.CalledProcessError:
        return False


while True:
    if ping_server(SERVER_HOST):
        current_time = time.strftime("%H:%M:%S")
        send_email("Server Status", f"{current_time} Server {SERVER_HOST} ist aktiv.")
        print(f"{current_time} SERVER AKTIV")
    else:
        current_time = time.strftime("%H:%M:%S")
        send_email("Achtung: Server Down Alarm", f"{current_time} Server {SERVER_HOST} antwortet nicht.")
        print(f"{current_time} SERVER ANTWORTET NICHT")
    break
