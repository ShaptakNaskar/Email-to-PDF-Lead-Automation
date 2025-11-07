import os
import time
import traceback
import threading
from datetime import datetime
from groq import Groq

# Import modular functions
from email_fetcher import authenticate_gmail, fetch_latest_email
from email_validator import validate_email
from web_scraper import scrape_website
from ai_processor import (
    test_groq_connection, summarize_with_groq, call_groq,
    get_extract_company_prompt, get_extract_description_prompt,
    get_generate_blurbs_prompt, extract_blurbs
)
from csv_manager import init_csv, get_processed_message_ids, add_or_update_lead, mark_as_done
from pdf_generator import generate_pdf
from email_sender import create_email_body, create_reply_message_with_attachment, send_reply_email

MASTER_LOG = "master_log.txt"
FAILED_LOG = "failed_steps.txt"
EMAIL_FETCH_INTERVAL = 15
PERSONALISED_DIR = "personalised"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def log_failure(step: str, error: str, log_file: str = FAILED_LOG):
    """Log failure to failed log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] FAILED STEP '{step}': {error}\n"
    print(f"💥 {log_entry.strip()}")
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def get_groq_api_key_at_runtime() -> str:
    """Prompt for Groq API key at runtime. Key exists only in memory."""
    api_key = input("🔑 Enter your Groq API key for this session: ").strip()
    if not api_key:
        raise ValueError("Groq API key is required!")
    log_message("✅ Groq API key entered. (Key will only be used in this session and destroyed after script.)")
    return api_key

def get_company_name_from_user() -> str:
    """Get company name from user input."""
    company_name = input("\n📝 Enter your company name: ").strip()
    if not company_name:
        company_name = "Your Company Name"
        log_message(f"⚠️ No company name provided. Using default: {company_name}")
    else:
        log_message(f"✅ Company name set to: {company_name}")
    return company_name

def get_sender_email_from_user() -> str:
    """Get sender email from user input."""
    sender_email = input("📧 Enter your email address: ").strip()
    if not sender_email:
        raise ValueError("Email address is required!")
    log_message(f"✅ Sender email set to: {sender_email}")
    return sender_email

def process_incoming_email(service, groq_client, message_data, company_name: str, sender_email: str):
    """Process an incoming email and send reply with PDF."""
    message_id = message_data['message_id']
    sender = message_data['sender']
    subject = message_data['subject']
    body = message_data['body']
    
    # Check if already processed
    processed_ids = get_processed_message_ids()
    if message_id in processed_ids:
        log_message(f"⏭️ Message {message_id} already processed. Skipping.")
        return False
    
    # Validate email
    is_valid, name, email, website = validate_email(sender, subject, body)
    if not is_valid:
        log_message(f"⚠️ Email from {sender} does not qualify. Skipping.")
        return False
    
    log_message(f"\n✨ New qualified email: {name} ({email}) | Website: {website}")
    
    # Add to CSV
    add_or_update_lead(message_id, name, email, website)
    log_message(f"📊 Added to CSV with Message ID: {message_id}")
    
    # Scrape website
    log_message(f"🌐 Scraping website: {website}")
    website_content = scrape_website(website)
    if not website_content:
        log_message(f"❌ Failed to scrape {website}. Cannot proceed.")
        return False
    
    # Summarize with Groq
    log_message(f"📄 Generating summary from website...")
    summary = summarize_with_groq(website_content, groq_client)
    if not summary:
        log_message(f"❌ Failed to generate summary. Cannot proceed.")
        return False
    
    # Extract company info
    company_name_extracted = call_groq(get_extract_company_prompt(summary), groq_client)
    if not company_name_extracted or company_name_extracted.lower() in ['unknown', 'n/a']:
        company_name_extracted = website.replace('www.', '').split('.')[0].replace('-', ' ').title()
    
    description = call_groq(get_extract_description_prompt(summary), groq_client)
    if not description or description.lower() in ['unknown', 'n/a']:
        description = "innovative solutions in the digital space."
    
    description = f"providing {description.lower().replace('providing ', '')}" if description.lower().startswith('providing ') else f"providing {description.lower()}"
    
    # Generate blurbs
    log_message(f"💭 Generating personalized blurbs...")
    blurb_text = call_groq(get_generate_blurbs_prompt(company_name, summary), groq_client)
    blurbs = extract_blurbs(blurb_text)
    
    # Generate PDF
    pdf_filename = generate_pdf(name, email, company_name_extracted, description, blurbs, message_id, sender_email)
    
    if not pdf_filename:
        log_message(f"❌ PDF generation failed.")
        return False
    
    # Send reply email with attachment
    log_message(f"📧 Sending reply email to {email}...")
    try:
        pdf_path = os.path.join(PERSONALISED_DIR, pdf_filename)
        reply_body = create_email_body(name, company_name, sender_email)
        
        # Get the original message to extract thread ID and in-reply-to ID
        original_msg = service.users().messages().get(userId='me', id=message_id).execute()
        thread_id = original_msg['threadId']
        
        # Create and send reply
        reply_message = create_reply_message_with_attachment(
            email,
            subject,
            reply_body,
            pdf_path,
            message_id,
            thread_id,
            sender_email
        )
        
        if send_reply_email(service, reply_message, thread_id):
            mark_as_done(message_id)
            log_message(f"✅ Email marked as Done in CSV")
            return True
        else:
            log_message(f"❌ Failed to send reply email.")
            return False
    
    except Exception as e:
        log_message(f"❌ Error sending reply: {type(e).__name__}: {str(e)}")
        return False

def main_loop(groq_api_key: str, company_name: str, sender_email: str):
    """Main indefinite loop - fetch email every N seconds."""
    log_message("🚀 Starting infinite email monitoring loop...")
    log_message(f"⏱️ Checking for new emails every {EMAIL_FETCH_INTERVAL} seconds...")
    log_message("🚫 System emails (no-reply, OAuth, password reset, etc.) will be IGNORED.")
    log_message(f"📝 Company Name: {company_name}")
    log_message(f"📧 Sender Email: {sender_email}")
    
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
    
    iteration = 0
    
    while True:
        iteration += 1
        log_message(f"\n--- Iteration {iteration} @ {datetime.now().strftime('%H:%M:%S')} ---")
        
        try:
            # Fetch latest email
            email_data = fetch_latest_email(service)
            
            if email_data:
                process_incoming_email(service, groq_client, email_data, company_name, sender_email)
            else:
                log_message("ℹ️ No new emails in inbox.")
        
        except Exception as e:
            log_failure("main_loop", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")
        
        # Wait before next check
        log_message(f"⏰ Waiting {EMAIL_FETCH_INTERVAL} seconds before next check...")
        time.sleep(EMAIL_FETCH_INTERVAL)

def main():
    """Initialize and start the main loop."""
    log_message("🚀 Modular Email Processing Pipeline")
    log_message("=" * 60)
    
    # Get company name
    company_name = get_company_name_from_user()
    
    # Get sender email
    sender_email = get_sender_email_from_user()
    
    # Get Groq API key at runtime
    groq_api_key = None
    try:
        groq_api_key = get_groq_api_key_at_runtime()
    except Exception as e:
        log_failure("get_groq_api_key_at_runtime", f"{type(e).__name__}: {str(e)}")
        return
    
    # Start main loop
    try:
        main_loop(groq_api_key, company_name, sender_email)
    except KeyboardInterrupt:
        log_message("\n\n🛑 Script interrupted by user. Exiting gracefully...")
    except Exception as e:
        log_failure("main", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_failure("startup", f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")
