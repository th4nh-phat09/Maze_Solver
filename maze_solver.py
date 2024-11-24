import pygame
import tkinter as tk
from algorithms.astar import astar_algorithm
from algorithms.bfs import bfs_algorithm
from algorithms.backtracking import backtracking_algorithm
from algorithms.simulated import simulated_annealing_algorithm

import os

# Cấu hình màn hình và tên ứng dụng
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze_Solver")

#Cập nhập đường dẫn thư mục image
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "image")


# Load hình ảnh
START_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "start.png"))
END_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "end.png"))
BARRIER_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "barrier.png"))
PATH_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "path.png"))
CELL_SIZE = WIDTH // 32 # Kích thước ô

#Resize lại hình ảnh để vừa với kích thước 1 ô
START_IMAGE = pygame.transform.scale(START_IMAGE, (CELL_SIZE, CELL_SIZE))
END_IMAGE = pygame.transform.scale(END_IMAGE, (CELL_SIZE, CELL_SIZE))
BARRIER_IMAGE = pygame.transform.scale(BARRIER_IMAGE, (CELL_SIZE, CELL_SIZE))
PATH_IMAGE = pygame.transform.scale(PATH_IMAGE, (CELL_SIZE, CELL_SIZE))

# Màu sắc cho các trạng thái khác
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Class Node là từng ô trên lưới
class Node:
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
    def getPos(self):
        return self.row, self.col
    

    def checkClosed(self):
        return self.color == (255, 204, 0)  # YELLOW

    def checkOpen(self):
        return self.color == (0, 0, 255)  # BLUE

    def checkBarrier(self):
        return self.image == BARRIER_IMAGE

    def checkStart(self):
        return self.image == START_IMAGE

    def checkEnd(self):
        return self.image == END_IMAGE

    def reset(self):
        self.color = WHITE
        self.image = None

    def makeStart(self):
        self.image = START_IMAGE

    def makeClosed(self):
        self.color = (255, 204, 0)  # YELLOW

    def makeOpen(self):
        self.color = (0, 0, 255)  # BLUE

    def makeBarrier(self):
        self.image = BARRIER_IMAGE

    def makeEnd(self):
        self.image = END_IMAGE

    def makePath(self):
        self.image = PATH_IMAGE

    def draw(self, win):
        if self.image:
            win.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].checkBarrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].checkBarrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].checkBarrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].checkBarrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# Hàm hỗ trợ cho A* và BFS
def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def drawGrid(win, rows, width):
    gap = width // rows

    # Vẽ các đường ngang
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))

    # Vẽ các đường dọc
    for j in range(rows):
        pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

#Vẽ lại bảng cập nhật ảnh cho bảng
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    drawGrid(win, rows, width)
    pygame.display.update()

def getClicked(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# Hàm chính cho Pygame
def main():
    ROWS = 32
    grid = makeGrid(ROWS, WIDTH)
    begin = None
    end = None
    run = True
    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = getClicked(pos, ROWS, WIDTH)
                node = grid[row][col]
                if not begin and Node != end and not node.checkBarrier():
                    begin = node
                    begin.makeStart()

                elif not end and Node != begin and not node.checkBarrier():
                    end = node
                    end.makeEnd()

                elif node != begin and Node != end:
                    node.makeBarrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = getClicked(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.reset()
                if node == begin:
                    begin = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and begin and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    astar_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, begin, end)

                if event.key == pygame.K_b and begin and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)
  
                    bfs_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), begin, end)

                if event.key == pygame.K_s and begin and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    simulated_annealing_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, begin, end)

                if event.key == pygame.K_t and begin and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)
    
                    backtracking_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, begin, end, {})


                    

    pygame.quit()

if __name__ == "__main__":
    main()

#test