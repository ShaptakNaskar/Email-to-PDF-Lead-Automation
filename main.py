# ============================================================================
# EMAIL PROCESSING PIPELINE - MAIN APPLICATION
# ============================================================================
# Primary entry point for the email monitoring and automation system
# ============================================================================

import os
import time
import traceback
from datetime import datetime
from groq import Groq

from config import EMAIL_FETCH_INTERVAL, MASTER_LOG, FAILED_LOG
from modules.email_handler import authenticate_gmail, fetch_latest_email, validate_email
from modules.web_scraper import scrape_website
from modules.ai_processor import (
    test_groq_connection, summarize_with_groq, 
    extract_company_name, extract_company_description, generate_blurbs
)
from modules.document_generator import generate_personalized_document, convert_docx_to_pdf
from modules.csv_manager import init_csv, add_or_update_lead, mark_as_done
from modules.telegram_notifier import (
    send_telegram_document, add_to_telegram_buffer, 
    flush_telegram_buffer, start_telegram_buffer_thread
)

# ============================================================================
# LOGGING UTILITIES
# ============================================================================

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to console, file, and Telegram buffer."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)
    
    # Add to Telegram buffer (escape HTML special characters)
    escaped_message = message.replace("<", "<").replace(">", ">").replace("&", "&")
    add_to_telegram_buffer(f"[{timestamp}] {escaped_message}")

def log_failure(step: str, error: str, log_file: str = FAILED_LOG):
    """Log failure to both file and Telegram."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] FAILED STEP '{step}': {error}\n"
    print(f"💥 {log_entry.strip()}")
    
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)
    
    # Telegram buffer
    escaped_error = error.replace("<", "<").replace(">", ">").replace("&", "&")
    add_to_telegram_buffer(f"💥 [{timestamp}] FAILED '{step}': {escaped_error}")

# ============================================================================
# EMAIL REPLY FUNCTIONALITY
# ============================================================================

def create_email_body(recipient_name: str) -> str:
    """Create professional email body for reply."""
    return f"""Hello {recipient_name},

Thank you for reaching out to us. We have reviewed your inquiry and are pleased to send you our personalized document, which outlines our services and how we can assist your organization.

Please find attached a detailed overview of our offerings tailored to your needs. We are confident that our solutions will provide significant value to your organization.

We would welcome the opportunity to discuss how we can support your business objectives. Please do not hesitate to contact us if you have any questions or would like to schedule a consultation.

