import random
import os

def clear_screen():
    # Clear the terminal/console screen
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols, num_mines):
    # Create an empty board filled with zeros
    board = [[0 for _ in range(cols)] for _ in range(rows)]

    # Place mines randomly on the board
    mines = random.sample(range(rows * cols), num_mines)
    for mine in mines:
        row = mine // cols
        col = mine % cols
        board[row][col] = '*'

    return board

def print_board(board, reveal_all=False):
    rows, cols = len(board), len(board[0])
    print("\n   " + " ".join(str(i) for i in range(cols)))

    for i in range(rows):
        print(f"{i}  ", end='')
        for j in range(cols):
            cell = board[i][j]
            if cell == 'F':
                print("\033[91mF\033[0m", end=' ')  # Red color for flagged cells
            elif type(cell) is int:
                print("\033[94m{}\033[0m".format(cell), end=' ')  # Blue color for revealed cells
            elif reveal_all and cell == '*':
                print("\033[31m*\033[0m", end=' ')  # Red color for revealed mines
            else:
                print("X", end=' ')  # Covered cells
        print()

def count_adjacent_mines(board, row, col):
    count = 0
    rows, cols = len(board), len(board[0])

    # Define the neighboring positions
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for dr, dc in neighbors:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == '*':
            count += 1

    return count

def reveal_cell(board, row, col):
    rows, cols = len(board), len(board[0])

    if not (0 <= row < rows and 0 <= col < cols):
        return

    if board[row][col] == '*':
        return

    # If the cell is already revealed or flagged, we don't need to do anything
    if type(board[row][col]) is int or board[row][col] == 'F':
        return

    # Count the number of adjacent mines
    count = count_adjacent_mines(board, row, col)
    board[row][col] = count

    # If the cell is empty, recursively reveal its neighbors
    if count == 0:
        reveal_cell(board, row - 1, col - 1)
        reveal_cell(board, row - 1, col)
        reveal_cell(board, row - 1, col + 1)
        reveal_cell(board, row, col - 1)
        reveal_cell(board, row, col + 1)
        reveal_cell(board, row + 1, col - 1)
        reveal_cell(board, row + 1, col)
        reveal_cell(board, row + 1, col + 1)

def flag_cell(board, row, col):
    if board[row][col] == 'F':
        board[row][col] = 'X'
    elif type(board[row][col]) is int:
        print("Cell already revealed. Cannot flag.")
    else:
        board[row][col] = 'F'

def check_win(board):
    for row in board:
        for cell in row:
            if cell != '*' and type(cell) is not int:
                return False
    return True

def play_game(rows, cols, num_mines):
    while True:
        board = create_board(rows, cols, num_mines)
        num_flags = 0
        num_revealed = 0
        print_board(board)

        while True:
            try:
                action = input("Enter 'R' to reveal, 'F' to flag/unflag a cell, or 'Q' to quit: ").upper()
                if action == 'Q':
                    return
                row = int(input("Enter the row (0 to {}): ".format(rows - 1)))
                col = int(input("Enter the column (0 to {}): ".format(cols - 1)))
            except ValueError:
                print("Invalid input. Please enter valid row and column numbers.")
                continue

            if not (0 <= row < rows and 0 <= col < cols):
                print("Invalid input. Row and column numbers must be within the board range.")
                continue

            if action == 'R':
                if board[row][col] == '*':
                    print("Game Over! You hit a mine.")
                    print_board(board, reveal_all=True)
                    break

                if type(board[row][col]) is not int:
                    num_revealed += 1

                reveal_cell(board, row, col)
            elif action == 'F':
                flag_cell(board, row, col)
                if board[row][col] == 'F':
                    num_flags += 1
                elif board[row][col] == 'X':
                    num_flags -= 1
            else:
                print("Invalid action. Please enter 'R', 'F', or 'Q'.")

            if num_revealed == rows * cols - num_mines:
                print("Congratulations! You've won!")
                print_board(board, reveal_all=True)
                break

            clear_screen()
            print("Remaining mines: {}".format(num_mines - num_flags))
            print_board(board)

        if check_win(board):
            print("Congratulations! You've won!")
            return

if __name__ == "__main__":
    rows, cols = 8, 8
    num_mines = 10
    play_game(rows, cols, num_mines)
