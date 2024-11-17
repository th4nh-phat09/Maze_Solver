import pygame
import tkinter as tk
from algorithms.astar import astar_algorithm
from algorithms.bfs import bfs_algorithm
import os

# Cấu hình màn hình và tên ứng dụng
WIDTH = 800
WIN = pygame.display.set_mode((900, WIDTH))
pygame.display.set_caption("Maze_Solver")

#Cập nhập đường dẫn thư mục image
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "image")


# Load hình ảnh
START_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "start.png"))
END_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "end.png"))
BARRIER_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "barrier.png"))
PATH_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "path.png"))
CELL_SIZE = WIDTH // 50  # Kích thước ô

#Resize lại hình ảnh để vừa với kích thước 1 ô
START_IMAGE = pygame.transform.scale(START_IMAGE, (CELL_SIZE, CELL_SIZE))
END_IMAGE = pygame.transform.scale(END_IMAGE, (CELL_SIZE, CELL_SIZE))
BARRIER_IMAGE = pygame.transform.scale(BARRIER_IMAGE, (CELL_SIZE, CELL_SIZE))
PATH_IMAGE = pygame.transform.scale(PATH_IMAGE, (CELL_SIZE, CELL_SIZE))

# Màu sắc cho các trạng thái khác
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Class Spot là từng ô trên lưới
class Spot:
    def __init__(self, row, col, width, total_rows):
        #Hàng và cột của ô trong lưới
        self.row = row 
        self.col = col 
        #Tọa độ của ô trên màn hình
        self.x = row * width
        self.y = col * width
        #Màu mặc định của ô đó trong lưới
        self.color = WHITE
        #Hình ảnh của ô đó hiện thị trong lưới
        self.image = None
        #Lưu các danh sách hàng xóm hay còn gọi là con
        self.neighbors = []
        #Chiều dài(cao) của một ô trong lưới
        self.width = width
        #Tổng số hàng của lưới
        self.total_rows = total_rows
    
    #Trả về vị trí (hàng, cột) của ô dưới dạng tuple
    # Ví dụ: (2,3) 
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

    # Vẽ các đường ngang
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

    # Vẽ các đường dọc
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

                elif spot != start and spot != end:
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

                    astar_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
 
                    bfs_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

    pygame.quit()

if __name__ == "__main__":
    main()
