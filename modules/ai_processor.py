# ============================================================================
# MODULE: AI PROCESSOR
# ============================================================================
# Handles Groq API interactions for summarization and content generation
# ============================================================================

import re
from datetime import datetime
from groq import Groq
from config import (
    GROQ_MODEL, GROQ_MAX_TOKENS, GROQ_TEMPERATURE,
    SUMMARY_PROMPT, EXTRACT_COMPANY_PROMPT, EXTRACT_DESCRIPTION_PROMPT,
    GENERATE_BLURBS_PROMPT, MASTER_LOG
)

def log_message(message: str, log_file: str = MASTER_LOG):
    """Log to console and file with timestamp."""
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
            messages=[{"role": "user", "content": "Say 'Connection successful!'"}],
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
            max_tokens=GROQ_MAX_TOKENS,
            temperature=GROQ_TEMPERATURE
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        log_message(f"❌ Groq API error: {error_msg}")
        return ""

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
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": SUMMARY_PROMPT.format(content=content)}],
            max_tokens=400,
            temperature=GROQ_TEMPERATURE
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

def extract_company_name(summary: str, client) -> str:
    """Extract company name from summary."""
    company_name = call_groq(EXTRACT_COMPANY_PROMPT.format(summary=summary), client)
    
    if not company_name or company_name.lower() in ['unknown', 'n/a', '']:
        company_name = "Professional Organization"
    
    return company_name

def extract_company_description(summary: str, client) -> str:
    """Extract company description from summary."""
    description = call_groq(EXTRACT_DESCRIPTION_PROMPT.format(summary=summary), client)
    
    if not description or description.lower() in ['unknown', 'n/a', '']:
        description = "innovative solutions in the digital space."
    
    # Ensure it starts with "providing"
    if not description.lower().startswith('providing '):
        description = f"providing {description.lower()}"
    
    return description

def generate_blurbs(company_name: str, summary: str, client) -> list:
    """Generate personalized service blurbs."""
    log_message(f"💭 Generating personalized blurbs for {company_name}...")
    
    blurb_text = call_groq(
        GENERATE_BLURBS_PROMPT.format(company_name=company_name, summary=summary),
        client
    )
    
    blurbs = extract_blurbs_from_text(blurb_text)
    
    return blurbs

def extract_blurbs_from_text(text: str) -> list:
    """Extract numbered blurbs from text."""
    blurbs = []
    
    # Match numbered items like "1. Text here" or "1) Text here"
    pattern = r'^\s*\d+[\.\)]\s*(.+)$'
    
    for line in text.split('\n'):
        match = re.match(pattern, line)
        if match:
            blurb = match.group(1).strip()
            if blurb:
                blurbs.append(blurb)
    
    # Ensure we have exactly 5 blurbs
    while len(blurbs) < 5:
        blurbs.append("Service offering tailored to your organization's needs.")
    
    return blurbs[:5]