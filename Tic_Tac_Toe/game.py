import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 38)
game_font = pygame.font.Font('freesansbold.ttf', 80)  # Font for X and O
title_text = font.render('Tic Tac Toe', True, (255, 0, 0))
winner_font = pygame.font.Font('freesansbold.ttf', 50)
button_font = pygame.font.Font('freesansbold.ttf', 32)  # Add font for buttons
winner_text = None
winner_text_rect = None

# Add button variables
restart_button = None
restart_rect = None
exit_button = None
exit_rect = None

# Game variables
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_active = True

def reset_game():
    global board, current_player, game_active, winner_text, winner_text_rect
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_active = True
    winner_text = None
    winner_text_rect = None

def draw_board():
    screen.fill((64, 224, 208))
    pygame.draw.rect(screen, "black", [50, 100, 550, 500], 5)
    pygame.draw.line(screen, "black", [230, 101], [230, 597], 5)
    pygame.draw.line(screen, "black", [420, 101], [420, 597], 5)
    pygame.draw.line(screen, "black", [51, 280], [598, 280], 5)
    pygame.draw.line(screen, "black", [51, 450], [598, 450], 5)
    screen.blit(title_text, (230, 30))

    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                text = game_font.render('X', True, (0, 0, 0))
                screen.blit(text, (120 + col * 190, 150 + row * 170))
            elif board[row][col] == 'O':
                text = game_font.render('O', True, (0, 0, 0))
                screen.blit(text, (120 + col * 190, 150 + row * 170))
    
    # Draw winner text and buttons if game is over
    if winner_text:
        # Create semi-transparent overlay
        overlay = pygame.Surface((650, 650))
        overlay.fill((255, 255, 255))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        # Draw winner text
        screen.blit(winner_text, winner_text_rect)
        # Draw buttons
        screen.blit(restart_button, restart_rect)
        screen.blit(exit_button, exit_rect)

def get_board_position(mouse_pos):
    x, y = mouse_pos
    # Check if click is within game board
    if 50 <= x <= 600 and 100 <= y <= 600:
        # Calculate row and column
        row = (y - 100) // 170
        col = (x - 50) // 190
        if 0 <= row <= 2 and 0 <= col <= 2:
            return row, col
    return None

def check_winner():
    # Check rows
    for row in board:
        if row.count(row[0]) == 3 and row[0] != '':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    
    # Check for draw
    if all(all(cell != '' for cell in row) for row in board):
        return 'Draw'
    
    return None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                pos = get_board_position(pygame.mouse.get_pos())
                if pos:
                    row, col = pos
                    if board[row][col] == '':  # If cell is empty
                        board[row][col] = current_player
                        winner = check_winner()
                        if winner:
                            game_active = False
                            if winner == 'Draw':
                                winner_message = "It's a Draw!"
                            else:
                                winner_message = f"Player {winner} wins!"
                            winner_text = winner_font.render(winner_message, True, (0, 0, 0))
                            winner_text_rect = winner_text.get_rect(center=(325, 325))
                            # Create buttons when game ends
                            restart_button = button_font.render("Restart", True, (0, 100, 0))
                            restart_rect = restart_button.get_rect(center=(225, 400))
                            exit_button = button_font.render("Exit", True, (139, 0, 0))
                            exit_rect = exit_button.get_rect(center=(425, 400))
                        current_player = 'O' if current_player == 'X' else 'X'
            else:  # Game is not active (ended)
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    reset_game()
                elif exit_rect.collidepoint(mouse_pos):
                    running = False

    draw_board()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()