import base64
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

MASTER_LOG = "master_log.txt"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def create_email_body(name: str, company_name: str, sender_email: str) -> str:
    """Create personalized email body."""
    return f"""Hello {name},

I am writing to you regarding {company_name}'s business opportunities and growth potential. I'm attaching a personalized brochure for you to review.

Feel free to reach out to me at {sender_email} if you have any questions.

Thank you for your consideration!

Best regards"""

def create_reply_message_with_attachment(to: str, subject: str, message_text: str, attachment_path: str, in_reply_to_id: str, thread_id: str, sender_email: str):
    """Create a reply message with attachment."""
    message = MIMEMultipart()
    
    message['to'] = to
    message['from'] = sender_email
    message['subject'] = subject if subject.startswith('Re:') else f"Re: {subject}"
    message['In-Reply-To'] = in_reply_to_id
    message['References'] = in_reply_to_id
    
    message.attach(MIMEText(message_text, 'plain'))
    
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(attachment_path)}'
        )
        message.attach(part)
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    return {
        'raw': raw,
        'threadId': thread_id
    }

def send_reply_email(service, message, thread_id: str) -> bool:
    """Send the reply email."""
    try:
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        log_message(f"✅ Reply email sent successfully (Message ID: {sent_message.get('id')})")
        return True
    except Exception as error:
        log_message(f"❌ Failed to send reply email: {str(error)}")
        return False
