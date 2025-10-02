def print_sudoku(board):
    """Print the Sudoku board in a formatted way"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            
            if j == 8:
                print(board[i][j] if board[i][j] != 0 else ".")
            else:
                print(str(board[i][j] if board[i][j] != 0 else ".") + " ", end="")

def find_empty(board):
    """Find an empty cell (represented by 0)"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

def is_valid(board, num, pos):
    """Check if placing num at position pos is valid"""
    # Check row
    for j in range(9):
        if board[pos[0]][j] == num and pos[1] != j:
            return False

    # Check column
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def solve_sudoku(board):
    """Solve Sudoku using backtracking algorithm"""
    find = find_empty(board)
    if not find:
        return True  # Puzzle solved
    
    row, col = find

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0  # Backtrack

    return False

def input_sudoku():
    """Allow user to input a Sudoku puzzle"""
    print("\nEnter your Sudoku puzzle (use 0 for empty cells):")
    print("Enter each row as 9 numbers separated by spaces")
    
    board = []
    for i in range(9):
        while True:
            try:
                row_input = input(f"Row {i+1}: ").strip().split()
                if len(row_input) != 9:
                    print("Please enter exactly 9 numbers")
                    continue
                
                row = [int(num) for num in row_input]
                if any(num < 0 or num > 9 for num in row):
                    print("Numbers must be between 0 and 9")
                    continue
                    
                board.append(row)
                break
            except ValueError:
                print("Please enter valid numbers only")
    
    return board

def main():
    """Main function to run the Sudoku solver"""
    print("=" * 50)
    print("           SUDOKU SOLVER")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Use sample puzzle")
        print("2. Input your own puzzle")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Sample Sudoku puzzle (0 represents empty cells)
            sample_board = [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]
            board = [row[:] for row in sample_board]  # Create a copy
            
        elif choice == "2":
            board = input_sudoku()
            
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
        print("\nOriginal Sudoku:")
        print_sudoku(board)
        
        print("\nSolving...")
        if solve_sudoku(board):
            print("\nSolved Sudoku:")
            print_sudoku(board)
        else:
            print("\nNo solution exists for this Sudoku puzzle!")
        
        # Ask if user wants to continue
        continue_choice = input("\nDo you want to solve another puzzle? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("Goodbye!")
            break

# Additional utility functions
def is_complete(board):
    """Check if the board is completely filled"""
    return all(cell != 0 for row in board for cell in row)

def validate_solution(board):
    """Validate if the solved board is correct"""
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == 0:
                return False
            # Temporarily remove the number to check validity
            board[i][j] = 0
            if not is_valid(board, num, (i, j)):
                board[i][j] = num
                return False
            board[i][j] = num
    return True

if __name__ == "__main__":
    main()
