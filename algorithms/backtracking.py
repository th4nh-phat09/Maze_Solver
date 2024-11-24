import pygame
def backtracking_algorithm(draw, grid, current, goal, path):

    """
    Thuật toán Backtracking để tìm đường đi trong mê cung.
    - draw: Hàm để vẽ lại lưới
    - grid: Lưới các ô
    - current: Ô hiện tại đang xét
    - goal: Ô đích cần đến
    - path: Dictionary lưu trữ đường đi
    """
    if current == goal:
        reconstructPath(path, goal, draw, current)
        goal.makeEnd()  # Đánh dấu ô đích
        return True

    # Đánh dấu ô hiện tại đã xét
    current.makeClosed()
    draw()
    #pygame.time.delay(50)  # Thêm độ trễ để dễ quan sát

    # Duyệt qua các ô hàng xóm
    for neighbor in current.neighbors:
        if not neighbor.checkClosed() and not neighbor.checkBarrier() and neighbor not in path:
            path[neighbor] = current  # Lưu lại bước đi
            neighbor.makeOpen()  # Đánh dấu ô đang được xét
            draw()
            #pygame.time.delay(50)

            # Gọi đệ quy Backtracking
            if backtracking_algorithm(draw, grid, neighbor, goal, path):
                return True

            # Nếu không tìm được đường, quay lui
            neighbor.reset()
            draw()
            #pygame.time.delay(50)




def reconstructPath(path, current, draw, begin):
    """
    Truy vết lại đường đi từ điểm đích về điểm bắt đầu.
    - path: Dictionary chứa thông tin các ô trước đó.
    - current: Ô hiện tại (thường là điểm đích).
    - draw: Hàm vẽ lại trạng thái lưới.
    - begin: Điểm bắt đầu (không tô màu).
    """
    while current in path:
        current = path[current]
        if current != begin:  # Không tô màu điểm bắt đầu
            current.makePath()  # Đánh dấu đường đi
            draw()

    return False
