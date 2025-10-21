import random

def play_game():
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("=" * 50)
    print("Welcome to the Number Guessing Game!")
    print("=" * 50)
    print(f"I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to guess it.")
    print()

    while attempts < max_attempts:
        try:

            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} - Enter your guess: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100!")
                continue

            if guess < secret_number:
                print("📈 Too low! Go HIGHER!")
            elif guess > secret_number:
                print("📉 Too high! Go LOWER!")
            else:
                print()
                print("=" * 50)
                print(f"🎉 Congratulations! You guessed it!")
                print(f"The number was {secret_number}")
                print(f"You won in {attempts} attempts!")
                print("=" * 50)
                return

            print()

        except ValueError:
            print("Invalid input! Please enter a valid number.")
            print()

    print()
    print("=" * 50)
    print(f"😞 Game Over! You've used all {max_attempts} attempts.")
    print(f"The secret number was {secret_number}")
    print("=" * 50)

def main():
    while True:
        play_game()

        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again not in ['yes', 'y']:
            print("\nThanks for playing! Goodbye! 👋")
            break
        print("\n")

if __name__ == "__main__":
    main()
