import sqlite3
from transformers import pipeline
import os

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

# Load the summarizer pipeline only once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to chunk long text into smaller parts
def chunk_text(text, chunk_size=512):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function to summarize a single email
def summarize_email(subject, body):
    email_text = f"Subject: {subject}\n\n{body}"
    chunks = chunk_text(email_text)
    summaries = [
        summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        for chunk in chunks
    ]
    return " ".join(summaries)

# Function to summarize latest N emails from DB
def extract_email_content(emails):
    """
    Input: list of email dicts with keys 'sender', 'subject', 'body'
    Output: list of dicts with 'sender', 'summary'
    """
    processed = []
    for email in emails:
        subject = email.get("subject", "")
        body = email.get("body", "")
        summary = summarize_email(subject, body)
        processed.append({
            "sender": email.get("sender"),
            "summary": summary
        })
    return processed
