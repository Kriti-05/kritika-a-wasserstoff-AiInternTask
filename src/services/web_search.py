# web_search.py
from serpapi import GoogleSearch
from src.utils.config import SERPAPI_API_KEY  # Store your API key in config.py

def serpapi_search(query, num_results=3):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    output = []

    if "organic_results" in results:
        for item in results["organic_results"][:num_results]:
            output.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            })
    return output

def is_question(text):
    question_words = ["?", "what", "how", "when", "why", "who", "can you", "could you", "do you know"]
    return any(q in text.lower() for q in question_words)
