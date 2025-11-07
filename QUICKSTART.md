# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (2 min)

```bash
pip install google-auth-oauthlib google-api-python-client groq beautifulsoup4 requests python-docx
```

Optional (for PDF export):
```bash
pip install docx2pdf
```

Or install **LibreOffice** from https://www.libreoffice.org/download/

### Step 2: Get Gmail Credentials (1 min)

1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable **Gmail API**
4. Create **OAuth 2.0 Desktop credentials**
5. Download and save as `credentials.json` in your project folder

### Step 3: Run First-Time Setup (1 min)

```bash
python gmail_auth.py
```

This opens your browser to authenticate with Gmail. After success, `token.pickle` is auto-created.

### Step 4: Start Listening (1 min)

```bash
python email_listener.py
```

You'll be prompted for:
```
📝 Enter your company name: MyCompany
📧 Enter your email address: me@mycompany.com
🔑 Enter your Groq API key: gsk_...
```

Then the system starts monitoring for emails!

---

## What Happens Next

1. **Email arrives** → System checks every 15 seconds
2. **Validation** → Filters for keywords (brochure, catalog, etc.)
3. **Website scrape** → Retrieves prospect company info
4. **AI processing** → Generates personalized content
5. **PDF creation** → Creates custom brochure
6. **Email sent** → Sends reply with attachment
7. **Logged** → Tracks everything in CSV

---

## Project Files You Need

```
your_project/
├── gmail_auth.py
├── email_listener.py
├── email_fetcher.py
├── email_validator.py
├── web_scraper.py
├── ai_processor.py
├── csv_manager.py
├── pdf_generator.py
├── email_sender.py
├── template.docx
└── credentials.json  ← Download from Google Cloud
```

---

## Customize Your Template

Open `template.docx` in Word or LibreOffice:

1. Edit company info
2. Update services/pricing
3. Keep these placeholders:
   - `(Name)` → Auto-filled with prospect name
   - `(company name)` → Auto-filled with prospect company
   - `(what your company deals with)` → Auto-filled by AI
   - `Input Blurbs here` → Auto-filled 5 times with service descriptions

Save and close. Template is ready!

---

## Check Logs

**All activities logged to `master_log.txt`:**
```
[2025-11-07 12:34:56] 🚀 Starting infinite email monitoring loop...
[2025-11-07 12:34:57] ✅ Gmail API authenticated.
[2025-11-07 12:35:01] ✨ New qualified email: John Smith (john@acme.com)
[2025-11-07 12:35:05] 📊 Added to CSV with Message ID: abc123
[2025-11-07 12:35:10] 🌐 Scraping: acme.com
...
```

**Errors logged to `failed_steps.txt`**

---

## Test It

### Send yourself a test email:

Subject: "Hi, do you have a brochure?"
Body: "I'm interested in your services. Our website is mycompany.com"

The system should:
1. ✅ Validate it (has "brochure" keyword)
2. ✅ Scrape mycompany.com
3. ✅ Generate personalized content
4. ✅ Create PDF
5. ✅ Send reply
6. ✅ Log everything

Check `qualified_leads.csv` to see your test lead!

---

## Troubleshooting

**"token.pickle not found"**
→ Run `python gmail_auth.py` first

**"credentials.json not found"**
→ Download from Google Cloud Console

**"Groq API error"**
→ Get free API key at https://console.groq.com

**"No new emails"**
→ System checks every 15 seconds, or edit `EMAIL_FETCH_INTERVAL` in `email_listener.py`

**"PDF conversion failed"**
→ Install LibreOffice or `pip install docx2pdf` (requires MS Word)

---

## Next Steps

1. **Production Setup**
   - Test with real prospects
   - Monitor logs for errors
   - Adjust `EMAIL_FETCH_INTERVAL` if needed

2. **Scale Up**
   - Use scheduled tasks to run 24/7
   - Monitor API usage (Gmail, Groq)
   - Backup `qualified_leads.csv` regularly

3. **Integrate**
   - Connect to CRM (Salesforce, Pipedrive, etc.)
   - Add webhook notifications
   - Track email open rates

4. **Package as EXE**
   - Distribute to team without Python
   - See README.md for instructions

---

## Support Resources

- **Full Documentation:** See `README.md`
- **Module Details:** See `MODULARIZATION.md`
- **Gmail API:** https://developers.google.com/gmail/api
- **Groq API:** https://console.groq.com
- **Logs:** Check `master_log.txt` and `failed_steps.txt`

---

## You're Ready!

Your modular email processing system is now live. Customize the template, monitor the logs, and watch qualified leads roll in! 🚀
