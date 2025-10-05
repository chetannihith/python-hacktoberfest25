import random
import time
import os

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_board(player1_pos, player2_pos, snakes, ladders):
    """Draws the game board in the terminal."""
    clear_screen()
    print("--- Snake and Ladder ---")
    
    board_map = {i: f"{i: >4}" for i in range(1, 101)}
    
    for start in snakes:
        board_map[start] = " 🐍 "
    for start in ladders:
        board_map[start] = " 🪜 "
        
    if player1_pos == player2_pos and player1_pos != 0:
        board_map[player1_pos] = "🧛‍♀️🦸‍♂️"
    else:
        if player1_pos != 0:
            board_map[player1_pos] = " 🧛‍♀️ "
        if player2_pos != 0:
            board_map[player2_pos] = " 🦸‍♂️ "

    for i in range(10, 0, -1):
        row = ""
        for j in range(1, 11):
            cell_num = (i - 1) * 10 + j
            if i % 2 == 0:
                cell_num = (i * 10) - (j - 1)
            
            row += f"|{board_map[cell_num]}"
        print(row + "|")
    print("-" * 51)
    print("🧛‍♀️: Player 1 | 🦸‍♂️: Player 2")
    print("🐍: Snake Head | 🪜: Ladder Bottom")
    # Added details for each snake and ladder
    if snakes:
        snake_details = "  ".join([f"🐍 {head}->{tail} (-{head-tail})" for head, tail in sorted(snakes.items())])
        print(snake_details)
    if ladders:
        ladder_details = "  ".join([f"🪜 {bottom}->{top} (+{top-bottom})" for bottom, top in sorted(ladders.items())])
        print(ladder_details)
    print("-" * 51)


def roll_dice():
    """Rolls a six-sided die."""
    return random.randint(1, 6)

def main():
    """Main function to run the Snake and Ladder game."""
    snakes = {
        17: 7, 54: 34, 62: 19, 64: 60,
        87: 24, 93: 73, 95: 75, 99: 78
    }
    ladders = {
        4: 14, 9: 31, 20: 38, 28: 84,
        40: 59, 51: 67, 63: 81, 71: 91
    }
    
    player_positions = {'Player 1': 0, 'Player 2': 0}
    current_player = 'Player 1'
    
    while True:
        draw_board(player_positions['Player 1'], player_positions['Player 2'], snakes, ladders)
        
        print(f"\n{current_player}'s turn.")
        input("Press Enter to roll the dice...")
        
        dice_roll = roll_dice()
        print(f"{current_player} rolled a {dice_roll}.")
        
        current_pos = player_positions[current_player]
        new_pos = current_pos + dice_roll
        
        if new_pos > 100:
            print("Overshot! You need to land exactly on 100.")
            new_pos = current_pos
        elif new_pos in snakes:
            print("Oh no! Landed on a snake.")
            new_pos = snakes[new_pos]
        elif new_pos in ladders:
            print("Wow! Found a ladder.")
            new_pos = ladders[new_pos]
            
        player_positions[current_player] = new_pos
        
        draw_board(player_positions['Player 1'], player_positions['Player 2'], snakes, ladders)
        print(f"\n{current_player} is now at position {new_pos}.")
        time.sleep(2)

        if new_pos == 100:
            print(f"\nCongratulations! {current_player} wins!")
            break
            
        # Switch player
        current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'

if __name__ == "__main__":
    main()
