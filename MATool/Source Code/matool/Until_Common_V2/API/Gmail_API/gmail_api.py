"""Send an email message from the user's account.
"""
import mimetypes
import os
import pickle
import base64

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from django.conf import settings

class GmailApi:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.compose','https://www.googleapis.com/auth/gmail.send']
    _service = ''
    def __init__(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(settings.BASE_DIR + '/static/json/json_gmail_api/token.pickle'):
            with open(settings.BASE_DIR + '/static/json/json_gmail_api/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        settings.BASE_DIR + '/static/json/json_gmail_api/credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(settings.BASE_DIR + '/static/json/json_gmail_api/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self._service = build('gmail', 'v1', credentials=creds)

    def send_message(self, user_id, message):
        """Send an email message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
            Sent Message.
        """
        try:
            service = self._service
            message = (service.users().messages().send(userId=user_id, body=message)
                    .execute())
            print ('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)


    def create_html_message(self,sender, to, subject, message_text,cc='',bcc=''):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEMultipart('alternative')
        message['subject'] = subject
        message['from'] = 'Leadplus Reporting System <noreply@leadplus.app>'
        message['to'] = to
        message['Cc'] = cc
        message['Bcc'] = bcc
        
        part1 = MIMEText(message_text,'html')
        message.attach(part1)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    def create_message_with_attachment(self,sender, to, subject, message_text, file,cc='',bcc=''):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.
            file: The path to the file to be attached.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEMultipart('alternative')
        message['subject'] = subject
        message['from'] = 'Leadplus Reporting System <noreply@leadplus.app>'
        message['to'] = to
        message['Cc'] = cc
        message['Bcc'] = bcc

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        if main_type == 'text':
            fp = open(file, 'r',encoding="utf-8")
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            # msg = MIMEBase(main_type, sub_type)
            msg = MIMEBase(main_type, "octet-stream")
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        # return {'raw': base64.urlsafe_b64encode(message.as_string())}
        # return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


