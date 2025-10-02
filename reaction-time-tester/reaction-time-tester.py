import time
import random

print("=== Reaction Time Tester ===")
print("When you see 'GO!', press Enter as fast as you can.")
input("Press Enter to start...")

while True:
    wait_time = random.uniform(2, 5)
    print("Get ready...")
    time.sleep(wait_time)
    print("GO!")
    start_time = time.time()
    input()
    reaction_time = time.time() - start_time
    print(f"Your reaction time: {reaction_time:.3f} seconds")
    
    again = input("Try again? (y/n): ").lower()
    if again != 'y':
        print("Thanks for playing!")
        break
