import requests
from bs4 import BeautifulSoup
from collections import Counter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.shortcuts import render

# Define a list of common stopwords to exclude from the filtered list
STOPWORDS = {'this', 'that','thus', 'although','therefore','too','much','very','less','more','should','will','would','can','could',
    'a', 'an', 'the', 'and', 'but', 'or', 'nor', 'so', 'yet', 'for', 'of', 
    'on', 'in', 'at', 'to', 'by', 'with', 'about', 'as', 'into', 'like', 
    'through', 'after', 'over', 'between', 'out', 'against', 'during', 
    'without', 'before', 'under', 'around', 'among', 'is', 'are', 'was', 
    'were', 'be', 'being', 'been', 'it', 'he', 'she', 'they', 'we', 'you', 
    'I', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'their', 'A', 'B', 'C', 'D', 'E','F','G','H', 'J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}

# Regex pattern to filter out numbers, mathematical operators, and symbols
IGNORE_PATTERN = r'\b(?:[0-9]+|alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|omicron|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|plus|minus|times|divide|sum|product)\b|\W+'

def fetch_meaning(word):
    """Fetch the first two meanings of a word using Free Dictionary API."""
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            # Get up to two meanings if available
            definitions = data[0]["meanings"][0]["definitions"]
            meaning_1 = definitions[0]["definition"] if len(definitions) > 0 else "Meaning not found"
            meaning_2 = definitions[1]["definition"] if len(definitions) > 1 else None
            return f"(i) {meaning_1}" + (f" (ii) {meaning_2}" if meaning_2 else "")
        else:
            return "Meaning not found"
    except (requests.RequestException, KeyError, IndexError):
        return "Meaning not found"

@csrf_exempt
def word_frequency_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data.get("url")
        if not url:
            return JsonResponse({"error": "No URL provided"}, status=400)

        try:
            # Fetch and parse the webpage content
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove <style>, <script>, and other inline CSS/display content
            for tag in soup(['style', 'script']):
                tag.decompose()  # This removes the tag from the soup

            text = soup.get_text().lower()

            # Remove mathematical symbols, numbers, and variable symbols
            text_cleaned = re.sub(IGNORE_PATTERN, ' ', text)
            words = text_cleaned.split()

            # Count all words
            word_count = Counter(words)
            top_words_all = word_count.most_common(10)

            # Filter out stopwords and count remaining words
            filtered_words = [word for word in words if word not in STOPWORDS]
            filtered_word_count = Counter(filtered_words)
            top_words_filtered = filtered_word_count.most_common(10)

            # Prepare meanings for the top 10 filtered words
            meanings = {word: fetch_meaning(word) for word, count in top_words_filtered}

            # Prepare the JSON response with both lists and meanings
            result_all = [{"word": word, "count": count} for word, count in top_words_all]
            result_filtered = [{"word": word, "count": count} for word, count in top_words_filtered]
            
            return JsonResponse({
                "top_words_all": result_all,
                "top_words_filtered": result_filtered,
                "meanings": meanings
            })
        except requests.RequestException:
            return JsonResponse({"error": "Failed to fetch URL"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def index(request):
    return render(request, 'index.html')
