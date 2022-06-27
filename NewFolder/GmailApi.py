from __future__ import print_function
from email.mime import base
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from Google import create_service
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailSend:
 
    def __init__(self) -> None:
        CLIENT_SECRET_FILE = "credentials.json"
        API_NAME = "gmail"
        API_VERSION = "v1"
        SCOPES = ['https://mail.google.com/']
        self.sender_email = "saakiiikas@gmail.com"
        self.service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    def send_email(self, msg, to, subject):
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = to
        mimeMessage['subject'] = subject

        mimeMessage.attach(MIMEText(msg, 'plain'))
        string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = self.service.users().messages().send(userId='me', body={'raw': string}).execute()
        print(message)
        return True