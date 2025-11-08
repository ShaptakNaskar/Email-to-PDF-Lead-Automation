# Quick Start & Setup Guide

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Active Gmail account
- [ ] Groq API key (free at https://groq.com)
- [ ] LibreOffice installed (for PDF conversion)
- [ ] Telegram account (optional, for notifications)

---

## Step 1: Create Google Cloud Project & Obtain Credentials

### 1.1 Create a New Project

1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a Project" → "NEW PROJECT"
3. Enter project name (e.g., "Email Pipeline")
4. Click "CREATE"

### 1.2 Enable Gmail API

1. In the search bar, type "Gmail API"
2. Click "Gmail API" from results
3. Click "ENABLE"

### 1.3 Create OAuth 2.0 Credentials

1. Click "Create Credentials" button
2. Choose:
   - **Application type:** Desktop application
   - Click "Create"
3. A dialog appears with your credentials
4. Click "DOWNLOAD JSON"
5. Save as `credentials.json` in project root

**Important:** Keep this file private and secure!

---

## Step 2: Set Up Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Optional:** For better console colors on Windows:

```bash
pip install colorama
```

---

## Step 4: Install LibreOffice (Required for PDF Conversion)

### Windows

Using Chocolatey:
```bash
choco install libreoffice
```

Or download from: https://www.libreoffice.org/download

### macOS

```bash
brew install libreoffice
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install libreoffice
```

---

## Step 5: Gmail Authentication (Run Once)

```bash
python gmail_auth.py
```

This will:
1. Open your browser automatically
2. Ask you to authorize the application
3. Create `token.pickle` (do NOT delete this)

**Note:** This only needs to be done once. The token is reused on subsequent runs.

---

## Step 6: Configure Your Settings

Edit `config.py` to customize:

### Email Keywords (What emails to process)

```python
KEYWORDS = [
    "brochure", "catalog", "proposal",  # Add your keywords
    "custom_keyword"
]
```

### Customize System Email Filters

Add domains/keywords you want to ignore:

```python
SYSTEM_EMAIL_DOMAINS = [
    "default_domains...",
    "your_domain_to_ignore.com"
]
```

### Telegram Notifications (Optional)

1. Chat with [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` command
3. Follow prompts to create a bot
4. Copy the BOT_TOKEN
5. Chat with [@userinfobot](https://t.me/userinfobot)
6. Copy your USER_ID
7. In `config.py`, update:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_USER_ID = "YOUR_USER_ID_HERE"
```

---

## Step 7: Customize Document Template

1. Open `template.docx` in Microsoft Word or LibreOffice
2. Edit branding, colors, fonts, contact info
3. Keep these placeholders (case-sensitive):
   - `(Name)` - recipient name
   - `(company name)` - company name
   - `(what your company deals with)` - description
   - `Input Blerbs here` - service recommendations (appears 5 times)
4. Save and close

---

## Step 8: Run the Application

```bash
python main.py
```

On first run, you'll be prompted for your Groq API key:

```
🔑 Enter your Groq API key for this session: [paste your key here]
```

The key is requested interactively and **not stored permanently** for security.

The application will now:
- Monitor your inbox every 15 seconds
- Process qualifying emails automatically
- Generate personalized documents
- Send replies with PDF attachments
- Log all activity to `master_log.txt`

**To stop:** Press `Ctrl+C`

---

## Project Structure After Setup

```
email-processing-pipeline/
├── config.py                    ✓ Configured
├── main.py
├── gmail_auth.py
├── requirements.txt
├── README.md
├── LICENSE (Apache 2.0)
├── .gitignore
├── modules/
│   ├── email_handler.py
│   ├── web_scraper.py
│   ├── ai_processor.py
│   ├── document_generator.py
│   ├── csv_manager.py
│   └── telegram_notifier.py
├── template.docx                ✓ Customized
├── credentials.json             ✓ Downloaded (KEEP PRIVATE!)
├── token.pickle                 ⚙ Auto-created
├── qualified_leads.csv          ⚙ Auto-created
├── master_log.txt               ⚙ Auto-created
├── failed_steps.txt             ⚙ Auto-created
├── scraped_sites/               ⚙ Auto-created
└── personalised/                ⚙ Auto-created
```

---

## Common Issues & Solutions

### "credentials.json not found"

**Solution:**
1. Download from Google Cloud Console (see Step 1.3)
2. Place in project root directory
3. Ensure filename is exactly `credentials.json`

### "Token invalid or expired"

**Solution:**
```bash
# Delete old token and re-authenticate
rm token.pickle
python gmail_auth.py
```

### "Groq API error"

**Solution:**
1. Verify API key at https://console.groq.com/keys
2. Check internet connection
3. Review `failed_steps.txt` for specific error

### "DOCX to PDF conversion failed"

**Solution:**
1. Ensure LibreOffice is installed (see Step 4)
2. Test installation:
   ```bash
   libreoffice --version
   ```
3. If not in PATH, add to system PATH manually

### "No emails being processed"

**Checklist:**
- [ ] Email in INBOX (not Labels/Filters)
- [ ] Email contains at least one keyword from `config.py`
- [ ] Not from system email domains
- [ ] Check `master_log.txt` for errors
- [ ] Ensure `gmail_auth.py` ran successfully

---

## Running in Background (Optional)

### Windows

Create `start_pipeline.bat`:
```batch
@echo off
python main.py
pause
```

Run at startup via Task Scheduler.

### macOS/Linux

Create `start_pipeline.sh`:
```bash
#!/bin/bash
cd /path/to/email-processing-pipeline
source venv/bin/activate
python main.py
```

Make executable:
```bash
chmod +x start_pipeline.sh
```

Run with nohup:
```bash
nohup ./start_pipeline.sh > pipeline.log 2>&1 &
```

---

## Next Steps

1. ✅ Complete all setup steps above
2. 📧 Send a test email with a keyword to your Gmail
3. 📊 Check `qualified_leads.csv` after processing
4. 📄 Verify PDF in `personalised/` folder
5. 📱 Check Telegram for notifications (if configured)
6. 📝 Review `master_log.txt` for execution details

---

## Security Best Practices

- [ ] Never commit `credentials.json` to Git
- [ ] Never share your Groq API key
- [ ] Keep `token.pickle` secure
- [ ] Use `.gitignore` (provided)
- [ ] Review generated leads before processing
- [ ] Test with sample emails first

---

## Support

For detailed documentation, see `README.md`

For troubleshooting, check:
1. `master_log.txt` - General activity
2. `failed_steps.txt` - Errors only
3. Console output during execution