import re
from datetime import datetime
from groq import Groq

MASTER_LOG = "master_log.txt"
GROQ_MODEL = "llama-3.1-8b-instant"

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to both console and file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(message)
    with open(log_file, 'a', encoding='utf-8') as logf:
        logf.write(log_entry)

def test_groq_connection(client):
    """Quick test to validate Groq API connection."""
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "Say 'API works!'"}],
            max_tokens=10,
            temperature=0.1
        )
        log_message(f"🔗 Groq connection test: {response.choices[0].message.content.strip()}")
        return True
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        log_message(f"❌ Groq connection test failed: {error_msg}")
        return False

def call_groq(prompt: str, client) -> str:
    """Helper to call Groq API."""
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        log_message(f"❌ Groq API error: {error_msg}")
        return ""

def get_summary_prompt(content: str) -> str:
    """Get the summary prompt."""
    return f"""Summarize the key information from this scraped webpage content in a single continuous paragraph of exactly 5-6 sentences. Focus on:

Company overview and services/products offered.
Contact details, location, and team (if available).
Any relevant business focus or unique selling points.

Keep it professional, concise, and factual. Do NOT use any markdown (like **bold**), bullet points, line breaks, or formatting—output everything as one unbroken paragraph with only spaces between sentences.

Content: {content}
"""

def get_extract_company_prompt(summary: str) -> str:
    """Get the extract company name prompt."""
    return f"""Extract the exact company name from this webpage summary. Respond with ONLY the company name (e.g., 'Mindedge Solutions'), nothing else.

Summary: {summary}
"""

def get_extract_description_prompt(summary: str) -> str:
    """Get the extract description prompt."""
    return f"""From this webpage summary, create a concise one-sentence description of what the company does or deals with, phrased as 'providing [services] to [industries/clients]'. Respond with ONLY that sentence, nothing else.

Summary: {summary}
"""

def get_generate_blurbs_prompt(company_name: str, summary: str) -> str:
    """Get the generate blurbs prompt with company name dynamically."""
    return f"""Generate 5 short, personalized blurbs (1-2 sentences each) for {company_name}'s services. Explain how EACH service from {company_name} can specifically benefit {company_name} based on their focus in this summary: {summary}.

Use the perspective of {company_name} offering help TO {company_name} (e.g., 'At {company_name}, we can optimize your workflows to enhance your digital marketing efficiency').

Keep each professional, concise, and starting with 'At {company_name},' or similar. Number them exactly 1-5, one per line—no extras or markdown:

1. For Process Optimization & Workflow Analysis
2. For Strategic Consulting & Planning
3. For Custom Solution Development
4. For Training & Knowledge Transfer
5. For Quality Assurance & Performance Monitoring
"""

def summarize_with_groq(content: str, client) -> str:
    """Generate summary using Groq API."""
    if not content.strip():
        log_message("⚠️ Content is empty – skipping summary.")
        return "No content available for summarization."
    
    original_len = len(content)
    
    if original_len > 4000:
        content = content[:4000] + "\n\n[Content truncated for summarization...]"
        log_message(f"📝 Content truncated to 4000 chars (original: {original_len} chars).")
    
    try:
        prompt = get_summary_prompt(content)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content.strip()
        summary = re.sub(r'\n+', ' ', summary)
        summary = re.sub(r'\*\*(.*?)\*\*', r'\1', summary)
        summary = re.sub(r'\s+', ' ', summary).strip()
        
        log_message(f"✅ Generated summary ({len(summary)} chars)")
        return summary
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        log_message(f"❌ Error generating summary: {error_msg}")
        return ""

def extract_blurbs(blurb_text: str) -> list:
    """Parse numbered blurbs from Groq response."""
    if not blurb_text:
        return ["At Your Company Name, we offer tailored support to enhance your operations."] * 5
    
    matches = re.findall(r'^\s*(\d+)\.\s*(.+?)(?=\n\d+\.|$)', blurb_text, re.MULTILINE | re.DOTALL)
    
    blurbs = []
    for num, text in matches:
        if 1 <= int(num) <= 5:
            clean_text = re.sub(r'\n+', ' ', text.strip())
            clean_text = re.sub(r'\s+', ' ', clean_text)
            blurbs.append(clean_text)
    
    while len(blurbs) < 5:
        blurbs.append("At Your Company Name, we provide expert guidance to achieve your business goals efficiently.")
    
    if len(blurbs) > 5:
        blurbs = blurbs[:5]
    
    return blurbs
