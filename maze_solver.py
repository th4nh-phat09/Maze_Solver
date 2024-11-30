import pygame
import tkinter as tk
import matplotlib.pyplot as plt
import time
import numpy as np
from tkinter import ttk
from algorithms.astar import astar_algorithm
from algorithms.bfs import bfs_algorithm
from algorithms.backtracking import backtracking_algorithm
from algorithms.simulated import simulated_annealing_algorithm
import os
import csv
from qlearning.train import train_agent


# Cấu hình màn hình và tên ứng dụng
WIDTH = 800
WIN = None  # Khởi tạo WIN sau
pygame.display.set_caption("Maze_Solver")

# Cập nhập đường dẫn thư mục image
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "image")


# Load hình ảnh
START_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "start.png"))
END_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "end.png"))
BARRIER_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "barrier.png"))
PATH_IMAGE = pygame.image.load(os.path.join(IMAGE_FOLDER, "path.png"))
CELL_SIZE = WIDTH // 32  # Kích thước ô

# Resize lại hình ảnh để vừa với kích thước 1 ô
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
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.image = None
        self.neighbors = []
        self.width = width
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
    def isPath(self):
       return self.image == PATH_IMAGE

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
def create_test_maze(grid):
    """Tạo mê cung cố định với start, end và barriers định sẵn"""
    # Đặt điểm start ở (2,2)
    start_node = grid[2][2]
    start_node.makeStart()
    
    # Đặt điểm end ở (12,12)
    end_node = grid[12][12]
    end_node.makeEnd()
    
    # Tạo các barrier cố định
    barriers = [
        (5,5), (5,6), (5,7), (5,8),  # Tường ngang
        (6,5), (7,5), (8,5),         # Tường dọc
        (8,6), (8,7), (8,8),         # Tường ngang khác
        (3,3), (4,4), (10,10)        # Một số barrier rời rạc
    ]
    
    for pos in barriers:
        grid[pos[0]][pos[1]].makeBarrier()
    
    return start_node, end_node

# Thêm hàm để chạy Q-learning training
def run_qlearning_training(grid, ROWS, WIDTH, WIN):
    """Chạy training Q-learning trên mê cung cố định"""
    print("=== BẮT ĐẦU QUÁ TRÌNH TRAINING Q-LEARNING ===")
    
    # Tạo mê cung test
    start_node, end_node = create_test_maze(grid)
    print(f"Đã tạo mê cung với điểm bắt đầu tại ({start_node.row}, {start_node.col}) và điểm kết thúc tại ({end_node.row}, {end_node.col})")
    
    # Cập nhật neighbors cho tất cả các node
    for row in grid:
        for node in row:
            node.updateNeighbors(grid)
    
    # Train agent với các tham số đúng
    try:
        agent = train_agent(
            grid=grid,
            start_pos=(start_node.row, start_node.col),  # Thay vì start_node
            end_pos=(end_node.row, end_node.col),        # Thay vì end_node 
            num_episodes=100,
            draw_function=lambda: draw(WIN, grid, ROWS, WIDTH)
        )
        print("Training hoàn tất thành công!")
    except Exception as e:
        print(f"Lỗi trong quá trình training: {str(e)}")

def show_algorithm_menu():
    root = tk.Tk()
    root.title("Chọn Thuật Toán")
    root.geometry("400x600")  # Tăng kích thước cửa sổ để chứa thêm nút
    
    style = ttk.Style()
    style.configure('TButton', padding=10, font=('Arial', 12))
    
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    ttk.Label(frame, text="Chọn Thuật Toán Tìm Đường", 
              font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=20)
    
    def start_maze_with_algorithm(algorithm):
        root.destroy()
        run_maze_solver(algorithm)
    
    def compare_algorithms():
        root.destroy()
        run_comparison()
    
    # Các nút cho từng thuật toán
    ttk.Button(frame, text="A* Algorithm", 
               command=lambda: start_maze_with_algorithm("astar")).grid(row=1, column=0, pady=10)
    
    ttk.Button(frame, text="BFS Algorithm", 
               command=lambda: start_maze_with_algorithm("bfs")).grid(row=2, column=0, pady=10)
    
    ttk.Button(frame, text="Backtracking Algorithm", 
               command=lambda: start_maze_with_algorithm("backtracking")).grid(row=3, column=0, pady=10)
    
    ttk.Button(frame, text="Simulated Annealing", 
               command=lambda: start_maze_with_algorithm("simulated")).grid(row=4, column=0, pady=10)
    
    ttk.Button(frame, text="Q-Learning (Test)", 
               command=lambda: start_maze_with_algorithm("qlearning")).grid(row=5, column=0, pady=10)
    
    # Nút so sánh thuật toán
    ttk.Button(frame, text="So sánh các thuật toán", 
               command=compare_algorithms,
               style='TButton').grid(row=6, column=0, pady=10)
    
    # Nút thoát
    ttk.Button(frame, text="Thoát", 
               command=root.destroy,
               style='TButton').grid(row=7, column=0, pady=20)
    
    root.mainloop()