Best regards,
Our Team
"""

def send_reply_email(service, email_recipient: str, original_subject: str, 
                    body: str, pdf_path: str, original_message_id: str) -> bool:
    """Send reply email with PDF attachment."""
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import base64
    
    try:
        # Create message
        message = MIMEMultipart()
        message['to'] = email_recipient
        message['subject'] = f"Re: {original_subject}"
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Add attachment
        if os.path.exists(pdf_path):
            part = MIMEBase('application', 'octet-stream')
            with open(pdf_path, 'rb') as attachment:
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(pdf_path)}')
            message.attach(part)
        
        # Send
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}
        
        service.users().messages().send(userId='me', body=send_message).execute()
        log_message(f"✅ Reply sent to {email_recipient}")
        return True
        
    except Exception as e:
        log_message(f"❌ Error sending reply: {type(e).__name__}: {str(e)}")
        return False

# ============================================================================
# MAIN PROCESSING FUNCTION
# ============================================================================

def process_incoming_email(service, groq_client, email_data: dict) -> bool:
    """Process a single incoming email through the entire pipeline."""
    
    try:
        message_id = email_data['message_id']
        sender = email_data['sender']
        subject = email_data['subject']
        body = email_data['body']
        
        log_message(f"\n📬 Processing email from {sender}")
        
        # Validate email
        is_valid, name, email, website = validate_email(sender, subject, body)
        
        if not is_valid:
            log_message(f"⚠️ Email does not meet qualification criteria. Skipping.")
            return False
        
        log_message(f"✅ Email validated - Name: {name}, Email: {email}, Website: {website}")
        
        # Add to CSV
        add_or_update_lead(message_id, name, email, website)
        log_message(f"📊 Added to leads database with Message ID: {message_id}")
        
        # Scrape website
        log_message(f"🌐 Scraping website: {website}")
        website_content = scrape_website(website)
        
        if not website_content:
            log_message(f"❌ Failed to scrape {website}. Cannot proceed.")
            return False
        
        # Summarize with Groq
        log_message(f"📄 Generating summary from website content...")
        summary = summarize_with_groq(website_content, groq_client)
        
        if not summary:
            log_message(f"❌ Failed to generate summary. Cannot proceed.")
            return False
        
        # Extract company info
        log_message(f"🏢 Extracting company information...")
        company_name = extract_company_name(summary, groq_client)
        log_message(f"   Company: {company_name}")
        
        description = extract_company_description(summary, groq_client)
        log_message(f"   Description: {description}")
        
        # Generate blurbs
        log_message(f"💭 Generating personalized service recommendations...")
        blurbs = generate_blurbs(company_name, summary, groq_client)
        
        # Generate document
        log_message(f"📝 Creating personalized document...")
        docx_filename = generate_personalized_document(
            name, company_name, description, blurbs, message_id
        )
        
        if not docx_filename:
            log_message(f"❌ Failed to generate document. Cannot proceed.")
            return False
        
        # Convert to PDF
        docx_path = os.path.join("personalised", docx_filename)
        pdf_filename = convert_docx_to_pdf(docx_path, "personalised")
        
        if not pdf_filename:
            log_message(f"❌ PDF conversion failed. Cannot proceed.")
            return False
        
        pdf_path = os.path.join("personalised", pdf_filename)
        
        # Send Telegram notification with PDF
        log_message(f"📲 Sending notification to Telegram...")
        if os.path.exists(pdf_path):
            if send_telegram_document(pdf_path):
                log_message(f"✅ PDF notification sent successfully!")
            else:
                log_message(f"⚠️ Telegram notification failed (check API token/User ID)")
        
        # Send reply email with PDF
        log_message(f"📧 Sending reply email to {email}...")
        email_body = create_email_body(name)
        
        if send_reply_email(service, email, subject, email_body, pdf_path, message_id):
            mark_as_done(message_id)
            log_message(f"✅ Lead marked as completed")
            return True
        else:
            log_message(f"❌ Failed to send reply email.")
            return False
            
    except Exception as e:
        log_failure("process_incoming_email", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")
        return False

# ============================================================================
# GROQ API KEY MANAGEMENT
# ============================================================================

def get_groq_api_key_at_runtime() -> str:
    """Prompt for Groq API key at runtime. Key exists only in memory."""
    api_key = input("🔑 Enter your Groq API key for this session: ").strip()
    
    if not api_key:
        raise ValueError("Groq API key is required!")
    
    log_message("✅ Groq API key entered. (Key will only be used in this session and destroyed after script.)")
    return api_key

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main_loop(groq_api_key: str):
    """Main indefinite loop - fetch and process emails."""
    log_message("🚀 Starting email monitoring system...")
    log_message(f"⏱️ Checking for new emails every {EMAIL_FETCH_INTERVAL} seconds...")
    log_message("🚫 System emails (no-reply, OAuth, password reset, etc.) will be IGNORED.")
    
    # Initialize CSV
    init_csv()
    
    # Authenticate Gmail
    service = authenticate_gmail()
    log_message("✅ Gmail API authenticated.")
    
    # Create Groq client
    groq_client = Groq(api_key=groq_api_key)
    
    # Test Groq connection
    if not test_groq_connection(groq_client):
        log_message("❌ Groq connection failed. Exiting.")
        return
    
    # Start Telegram buffer flushing thread
    start_telegram_buffer_thread()
    log_message("📲 Telegram notification system started.")
    
    iteration = 0
    
    while True:
        iteration += 1
        log_message(f"\n--- Iteration {iteration} @ {datetime.now().strftime('%H:%M:%S')} ---")
        
        try:
            # Fetch latest email
            email_data = fetch_latest_email(service)
            
            if email_data:
                process_incoming_email(service, groq_client, email_data)
            else:
                log_message("ℹ️ No new emails in inbox.")
        
        except Exception as e:
            log_failure("main_loop", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")
        
        # Wait before next check
        log_message(f"⏰ Waiting {EMAIL_FETCH_INTERVAL} seconds before next check...")
        time.sleep(EMAIL_FETCH_INTERVAL)

def main():
    """Initialize and start the main loop."""
    log_message("=" * 70)
    log_message("AUTOMATED EMAIL PROCESSING PIPELINE")
    log_message("=" * 70)
    
    # Get Groq API key at runtime
    groq_api_key = None
    
    try:
        groq_api_key = get_groq_api_key_at_runtime()
    except Exception as e:
        log_failure("get_groq_api_key_at_runtime", f"{type(e).__name__}: {str(e)}")
        return
    
    # Start main loop
    try:
        main_loop(groq_api_key)
    except KeyboardInterrupt:
        log_message("\n\n🛑 Application stopped by user. Exiting gracefully...")
        flush_telegram_buffer()
    except Exception as e:
        log_failure("main", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_failure("startup", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")