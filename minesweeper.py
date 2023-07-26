import random

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

def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))

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

    # If the cell is already revealed, we don't need to do anything
    if type(board[row][col]) is int:
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

def play_game(rows, cols, num_mines):
    board = create_board(rows, cols, num_mines)
    print_board(board)

    while True:
        try:
            row = int(input("Enter the row (0 to {}): ".format(rows - 1)))
            col = int(input("Enter the column (0 to {}): ".format(cols - 1)))
        except ValueError:
            print("Invalid input. Please enter valid row and column numbers.")
            continue

        if not (0 <= row < rows and 0 <= col < cols):
            print("Invalid input. Row and column numbers must be within the board range.")
            continue

        if board[row][col] == '*':
            print("Game Over! You hit a mine.")
            return

        reveal_cell(board, row, col)
        print_board(board)

if __name__ == "__main__":
    rows, cols = 8, 8
    num_mines = 10
    play_game(rows, cols, num_mines)