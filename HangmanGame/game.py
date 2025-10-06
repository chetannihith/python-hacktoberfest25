import random
from colorama import Fore

from hangman_pics import HANGMAN_PICS
from words import WORD_CATEGORIES

def make_guess(guess: str, chosen_word: str, blank_list: list[str]) -> bool:
    correct = False
    for i, letter in enumerate(chosen_word):
        if guess == letter:
            blank_list[i] = guess
            correct = True
    if not correct:
        print(Fore.RED + f"There is no '{guess}', sorry.")
    return correct

def play_game() -> None:
    print(Fore.CYAN + "Welcome to Hangman!")
    print(Fore.CYAN + "Available categories:")
    print(", ".join(WORD_CATEGORIES.keys()))

    while True:
        category = input(Fore.YELLOW + "\nChoose a category: ").lower().strip()
        if category in WORD_CATEGORIES:
            break
        print(Fore.RED + "Invalid category! Try again.")

    while True:
        difficulty = input(Fore.YELLOW + "Choose difficulty (easy / medium / hard): ").lower().strip()
        if difficulty in ["easy", "medium", "hard"]:
            break
        print(Fore.RED + "Invalid difficulty! Try again.")

    chosen_word = random.choice(WORD_CATEGORIES[category][difficulty])
    blank_list = ["_"] * len(chosen_word)
    guessed_letters = []
    attempts = 0
    score = 0

    print(Fore.GREEN + f"The word has {len(chosen_word)} letters.")
    print(HANGMAN_PICS[attempts])
    print(" ".join(blank_list))

    while attempts < len(HANGMAN_PICS) - 1:
        guess = input(Fore.YELLOW + "\nMake a guess: ").lower().strip()

        if not guess.isalpha() or len(guess) != 1:
            print(Fore.RED + "Enter a single letter (a-z).")
            continue

        if guess in guessed_letters:
            print(Fore.RED + "You already guessed that letter!")
            continue

        guessed_letters.append(guess)
        correct_guess = make_guess(guess, chosen_word, blank_list)

        if correct_guess:
            score += 10
            print(Fore.GREEN + "Correct!")
        else:
            attempts += 1
            score -= 5

        print(HANGMAN_PICS[attempts])
        print("Word: " + Fore.CYAN + " ".join(blank_list))
        print(Fore.MAGENTA + f"Guessed letters: {', '.join(guessed_letters)}")
        print(Fore.BLUE + f"Score: {score}")

        if "_" not in blank_list:
            print(Fore.GREEN + "\nYOU WIN!")
            print(Fore.CYAN + f"The word was: {chosen_word}")
            print(Fore.GREEN + f"Final Score: {score}")
            break
    else:
        print(Fore.RED + "\nGAME OVER.")
        print(Fore.CYAN + f"The word was: {chosen_word}")
        print(Fore.RED + f"Final Score: {score}")