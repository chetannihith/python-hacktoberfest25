def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-"*5)

def tic_tac_toe():
    board = [[" "]*3 for _ in range(3)]
    player = "X"

    def check_winner():
        # Rows, columns, diagonals
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != " ":
                return True
            if board[0][i] == board[1][i] == board[2][i] != " ":
                return True
        if board[0][0] == board[1][1] == board[2][2] != " ":
            return True
        if board[0][2] == board[1][1] == board[2][0] != " ":
            return True
        return False

    for turn in range(9):
        print_board(board)
        try:
            row = int(input(f"Player {player}, enter row (0-2): "))
            col = int(input(f"Player {player}, enter column (0-2): "))
            if board[row][col] != " ":
                print("Cell already taken. Try again.")
                continue
            board[row][col] = player
        except (ValueError, IndexError):
            print("Invalid input. Try again.")
            continue

        if check_winner():
            print_board(board)
            print(f"Player {player} wins!")
            return

        player = "O" if player == "X" else "X"

    print_board(board)
    print("It's a tie!")

if __name__ == "__main__":
    tic_tac_toe()
