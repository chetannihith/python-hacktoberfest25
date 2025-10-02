import os
import random

# --- Platform-Agnostic Input Handling ---
# Necessary for instant key presses (no 'Enter' required)
try:
    # Windows-specific non-blocking input
    import msvcrt
    def get_key():
        return msvcrt.getch().decode()
except ImportError:
    # Linux/macOS non-blocking input (requires 'pip install getch')
    import sys, tty, termios
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# --- Game Constants ---
MAP_WIDTH = 50
MAP_HEIGHT = 20
WALL = '#'
FLOOR = '.'
PLAYER = '@'
MONSTER = 'M'
TREASURE = 'T'

# --- Game State ---
player_x, player_y = 5, 5
player_hp = 10
player_gold = 0
game_messages = ["Welcome to the ASCII Dungeon!", "Find the treasure, but beware of the Monster (M)."]

# The map is mutable, so we copy it to modify the player/monster positions
GAME_MAP_DATA = [
    list("##################################################"),
    list("#................................................#"),
    list("#..#######################.######################"),
    list("#..#.....................T.......................#"),
    list("#..#.............................................#"),
    list("#..#########################.####################"),
    list(f"#...........................M....................#"),
    list("#..##############################################"),
    list("#..#.............................................#"),
    list("#..#.............................................#"),
    list("#..#.............................................#"),
    list("#..#.............................................#"),
    list("#..##############################################"),
    list("#................................................#"),
    list("##################################################"),
]

# Note: In a real roguelike, MONSTER and TREASURE wouldn't be in the map data 
# but in separate lists of Python objects, making the logic much cleaner.
monsters = [{'x': 25, 'y': 6, 'char': MONSTER, 'hp': 3}]


# --- Core Game Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def add_message(message):
    """Adds a message to the log and keeps it clean."""
    game_messages.append(message)
    # Keep only the last 4 messages visible
    if len(game_messages) > 4:
        game_messages.pop(0)

def render():
    """Draws the entire game state to the terminal."""
    clear_screen()
    
    # 1. Create a dynamic map copy for rendering
    current_map = [row[:] for row in GAME_MAP_DATA]

    # 2. Place entities (Monster and Player)
    for m in monsters:
        current_map[m['y']][m['x']] = m['char']
        
    current_map[player_y][player_x] = PLAYER

    # 3. Draw the map
    for row in current_map:
        print("".join(row))

    # 4. Draw the UI
    print("=" * MAP_WIDTH)
    print(f"HP: {player_hp} | Gold: {player_gold} | POS: ({player_x}, {player_y})")
    print("-" * MAP_WIDTH)
    print("Messages:")
    for msg in game_messages:
        print(f"> {msg}")
    print("=" * MAP_WIDTH)
    print("WASD to move. Q to quit.")


def move_player(dx, dy):
    """Calculates new position, checks for collisions, and processes actions."""
    global player_x, player_y, player_hp, player_gold
    
    new_x = player_x + dx
    new_y = player_y + dy

    # 1. Check bounds and Walls
    if 0 <= new_y < MAP_HEIGHT and 0 <= new_x < MAP_WIDTH:
        target_tile = GAME_MAP_DATA[new_y][new_x]

        if target_tile == WALL:
            add_message("You hit a wall!")
            return # Stop movement

        # 2. Check for Monster
        for m in monsters:
            if m['x'] == new_x and m['y'] == new_y and m['hp'] > 0:
                add_message(f"You attack the Monster!")
                m['hp'] -= 1
                player_hp -= 1 # Monster hits back
                add_message(f"Monster HP: {m['hp']}. Your HP: {player_hp}.")
                if m['hp'] <= 0:
                    add_message("The Monster is defeated!")
                return # Stop movement (combat happens instead)

        # 3. Check for Treasure (Looting)
        if target_tile == TREASURE:
            player_gold += 50
            add_message("You found 50 Gold!")
            # Permanently remove the treasure from the map
            GAME_MAP_DATA[new_y][new_x] = FLOOR

        # 4. Final Move
        player_x, player_y = new_x, new_y
    
def handle_input():
    """Reads player input and triggers the next action."""
    key = get_key().lower()
    
    if key == 'q':
        return False
        
    # WASD Movement
    elif key == 'w':
        move_player(0, -1)
    elif key == 's':
        move_player(0, 1)
    elif key == 'a':
        move_player(-1, 0)
    elif key == 'd':
        move_player(1, 0)
        
    return True

# --- Main Game Loop ---
if __name__ == "__main__":
    running = True
    
    # Wait for the first key press
    render()
    add_message("Press any key to begin your adventure...")
    get_key()
    
    while running:
        # 1. Render the game state
        render()
        
        # 2. Check for game-ending conditions
        if player_hp <= 0:
            add_message("You died!")
            running = False
            continue
        
        # 3. Handle player input and update game state
        running = handle_input()
        
        # 4. Simple Monster AI (Monster is stationary in this example, 
        #    but you would place monster movement/logic here.)
        
    clear_screen()
    print("=" * MAP_WIDTH)
    print(f"GAME OVER. Your final score was {player_gold} gold.")
    print("=" * MAP_WIDTH)