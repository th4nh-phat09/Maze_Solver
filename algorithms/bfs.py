import pygame

def bfs_algorithm(draw, begin, end):
    queue = [begin]
    cameFrom = {}

    # Đánh dấu các ô đã được kiểm tra
    visited = set()
    visited.add(begin)
    
    while queue:
        current = queue.pop(0)

        

        for neighbor in current.neighbors:
            if neighbor not in cameFrom and neighbor not in visited:
                queue.append(neighbor)
                cameFrom[neighbor] = current
                if neighbor == end:
                    reconstructPath(cameFrom, end, draw, begin)
                    return True
                visited.add(neighbor)
                neighbor.makeOpen()

        # Chỉ vẽ lại sau mỗi lần duyệt ô và thêm độ trễ
        if current != begin:
            current.makeClosed()
        
        draw()  # Vẽ lại sau mỗi vòng lặp BFS
        pygame.time.delay(50)  # Thêm độ trễ 50ms để không quá nhanh

    draw()  # Vẽ lại toàn bộ bảng sau khi BFS kết thúc
    return False

def reconstructPath(cameFrom, current, draw, begin):
    while current in cameFrom:
        current = cameFrom[current]
        if current != begin:  # Kiểm tra nếu không phải điểm bắt đầu
            current.makePath()
    draw()  # Vẽ lại toàn bộ bảng sau khi hoàn thành đường đi
