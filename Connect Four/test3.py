import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Define constants
BLUE = '#0000FF'
BLACK = '#000000'
RED = '#FF0000'
YELLOW = '#FFFF00'

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

# Function to create the game board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Function to drop a piece on the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if dropping a piece in the column is valid
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Get the next open row in the chosen column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to print the board (not used in streamlit directly)
def print_board(board):
    print(np.flip(board, 0))

# Check for a winning move
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# Evaluate a window of four cells for scoring
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Score the position by evaluating the entire board
def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    ## Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Check if the board is a terminal node
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# Minimax algorithm to simulate the AI opponent
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Get a list of valid locations
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Choose the best move for the AI
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

# Draw the Connect 4 board using Matplotlib
def draw_board(board):
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_facecolor(BLUE)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                circle = plt.Circle((c, ROW_COUNT - 1 - r), 0.45, color=RED, ec="black")
            elif board[r][c] == AI_PIECE:
                circle = plt.Circle((c, ROW_COUNT - 1 - r), 0.45, color=YELLOW, ec="black")
            else:
                circle = plt.Circle((c, ROW_COUNT - 1 - r), 0.45, color=BLACK, ec="black")
            ax.add_artist(circle)

    plt.xlim(-0.5, COLUMN_COUNT - 0.5)
    plt.ylim(-0.5, ROW_COUNT - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    st.pyplot(fig)

# Main game loop
if 'board' not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.game_over = False
    st.session_state.turn = random.randint(PLAYER, AI)

board = st.session_state.board

# Display the board
draw_board(board)

# Check for game over
if st.session_state.game_over:
    st.write("Game Over!")
    if st.button("Play again!"):
        st.session_state.board = create_board()
        st.session_state.game_over = False
        st.session_state.turn = random.randint(PLAYER, AI)
        st.experimental_rerun()

# Player turn
if not st.session_state.game_over:
    if st.session_state.turn == PLAYER:
        col = st.number_input("Select a column (0-6):", min_value=0, max_value=COLUMN_COUNT-1, step=1)
        if st.button("Drop Piece"):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    st.write("Player 1 wins!!")
                    st.session_state.game_over = True

                st.session_state.turn += 1
                st.session_state.turn %= 2

                draw_board(board)

    # AI turn
    if st.session_state.turn == AI and not st.session_state.game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                st.write("Player 2 (AI) wins!!")
                st.session_state.game_over = True

            st.session_state.turn += 1
            st.session_state.turn %= 2

            draw_board(board)

def main():
    # Kiểm tra và khởi tạo bảng nếu chưa có
    if 'board' not in st.session_state:
        st.session_state.board = create_board()
        st.session_state.game_over = False
        st.session_state.turn = random.randint(PLAYER, AI)

    board = st.session_state.board

    if st.session_state.game_over:
        st.write("Game Over!")
        if st.button("Play Again"):
            st.session_state.board = create_board()
            st.session_state.game_over = False
            st.session_state.turn = random.randint(PLAYER, AI)
            st.experimental_rerun()

    if not st.session_state.game_over:
        cols = st.columns(COLUMN_COUNT)
        move_made = False
        for col in range(COLUMN_COUNT):
            if cols[col].button(f"Column {col}"):
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE if st.session_state.turn == PLAYER else AI_PIECE)
                    move_made = True
                    if winning_move(board, PLAYER_PIECE if st.session_state.turn == PLAYER else AI_PIECE):
                        st.write(f"{'Player' if st.session_state.turn == PLAYER else 'AI'} wins!")
                        st.session_state.game_over = True
                    st.session_state.turn = AI if st.session_state.turn == PLAYER else PLAYER
                    break

        if move_made:
            draw_board(board)
            st.experimental_rerun()
        else:
            draw_board(board)

main()