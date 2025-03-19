import pygame
import time
import heapq
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAP = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
]
# Vị trí ban đầu và đích
START = (0, 0)
GOAL = (14, 14)
DIRECTIONS = {
    pygame.K_UP: (-1, 0),
    pygame.K_DOWN: (1, 0),
    pygame.K_LEFT: (0, -1),
    pygame.K_RIGHT: (0, 1),
}
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def a_star_search(start, goal):
    heap = [(0, start)]
    came_from = {start: None} # ng
    cost_so_far = {start: 0} #cp
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dr, dc in DIRECTIONS.values():
            next_pos = (current[0] + dr, current[1] + dc)
            if 0 <= next_pos[0] < ROWS and 0 <= next_pos[1] < COLS and MAP[next_pos[0]][next_pos[1]] == 0:
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(next_pos, goal)
                    heapq.heappush(heap, (priority, next_pos))
                    came_from[next_pos] = current
    return None
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Đua Xe 🚗")
player_pos = list(START)
running = True
start_time = time.time()
show_path = False
shortest_path = []
while running:
    screen.fill(WHITE)
    if show_path:
        shortest_path = a_star_search(tuple(player_pos), GOAL)
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE if MAP[r][c] == 0 else BLACK
            pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    # Vẽ đường đi A* (màu vàng)
    if shortest_path:
        for pos in shortest_path:
            pygame.draw.rect(screen, YELLOW, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Vẽ xe (màu xanh lá)
    pygame.draw.rect(screen, GREEN, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Vẽ đích (màu đỏ)
    pygame.draw.rect(screen, RED, (GOAL[1] * CELL_SIZE, GOAL[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in DIRECTIONS:
                dr, dc = DIRECTIONS[event.key]
                new_pos = (player_pos[0] + dr, player_pos[1] + dc)
                if 0 <= new_pos[0] < ROWS and 0 <= new_pos[1] < COLS and MAP[new_pos[0]][new_pos[1]] == 0:
                    player_pos = list(new_pos)
            elif event.key == pygame.K_h:
                show_path = True
    if tuple(player_pos) == GOAL:
        print(f"🎉 Bạn đã hoàn thành trong {round(time.time() - start_time, 2)} giây! 🏁")
        running = False
pygame.quit()
