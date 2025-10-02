# URL Shortener

A simple Python URL Shortener with persistent short URLs and a clean web interface.

## Features
- Shorten long URLs
- Redirect short URLs to original URLs
- Persistent storage in `urls.json`
- Responsive and user-friendly UI

## Requirements
- Python 3.7+
- Flask

## Usage
Run the script:

python url_shortener.py
Open your browser and go to: http://127.0.0.1:5000/
Enter the long URL in the input box and click Shorten.

The short URL will appear below the input box.

Click the short URL or copy it into a browser — it will redirect to the original long URL while keeping the same domain (http://127.0.0.1:5000/<shortcode>).

