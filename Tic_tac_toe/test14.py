import streamlit as st
import time

if 'game_over' not in st.session_state:
    st.session_state.game_over = False

if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False

def check_win():
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]
    board = st.session_state.board
    for a, b, c in lines:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def check_draw():
    return ' ' not in st.session_state.board

def reset_game():
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False

def player_move(index):
    if st.session_state.board[index] == ' ' and not st.session_state.game_over:
        st.session_state.board[index] = 'X'
        winner = check_win()
        if winner:
            st.session_state.game_over = True
            st.success(f"Game Over! {winner} wins!")
        elif check_draw():
            st.session_state.game_over = True
            st.info("Game Over! It's a draw!")
        else:
            st.session_state.current_player = 'O'
            ai_move()

def ai_move():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if st.session_state.board[i] == ' ':
            st.session_state.board[i] = 'O'
            score = minimax(0, False)
            st.session_state.board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        st.session_state.board[best_move] = 'O'
        winner = check_win()
        if winner:
            st.session_state.game_over = True
            st.success(f"Game Over! {winner} wins!")
        elif check_draw():
            st.session_state.game_over = True
            st.info("Game Over! It's a draw!")
    st.session_state.current_player = 'X'

def minimax(depth, is_maximizing):
    if check_win():
        return 1 if check_win() == 'O' else -1
    elif check_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if st.session_state.board[i] == ' ':
                st.session_state.board[i] = 'O'
                score = minimax(depth + 1, False)
                st.session_state.board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if st.session_state.board[i] == ' ':
                st.session_state.board[i] = 'X'
                score = minimax(depth + 1, True)
                st.session_state.board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Streamlit interface to display the board and handle interaction
st.write('<h1 style="font-size: 20px; color: #F7418F;">Tic Toc Toe</h1>', unsafe_allow_html=True)
st.write('<h2 style="font-size: 15px; color: #F7418F;">Máy đấu với người</h2>', unsafe_allow_html=True)
if not st.session_state.game_over:
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            index = i + j
            cols[j].button(st.session_state.board[index], key=index, on_click=player_move, args=(index,))

if st.session_state.game_over:
    if st.button("Play Again"):
        reset_game()
