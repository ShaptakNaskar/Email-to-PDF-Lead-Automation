import re
from datetime import datetime

MASTER_LOG = "master_log.txt"

# System email domains and keywords to ignore
SYSTEM_EMAIL_DOMAINS = [
    "google.com", "microsoft.com", "outlook.com", "apple.com",
    "noreply@", "no-reply@", "donotreply@", "do-not-reply@",
    "notification@", "notifications@", "alert@", "alerts@",
    "support@", "help@", "info@", "contact@",
    "github.com", "gitlab.com", "bitbucket.com",
    "linkedin.com", "facebook.com", "twitter.com", "instagram.com",
    "amazon.com", "aws.amazon.com",
    "mail.google.com", "mail.office.com"
]

SYSTEM_EMAIL_KEYWORDS = [
    "do not reply", "don't reply", "donotreply", "no-reply",
    "account activation", "verify your account", "confirm your email",
    "reset your password", "password reset", "change password",
    "confirm your identity", "two-factor authentication", "2fa",
    "welcome to", "welcome aboard", "get started",
    "verify your phone", "confirm your number",
    "suspicious activity", "unusual activity",
    "subscription confirmation", "booking confirmation",
    "order confirmation", "purchase confirmation",
    "payment received", "payment confirmation",
    "login attempt", "new login", "login from",
    "unsubscribe", "manage subscriptions", "manage preferences"
]

KEYWORDS = [
    "brochure", "catalogue", "catalog", "leaflet",
    "pamphlet", "prospectus", "flyer", "portfolio",
    "booklet", "information pack", "document", "presentation"
]

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def is_system_email(sender: str, subject: str, body: str) -> bool:
    """
    Detect if email is from a system/automated source.
    Returns True if email should be IGNORED (is a system email).
    """
    if not sender:
        return True
    
    sender_lower = sender.lower()
    subject_lower = subject.lower() if subject else ""
    body_lower = body.lower() if body else ""
    
    full_content = f"{subject_lower} {body_lower}"
    
    # Check against system email domains
    for domain in SYSTEM_EMAIL_DOMAINS:
        if domain.lower() in sender_lower:
            log_message(f"🚫 Detected system email domain: {domain}")
            return True
    
    # Check against system email keywords
    for keyword in SYSTEM_EMAIL_KEYWORDS:
        if keyword.lower() in full_content:
            log_message(f"🚫 Detected system email keyword: '{keyword}'")
            return True
    
    return False

def extract_websites(text):
    """Find URLs or bare domains in the email body."""
    urls = re.findall(r'(https?://[^\s]+)', text)
    bare_domains = re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', text)
    
    all_domains = set()
    
    for url in urls:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        if domain:
            all_domains.add(domain.lower())
    
    for d in bare_domains:
        if '.' in d:
            all_domains.add(d.lower())
    
    return list(all_domains)

def contains_keywords(text):
    """Detect brochure/catalogue-related words."""
    return any(word in text.lower() for word in KEYWORDS)

def validate_email(sender: str, subject: str, body: str) -> tuple:
    """
    Validate if email qualifies for processing.
    Returns: (is_valid, name, email, website)
    """
    # First: Check if it's a system email (reject if it is)
    if is_system_email(sender, subject, body):
        return False, "", "", ""
    
    # Extract name and email
    sender_match = re.search(r'([\w\s]+) <([^>]+)>', sender)
    
    if sender_match:
        name = sender_match.group(1).strip()
        email = sender_match.group(2).strip()
    else:
        name = ""
        email = ""
    
    # Check keywords
    full_text = f"{subject} {body}"
    has_keywords = contains_keywords(full_text)
    
    # Extract websites
    websites = extract_websites(body)
    
    # Fallback: use email domain if no website found
    if not websites and email:
        email_domain = email.split('@')[-1]
        if not re.search(r'gmail|yahoo|outlook|hotmail', email_domain):
            websites = [email_domain]
    
    # Validate
    is_valid = bool(email and name and has_keywords and websites)
    website = websites[0] if websites else ""
    
    return is_valid, name, email, website
