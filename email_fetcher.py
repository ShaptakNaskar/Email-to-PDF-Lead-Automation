import os
import base64
from datetime import datetime
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pickle

MASTER_LOG = "master_log.txt"
TOKEN_FILE = "token.pickle"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def authenticate_gmail():
    """Authenticate with Gmail API using existing token.pickle from gmail_auth.py."""
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"❌ {TOKEN_FILE} not found! Run gmail_auth.py first to authenticate.")
    
    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)
    
    return build('gmail', 'v1', credentials=creds)

def clean_html_to_text(html_content):
    """Convert HTML email content into plain readable text."""
    import re
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n')
    text = re.sub(r'\n\s*\n+', '\n\n', text.strip())
    return text

def extract_message_data(message):
    """Extract sender, subject, and body text from a Gmail API message."""
    import re
    headers = message['payload'].get('headers', [])
    sender = subject = None
    
    for header in headers:
        name = header['name'].lower()
        if name == 'from':
            sender = header['value']
        elif name == 'subject':
            subject = header['value']
    
    body = ""
    parts = message['payload'].get('parts', [])
    
    if parts:
        for part in parts:
            mime_type = part.get('mimeType', '')
            data = part['body'].get('data')
            
            if data:
                decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                if mime_type == 'text/plain':
                    body += decoded_data
                elif mime_type == 'text/html' and not body:
                    body += clean_html_to_text(decoded_data)
    else:
        data = message['payload']['body'].get('data')
        if data:
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            if message['payload']['mimeType'] == 'text/html':
                body = clean_html_to_text(decoded_data)
            else:
                body = decoded_data
    
    return sender, subject, body.strip()

def fetch_latest_email(service):
    """Fetch the latest email from Gmail inbox."""
    try:
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=1,
            q=''
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return None
        
        message_id = messages[0]['id']
        msg = service.users().messages().get(userId='me', id=message_id).execute()
        
        sender, subject, body = extract_message_data(msg)
        
        return {
            'message_id': message_id,
            'sender': sender,
            'subject': subject,
            'body': body
        }
    
    except Exception as e:
        log_message(f"❌ Error fetching email: {type(e).__name__}: {str(e)}")
        return None
