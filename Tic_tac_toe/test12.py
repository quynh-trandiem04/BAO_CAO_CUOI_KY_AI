import streamlit as st

# Define the initial state and game functions
if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.player = 'X'

def check_win():
    board = st.session_state.board
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]
    for a, b, c in lines:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def check_draw():
    return ' ' not in st.session_state.board

def make_move(position):
    if st.session_state.board[position] == ' ':
        st.session_state.board[position] = st.session_state.player
        winner = check_win()
        if winner:
            st.success(f"Game Over! {winner} wins!")
        elif check_draw():
            st.info("Game Over! It's a draw!")
        else:
            st.session_state.player = 'O' if st.session_state.player == 'X' else 'X'

def reset_game():
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.player = 'X'

# Display the Tic Tac Toe board
st.markdown('<h1 style="font-size: 20px; color: #F7418F;">Tic Tac Toe</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="font-size: 15px; color: #F7418F;">Người đấu với người</h2>', unsafe_allow_html=True)
button_style = "color: white; background-color: #FF6347; border: 2px solid #4682B4; border-radius: 5px; font-size: 18px;"
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        index = 3 * i + j
        cols[j].button(st.session_state.board[index], key=index, on_click=make_move, args=(index,), use_container_width=True)

st.button("Reset Game", on_click=reset_game)

