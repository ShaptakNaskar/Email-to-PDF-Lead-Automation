# Modular Email Processing Pipeline - Documentation

## Overview

This is a **modular, flexible email processing system** designed to help businesses generate personalized brochures and send them to qualified leads. The system automatically fetches emails, validates them, scrapes company websites, generates personalized PDFs using AI, and sends replies with attachments.

**Key improvements:**
- ✅ Fully modularized architecture (each function in separate scripts)
- ✅ Company name fetched from user input (no hardcoding)
- ✅ Email address fetched from user input
- ✅ Template cleaned of all hardcoded references
- ✅ Flexible and extensible for custom workflows

---

## File Structure

```
project/
├── gmail_auth.py              # One-time Gmail OAuth authentication
├── email_listener.py          # Main orchestrator (entry point)
├── email_fetcher.py           # Fetch and parse Gmail messages
├── email_validator.py         # Validate if email qualifies for processing
├── web_scraper.py             # Scrape website content
├── ai_processor.py            # Groq AI for summarization & content generation
├── csv_manager.py             # CSV database management
├── pdf_generator.py           # Generate personalized PDFs
├── email_sender.py            # Send reply emails with attachments
├── template.docx              # Editable brochure template
├── credentials.json           # Gmail OAuth credentials (download from Google Cloud)
├── qualified_leads.csv        # Auto-generated leads database
├── master_log.txt             # Runtime logs
├── failed_steps.txt           # Error logs
└── personalised/              # Directory for generated PDFs
```

---

## Setup Instructions

### 1. Install Python and Dependencies

Ensure you have **Python 3.11+** installed. Then install required packages:

```bash
pip install google-auth-oauthlib google-api-python-client groq beautifulsoup4 requests python-docx docx2pdf
```

**For PDF conversion:**
- Install **LibreOffice** (recommended): https://www.libreoffice.org/download/
- Or install `docx2pdf`: `pip install docx2pdf` (requires MS Word)

### 2. Get Gmail OAuth Credentials

1. Go to **https://console.cloud.google.com**
2. Create a new project
3. Enable **Gmail API**
4. Create **OAuth 2.0 Desktop App credentials**
5. Download the JSON file and save as `credentials.json` in your project directory

### 3. Run Gmail Authentication (One-Time)

```bash
python gmail_auth.py
```

This will:
- Open a browser for OAuth login
- Generate `token.pickle` (authentication token)
- Store it for future use

---

## Usage

### Running the Application

```bash
python email_listener.py
```

On startup, you'll be prompted for:

1. **Your Company Name**: The name of your business (used in emails and PDFs)
2. **Your Email Address**: Your email for replies
3. **Groq API Key**: Your API key from https://console.groq.com

**Example:**
```
📝 Enter your company name: Mindedge Solutions
📧 Enter your email address: contact@mindedge.com
🔑 Enter your Groq API key for this session: gsk_xxx...
```

The system will then:
- Check for new emails every 15 seconds
- Validate emails (filters system emails, checks for brochure keywords)
- Scrape prospect websites
- Summarize website content using Groq AI
- Generate personalized blurbs
- Create custom PDFs
- Send replies with attachments
- Log all activities

---

## Configuration

All modules respect these configurable values:

**In `email_listener.py`:**
```python
EMAIL_FETCH_INTERVAL = 15  # Seconds between email checks
PERSONALISED_DIR = "personalised"  # Output directory for PDFs
```

**In `ai_processor.py`:**
```python
GROQ_MODEL = "llama-3.1-8b-instant"  # AI model for content generation
```

**In other modules:**
- `MASTER_LOG` - File for runtime logs
- `FAILED_LOG` - File for error logs
- `OUTPUT_CSV` - Leads database filename

---

## Customizing the Template

Edit `template.docx` with Microsoft Word or LibreOffice:

1. **Placeholders to customize:**
   - `(Name)` → Prospect's name (auto-filled)
   - `(company name)` → Prospect's company (auto-filled)
   - `(what your company deals with)` → Auto-filled with Groq AI summary
   - `Input Blurbs here` → Auto-filled with personalized service descriptions

2. **Edit static content:**
   - Company background and services
   - Pricing information
   - Contact information
   - Call-to-action sections

3. **Keep the structure:**
   - Ensure the `Input Blurbs here` text appears 5 times (once per service)
   - Don't rename the placeholders

---

## Module Reference

### `gmail_auth.py`
Handles Gmail OAuth authentication. Run once to generate `token.pickle`.

**Key Function:**
- `authenticate_gmail()` - Returns Gmail service object

### `email_listener.py`
Main orchestrator that coordinates all modules and runs the infinite loop.

**Key Functions:**
- `main_loop()` - Infinite loop checking for new emails
- `process_incoming_email()` - Handles each qualified email
- `get_company_name_from_user()` - Gets company name input
- `get_sender_email_from_user()` - Gets sender email input

### `email_fetcher.py`
Fetches and parses emails from Gmail.

**Key Functions:**
- `fetch_latest_email(service)` - Fetches newest email
- `extract_message_data(message)` - Parses email content

### `email_validator.py`
Validates if emails qualify for processing.

**Key Functions:**
- `validate_email()` - Checks for keywords, system emails, websites
- `is_system_email()` - Filters automated/system emails
- `contains_keywords()` - Detects brochure-related keywords

### `web_scraper.py`
Scrapes website content for AI processing.

**Key Functions:**
- `scrape_website(url)` - Downloads and cleans website text
- `fetch_website_content(url)` - HTTP request with error handling

### `ai_processor.py`
Uses Groq AI for content generation and summarization.

