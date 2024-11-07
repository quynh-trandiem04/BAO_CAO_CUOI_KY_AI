import streamlit as st
import numpy as np
from search import astar_search, EightPuzzle
import time

def load_css():
    st.markdown("""
        <style>
            .stButton>button {
                color: white;
                border: 2px solid #FF6699;
                background-color: #FF6699;
                padding: 10px 24px;
                transition: all 0.3s;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: white;
                color: #FF6699;
            }
        </style>
    """, unsafe_allow_html=True)

def scramble(state, puzzle):
    """Scrambles the puzzle starting from the goal state."""
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    scramble = [np.random.choice(possible_actions) for _ in range(60)]
    for move in scramble:
        if move in puzzle.actions(state):
            state = puzzle.result(state, move)
    return state

def exchange(state, index, zero_ix, puzzle):
    """Interchanges the position of the selected tile with the zero tile under certain conditions."""
    actions = puzzle.actions(state)
    i_diff = index // 3 - zero_ix // 3
    j_diff = index % 3 - zero_ix % 3
    current_action = ''
    
    if i_diff == 1:
        current_action += 'DOWN'
    elif i_diff == -1:
        current_action += 'UP'
    if j_diff == 1:
        current_action += 'RIGHT'
    elif j_diff == -1:
        current_action += 'LEFT'
    
    if abs(i_diff) + abs(j_diff) == 1 and current_action in actions:
        state = list(state)
        state[zero_ix], state[index] = state[index], state[zero_ix]
        state = tuple(state)
        puzzle = EightPuzzle(state)
    return state, puzzle

def app():
    load_css()  
    st.write('<h1 style="font-size: 20px; color: #F7418F;">8-Puzzle Solver</h1>', unsafe_allow_html=True)
    state = tuple(st.session_state.get('state', [1, 2, 3, 4, 5, 6, 7, 8, 0]))
    puzzle = EightPuzzle(state)
    
    if 'solution' not in st.session_state or st.button('Scramble'):
        state = scramble(state, puzzle)
        st.session_state['state'] = state
        puzzle = EightPuzzle(state)
        st.session_state['solution'] = None

    cols = st.columns(3)
    index = 0
    zero_ix = state.index(0)
    
    for row in range(3):
        for col in range(3):
            button_label = str(state[index]) if state[index] != 0 else ''
            if cols[col].button(button_label, key=f'button{index}'):
                state, puzzle = exchange(state, index, zero_ix, puzzle)
                st.session_state['state'] = state
                puzzle = EightPuzzle(state)
            index += 1
    
    if st.button('Solve'):
        solution = astar_search(puzzle).solution()
        st.session_state['solution'] = solution
        st.session_state['current_step'] = 0
    
    if 'solution' in st.session_state and st.session_state['solution'] is not None:
        if 'current_step' in st.session_state and st.session_state['current_step'] < len(st.session_state['solution']):
            move = st.session_state['solution'][st.session_state['current_step']]
            state = puzzle.result(state, move)
            st.session_state['state'] = state
            puzzle = EightPuzzle(state)
            st.session_state['current_step'] += 1
            time.sleep(0.5)  
            st.experimental_rerun()

app()
