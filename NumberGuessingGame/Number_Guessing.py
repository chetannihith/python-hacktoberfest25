import random
print("Welcome to the Number Guessing Game!")
print("you have to enter a range")
while True: 
    a=int(input("Enter the lower bound: "))
    b=int(input("Enter the upper bound: "))
    if a >= b:
        print("Invalid range. The lower bound must be less than the upper bound.")
        continue
    if a < 0 or b < 0:
        print("Invalid range. Both bounds must be non-negative.")
        continue
    if a == b:
        print("Invalid range. The lower and upper bounds must be different.")
        continue
    if b-a<2:
        print("Invalid range. The difference between the bounds must be at least 2.")
        continue
    break
n=random.randint(a, b)
if b-a>500:
    print("That's a huge range! do you want any hints?")
    confirm=input("Enter \"y\" to confirm or \"n\" to cancel: ")
    if confirm != "y" and confirm != "Y":
        print("Okay, let's try again.")
    else:
        print("Okay, I will give you hints.")
        e=n+70
        f=n-70
        print(f"The number is between {e} and {f}.")
print(f"I have selected a number between {a} and {b}. Try to guess it!")
print(" In how many guess do you think you can guess the number?")
choice=input("if you want to choose a number of guesses, enter \"y\", otherwise enter \"n\" to generate a random number of guesses: ")
if choice=="y"or choice=="Y":
    while True:
        max_guesses=int(input("Enter the maximum number of guesses: "))
        if max_guesses < 1:
             print("Invalid input. Please enter a positive integer.")
             continue
        if max_guesses > 30:
             print("That's a lot of guesses! Are you sure you want to do that?")
             confirm=input("Enter \"y\" to confirm or \"n\" to cancel: ")
             if confirm != "y" and confirm != "Y":
                 print("Okay, let's try again.")
                 continue
        break
else:
    max_guesses=random.randint(1, 20)
c=0
print(f"You have {max_guesses} guesses to find the number.")
while c < max_guesses:
    guess=int(input("Enter your guess: "))
    if guess==n:
        print("Congratulations! You guessed the number.")
        c += 1
        print(f"You guessed it in {c} tries.")
        break
    elif guess<n:
        print("Your guess is too low. Try again.")
        c += 1
    else:
        print("Your guess is too high. Try again.")
        c += 1
    if max_guesses - c <= 2:
        print("you have few guesses left.")
        x=input("Do you want a hint? Enter \"y\" for yes or \"n\" for no: ")
        if x == "y" or x=="Y":
            if n - 10 > a and n + 10 < b:
                print(f"The number is between {n - 10} and {n + 10}.")
            elif n - 10 <= a:
                print(f"The number is greater than {n - 10}.")
            elif n + 10 >= b:
                print(f"The number is less than {n + 10}.")
            else:
                if n%2==0:
                    print("The number is even.")
                else:
                    print("The number is odd.")
            if n - 10 > a:
                print(f"The number is greater than {n - 10}.")
            if n + 10 < b:
                print(f"The number is less than {n + 10}.")
if c > max_guesses and guess != n:
    print(f"Sorry, you've used all {max_guesses} guesses. The number was {n}.")