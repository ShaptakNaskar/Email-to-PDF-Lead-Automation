# File Manifest & Deliverables

## Created Files Summary

### Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `README.md` | Complete system documentation | ~4500 words |
| `MODULARIZATION.md` | Detailed changes & benefits | ~2500 words |
| `QUICKSTART.md` | 5-minute setup guide | ~1200 words |
| `FILE_MANIFEST.md` | This file - files overview | Reference |

---

## Core Python Modules

### Main Application

**`email_listener.py`** - Main orchestrator (Entry point)
- Coordinates all modules
- Infinite email monitoring loop (checks every 15 seconds)
- Prompts for user inputs: company name, email, Groq API key
- Processes each qualified email end-to-end
- **When to run:** `python email_listener.py`

### Authentication

**`gmail_auth.py`** - One-time Gmail OAuth setup
- Handles Gmail OAuth 2.0 authentication
- Creates and saves `token.pickle` for future sessions
- **When to run:** First time only: `python gmail_auth.py`

### Email Processing

**`email_fetcher.py`** - Fetches and parses Gmail messages
- `fetch_latest_email()` - Retrieves newest unread email
- `extract_message_data()` - Parses sender, subject, body
- `clean_html_to_text()` - Converts HTML emails to plain text
- Handles multipart MIME messages

**`email_validator.py`** - Validates if emails qualify
- `validate_email()` - Main validation function
- `is_system_email()` - Filters automated/system emails
- `contains_keywords()` - Checks for brochure-related keywords
- `extract_websites()` - Finds URLs in email body
- Configurable keywords and system email domains

### Data Collection

**`web_scraper.py`** - Scrapes prospect websites
- `scrape_website()` - Downloads and cleans website content
- `fetch_website_content()` - HTTP requests with error handling
- `clean_html_to_text_scrape()` - Extracts readable text using BeautifulSoup
- User-agent spoofing to avoid blocking
- 10-second timeout to prevent hangs

**`csv_manager.py`** - Manages leads database
- `init_csv()` - Creates CSV with proper headers
- `add_or_update_lead()` - Adds new prospects
- `get_processed_message_ids()` - Gets already-processed emails
- `mark_as_done()` - Marks emails as completed
- `migrate_csv_format()` - Converts old format to new
- Auto-creates `qualified_leads.csv`

### AI Processing

**`ai_processor.py`** - Groq AI for content generation
- `summarize_with_groq()` - Creates 5-6 sentence website summary
- `call_groq()` - Generic Groq API wrapper
- `test_groq_connection()` - Validates API key
- `extract_blurbs()` - Parses numbered service descriptions
- **Prompts (dynamic with company name):**
  - `get_summary_prompt()` - Website summarization
  - `get_extract_company_prompt()` - Company name extraction
  - `get_extract_description_prompt()` - Service description
  - `get_generate_blurbs_prompt()` - Personalized service blurbs
- Error handling with fallback blurbs

### PDF & Email Generation

**`pdf_generator.py`** - Creates personalized PDFs
- `generate_pdf()` - Main PDF generation workflow
- `convert_docx_to_pdf()` - Handles DOCX → PDF conversion
- `replace_single_placeholder()` - Replaces template variables
- `replace_blurbs()` - Inserts AI-generated content
- Supports LibreOffice (preferred) and docx2pdf fallback
- Auto-creates `personalised/` directory

**`email_sender.py`** - Sends reply emails with attachments
- `create_email_body()` - Generates personalized email text
- `create_reply_message_with_attachment()` - Builds MIME message
- `send_reply_email()` - Sends via Gmail API
- Handles file attachments and threading

---

## Configuration Files

### Required Files (User Must Provide)

**`credentials.json`**
- Gmail OAuth 2.0 credentials
- Downloaded from Google Cloud Console
- Securely stores OAuth client ID and secret
- Consumed once during `gmail_auth.py`

**`template.docx`**
- Microsoft Word document (DOCX format)
- Contains brochure template with placeholders
- **Placeholders to keep:**
  - `(Name)` - Prospect name
  - `(company name)` - Company name
  - `(what your company deals with)` - Service description
  - `Input Blurbs here` - (5 instances for service descriptions)
- **Hardcoded references removed:**
  - "Sappy's Enclove" → "Your Company Name"
  - "+919875367147" → (removed)
  - "ddtectiv.ddip2017@gmail.com" → "your-email@company.com"

### Auto-Generated Files

**`token.pickle`**
- Binary file created by `gmail_auth.py`
- Stores Gmail OAuth token
- Persists across sessions
- Deleted/regenerated if authentication expires

**`qualified_leads.csv`**
- Leads database (comma-separated values)
- **Columns:** Message_ID, Name, Email, Website, Summary, PDF, Done
- Tracks all processed prospects
- Updated after each successful email processing
- Easy to export to Excel/CRM

**`master_log.txt`**
- All operations logged with timestamps
- Append-only (grows over time)
- Example entries:
  - `[2025-11-07 12:34:56] ✅ Gmail API authenticated.`
  - `[2025-11-07 12:35:01] ✨ New qualified email: John Smith`
  - `[2025-11-07 12:35:10] 📊 Added to CSV with Message ID: abc123`

**`failed_steps.txt`**
- Errors and failures logged separately
- Append-only (grows over time)
- Example entries:
  - `[2025-11-07 12:36:00] FAILED STEP 'pdf_generation': LibreOffice timeout`

### Auto-Generated Directories

**`personalised/`**
- Output directory for generated PDFs and DOCXs
- File naming: `{CompanyName}_{MessageIDPrefix}.pdf`
- Example: `ACME_Corp_a1b2c3d4.pdf`
- Auto-created on first run

---

## Module Dependencies

### Import Map

