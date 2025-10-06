import random
import sys

# Define color codes for terminal output
class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GRAY = '\033[90m'
    ENDC = '\033[0m'

# A small, curated list of 5-letter words
# For a full version, you would load this from a large text file.
WORD_LIST = [
    "apple", "beach", "brain", "bread", "chair", "chest", "chord", "click",
    "clock", "cloud", "dance", "diary", "dream", "dress", "drink", "earth",
    "flute", "fruit", "ghost", "grape", "green", "happy", "heart", "house",
    "human", "juice", "light", "lunch", "magic", "money", "music", "night",
    "ocean", "party", "pizza", "plant", "plane", "queen", "quiet", "river",
    "robot", "rocky", "round", "sadly", "scale", "shark", "shiny", "shirt",
    "short", "skill", "sleep", "smile", "sound", "space", "stare", "storm",
    "story", "sugar", "sunny", "sword", "table", "thank", "theme", "thing",
    "thumb", "tiger", "torch", "train", "trend", "truth", "twice", "uncle",
    "unity", "value", "video", "visit", "voice", "waste", "watch", "water",
    "while", "white", "woman", "world", "youth", "zebra"
]

def get_random_word():
    """Selects a random word from the word list."""
    return random.choice(WORD_LIST).upper()

def print_feedback(guess, feedback):
    """Prints the guessed word with color-coded feedback."""
    colored_guess = []
    for i in range(len(guess)):
        if feedback[i] == 'G':
            colored_guess.append(f"{colors.GREEN}{guess[i]}{colors.ENDC}")
        elif feedback[i] == 'Y':
            colored_guess.append(f"{colors.YELLOW}{guess[i]}{colors.ENDC}")
        else:
            colored_guess.append(f"{colors.GRAY}{guess[i]}{colors.ENDC}")
    print(" ".join(colored_guess))

def get_feedback(guess, secret_word):
    """
    Compares the guess to the secret word and returns feedback.
    'G' for Green (correct letter, correct position)
    'Y' for Yellow (correct letter, wrong position)
    '-' for Gray (letter not in word)
    """
    guess = guess.upper()
    feedback = [''] * 5
    secret_word_list = list(secret_word)
    guess_list = list(guess)

    # First pass for correct letters in the correct position (Green)
    for i in range(5):
        if guess_list[i] == secret_word_list[i]:
            feedback[i] = 'G'
            # Mark letters as used to handle duplicates correctly
            secret_word_list[i] = None
            guess_list[i] = None

    # Second pass for correct letters in the wrong position (Yellow)
    for i in range(5):
        # Skip letters that were already marked Green
        if guess_list[i] is not None:
            if guess_list[i] in secret_word_list:
                feedback[i] = 'Y'
                # Mark the letter in the secret word as used
                secret_word_list[secret_word_list.index(guess_list[i])] = None
            else:
                feedback[i] = '-' # Gray

    return "".join(feedback)

def play_wordle():
    """Main function to run the Wordle game."""
    secret_word = get_random_word()
    attempts = 6
    guesses = []

    print("--- Welcome to Python Wordle! ---")
    print("You have 6 attempts to guess the 5-letter word.")
    
    # Uncomment the line below for debugging/testing
    # print(f"Secret word is: {secret_word}")

    while attempts > 0:
        print(f"\nAttempts remaining: {attempts}")
        
        try:
            guess = input("Enter your guess: ").strip().lower()
        except KeyboardInterrupt:
            print("\nExiting game. Goodbye!")
            sys.exit()

        # --- Input Validation ---
        if len(guess) != 5:
            print("Invalid input. Please enter a 5-letter word.")
            continue
        if not guess.isalpha():
            print("Invalid input. Please use only letters.")
            continue
        
        # Add guess to history
        guesses.append(guess.upper())
        
        # Get and display feedback for the guess
        feedback = get_feedback(guess, secret_word)
        print_feedback(guess.upper(), feedback)

        # --- Win/Loss Conditions ---
        if guess.upper() == secret_word:
            print(f"\n{colors.GREEN}Congratulations! You guessed the word: {secret_word}{colors.ENDC}")
            return
        
        attempts -= 1

    # If the loop finishes, the player has lost
    print(f"\nGame over! The word was: {colors.YELLOW}{secret_word}{colors.ENDC}")


if __name__ == "__main__":
    play_wordle()