import random
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Word categories with different difficulty levels
word_categories = {
    "easy": {
        "fruits": ["apple", "banana", "orange", "grape", "mango"],
        "animals": ["cat", "dog", "bird", "fish", "duck"],
        "colors": ["red", "blue", "green", "pink", "black"]
    },
    "medium": {
        "countries": ["france", "spain", "japan", "brazil", "india"],
        "sports": ["soccer", "tennis", "cricket", "hockey", "rugby"],
        "food": ["pizza", "pasta", "sushi", "burger", "salad"]
    },
    "hard": {
        "science": ["quantum", "molecule", "gravity", "electron", "neutron"],
        "technology": ["computer", "internet", "software", "database", "network"],
        "space": ["galaxy", "planet", "asteroid", "nebula", "comet"]
    }
}

HANGMANPICS = ['''  +---+
  |   |
      |
      |
      |
      |
=========''', '''  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

def select_difficulty():
    while True:
        print(Fore.CYAN + "\nSelect difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard" + Style.RESET_ALL)
        choice = input("Enter your choice (1-3): ")
        if choice in ["1", "2", "3"]:
            return {"1": "easy", "2": "medium", "3": "hard"}[choice]

def select_category(difficulty):
    categories = list(word_categories[difficulty].keys())
    while True:
        print(Fore.CYAN + "\nSelect a category:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.title()}")
        print(Style.RESET_ALL)
        choice = input(f"Enter your choice (1-{len(categories)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]

def get_word(difficulty, category):
    return random.choice(word_categories[difficulty][category])

def display_game_state(hangman, word_display, guessed_letters, score):
    print("\n" + Fore.YELLOW + hangman + Style.RESET_ALL)
    print(Fore.GREEN + f"Word: {' '.join(word_display)}" + Style.RESET_ALL)
    print(Fore.BLUE + f"Guessed letters: {', '.join(sorted(guessed_letters))}" + Style.RESET_ALL)
    print(Fore.MAGENTA + f"Score: {score}" + Style.RESET_ALL)

def play_game():
    difficulty = select_difficulty()
    category = select_category(difficulty)
    chosen_word = get_word(difficulty, category)
    word_display = ["_" for _ in chosen_word]
    guessed_letters = set()
    lives = 6
    score = 0
    
    print(Fore.CYAN + f"\nCategory: {category.title()}" + Style.RESET_ALL)
    
    while lives > 0:
        display_game_state(HANGMANPICS[6 - lives], word_display, guessed_letters, score)
        
        guess = input("\nGuess a letter: ").lower()
        if not guess.isalpha() or len(guess) != 1:
            print(Fore.RED + "Please enter a single letter!" + Style.RESET_ALL)
            continue
        
        if guess in guessed_letters:
            print(Fore.RED + "You already guessed that letter!" + Style.RESET_ALL)
            continue
        
        guessed_letters.add(guess)
        
        if guess in chosen_word:
            correct_count = 0
            for i, letter in enumerate(chosen_word):
                if letter == guess:
                    word_display[i] = guess
                    correct_count += 1
            score += correct_count * 10
            print(Fore.GREEN + f"Correct! +{correct_count * 10} points" + Style.RESET_ALL)
        else:
            lives -= 1
            print(Fore.RED + f"Wrong! {lives} lives remaining" + Style.RESET_ALL)
        
        if "_" not in word_display:
            display_game_state(HANGMANPICS[6 - lives], word_display, guessed_letters, score)
            print(Fore.GREEN + f"\nCongratulations! You won with a score of {score}!" + Style.RESET_ALL)
            return True
    
    display_game_state(HANGMANPICS[6], word_display, guessed_letters, score)
    print(Fore.RED + f"\nGame Over! The word was '{chosen_word}'" + Style.RESET_ALL)
    return False

def main():
    print(Fore.YELLOW + "\nWelcome to Hangman!" + Style.RESET_ALL)
    
    while True:
        play_game()
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print(Fore.YELLOW + "\nThanks for playing!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()