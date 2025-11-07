import csv
import os
from datetime import datetime

MASTER_LOG = "master_log.txt"
OUTPUT_CSV = "qualified_leads.csv"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def migrate_csv_format():
    """Migrate old CSV format to new format if needed."""
    if not os.path.exists(OUTPUT_CSV):
        return
    
    rows = []
    old_fieldnames = None
    
    try:
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            old_fieldnames = reader.fieldnames
            rows = list(reader)
    except Exception as e:
        log_message(f"❌ Error reading CSV: {e}")
        return
    
    if not old_fieldnames:
        return
    
    has_emailed = 'Emailed' in old_fieldnames
    has_message_id = 'Message_ID' in old_fieldnames
    
    if not has_emailed and has_message_id:
        return
    
    if has_emailed:
        log_message("🔄 Migrating CSV from old format to new format...")
        
        new_rows = []
        for row in rows:
            new_row = {
                'Message_ID': row.get('Message_ID', ''),
                'Name': row.get('Name', ''),
                'Email': row.get('Email', ''),
                'Website': row.get('Website', ''),
                'Summary': row.get('Summary', ''),
                'PDF': row.get('PDF', ''),
                'Done': 'Yes' if row.get('Emailed', '').lower() == 'yes' else ''
            }
            new_rows.append(new_row)
        
        fieldnames = ['Message_ID', 'Name', 'Email', 'Website', 'Summary', 'PDF', 'Done']
        
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)
        
        log_message(f"✅ CSV migrated successfully. {len(new_rows)} rows converted.")

def init_csv():
    """Initialize CSV file with headers if it doesn't exist."""
    migrate_csv_format()
    
    if not os.path.exists(OUTPUT_CSV):
        fieldnames = ['Message_ID', 'Name', 'Email', 'Website', 'Summary', 'PDF', 'Done']
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
        log_message(f"📊 Created new CSV: {OUTPUT_CSV}")

def get_processed_message_ids():
    """Get all message IDs that have been marked as Done."""
    processed = set()
    
    if os.path.exists(OUTPUT_CSV):
        try:
            with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    message_id = row.get('Message_ID', '').strip()
                    done = row.get('Done', '').strip().lower()
                    if message_id and done == 'yes':
                        processed.add(message_id)
        except Exception as e:
            log_message(f"❌ Error reading processed message IDs: {e}")
    
    return processed

def add_or_update_lead(message_id: str, name: str, email: str, website: str):
    """Add a new lead or update existing one in CSV."""
    fieldnames = ['Message_ID', 'Name', 'Email', 'Website', 'Summary', 'PDF', 'Done']
    rows = []
    
    if os.path.exists(OUTPUT_CSV):
        try:
            with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            log_message(f"❌ Error reading CSV: {e}")
            rows = []
    
    found = False
    for row in rows:
        if row.get('Message_ID') == message_id:
            found = True
            break
    
    if not found:
        new_row = {
            'Message_ID': message_id,
            'Name': name,
            'Email': email,
            'Website': website,
            'Summary': '',
            'PDF': '',
            'Done': ''
        }
        rows.append(new_row)
    
    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        log_message(f"❌ Error writing to CSV: {e}")

def mark_as_done(message_id: str):
    """Mark a message as Done in CSV."""
    fieldnames = ['Message_ID', 'Name', 'Email', 'Website', 'Summary', 'PDF', 'Done']
    rows = []
    
    try:
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        log_message(f"❌ Error reading CSV: {e}")
        return
    
    for row in rows:
        if row.get('Message_ID') == message_id:
            row['Done'] = 'Yes'
            break
    
    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        log_message(f"❌ Error writing to CSV: {e}")
