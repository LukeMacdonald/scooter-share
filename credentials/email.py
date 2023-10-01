import os
import base64
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This code was sourced from https://developers.google.com/gmail/api/quickstart/python
def create_service(api_name,api_version, *scopes):
    """
    Creates a connection to a Google API service using OAuth 2.0 authentication.

    Parameters:
        api_name (str): The name of the API to connect to (e.g., 'gmail', 'calendar', etc.).
        api_version (str): The version of the API (e.g., 'v1', 'v3', etc.).
        *scopes (list): Variable number of scope strings indicating the access level the application is requesting.

    Returns:
        Google API service object or None: Returns the API service object if connection is successful, None otherwise.
    """
    client_secret_file  = 'credentials/client_secret.json'
        
    cred = None

    pickle_file = f'credentials/token_{api_name}.pickle'
  
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file , scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_name, api_version, credentials=cred)
        print(api_name, 'service created successfully')
        return service
    except Exception as error:
        print('Unable to connect.')
        print(error)
        return None

def send_email(subject, to_email, html_content):
    """
    Sends an HTML email using Gmail API.

    Parameters:
        subject (str): The subject of the email.
        to_email (str): The recipient's email address.
        html_content (str): The HTML content of the email.

    Returns:
        dict: The response from the Gmail API after sending the email.
    """    
    try:
        service = create_service('gmail','v1', ['https://mail.google.com/'])
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = to_email
        mimeMessage['subject'] = subject
        mimeMessage.attach(MIMEText(html_content, 'html'))  # Set the content type to 'html' for HTML emails
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        return message
    except Exception as error:
        # Handle exceptions and errors gracefully
        print(f"Error occurred: {error}")
        return None
    