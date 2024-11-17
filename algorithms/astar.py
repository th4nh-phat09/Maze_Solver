import pygame
import math  
from queue import PriorityQueue


def astar_algorithm(draw, grid, begin, goal):
    """
    draw: Hàm để vẽ (sử dụng pygame)
    grid: Lưới các ô vuông (grid)
    begin: Điểm bắt đầu
    goal: Điểm đích
    """
    # Khởi tạo tập các nút biên (open set) O ← {S}
    open_set = PriorityQueue()
    count = 0
    #Thêm vào hàng đợi ưu tiên
    open_set.put((0, count, begin))  # (f(N), count, N)
    came_from = {}

    # g(N): chi phí từ nút bắt đầu đến nút N
    g_score = {}
    for row in grid:
        for node in row:
            g_score[node] = float('inf')
    g_score[begin] = 0

    # f(N) = g(N) + h(N)
    f_score = {}
    for row in grid:
        for node in row:
            f_score[node] = float('inf')
    f_score[begin] = heuristic(begin.getPos(), goal.getPos())

    # open_set_hash để theo dõi các nút đang được xét
    open_set_hash = {begin}

    # Vòng lặp chính (While O không rỗng)
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # 1. Lấy nút N có f(N) nhỏ nhất ra khỏi O
        #Khi gọi get(), nó trả về một tuple có dạng (f_score, count, node).
        #[2] ở đây không phải là chỉ số của f_score nhỏ nhất, mà là chỉ số của phần tử trong tuple.
        current = open_set.get()[2]  # Lấy nút N
        open_set_hash.remove(current)

        # 2. Nếu N thuộc G, return đường đi tới N
        if current == goal:
            reconstructPath(came_from, goal, draw)
            goal.makeEnd()  # Đánh dấu điểm kết thúc
            begin.makeStart() #Đánh dấu điểm bắt đầu
            return True

        # 3. Với mọi M ∈ P(N) (các hàng xóm của N)
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # Giả định chi phí qua N

            # Nếu tìm được đường đi tốt hơn tới M
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.getPos(), goal.getPos())

                # Thêm M vào tập biên O
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.makeOpen()  # Đánh dấu M là nút đang xét

        draw()  # Vẽ lại trạng thái

        # Đánh dấu nút N đã xét xong
        if current != begin:
            current.makeClosed()

    # Trả về thất bại nếu không tìm được đường đi
    return False


def heuristic(p1, p2):
    """
    Hàm heuristic tính khoảng cách Euclidean giữa 2 điểm (Pythagoras).
    """
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def reconstructPath(came_from, current, draw):
    """
    Truy vết lại đường đi từ điểm đích về điểm bắt đầu.
    """
    while current in came_from:
        current = came_from[current]
        current.makePath()
        draw()
