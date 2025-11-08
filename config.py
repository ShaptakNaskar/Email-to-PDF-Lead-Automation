# ============================================================================
# EMAIL PROCESSING PIPELINE - CONFIGURATION
# ============================================================================
# Central configuration file for all application settings
# Modify this file to customize behavior without changing code
# ============================================================================

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_FETCH_INTERVAL = 15  # Seconds between inbox checks
TOKEN_FILE = "token.pickle"
OUTPUT_CSV = "qualified_leads.csv"

# Keywords that trigger lead qualification
# Add or remove keywords to match your business needs
KEYWORDS = [
    "brochure", "catalogue", "catalog", "leaflet",
    "pamphlet", "prospectus", "flyer", "portfolio",
    "booklet", "information pack", "document", "presentation"
]

# System email domains to ignore (no-reply, automation, etc.)
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

# System email keywords to ignore
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

# ============================================================================
# FILE & DIRECTORY CONFIGURATION
# ============================================================================

TEMPLATE_FILE = "template.docx"  # Your customizable template
SCRAPED_DIR = "scraped_sites"    # Cached website content
PERSONALISED_DIR = "personalised"  # Generated documents
MASTER_LOG = "master_log.txt"    # Activity log
FAILED_LOG = "failed_steps.txt"  # Error log

# ============================================================================
# AI & GROQ CONFIGURATION
# ============================================================================

GROQ_MODEL = "llama-3.1-8b-instant"  # AI model to use
GROQ_MAX_TOKENS = 600  # Maximum response length
GROQ_TEMPERATURE = 0.3  # Determinism (0.0 = deterministic, 1.0 = creative)

# ============================================================================
# AI PROMPTS - Customize to change AI behavior
# ============================================================================

EXTRACT_COMPANY_PROMPT = """
Extract the exact company name from this webpage summary. Respond with ONLY the company name (e.g., 'Acme Corporation'), nothing else.

Summary: {summary}
"""

EXTRACT_DESCRIPTION_PROMPT = """
From this webpage summary, create a concise one-sentence description of what the company does or deals with, phrased as 'providing [services] to [industries/clients]'. Respond with ONLY that sentence, nothing else.

Summary: {summary}
"""

GENERATE_BLURBS_PROMPT = """
Generate 5 short, personalized blurbs (1-2 sentences each) for our organization's services. Explain how EACH of our services can specifically benefit {company_name} based on their focus in this summary: {summary}.

Use the perspective of our organization offering help TO {company_name} (e.g., 'We can optimize your workflows to enhance your digital efficiency').

Keep each professional, concise, and starting with 'We can' or similar. Number them exactly 1-5, one per line—no extras or markdown:

1. Process Optimization & Workflow Analysis
2. Strategic Consulting & Planning
3. Custom Solution Development
4. Training & Knowledge Transfer
5. Quality Assurance & Performance Monitoring
"""

SUMMARY_PROMPT = """
Summarize the key information from this scraped webpage content in a single continuous paragraph of exactly 5-6 sentences. Focus on:

- Company overview and services/products offered
- Contact details, location, and team (if available)
- Any relevant business focus or unique selling points

Keep it professional, concise, and factual. Do NOT use any markdown (like **bold**), bullet points, line breaks, or formatting—output everything as one unbroken paragraph with only spaces between sentences.

Content: {content}
"""

# ============================================================================
# TELEGRAM CONFIGURATION (Optional)
# ============================================================================

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
TELEGRAM_USER_ID = "YOUR_USER_ID_HERE"      # Get from @userinfobot
TELEGRAM_BUFFER_INTERVAL = 15  # Send buffered messages every 15 seconds
TELEGRAM_MAX_MESSAGE_LENGTH = 4096  # Telegram's limit

# ============================================================================
# DOCUMENT GENERATION
# ============================================================================

EMAIL_SUBJECT = "Professional Solutions for Your Organization"  # Reply subject
DEFAULT_COMPANY_NAME = "Our Organization"  # Fallback name