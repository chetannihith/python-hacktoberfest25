import random

def coin_toss():
    print("Coin Toss Simulator")
    while True:
        input("Press Enter to toss the coin...")
        result = random.choice(["Heads", "Tails"])
        print(f"It's {result}!")
        again = input("Toss again? (y/n): ").lower()
        if again != "y":
            break

if __name__ == "__main__":
    coin_toss()