def run_maze_solver(algorithm_choice):
    global WIN
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    ROWS = 16
    grid = makeGrid(ROWS, WIDTH)
    
    if algorithm_choice == "qlearning":
        run_qlearning_training(grid, ROWS, WIDTH, WIN)
        show_algorithm_menu()
        return
    begin = None
    end = None
    run = True
    
    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = getClicked(pos, ROWS, WIDTH)
                node = grid[row][col]
                if not begin and node != end:
                    begin = node
                    begin.makeStart()
                elif not end and node != begin:
                    end = node
                    end.makeEnd()
                elif node != end and node != begin:
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

                    if algorithm_choice == "astar":
                        astar_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, begin, end)
                    elif algorithm_choice == "bfs":
                        bfs_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), begin, end)
                    elif algorithm_choice == "backtracking":
                        backtracking_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, begin, end, {})
                        begin.makeStart()
                        draw(WIN, grid, ROWS, WIDTH)
                    elif algorithm_choice == "simulated":
                        simulated_annealing_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), begin, end)
                    
                    pygame.time.delay(2000)
                    run = False
                    pygame.quit()
                    show_algorithm_menu()

def run_comparison():
    global WIN
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    ROWS = 16
    grid = makeGrid(ROWS, WIDTH)
    
  # Đặt điểm bắt đầu ở vị trí (3,3)
    start_node = grid[3][3]
    start_node.makeStart()
    
    # Đặt điểm kết thúc ở vị trí (25,25)
    end_node = grid[12][12]
    end_node.makeEnd()
    
    # Tạo chướng ngại vật theo mẫu mới
    obstacles = [
        # Tạo một bức tường ngang
        (7, 4), (7, 5), (7, 6), (7, 7), (7, 8),
        # Tạo một bức tường dọc
        (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
        # Một vài chướng ngại vật rời rạc
        (5, 5), (9, 9), (6, 10), (10, 6)
    ]
    
    for obs in obstacles:
        grid[obs[0]][obs[1]].makeBarrier()
    
    # Cập nhật neighbors cho tất cả các node
    for row in grid:
        for node in row:
            node.updateNeighbors(grid)
    
    # Dictionary để lưu kết quả
    results = {
        'A*': {'time': 0, 'path_length': 0},
        'BFS': {'time': 0, 'path_length': 0},
        'Backtracking': {'time': 0, 'path_length': 0},
        'Simulated Annealing': {'time': 0, 'path_length': 0}
    }
    
    # Chạy từng thuật toán và đo thời gian
    algorithms = {
        'A*': lambda: astar_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start_node, end_node),
        'BFS': lambda: bfs_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), start_node, end_node),
        'Backtracking': lambda: backtracking_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start_node, end_node, {}),
        'Simulated Annealing': lambda: simulated_annealing_algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), start_node, end_node)
    }
    
    for name, algo in algorithms.items():
        # Reset grid trước mỗi lần chạy
        for row in grid:
            for node in row:
                if not (node.checkStart() or node.checkEnd() or node.checkBarrier()):
                    node.reset()
        
        start_time = time.time()
        algo()
        end_time = time.time()

        # Vẽ lại điểm start và end sau khi thuật toán hoàn thành
        start_node.makeStart()  
        end_node.makeEnd()      
        
        # Tính thời gian và độ dài đường đi
        results[name]['time'] = end_time - start_time
        results[name]['path_length'] = count_path_length(grid)
        
        # Hiển thị kết quả trên màn hình
        draw(WIN, grid, ROWS, WIDTH)
        pygame.time.delay(1000)
    
    pygame.quit()

    save_results_to_csv(results)
    
    # Vẽ biểu đồ so sánh
    plot_comparison(results)

def save_results_to_csv(results):
    # Tạo thư mục dataset nếu chưa tồn tại
    dataset_folder = os.path.join(os.path.dirname(__file__), "dataset")
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    filename = 'maze_solver_results.csv'
    filepath = os.path.join(dataset_folder, filename)
    
    # Lấy timestamp hiện tại
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Kiểm tra xem file đã tồn tại chưa
    file_exists = os.path.exists(filepath)
    
    with open(filepath, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Chỉ ghi header nếu file mới
        if not file_exists:
            writer.writerow([ 'Algorithms', 'Run(s)', 'Moves(square)'])
        
        # Ghi dữ liệu cho từng thuật toán với cùng một timestamp
        for algo_name, data in results.items():
            writer.writerow([
                algo_name,
                f"{data['time']:.3f}",
                data['path_length']
            ])

def count_path_length(grid):
    count = 0
    for row in grid:
        for node in row:
            if node.isPath():
                count += 1
    return count

def plot_comparison(results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    algorithms = list(results.keys())
    times = [results[algo]['time'] for algo in algorithms]
    path_lengths = [results[algo]['path_length'] for algo in algorithms]
    
    # Plot thời gian thực thi
    bars1 = ax1.bar(algorithms, times, color=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])
    ax1.set_title('Thời gian thực thi', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Thời gian (giây)', fontsize=10)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Thêm giá trị lên đỉnh cột
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}s',
                ha='center', va='bottom')
    
    # Plot độ dài đường đi
    bars2 = ax2.bar(algorithms, path_lengths, color=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])
    ax2.set_title('Độ dài đường đi', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Số ô', fontsize=10)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # Thêm giá trị lên đỉnh cột
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)} ô',
                ha='center', va='bottom')
    
    # Thêm lưới và điều chỉnh layout
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax2.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Thêm tiêu đề chung
    fig.suptitle('So sánh hiệu suất các thuật toán', fontsize=14, fontweight='bold', y=1.05)
    
    plt.show()

def main():
    show_algorithm_menu()
if __name__ == "__main__":
    main()
#test config ver2