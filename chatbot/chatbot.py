
import google.generativeai as genai
import os
import getpass
import sys
from typing import Dict, Any

os.environ["GRPC_VERBOSITY"] = "NONE"

# Configuration API key
def configure_api_key() -> None:
    """
    Configures the Google Gemini API key.

    First, it attempts to get the key from the GOOGLE_API_KEY environment variable.
    If not found, it securely prompts the user to enter it using getpass.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("API key found in the GOOGLE_API_KEY environment variable.")
        try:
            genai.configure(api_key=api_key)
            return
        except Exception as e:
            print(f"Error configuring API with environment key: {e}")
            print("Attempting to prompt for the key manually...")

    print("The GOOGLE_API_KEY environment variable was not set or the key is invalid.")
    try:
        api_key = getpass.getpass("Please enter your Google API Key (input will be invisible): ")

        if not api_key:
            print("No API key provided. Exiting.")
            sys.exit(1)

        genai.configure(api_key=api_key)
        print("API key configured successfully.")

    except Exception as e:
        print(f"A fatal error occurred while configuring the API: {e}")
        sys.exit(1)

def main() -> None:
    """
    Main function that initializes the Gemini model, starts a chat session,
    and runs the user interaction loop in the terminal.
    """
    configure_api_key()

    generation_config: Dict[str, Any] = {
        "candidate_count": 1,
        "temperature": 0.7,
    }

    safety_settings: Dict[str, Any] = {
        "HARASSMENT": "BLOCK_NONE",
        "HATE": "BLOCK_NONE",
        "SEXUAL": "BLOCK_NONE",
        "DANGEROUS": "BLOCK_NONE",
    }

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-pro',
            generation_config=generation_config,
            safety_settings=safety_settings
        )
    except Exception as e:
        print(f"Error initializing the 'gemini-2.5-pro' model: {e}")
        print("Check if the model name is correct and if your API key is valid.")
        sys.exit(1)

    chat = model.start_chat(history=[])

    # Chatbot intruduction
    print("\n" + "=" * 80)
    print("Welcome to the Gemini Chatbot! Type 'exit' to end the conversation.")
    print("Model: gemini-2.5-pro")
    print("=" * 80)

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            print("\nInput interrupted. Shutting down chat.")
            break
        except KeyboardInterrupt:
            print("\nChat interrupted by the user. Shutting down.")
            break

        if user_input.lower() == 'exit':
            print("Goodbye! The chat has ended.")
            break
        
        if not user_input.strip():
            continue

        try:
            response = chat.send_message(user_input)
            print(f"Gemini: {response.text}\n")
            
        except genai.errors.APIError as api_e:
            print(f"\n[API ERROR] An issue occurred while communicating with Gemini: {api_e}")
            print("Try again or check the status of your API Key.")
        except Exception as e:
            print(f"\n[UNEXPECTED ERROR] An error occurred during the conversation: {e}")

if __name__ == "__main__":
    main()
