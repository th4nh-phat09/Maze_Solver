#%%
import pygame
import math
from queue import PriorityQueue
import tkinter as tk

# Cấu hình màn hình và tên ứng dụng
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Algorithm with Images")

# Load hình ảnh
START_IMAGE = pygame.image.load("start.png")
END_IMAGE = pygame.image.load("end.png")
BARRIER_IMAGE = pygame.image.load("barrier.png")
PATH_IMAGE = pygame.image.load("path.png")
CELL_SIZE = WIDTH // 50  # Kích thước ô

START_IMAGE = pygame.transform.scale(START_IMAGE, (CELL_SIZE, CELL_SIZE))
END_IMAGE = pygame.transform.scale(END_IMAGE, (CELL_SIZE, CELL_SIZE))
BARRIER_IMAGE = pygame.transform.scale(BARRIER_IMAGE, (CELL_SIZE, CELL_SIZE))
PATH_IMAGE = pygame.transform.scale(PATH_IMAGE, (CELL_SIZE, CELL_SIZE))

# Màu sắc cho các trạng thái khác
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Lớp Spot đại diện cho từng ô trên lưới
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.image = None
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == (255, 0, 0)  # RED

    def is_open(self):
        return self.color == (0, 255, 0)  # GREEN

    def is_barrier(self):
        return self.image == BARRIER_IMAGE

    def is_start(self):
        return self.image == START_IMAGE

    def is_end(self):
        return self.image == END_IMAGE

    def reset(self):
        self.color = WHITE
        self.image = None

    def make_start(self):
        self.image = START_IMAGE

    def make_closed(self):
        self.color = (255, 0, 0)  # RED

    def make_open(self):
        self.color = (0, 255, 0)  # GREEN

    def make_barrier(self):
        self.image = BARRIER_IMAGE

    def make_end(self):
        self.image = END_IMAGE

    def make_path(self):
        self.image = PATH_IMAGE

    def draw(self, win):
        if self.image:
            win.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# Hàm hỗ trợ cho A* và BFS
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def bfs_algorithm(draw, grid, start, end):
    queue = [start]
    came_from = {}
    while queue:
        current = queue.pop(0)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def astar_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# Hàm chính cho Pygame
def main():
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    run = True
    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                if not start and spot != end and not spot.is_barrier():
                    start = spot
                    start.make_start()

                elif not end and spot != start and not spot.is_barrier():
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # Chạy thuật toán A* hoặc BFS tùy theo lựa chọn
                    if chosen_algorithm == "A*":
                        astar_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
                    elif chosen_algorithm == "BFS":
                        bfs_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    pygame.quit()

# Hàm giao diện với tkinter
def select_algorithm(algorithm):
    global chosen_algorithm
    chosen_algorithm = algorithm
    main()

# Tạo giao diện tkinter
root = tk.Tk()
root.title("Pathfinding Algorithm")

chosen_algorithm = None

astar_button = tk.Button(root, text="A* Algorithm", command=lambda: select_algorithm("A*"))
astar_button.pack(pady=10)

bfs_button = tk.Button(root, text="BFS Algorithm", command=lambda: select_algorithm("BFS"))
bfs_button.pack(pady=10)

root.mainloop()

# %%
