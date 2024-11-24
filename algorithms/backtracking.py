import pygame
def backtracking_algorithm(draw, grid, current, goal, path):
    #Nếu tới đích in ra đường đi
    if current == goal:
        reconstructPath(path, current, draw)
        goal.makeEnd()  # Đánh dấu ô đích
        return True

    # Đánh dấu ô hiện tại đã xét
    current.makeClosed()
    draw()
    pygame.time.delay(50)  # Thêm độ trễ để dễ quan sát

    # Duyệt ô hàng xóm
    for neighbor in current.neighbors:
        if not neighbor.checkBarrier() and neighbor not in path:
            path[neighbor] = current  # Lưu lại bước đi
            neighbor.makeOpen()  # Đánh dấu ô đang được xét
            draw()
            pygame.time.delay(10)
            # Gọi đệ quy Backtracking
            if backtracking_algorithm(draw, grid, neighbor, goal, path):
                return True
            draw()
            #pygame.time.delay(50)
    return False




def reconstructPath(path, current, draw):
    """
    Truy vết lại đường đi từ điểm đích về điểm bắt đầu.
    - path: Dictionary chứa thông tin các ô trước đó.
    - current: Ô hiện tại (thường là điểm đích).
    - draw: Hàm vẽ lại trạng thái lưới.
    - begin: Điểm bắt đầu (không tô màu).
    """
    while current in path:
        current = path[current]
        current.makePath()  # Đánh dấu đường đi
        draw()


