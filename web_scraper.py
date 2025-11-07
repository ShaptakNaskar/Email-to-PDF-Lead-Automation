import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

MASTER_LOG = "master_log.txt"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def sanitize_filename(name):
    """Make filenames safe for all OS."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def fetch_website_content(url):
    """Fetch website content politely."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ElegantScraper/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            log_message(f"⚠️ Could not fetch {url} — HTTP {response.status_code}")
            return None
    except Exception as e:
        log_message(f"❌ Error fetching {url}: {e}")
        return None

def clean_html_to_text_scrape(html):
    """Extract main readable text using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text.strip())
    
    return text

def scrape_website(website: str):
    """Scrape and clean a website, return text content."""
    if not website.startswith("http"):
        website = f"https://{website}"
    
    log_message(f"🌐 Scraping: {website}")
    
    html = fetch_website_content(website)
    
    if not html:
        log_message(f"💤 Failed to scrape {website}")
        return None
    
    text = clean_html_to_text_scrape(html)
    
    return text
