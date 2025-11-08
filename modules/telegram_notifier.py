# ============================================================================
# MODULE: TELEGRAM NOTIFIER
# ============================================================================
# Handles Telegram notifications with message buffering
# ============================================================================

import os
import requests
import threading
import time
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID, TELEGRAM_BUFFER_INTERVAL, TELEGRAM_MAX_MESSAGE_LENGTH, MASTER_LOG

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

# Global message buffer
telegram_message_buffer = []
telegram_buffer_lock = threading.Lock()

def add_to_telegram_buffer(message: str):
    """Add a message to the Telegram buffer."""
    with telegram_buffer_lock:
        telegram_message_buffer.append(message)

def send_telegram_message(text: str) -> bool:
    """Send a single message to Telegram."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return False

    if not TELEGRAM_USER_ID or TELEGRAM_USER_ID == "YOUR_USER_ID_HERE":
        return False

    try:
        telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        data = {
            "chat_id": TELEGRAM_USER_ID,
            "text": text,
            "parse_mode": "HTML"
        }

        response = requests.post(f"{telegram_api_url}/sendMessage", json=data, timeout=10)
        return response.status_code == 200

    except Exception as e:
        print(f"⚠️ Telegram send failed: {e}")
        return False

def send_telegram_document(file_path: str) -> bool:
    """Send a PDF document to Telegram."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return False

    if not TELEGRAM_USER_ID or TELEGRAM_USER_ID == "YOUR_USER_ID_HERE":
        return False

    if not os.path.exists(file_path):
        return False

    try:
        telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': TELEGRAM_USER_ID}
            response = requests.post(
                f"{telegram_api_url}/sendDocument",
                data=data,
                files=files,
                timeout=30
            )
            return response.status_code == 200

    except Exception as e:
        print(f"⚠️ Telegram PDF send failed: {e}")
        return False

def flush_telegram_buffer():
    """Flush buffered messages to Telegram."""
    global telegram_message_buffer

    with telegram_buffer_lock:
        if not telegram_message_buffer:
            return

        # Combine all messages
        combined_message = "\n".join(telegram_message_buffer)

        # Split into chunks if too long
        if len(combined_message) > TELEGRAM_MAX_MESSAGE_LENGTH:
            chunks = [
                combined_message[i:i+TELEGRAM_MAX_MESSAGE_LENGTH]
                for i in range(0, len(combined_message), TELEGRAM_MAX_MESSAGE_LENGTH)
            ]
            for chunk in chunks:
                send_telegram_message(chunk)
        else:
            send_telegram_message(combined_message)

        telegram_message_buffer = []

def start_telegram_buffer_thread():
    """Start background thread to flush Telegram buffer every 15 seconds."""
    def buffer_flusher():
        while True:
            time.sleep(TELEGRAM_BUFFER_INTERVAL)
            flush_telegram_buffer()

    thread = threading.Thread(target=buffer_flusher, daemon=True)
    thread.start()