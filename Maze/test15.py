import pygame
import sys
import random
import heapq

# Định nghĩa các màu sắc và kích thước
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (160, 160, 160)
CELL_SIZE = 40
CELL_NUMBER = 15
WIDTH = CELL_SIZE * CELL_NUMBER
HEIGHT = CELL_SIZE * CELL_NUMBER + 100

import random


def create_maze():
    CELL_NUMBER = 15  # Số ô trong mỗi hàng và mỗi cột
    maze = []
    for row in range(CELL_NUMBER):
        maze.append([])
        for col in range(CELL_NUMBER):
            if row == 0 or row == CELL_NUMBER - 1 or col == 0 or col == CELL_NUMBER - 1:
                maze[row].append(1)  # Tạo tường xung quanh
            else:
                maze[row].append(0)
    maze[1][1] = 2  # Điểm bắt đầu
    maze[CELL_NUMBER-2][CELL_NUMBER-2] = 3  # Điểm kết thúc
    # Thêm chướng ngại vật ngẫu nhiên
    for _ in range(20):  # Số lượng chướng ngại vật
        x = random.randint(1, CELL_NUMBER-2)
        y = random.randint(1, CELL_NUMBER-2)
        if maze[x][y] == 0:
            maze[x][y] = 1
    return maze


def draw_maze(screen, maze):
    for row in range(CELL_NUMBER):
        for col in range(CELL_NUMBER):
            color = WHITE
            if maze[row][col] == 1:
                color = BLACK
            elif maze[row][col] == 2:
                color = GREEN
            elif maze[row][col] == 3:
                color = RED
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_button(screen, text, position, color=GREY):
    font = pygame.font.SysFont(None, 30)
    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=(position[0] + 50, position[1] + 20))
    pygame.draw.rect(screen, color, (*position, 100, 40))
    screen.blit(text, text_rect)

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
            return path[::-1]  # return reversed path

        close_set.add(current)
        for i, j in neighbors:
            neighbor = (current[0] + i, current[1] + j)
            if 0 <= neighbor[0] < CELL_NUMBER and 0 <= neighbor[1] < CELL_NUMBER and maze[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = gscore[current] + heuristic(current, neighbor)
                if neighbor not in close_set and (neighbor not in gscore or tentative_g_score < gscore[neighbor]):
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
            # No need to continue further for invalid or obstacle cells

    return False  # if no path is found


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Hàm khởi tạo mê cung và vẽ các thành phần
# (Được rút gọn để tập trung vào thuật toán, xem mã nguồn đầy đủ để các hàm khởi tạo và vẽ)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Solver Game")

    maze = create_maze()
    start = (1, 1)
    end = (CELL_NUMBER-2, CELL_NUMBER-2)
    path = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 130 <= mouse_pos[0] <= 230 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 10:
                    path = a_star_search(maze, start, end)
                    print("Run Button Clicked")

        screen.fill(WHITE)
        draw_maze(screen, maze)
        for step in path:
            pygame.draw.rect(screen, BLUE, (step[1]*CELL_SIZE, step[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        draw_button(screen, 'Run', (130, HEIGHT - 50))
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
