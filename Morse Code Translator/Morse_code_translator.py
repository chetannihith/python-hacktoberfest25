"""
Morse Code Translator

Description: A complete Morse code translator that converts text to Morse code and vice versa.
Supports letters, numbers, punctuation, and includes audio playback functionality.

Time Complexity: O(n) - Processes each character once
Space Complexity: O(1) - Uses constant space for the Morse code dictionary

Features:
- Text to Morse code conversion
- Morse code to text decoding
- Audio playback of Morse code
- Input validation and error handling
- Support for common punctuation
"""

import time
import winsound  # Windows only for beeps
import os

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..', 
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Reverse dictionary for decoding
TEXT_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def text_to_morse(text):
    """
    Convert text to Morse code.
    
    Args:
        text (str): Input text to convert
        
    Returns:
        str: Morse code representation
    """
    morse_code = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        else:
            morse_code.append('?')  # Unknown character
    
    return ' '.join(morse_code)

def morse_to_text(morse_code):
    """
    Convert Morse code to text.
    
    Args:
        morse_code (str): Morse code string
        
    Returns:
        str: Decoded text
    """
    words = morse_code.split(' / ')
    text = []
    
    for word in words:
        letters = word.split(' ')
        decoded_word = []
        for letter in letters:
            if letter in TEXT_DICT:
                decoded_word.append(TEXT_DICT[letter])
            elif letter:  # Non-empty unknown code
                decoded_word.append('?')
        text.append(''.join(decoded_word))
    
    return ' '.join(text)

def play_morse_code(morse_code, dot_duration=100, dash_duration=300):
    """
    Play Morse code as audio beeps (Windows only).
    
    Args:
        morse_code (str): Morse code to play
        dot_duration (int): Duration of dot beep in ms
        dash_duration (int): Duration of dash beep in ms
    """
    frequency = 800  # Beep frequency in Hz
    
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(frequency, dot_duration)
            time.sleep(dot_duration / 1000)
        elif symbol == '-':
            winsound.Beep(frequency, dash_duration)
            time.sleep(dash_duration / 1000)
        elif symbol == ' ':
            time.sleep(dot_duration * 3 / 1000)  # Letter space
        elif symbol == '/':
            time.sleep(dot_duration * 7 / 1000)  # Word space
        else:
            time.sleep(dot_duration / 1000)

def validate_morse_code(morse_code):
    """
    Validate if the input is valid Morse code.
    
    Args:
        morse_code (str): Morse code to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    valid_symbols = {'.', '-', ' ', '/'}
    return all(char in valid_symbols for char in morse_code)

def display_morse_chart():
    """Display Morse code chart for reference."""
    print("\n" + "="*50)
    print("MORSE CODE CHART")
    print("="*50)
    
    # Group by categories
    letters = [(k, v) for k, v in MORSE_CODE_DICT.items() if k.isalpha()]
    numbers = [(k, v) for k, v in MORSE_CODE_DICT.items() if k.isdigit()]
    punctuation = [(k, v) for k, v in MORSE_CODE_DICT.items() 
                  if not k.isalnum() and k != ' ']
    
    print("\nLETTERS:")
    for i in range(0, len(letters), 4):
        row = letters[i:i+4]
        for char, code in row:
            print(f"  {char}: {code:<8}", end="")
        print()
    
    print("\nNUMBERS:")
    for i in range(0, len(numbers), 5):
        row = numbers[i:i+5]
        for char, code in row:
            print(f"  {char}: {code:<8}", end="")
        print()
    
    print("\nPUNCTUATION:")
    for char, code in punctuation:
        print(f"  {char}: {code:<8}", end="")
    print("\n" + "="*50)

def main():
    """Main function to run the Morse Code Translator."""
    print("="*60)
    print("           MORSE CODE TRANSLATOR")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Text to Morse Code")
        print("2. Morse Code to Text")
        print("3. Play Morse Code Audio")
        print("4. Display Morse Code Chart")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            text = input("Enter text to convert to Morse code: ")
            morse_result = text_to_morse(text)
            print(f"\nMorse Code: {morse_result}")
            
        elif choice == '2':
            morse_input = input("Enter Morse code (use '/' for word separation): ")
            if validate_morse_code(morse_input):
                text_result = morse_to_text(morse_input)
                print(f"\nDecoded Text: {text_result}")
            else:
                print("Error: Invalid Morse code characters detected!")
                
        elif choice == '3':
            if os.name != 'nt':
                print("Audio playback is only available on Windows.")
                continue
                
            morse_input = input("Enter Morse code to play: ")
            if validate_morse_code(morse_input):
                print("Playing Morse code... (Press Ctrl+C to stop)")
                try:
                    play_morse_code(morse_input)
                    print("Playback completed!")
                except KeyboardInterrupt:
                    print("\nPlayback stopped by user.")
            else:
                print("Error: Invalid Morse code characters!")
                
        elif choice == '4':
            display_morse_chart()
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please enter 1-5.")

# Test functions
def run_tests():
    """Run comprehensive tests to verify functionality."""
    print("Running tests...")
    
    test_cases = [
        ("SOS", "... --- ..."),
        ("HELLO WORLD", ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."),
        ("123", ".---- ..--- ...--"),
        ("PYTHON", ".--. -.-- - .... --- -."),
    ]
    
    passed = 0
    for text, expected_morse in test_cases:
        result = text_to_morse(text)
        decoded = morse_to_text(expected_morse)
        
        text_match = decoded.upper() == text.upper()
        morse_match = result == expected_morse
        
        if text_match and morse_match:
            print(f"✓ PASS: '{text}' -> '{expected_morse}'")
            passed += 1
        else:
            print(f"✗ FAIL: '{text}'")
            print(f"  Expected Morse: '{expected_morse}'")
            print(f"  Got Morse: '{result}'")
            print(f"  Decoded back: '{decoded}'")
    
    print(f"\nTest Results: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)

if __name__ == "__main__":
    # Run tests first
    if run_tests():
        print("\nAll tests passed! Starting interactive mode...\n")
        main()
    else:
        print("\nSome tests failed! Please check the implementation.")
