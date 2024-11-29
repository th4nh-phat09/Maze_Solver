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
    open = PriorityQueue()
    count = 0
    #Thêm vào hàng đợi ưu tiên
    open.put((0, count, begin))  # (f(N), count, N)
    path = {} #đường đi ban đầu băng đầu là rỗng
    # open_set_hash để theo dõi các nút đang được xét
    openHash = {begin}

    # g(N): chi phí từ nút bắt đầu đến nút N
    g= {}
    f= {}
    for row in grid:
        for node in row:
            g[node] = float('inf')
            f[node] = float('inf')
    g[begin] = 0
    f[begin] = heuristic(begin.getPos(), goal.getPos()) # f(N) = g(N) + h(N)

    # Vòng lặp chính (While O không rỗng)
    while not open.empty():
        # 1. Lấy nút N có f(N) nhỏ nhất ra khỏi O
        #Khi gọi get(), nó trả về một tuple có dạng (f_score, count, node).
        #2. ở đây    phải là chỉ số của f_score nhỏ nhất, mà là chỉ số của phần tử trong tuple.
        current = open.get()[2]  # Lấy nút N
        openHash.remove(current)

        # 2. Nếu N là Goal, return đường đi tới N
        if current == goal:
            reconstructPath(path, goal, draw)
            begin.makeStart() #Đánh dấu điểm bắt đầu
            draw()
            return True

        # 3. Với mọi M ∈  hàng xóm của N
        for neighbor in current.neighbors:
            temp = g[current] + 1  # Giả định chi phí qua N

            # Nếu tìm được đường đi tốt hơn tới M
            if temp< g[neighbor]:
                path[neighbor] = current
                g[neighbor] = temp
                f[neighbor] = temp + heuristic(neighbor.getPos(), goal.getPos())
                # Thêm M vào tập biên O
                # Có thể loại bỏ việc sử dụng open_set_hash nếu bạn có cách khác để kiểm tra xem một nút đã có trong tập mở (open set) hay chưa.
               # Tuy nhiên, điều này có thể làm giảm hiệu suất của thuật toán, vì việc kiểm tra sự tồn tại trong một tập hợp (set) thường nhanh hơn so với việc kiểm tra trong một hàng đợi ưu tiên (priority queue).
                if neighbor not in openHash:
                    count += 1
                    open.put((f[neighbor], count, neighbor))
                    openHash.add(neighbor)
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


def reconstructPath(path, current, draw):
    """
    Truy vết lại đường đi từ điểm đích về điểm bắt đầu.
    """
    while current in path:
        current = path[current]
        current.makePath()
        draw()
