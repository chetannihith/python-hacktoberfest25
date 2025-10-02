import random

def word_scramble():
    words = ["python", "hacktober", "developer", "programming", "challenge"]
    word = random.choice(words)
    scrambled = "".join(random.sample(word, len(word)))
    
    print("Welcome to Word Scramble!")
    print(f"Scrambled word: {scrambled}")

    while True:
        guess = input("Your guess: ").lower()
        if guess == word:
            print("Correct! You guessed the word.")
            break
        else:
            print("Incorrect. Try again!")

if __name__ == "__main__":
    word_scramble()
