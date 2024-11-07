import streamlit as st
import numpy as np
import heapq

# Các hằng số
CELL_SIZE = 40
CELL_NUMBER = 15
WALL = 1
PATH = 0
START = 2
END = 3

# Tạo mê cung
def create_maze():
    maze = np.zeros((CELL_NUMBER, CELL_NUMBER), dtype=int)
    maze[0, :] = maze[-1, :] = WALL
    maze[:, 0] = maze[:, -1] = WALL
    maze[1, 1] = START
    maze[CELL_NUMBER-2, CELL_NUMBER-2] = END
    np.random.seed(None)  # Sử dụng seed ngẫu nhiên để tạo ra các mê cung khác nhau
    for _ in range(20):
        x, y = np.random.randint(1, CELL_NUMBER-1, size=2)
        if maze[x, y] == PATH:
            maze[x, y] = WALL
    return maze

# Hàm heuristic (khoảng cách Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Thuật toán A*
def a_star_search(maze, start, end):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, end)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Trả về đường đi ngược từ điểm kết thúc đến điểm bắt đầu

        close_set.add(current)
        for i, j in neighbors:
            neighbor = (current[0] + i, current[1] + j)
            if 0 <= neighbor[0] < CELL_NUMBER and 0 <= neighbor[1] < CELL_NUMBER and maze[neighbor] != WALL:
                tentative_g_score = gscore[current] + 1
                if neighbor not in close_set and (neighbor not in gscore or tentative_g_score < gscore[neighbor]):
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False  # Trả về False nếu không tìm thấy đường đi

# Ứng dụng chính
def main():
    st.write('<h2 style="font-size: 20px; color: #F7418F;">Giải mê cung với thuật toán A*</h2>', unsafe_allow_html=True)

    if 'maze' not in st.session_state or st.button('Tạo mê cung mới'):
        st.session_state.maze = create_maze()

    maze = st.session_state.maze
    start = (1, 1)
    end = (CELL_NUMBER-2, CELL_NUMBER-2)

    # Hiển thị mê cung
    maze_display = np.full((CELL_NUMBER, CELL_NUMBER), '⬜️', dtype=str)
    for x in range(CELL_NUMBER):
        for y in range(CELL_NUMBER):
            if maze[x, y] == WALL:
                maze_display[x, y] = '⬛️'
            elif maze[x, y] == START:
                maze_display[x, y] = '🟩️'
            elif maze[x, y] == END:
                maze_display[x, y] = '🟥'

    st.text('\n'.join(''.join(row) for row in maze_display))

    if st.button('Tìm đường đi'):
        path = a_star_search(maze, start, end)
        if path:
            for (x, y) in path:
                if (x, y) != start and (x, y) != end:
                    maze_display[x, y] = '🔵️'
            st.text('\n'.join(''.join(row) for row in maze_display))
        else:
            st.error("Không tìm thấy lối đi!")

if __name__ == "__main__":
    main()
