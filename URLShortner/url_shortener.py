# url_shortener.py
from flask import Flask, redirect, request, render_template_string
import random
import string
import json
import os

app = Flask(__name__)
DATA_FILE = "urls.json"

# Load saved URLs
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        url_mapping = json.load(f)
else:
    url_mapping = {}

def save_urls():
    with open(DATA_FILE, "w") as f:
        json.dump(url_mapping, f)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Improved HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Python URL Shortener</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background: #f4f7f8;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    .container {
        background: #fff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
        text-align: center;
    }
    h2 {
        margin-bottom: 20px;
        color: #333;
    }
    input[type="text"] {
        width: 80%;
        padding: 10px;
        margin-bottom: 20px;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
    }
    input[type="submit"] {
        padding: 10px 20px;
        font-size: 16px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    input[type="submit"]:hover {
        background-color: #45a049;
    }
    .short-url {
        margin-top: 20px;
        font-size: 16px;
        color: #333;
        word-break: break-all;
    }
    a {
        color: #2196F3;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
</head>
<body>
<div class="container">
    <h2>Python URL Shortener</h2>
    <form method="POST">
        <input type="text" name="long_url" placeholder="Enter your long URL" required>
        <br>
        <input type="submit" value="Shorten">
    </form>
    {% if short_url %}
        <div class="short-url">
            Short URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
        </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    if request.method == "POST":
        long_url = request.form["long_url"]
        code = generate_code()
        url_mapping[code] = long_url
        save_urls()
        short_url = request.host_url + code
    return render_template_string(HTML_TEMPLATE, short_url=short_url)

@app.route("/<code>")
def redirect_short_url(code):
    long_url = url_mapping.get(code)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
