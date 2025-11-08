# ============================================================================
# GMAIL AUTHENTICATION MODULE
# ============================================================================
# Standalone OAuth 2.0 authentication script for Gmail
# Run this ONCE before running main.py
# ============================================================================

import os
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configuration
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
MASTER_LOG = "master_log.txt"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def authenticate_gmail():
    """Authenticate with Gmail API via OAuth 2.0 and return a Gmail service."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"❌ {CREDENTIALS_FILE} not found! Download it from Google Cloud Console.")

            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def main():
    """Run Gmail authentication only."""
    try:
        log_message("🚀 Starting Gmail Authentication...")
        service = authenticate_gmail()
        log_message("✅ Gmail authentication successful!")
        log_message(f"✨ Token saved to '{TOKEN_FILE}'")
        log_message("ℹ️ You can now use the token in the main script.")
    except FileNotFoundError as e:
        log_message(f"❌ Error: {str(e)}")
    except Exception as e:
        log_message(f"❌ Authentication failed: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"💥 Fatal error: {type(e).__name__}: {str(e)}")