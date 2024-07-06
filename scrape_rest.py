from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse

app = Flask(__name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def check_and_scrape(url, num_words):
    if not is_valid_url(url):
        return "Invalid URL"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ' '.join(soup.get_text(separator=' ', strip=True).split()[:num_words])
            return text
        else:
            return f"Error accessing {url}: Status code {response.status_code}"
    except requests.RequestException as e:
        return f"Error accessing {url}: {e}"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    num_words = data.get('num_words', 3000)  # Default to 3000 words if not specified

    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        num_words = int(num_words)
    except ValueError:
        return jsonify({"error": "num_words must be an integer"}), 400

    scraped_text = check_and_scrape(url, num_words)
    return jsonify({"scraped_text": scraped_text})

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "hello from rest api"})

if __name__ == '__main__':
    app.run(debug=True)