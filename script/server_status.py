import smtplib, ssl
import subprocess
from email.mime.text import MIMEText
import time
import pytz
from datetime import datetime
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
        print(subprocess.check_output(['curl', host], universal_newlines=True))
        return True
    except subprocess.CalledProcessError:
        return False
    

TZ_MADRID = pytz.timezone('Europe/Madrid')
CURRENT_TIME = datetime.now(TZ_MADRID).strftime('%H:%M:%S')
CURRENT_HOUR = datetime.now(TZ_MADRID).strftime('%H')

if ping_server(SERVER_HOST):
    if CURRENT_HOUR == '09':
        send_email('Server Status', f'{CURRENT_TIME} Server {SERVER_HOST} ist aktiv.')
        print(f'{CURRENT_TIME} SERVER AKTIV')
    else:
        print(f'{CURRENT_TIME} Server ist aktiv')
else:
    send_email('Achtung: Server Down Alarm', f'{CURRENT_TIME} Server {SERVER_HOST} antwortet nicht.')
    print(f'{CURRENT_TIME} SERVER ANTWORTET NICHT')

