## Gemini Terminal Chatbot (Python)

This project implements a simple, interactive chatbot using the Google GenAI Python SDK (google-generativeai) with the gemini-2.5-pro model, running directly in your terminal.

## Requirements
- Python 3.8 installed.
- A Google API key (you can obtain one from Google AI Studio)

## Configuration

1. Dependency Installation
Install the google-generativeai library using pip:

pip install google-generativeai

2. API Key Setup
The API key can be configured in two ways:
Option A: Environment Variable (Recommended)
This is the most secure method, preventing the key from being stored in logs or files.

Linux/macOS:export GOOGLE_API_KEY="YOUR_KEY_HERE"

Windows (Command Prompt):

set GOOGLE_API_KEY="YOUR_KEY_HERE"

Option B: Manual Input

If the environment variable is not configured, the script will prompt for the key upon startup. You will need to type it into the terminal (the input will be invisible for security, thanks to the getpass module).

## Execution
Run the script chatbot.py from your terminal:

python chatbot.py

## Interaction Commands

To chat: Type your question and press Enter.
To exit: Type exit (or press Ctrl+C / Ctrl+D).

## Example

You: which is the capital of Angola?
Gemini: The capital of Angola is Luanda.

## Author

Felipe (Morango)
