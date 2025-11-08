# Automated Email Processing Pipeline

A professional-grade, modular Python application for automated email monitoring, website content analysis, and personalized document generation using AI-powered insights.

## Overview

This system monitors an email inbox for incoming messages, validates and filters content, scrapes associated websites, generates AI-driven summaries and personalized recommendations, and automatically sends tailored responses with generated documents.

**Key Features:**

- Automated email monitoring with configurable polling intervals
- Intelligent system email detection and filtering
- Website content scraping and analysis
- AI-powered summarization and content generation (powered by Groq LLaMA)
- Automated personalized document generation (DOCX to PDF conversion)
- Email reply automation with attachment handling
- Telegram notification support with message buffering
- Comprehensive logging and audit trails
- CSV-based lead management and tracking

## Prerequisites

- Python 3.8 or higher
- Active Gmail account with API access enabled
- Groq API key (free tier available at https://groq.com)
- LibreOffice or Microsoft Office for DOCX-to-PDF conversion
- Telegram bot (optional, for real-time notifications)

## Installation

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/ShaptakNaskar/Email-to-PDF-Lead-Automation
cd email-processing-pipeline
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

**Activate the virtual environment:**

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- `google-auth-oauthlib` - Gmail API authentication
- `google-auth-httplib2` - Google authentication
- `google-api-python-client` - Gmail API client
- `python-docx` - Word document manipulation
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `groq` - Groq API client

## Configuration

### Step 1: Set Up Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Save it as `credentials.json` in your project root directory

**Important:** Keep `credentials.json` secure and never commit it to version control.

### Step 2: Obtain Groq API Key

1. Visit [Groq Console](https://console.groq.com/keys)
2. Create a new API key
3. The key will be requested at runtime (not stored permanently)

### Step 3: Configure Telegram (Optional)

For Telegram notifications:

1. Chat with [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow prompts
3. Copy your BOT_TOKEN
4. Chat with [@userinfobot](https://t.me/userinfobot) to get your USER_ID
5. Update configuration in `config.py`

### Step 4: Customize Template and Configuration

1. Edit `template.docx` with your company branding and messaging
2. Update `config.py` with your business details, keywords, and system email filters

## Running the Application

### Initial Setup: Gmail Authentication

Before running the main script, authenticate with Gmail:

```bash
python gmail_auth.py
```

This will:
- Open your browser for OAuth authorization
- Create and save `token.pickle` securely
- Log the process to `master_log.txt`

**This only needs to be done once.** The token will be reused in subsequent runs.

### Run the Main Application

```bash
python main.py
```

The application will:
1. Request your Groq API key (entered interactively, not saved)
2. Start monitoring your email inbox
3. Process incoming emails every 15 seconds
4. Log all activity to console and log files
5. Send Telegram notifications (if configured)

**To stop the application:** Press `Ctrl+C` to exit gracefully

## Project Structure

```
email-processing-pipeline/
├── README.md                    # This file
├── LICENSE                      # Apache 2.0 License
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration and constants
├── main.py                      # Application entry point
├── gmail_auth.py                # Gmail OAuth authentication
├── modules/
│   ├── __init__.py
│   ├── email_handler.py         # Email fetching and validation
│   ├── web_scraper.py           # Website scraping utilities
│   ├── ai_processor.py          # Groq API integration
│   ├── document_generator.py    # PDF generation
│   ├── telegram_notifier.py     # Telegram messaging
│   └── csv_manager.py           # Lead database management
├── template.docx                # Customizable document template
├── credentials.json             # (Create) Gmail API credentials
├── token.pickle                 # (Auto-created) Gmail session token
├── qualified_leads.csv          # (Auto-created) Lead database
├── master_log.txt               # (Auto-created) Activity log
├── failed_steps.txt             # (Auto-created) Error log
├── scraped_sites/               # (Auto-created) Cached website content
└── personalised/                # (Auto-created) Generated documents
```

## Configuration Details

Edit `config.py` to customize:

- **Email monitoring:** Polling intervals and keywords
- **Filtering:** System email domains and keywords to ignore
- **Telegram:** Bot token and user ID (optional)
- **Groq AI:** Model selection and prompt templates
- **File paths:** Output directories and naming conventions

### Example Configuration Changes

**Change email fetch interval:**
```python
EMAIL_FETCH_INTERVAL = 30  # Check every 30 seconds instead of 15
```

**Add custom keywords:**
```python
KEYWORDS = [
    "brochure", "catalog", "proposal",  # Default
    "custom_keyword_1", "custom_keyword_2"  # Your additions
]
```

**Update system email filters:**
```python
SYSTEM_EMAIL_DOMAINS = [
    # Default domains
    ...
    "your_domain_to_ignore.com"  # Add custom domains
]
```

## Customizing the Template Document

The `template.docx` file contains placeholders that are automatically replaced:

- `(Name)` → Recipient name
- `(company name)` → Extracted company name
- `(what your company deals with)` → AI-generated company description
- Numbered sections (1-5) → AI-generated personalized blurbs

**To customize:**

1. Open `template.docx` in Microsoft Word or LibreOffice
2. Modify branding, colors, fonts, and layout
3. Keep the placeholder text exactly as shown (case-sensitive)
4. Save and test with a sample email

## How It Works

### Email Processing Pipeline

1. **Fetch Email** → Poll Gmail inbox for new messages
2. **Validate** → Check sender, subject, and content for relevance
3. **Filter** → Reject system emails (no-reply, OAuth, etc.)
4. **Extract** → Parse sender name, email, and website references
5. **Scrape** → Fetch and clean website HTML content
6. **Summarize** → Generate AI summary using Groq API
7. **Personalize** → Extract company info and generate service blurbs
8. **Generate** → Create DOCX from template with personalized content
9. **Convert** → Convert DOCX to PDF
10. **Send** → Email PDF reply to sender and/or notify via Telegram
11. **Track** → Record lead status in CSV database

### Example Workflow

**Incoming Email:**
```
From: John Smith <john@acmecorp.com>
Subject: Looking for brochure on your services
Body: We saw your portfolio and are interested in learning more...
```

**Processing:**
- Validates as legitimate (contains keyword "brochure")
- Scrapes acmecorp.com for company information
- AI generates: company description, personalized service recommendations
- Creates personalized PDF with your template + AI content
- Sends PDF reply to john@acmecorp.com
- Records in `qualified_leads.csv` with status "Done"

## Logging

The application generates three log files:

- **master_log.txt** → Complete activity log with timestamps
- **failed_steps.txt** → Errors and failures for debugging
- **qualified_leads.csv** → Database of processed leads

View logs in real-time:

**On Windows:**
```bash
type master_log.txt
```

**On macOS/Linux:**
```bash
tail -f master_log.txt
```

## Troubleshooting

### "credentials.json not found"
**Solution:** Download from Google Cloud Console and place in project root.

### "Token invalid or expired"
**Solution:** Delete `token.pickle` and run `python gmail_auth.py` again.

### "Groq API error"
**Solution:** Verify API key is correct. Visit https://console.groq.com/keys to check.

### "DOCX to PDF conversion failed"
**Solution:** Ensure LibreOffice is installed and in system PATH.

**Installation:**
- **Windows:** Download from libreoffice.org or install via `choco install libreoffice`
- **macOS:** `brew install libreoffice`
- **Linux:** `sudo apt-get install libreoffice`

### "No emails being processed"
**Solution:** Check:
1. Email arrives in INBOX (not other labels)
2. Keywords in config.py match your incoming emails
3. Gmail authentication is valid
4. Check `master_log.txt` for specific errors

## Important Notes

### Security

- Never commit `credentials.json` or `token.pickle` to version control
- The Groq API key is requested at runtime and never stored
- Use `.gitignore` to exclude sensitive files:

```
credentials.json
token.pickle
qualified_leads.csv
master_log.txt
failed_steps.txt
scraped_sites/
personalised/
```

### Privacy & Compliance

- Ensure you have permission to send automated emails to recipients
- Comply with GDPR, CAN-SPAM, and local email regulations
- Use appropriate "From" headers and unsubscribe mechanisms
- Store lead data securely and comply with data protection laws

### Rate Limiting

- Gmail API: 100,000 requests/day (sufficient for most use cases)
- Groq API: Free tier has fair-use limits (implement delays if needed)
- Website scraping: Respects rate limits and uses `robots.txt`

## Advanced Features

### Custom Prompt Templates

Edit prompts in `config.py` to change AI behavior:

```python
GENERATE_BLURBS_PROMPT = """
Customize this prompt to control how AI generates recommendations...
"""
```

### Batch Processing

To process multiple emails manually:

```python
# Edit main.py to modify polling interval
EMAIL_FETCH_INTERVAL = 1  # Process every 1 second
```

### Telegram Batch Notifications

Messages are automatically buffered and sent every 15 seconds to reduce API calls.

## License

This project is licensed under the **Apache License 2.0**. See `LICENSE` file for details.

You are free to use, modify, and distribute this software with attribution.

## Support & Contributing

For issues, feature requests, or contributions, please refer to the project repository.

## Changelog

### Version 1.0.0
- Initial release
- Modular architecture
- Professional logging
- Groq AI integration
- Telegram notifications
- CSV lead management

---

**Built for professionals. Optimized for scale.**
