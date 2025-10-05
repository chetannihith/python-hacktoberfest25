from game import play_game
from colorama import Fore, init

init(autoreset=True)

def main() -> None:
    while True:
        play_game()
        replay = input(Fore.YELLOW + "\nPlay again? (y/n): ").lower().strip()
        if replay != "y":
            print(Fore.CYAN + "\nThanks for playing Hangman!")
            break

if __name__ == "__main__":
    main()
