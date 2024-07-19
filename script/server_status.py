from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import os
import pytz
import smtplib
import subprocess

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
SERVER_HOST = os.environ.get('SERVER_HOST')

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    # Attachment; filename="server_status.csv"'
    with open('server_status.csv', 'rb') as csvfile:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(csvfile.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename='server_status.csv')
        msg.attach(attachment)

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(msg)


def ping_server(host):
    try:
        subprocess.check_output(['curl', host], universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False
    

TZ_MADRID = pytz.timezone('Europe/Madrid')
CURRENT_TIME = datetime.now(TZ_MADRID).strftime('%H:%M:%S')
CURRENT_HOUR = datetime.now(TZ_MADRID).strftime('%H')
CURRENT_DAY = datetime.now(TZ_MADRID).strftime('%A')


if ping_server(SERVER_HOST):
    if CURRENT_DAY == 'Friday' and CURRENT_HOUR == '07':
        with open('server_status.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([CURRENT_TIME, CURRENT_DAY, SERVER_HOST, 'Server ist aktiv'])
        send_email('Server Status', f'{CURRENT_TIME} Server {SERVER_HOST} ist aktiv.')
    else:
        with open('server_status.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([CURRENT_TIME, CURRENT_DAY, SERVER_HOST, 'Server ist aktiv'])
else:
    with open('server_status.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([CURRENT_TIME, CURRENT_DAY, SERVER_HOST, 'ANTWORTET NICHT'])
    send_email('Achtung: Server Down Alarm', f'{CURRENT_TIME} Server {SERVER_HOST} antwortet nicht.')