```
email_listener.py (Main)
├── gmail_auth.py → authenticates Gmail
├── email_fetcher.py → fetches emails
├── email_validator.py → validates emails
├── web_scraper.py → scrapes websites
├── ai_processor.py → processes with Groq
├── csv_manager.py → manages database
├── pdf_generator.py → generates PDFs
└── email_sender.py → sends emails

External Dependencies:
├── google-auth-oauthlib (Gmail auth)
├── google-api-python-client (Gmail API)
├── groq (Groq AI API)
├── beautifulsoup4 (HTML parsing)
├── requests (HTTP requests)
├── python-docx (DOCX manipulation)
├── libmimetype (MIME handling - stdlib)
└── Optional: docx2pdf (PDF conversion fallback)
```

---

## Execution Flow Diagram

```
START
  ↓
gmail_auth.py (one-time)
  ├─ Create credentials.json? YES → Download from Google Cloud
  ├─ Run gmail_auth.py
  └─ Creates token.pickle
  ↓
email_listener.py (main loop)
  ├─ Get user inputs:
  │  ├─ Company name
  │  ├─ Email address
  │  └─ Groq API key
  ├─ Initialize CSV
  ├─ Authenticate Gmail
  ├─ Test Groq connection
  │
  └─ INFINITE LOOP (15 sec intervals):
     ├─ Fetch latest email
     ├─ Validate email
     │  ├─ Check: not system email? YES
     │  ├─ Check: has keywords? YES
     │  ├─ Check: has valid email? YES
     │  └─ Check: website found? YES → PROCEED
     ├─ Scrape website
     ├─ Summarize with Groq
     ├─ Extract company info with Groq
     ├─ Generate service blurbs with Groq
     ├─ Generate PDF from template
     ├─ Send reply email with attachment
     ├─ Mark as Done in CSV
     ├─ Log success
     └─ Wait 15 seconds
```

---

## Configuration Reference

### User Inputs (Prompted at Runtime)

```
Prompt 1: Company name
  Input: "Mindedge Solutions"
  Used in: Email template, PDF, Groq prompts

Prompt 2: Email address
  Input: "contact@mindedge.com"
  Used in: Reply emails, email body

Prompt 3: Groq API key
  Input: "gsk_..."
  Used in: All Groq API calls
  Security: Exists only in memory, not saved
```

### Configurable Constants

**`email_listener.py`:**
```python
EMAIL_FETCH_INTERVAL = 15  # seconds between checks
PERSONALISED_DIR = "personalised"  # output directory
```

**`ai_processor.py`:**
```python
GROQ_MODEL = "llama-3.1-8b-instant"  # AI model
```

**All modules:**
```python
MASTER_LOG = "master_log.txt"  # activity log
FAILED_LOG = "failed_steps.txt"  # error log
OUTPUT_CSV = "qualified_leads.csv"  # leads database
TOKEN_FILE = "token.pickle"  # auth token
TEMPLATE_FILE = "template.docx"  # brochure template
```

---

## Data Flow Summary

```
Gmail Email
  ↓
Email Fetcher → Extract sender, subject, body
  ↓
Email Validator → Filter system emails, check keywords
  ↓
Web Scraper → Download website content
  ↓
AI Processor → Summarize, extract info, generate blurbs
  ↓
PDF Generator → Replace template vars, create PDF
  ↓
Email Sender → Send reply with attachment
  ↓
CSV Manager → Update qualified_leads.csv
  ↓
Logging → Record in master_log.txt
```

---

## Folder Structure (After First Run)

```
your_project/
├── Documentation/
│  ├── README.md (4500 words)
│  ├── MODULARIZATION.md (2500 words)
│  ├── QUICKSTART.md (1200 words)
│  └── FILE_MANIFEST.md (this file)
│
├── Code/
│  ├── email_listener.py (main orchestrator)
│  ├── gmail_auth.py (one-time auth)
│  ├── email_fetcher.py (email retrieval)
│  ├── email_validator.py (email validation)
│  ├── web_scraper.py (website scraping)
│  ├── ai_processor.py (AI processing)
│  ├── csv_manager.py (database management)
│  ├── pdf_generator.py (PDF creation)
│  └── email_sender.py (email transmission)
│
├── Config/
│  ├── credentials.json (user-provided)
│  └── template.docx (user-provided/editable)
│
├── Data/
│  ├── token.pickle (auto-generated)
│  ├── qualified_leads.csv (auto-generated)
│  ├── master_log.txt (auto-generated)
│  ├── failed_steps.txt (auto-generated)
│  └── personalised/ (auto-generated)
│     ├── Company1_msg12345.pdf
│     ├── Company1_msg12345.docx
│     ├── Company2_msg67890.pdf
│     └── ...
```

---

## Getting Started Checklist

- [ ] Copy all 9 `.py` files to project directory
- [ ] Copy `README.md`, `MODULARIZATION.md`, `QUICKSTART.md`
- [ ] Download `credentials.json` from Google Cloud
- [ ] Edit `template.docx` with your company info
- [ ] Install dependencies: `pip install ...`
- [ ] Run `python gmail_auth.py` (one-time setup)
- [ ] Run `python email_listener.py` (main loop)
- [ ] Provide company name, email, Groq API key
- [ ] Monitor `master_log.txt` for activity
- [ ] Check `qualified_leads.csv` for leads
- [ ] Review generated PDFs in `personalised/` folder

---

## Support & Troubleshooting

- **Setup Issues:** See QUICKSTART.md
- **Detailed Info:** See README.md
- **Architecture:** See MODULARIZATION.md
- **Logs:** Check `master_log.txt` and `failed_steps.txt`
- **API Keys:** Get from Google Cloud Console and Groq Console

---

**System is ready for production use! 🚀**
