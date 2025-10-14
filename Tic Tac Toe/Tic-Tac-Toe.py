import random
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def board(spaces):
    clear_screen()
    print(f" {spaces[0]} | {spaces[1]} | {spaces[2]} ")
    print("___|___|___")
    print("   |   |   ")
    print(f" {spaces[3]} | {spaces[4]} | {spaces[5]} ")
    print("___|___|___")
    print("   |   |   ")
    print(f" {spaces[6]} | {spaces[7]} | {spaces[8]} ")
    print()

def player_move(spaces, player_symbol, player_name):
    while True:
        try:
            move = int(input(f"{player_name} ({player_symbol}), enter a number (1-9): "))
            if 1 <= move <= 9:
                if spaces[move - 1] == ' ':
                    spaces[move - 1] = player_symbol
                    break
                else:
                    print("That space is already taken. Try again.")
            else:
                print("Invalid input. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def computer_move(spaces, computer_symbol):
    print("Computer is thinking...")
    time.sleep(1)
    
    empty_indices = [i for i, space in enumerate(spaces) if space == ' ']
    if empty_indices:
        move = random.choice(empty_indices)
        spaces[move] = computer_symbol

def check_win(spaces):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]          
    ]
    for condition in win_conditions:
        if spaces[condition[0]] == spaces[condition[1]] == spaces[condition[2]] != ' ':
            return spaces[condition[0]]
    return None

def check_tie(spaces):
    return ' ' not in spaces

def play_game():
    while True:
        spaces = [' '] * 9
        player1_symbol = 'X'
        player2_symbol = 'O'
        computer_symbol = 'O'
        
        choice = ''
        while choice not in ['1', '2']:
            clear_screen()
            print("Welcome to Tic-Tac-Toe!")
            choice = input("Press 1 to play with another player.\nPress 2 to play with the computer.\nEnter your choice: ")

        if choice == '1':
            current_player_symbol = player1_symbol
            current_player_name = "Player 1"
            while True:
                board(spaces)
                player_move(spaces, current_player_symbol, current_player_name)
                
                winner = check_win(spaces)
                if winner:
                    board(spaces)
                    print(f"Congratulations {current_player_name}, you won!")
                    break
                
                if check_tie(spaces):
                    board(spaces)
                    print("It's a tie!")
                    break

                if current_player_symbol == player1_symbol:
                    current_player_symbol = player2_symbol
                    current_player_name = "Player 2"
                else:
                    current_player_symbol = player1_symbol
                    current_player_name = "Player 1"

        else:
            while True:
                board(spaces)
                player_move(spaces, player1_symbol, "Player 1")

                winner = check_win(spaces)
                if winner:
                    board(spaces)
                    print("Congratulations, you won!")
                    break
                
                if check_tie(spaces):
                    board(spaces)
                    print("It's a tie!")
                    break

                board(spaces)
                computer_move(spaces, computer_symbol)

                winner = check_win(spaces)
                if winner:
                    board(spaces)
                    print("You lose! The computer has won.")
                    break

                if check_tie(spaces):
                    board(spaces)
                    print("It's a tie!")
                    break

        play_again = input("Do you want to play again? (Y/N): ").upper()
        if play_again != 'Y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