**Key Functions:**
- `summarize_with_groq()` - Creates 5-6 sentence website summary
- `call_groq()` - Generic Groq API call
- `extract_blurbs()` - Parses numbered service descriptions
- `test_groq_connection()` - Validates API key

### `csv_manager.py`
Manages the leads database (CSV file).

**Key Functions:**
- `init_csv()` - Creates CSV with proper headers
- `add_or_update_lead()` - Adds new prospects
- `mark_as_done()` - Marks emails as processed
- `get_processed_message_ids()` - Retrieves already-processed emails

### `pdf_generator.py`
Generates personalized PDFs from the template.

**Key Functions:**
- `generate_pdf()` - Main PDF generation workflow
- `convert_docx_to_pdf()` - Handles DOCX → PDF conversion
- `replace_single_placeholder()` - Replaces template variables
- `replace_blurbs()` - Inserts AI-generated service descriptions

### `email_sender.py`
Creates and sends reply emails with PDF attachments.

**Key Functions:**
- `create_email_body()` - Generates personalized email text
- `create_reply_message_with_attachment()` - Builds MIME email
- `send_reply_email()` - Sends via Gmail API

---

## Workflow Example

**Input Email:**
```
From: John Smith <john@acmecorp.com>
Subject: Looking for a brochure on your services
Body: Hi, I'm interested in your workflow optimization services...
```

**System Processing:**
1. ✅ Validates email (has keywords, real person)
2. 🌐 Scrapes acmecorp.com
3. 📝 Generates summary: "ACME Corp provides digital marketing solutions..."
4. 🤖 Groq AI extracts company name: "ACME Corp"
5. 💭 Groq AI generates personalized service descriptions
6. 📄 Creates PDF: `ACME_Corp_a1b2c3d4.pdf`
7. 📧 Sends reply with attachment
8. ✅ Marks in CSV as "Done"

**Output CSV Entry:**
```
Message_ID,Name,Email,Website,Summary,PDF,Done
a1b2c3d4,John Smith,john@acmecorp.com,acmecorp.com,"ACME Corp provides...",ACME_Corp_a1b2c3d4.pdf,Yes
```

---

## Error Handling

### Common Issues

**"token.pickle not found"**
- Solution: Run `python gmail_auth.py` first

**"credentials.json not found"**
- Solution: Download OAuth credentials from Google Cloud Console

**"Neither LibreOffice nor docx2pdf is available"**
- Solution: Install LibreOffice or: `pip install docx2pdf` (requires MS Word)

**"Groq API connection failed"**
- Solution: Check API key, ensure internet connection, verify Groq status at https://status.groq.com

### Logs

- **`master_log.txt`** - All operations logged with timestamps
- **`failed_steps.txt`** - Errors and failures logged separately

Check these files for troubleshooting.

---

## Extending the System

### Adding Custom Email Validation

Edit `email_validator.py`:
```python
KEYWORDS = [
    "brochure", "your_keyword", ...
]
```

### Changing AI Model

Edit `ai_processor.py`:
```python
GROQ_MODEL = "llama-2-70b-chat"  # Different model
```

### Custom Email Templates

Replace `template.docx` with your own Word document, keeping the placeholders:
- `(Name)`
- `(company name)`
- `(what your company deals with)`
- `Input Blurbs here` (5 times)

### Scheduled Execution

Use system schedulers to run the script:

**Windows (Task Scheduler):**
```
Program: C:\Users\Sappy\AppData\Local\Programs\Python\Python311\python.exe
Arguments: C:\path\to\email_listener.py
```

**Linux/Mac (cron):**
```bash
0 9 * * * /usr/bin/python3 /path/to/email_listener.py
```

---

## Security Notes

1. **API Keys**: Never hardcode Groq/Gmail keys - they're prompted at runtime
2. **Credentials**: `token.pickle` and `credentials.json` are sensitive - keep them private
3. **Logs**: Review logs for sensitive information before sharing
4. **Email**: Don't share email addresses in logs/reports

---

## Performance Tips

1. Increase `EMAIL_FETCH_INTERVAL` if you're rate-limited by Gmail API
2. Reduce timeout values in `web_scraper.py` for faster processing
3. Use `--onefile` option when packaging as EXE for faster startup
4. Monitor Groq API usage - consider rate limits

---

## Packaging as .EXE

To distribute this as a standalone Windows executable:

```bash
C:\Users\Sappy\AppData\Local\Programs\Python\Python311\python.exe -m PyInstaller --onefile --console ^
  --hidden-import=groq ^
  --hidden-import=google.auth ^
  --hidden-import=google.auth.transport.requests ^
  --hidden-import=google.oauth2.credentials ^
  --hidden-import=google_auth_oauthlib.flow ^
  --hidden-import=googleapiclient.discovery ^
  --hidden-import=bs4 ^
  --hidden-import=docx ^
  email_listener.py
```

The `.exe` will be in the `dist/` folder.

---

## Support

For issues or questions:
1. Check logs in `master_log.txt` and `failed_steps.txt`
2. Verify API credentials (Gmail, Groq)
3. Ensure all dependencies are installed: `pip list`
4. Test individual modules separately for debugging

---

## License

This system is provided under Apache License 2.0.
---

## Changelog

**v2.0 - Modular Release**
- ✅ Split monolithic script into 9 focused modules
- ✅ Removed hardcoded "Sappy's Enclove" references
- ✅ Added user input for company name and email
- ✅ Updated template with generic placeholders
- ✅ Improved error handling and logging
- ✅ Enhanced documentation

**v1.0 - Original Release**
- Initial working version (monolithic)
