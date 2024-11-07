import streamlit as st
import numpy as np
import random
import pandas as pd

def color_value(value):
    if value == 2:
        return 'background-color: #eee4da'
    elif value == 4:
        return 'background-color: #ede0c8'
    elif value == 8:
        return 'background-color: #f2b179'
    elif value == 16:
        return 'background-color: #f59563'
    elif value == 32:
        return 'background-color: #f67c5f'
    elif value == 64:
        return 'background-color: #f65e3b'
    elif value == 128:
        return 'background-color: #edcf72'
    elif value == 256:
        return 'background-color: #edcc61'
    elif value == 512:
        return 'background-color: #edc850'
    elif value == 1024:
        return 'background-color: #edc53f'
    elif value == 2048:
        return 'background-color: #edc22e'
    else:
        return 'background-color: #cdc1b4'  # For empty cells or other values
    
def display_board(board):
    board_df = pd.DataFrame(board)
    styled_board = board_df.style.applymap(color_value).format(None, na_rep="")
    st.write(styled_board, unsafe_allow_html=True)

def main():
    if 'board' not in st.session_state or st.button('Reset Game'):
        st.session_state.board = initialize_game()

    game_board = st.session_state.board
    display_board(game_board)

    if not can_move(game_board):
        st.error("Game Over! No moves left.")
        return

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button('Left'):
            game_board, moved = move_left(game_board)
            if moved:
                add_new_tile(game_board)

    with col2:
        if st.button('Right'):
            game_board, moved = move_right(game_board)
            if moved:
                add_new_tile(game_board)

    with col3:
        if st.button('Up'):
            game_board, moved = move_up(game_board)
            if moved:
                add_new_tile(game_board)

    with col4:
        if st.button('Down'):
            game_board, moved = move_down(game_board)
            if moved:
                add_new_tile(game_board)

    with col5:
        if st.button('AI Move'):
            best_move, best_move_name, _ = find_best_move(game_board)
            if best_move:
                game_board, moved = best_move(game_board)
                if moved:
                    add_new_tile(game_board)
                    st.write(f"AI chose to move {best_move_name}")

    with col6:
        if st.button('Reset'):
            st.session_state.board = initialize_game()
            game_board = st.session_state.board

    st.session_state.board = game_board
    display_board(game_board)



def initialize_game() -> np.ndarray:
    board = np.zeros((4, 4), dtype=int)
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board: np.ndarray) -> None:
    empty_positions = list(zip(*np.where(board == 0)))
    if empty_positions:
        i, j = random.choice(empty_positions)
        board[i, j] = 2

def compress(board: np.ndarray) -> tuple[np.ndarray, bool]:
    new_board = np.zeros_like(board)
    moved = False
    for i in range(4):
        pos = 0
        for j in range(4):
            if board[i][j] != 0:
                if pos != j:
                    moved = True
                new_board[i][pos] = board[i][j]
                pos += 1
    return new_board, moved

def merge(board: np.ndarray) -> tuple[np.ndarray, bool]:
    moved = False
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j + 1] = 0
                moved = True
    return board, moved

def move_left(board: np.ndarray) -> tuple[np.ndarray, bool]:
    board, moved1 = compress(board)
    board, moved2 = merge(board)
    board, moved3 = compress(board)
    moved = moved1 or moved2 or moved3
    return board, moved

def move_right(board: np.ndarray) -> tuple[np.ndarray, bool]:
    board = np.fliplr(board)
    board, moved = move_left(board)
    board = np.fliplr(board)
    return board, moved

def move_up(board: np.ndarray) -> tuple[np.ndarray, bool]:
    board = np.transpose(board)
    board, moved = move_left(board)
    board = np.transpose(board)
    return board, moved

def move_down(board: np.ndarray) -> tuple[np.ndarray, bool]:
    board = np.transpose(board)
    board, moved = move_right(board)
    board = np.transpose(board)
    return board, moved

def can_move(board: np.ndarray) -> bool:
    if np.any(board == 0):
        return True

    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1]:
                return True
            if board[j][i] == board[j + 1][i]:
                return True

    return False

def score(board: np.ndarray) -> int:
    return np.max(board)

def minimax(
    board: np.ndarray,
    depth: int,
    alpha: int,
    beta: int,
    is_maximizing: bool,
) -> tuple[int, callable]:
    """
    Minimax algorithm with alpha-beta pruning.

    :param board: The current game board
    :param depth: The current search depth
    :param alpha: The best score for the maximizing player
    :param beta: The best score for the minimizing player
    :param is_maximizing: Whether the current player is maximizing (True) or minimizing (False)
    :return: The best score and move for the current player
    """
    if depth == 0 or not can_move(board):
        return score(board), None

    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        for move in [move_left, move_right, move_up, move_down]:
            new_board, moved = move(board)
            if moved:
                eval, _ = minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in [move_left, move_right, move_up, move_down]:
            new_board, moved = move(board)
            if moved:
                eval, _ = minimax(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval, best_move

def find_best_move(board: np.ndarray) -> tuple[callable, str, int]:
    """
    Find the best move for the current game board.

    :param board: The current game board
    :return: The best move, move name, and score
    """
    best_score = float('-inf')
    best_move = None
    best_move_name = None
    alpha, beta = float('-inf'), float('inf')
    moves = [move_left, move_right, move_up, move_down]
    move_names = ['Left', 'Right', 'Up', 'Down']

    for move, name in zip(moves, move_names):
        new_board, moved = move(board)
        if moved:
            score, _ = minimax(new_board, 3, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = move
                best_move_name = name
            alpha = max(alpha, score)
    return best_move, best_move_name, best_score

if __name__ == "__main__":
    main()