import random
import time
import os

lose_game = [
    "Oops! That didn't go well.",
    "Better luck next time!",
    "The computer strikes again!",
    "You got outplayed!",
    "That was embarrassing... for you.",
]

options = ("rock", "paper", "scissors")
wins = 0
losses = 0
ties = 0
tries = 0
running = True

while running:
    player = None
    computer = random.choice(options)

    while player not in options:
        player = input("Pick a choice: rock, paper, scissors? ").lower()

    time.sleep(0.5)
    print("Rock...")
    time.sleep(0.5)
    print("Paper...")
    time.sleep(0.5)
    print("Scissors...")
    time.sleep(0.5)
    print("Shoot!")
    time.sleep(0.5)

    print(f"computer: {computer}")
    print(f"player: {player}")

    if player == computer:
        print("It's a tie")
        ties += 1
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        print("yayy! you win")
        wins += 1
    else:
        print("Oh no! you lose")
        print(random.choice(lose_game))
        losses += 1

    tries += 1
    print("Do you want to play again? (y/n)")
    answer = input().lower()
    if answer != "y":
        running = False

print(f"Final Score: Wins: {wins}, Losses: {losses}, Ties: {ties}, Tries: {tries}")
if wins > losses:
    print("You are the winner! Congratulations!")
else:
    print(random.choice(lose_game))
print("Thank you for playing!")