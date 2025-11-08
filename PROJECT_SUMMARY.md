# Project Summary & File Organization

## 📦 Complete Project Structure

```
email-processing-pipeline/
│
├── 📋 DOCUMENTATION
│   ├── README.md                          # Main documentation
│   ├── SETUP_GUIDE.md                    # Step-by-step setup instructions
│   └── LICENSE                           # Apache 2.0 License
│
├── 🐍 MAIN APPLICATION
│   ├── main.py                           # Application entry point
│   ├── gmail_auth.py                     # One-time Gmail authentication
│   └── config.py                         # Configuration & customization
│
├── 📚 MODULAR COMPONENTS (modules/)
│   ├── __init__.py                       # Package initializer
│   ├── email_handler.py                  # Gmail API & email validation
│   ├── web_scraper.py                    # Website content scraping
│   ├── ai_processor.py                   # Groq API integration
│   ├── document_generator.py             # Document & PDF creation
│   ├── csv_manager.py                    # Lead database management
│   └── telegram_notifier.py              # Telegram notifications
│
├── 📦 DEPENDENCIES
│   └── requirements.txt                  # Python packages
│
├── 🔒 SECURITY
│   └── .gitignore                        # Git exclusions
│
├── 📄 TEMPLATES
│   └── template.docx                     # Customizable Word template
│
├── 🔐 AUTHENTICATION (auto-created)
│   ├── credentials.json                  # Download from Google Cloud
│   └── token.pickle                      # Auto-created by gmail_auth.py
│
└── 📊 RUNTIME DATA (auto-created)
    ├── qualified_leads.csv               # Lead database
    ├── master_log.txt                    # Activity logs
    ├── failed_steps.txt                  # Error logs
    ├── scraped_sites/                    # Cached website content
    └── personalised/                     # Generated DOCX/PDF files
```

---

## 🚀 Quick Start (3 Minutes)

### 1. Install & Configure

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Download credentials.json from Google Cloud Console
# Place in project root directory
```

### 2. Authenticate Gmail (Run Once)

```bash
python gmail_auth.py
# Follow browser prompts to authorize
```

### 3. Start the Application

```bash
python main.py
# Enter Groq API key when prompted
```

---

## 📝 File Descriptions

### Core Files

| File | Purpose | User Action |
|------|---------|-------------|
| `main.py` | Application entry point | Run: `python main.py` |
| `gmail_auth.py` | Gmail OAuth setup | Run once: `python gmail_auth.py` |
| `config.py` | All settings & customization | Edit keywords, Telegram, etc. |

### Modules (Reusable Components)

| Module | Responsibility |
|--------|-----------------|
| `email_handler.py` | Gmail API, email validation, system email filtering |
| `web_scraper.py` | Website content fetching and cleaning |
| `ai_processor.py` | Groq API calls, summarization, content generation |
| `document_generator.py` | Template rendering, DOCX/PDF creation |
| `csv_manager.py` | Lead database read/write operations |
| `telegram_notifier.py` | Telegram messaging and notifications |

### Documentation

| File | Contains |
|------|----------|
| `README.md` | Complete feature overview and usage |
| `SETUP_GUIDE.md` | Step-by-step configuration instructions |
| `LICENSE` | Apache 2.0 open-source license |

---

## ⚙️ Key Configuration Points

### Edit These in `config.py`

**1. Email Monitoring**
```python
EMAIL_FETCH_INTERVAL = 15  # Check every 15 seconds
KEYWORDS = ["brochure", "catalog", ...]  # Add your keywords
```

**2. System Email Filtering**
```python
SYSTEM_EMAIL_DOMAINS = ["noreply@", ...]  # Domains to ignore
SYSTEM_EMAIL_KEYWORDS = ["do not reply", ...]  # Keywords to ignore
```

**3. Telegram Notifications (Optional)**
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_USER_ID = "YOUR_USER_ID_HERE"
```

**4. AI Customization**
```python
GROQ_MODEL = "llama-3.1-8b-instant"
GENERATE_BLURBS_PROMPT = """Custom prompt here..."""  # Modify AI behavior
```

---

## 📋 Customization Checklist

- [ ] Update `config.py` with your keywords and filters
- [ ] Customize `template.docx` with your branding
- [ ] Update AI prompts in `config.py` for your use case
- [ ] Configure Telegram bot (optional)
- [ ] Test with sample email before full deployment

---

## 🔒 Security Considerations

**Files to Keep Private:**
- `credentials.json` - Never commit to Git
- `token.pickle` - Keep secure and backed up
- Groq API key - Entered at runtime, never stored

**Provided `.gitignore`:**
```
credentials.json
token.pickle
qualified_leads.csv
master_log.txt
failed_steps.txt
scraped_sites/
personalised/
```

---

## 📊 Processing Pipeline Overview

```
Email Received
    ↓
Validate (Keywords, Sender, System Email Check)
    ↓
Extract (Name, Email, Website)
    ↓
Scrape Website
    ↓
AI Summarization
    ↓
Company Information Extraction
    ↓
Generate Service Recommendations
    ↓
Create Personalized Document
    ↓
Convert DOCX → PDF
    ↓
Send Reply with PDF
    ↓
Send Telegram Notification
    ↓
Record in CSV Database
```

---

## 📈 Scalability Features

- **Modular Design:** Each function is independent and reusable
- **Configurable:** All settings in one file (`config.py`)
- **Logging:** Comprehensive activity and error logs
- **Buffering:** Telegram notifications batched to reduce API calls
- **CSV Database:** Track all processed leads
- **Error Handling:** Graceful failure with detailed logging

---

## 🛠 Maintenance & Support

### Regular Tasks

1. **Monitor Logs**
   ```bash
   tail -f master_log.txt        # Real-time activity
   cat failed_steps.txt           # Recent errors
   ```

2. **Review Leads**
   ```bash
   # Check qualified_leads.csv for processed emails
   ```

3. **Verify PDFs**
   ```bash
   # Check personalised/ folder for generated documents
   ```

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No emails processing | Wrong keywords | Update `KEYWORDS` in config.py |
| PDF conversion fails | LibreOffice missing | Install LibreOffice (see SETUP_GUIDE.md) |
| Groq API errors | Invalid key | Verify at https://console.groq.com/keys |
| Gmail auth fails | Token expired | Delete `token.pickle`, run `gmail_auth.py` |

---

## 📄 License & Attribution

This project is released under the **Apache License 2.0**, which means:

✅ **You can:**
- Use commercially
- Modify the code
- Distribute modified versions
- Use privately

⚠️ **You must:**
- Include a copy of the license
- Provide attribution
- Document changes made

**No warranty provided.** See `LICENSE` file for complete terms.

---

## 📞 Support Resources

- `README.md` - Detailed feature documentation
- `SETUP_GUIDE.md` - Step-by-step configuration
- `master_log.txt` - Debug activity logs
- `failed_steps.txt` - Error tracking
- Code comments - Inline documentation

---

## Version Information

**Current Version:** 1.0.0

**Python Requirement:** 3.8+

**Key Dependencies:**
- Google APIs (Gmail)
- Groq API
- python-docx
- BeautifulSoup4
- Requests

---

**Built for professionals. Optimized for production use.**