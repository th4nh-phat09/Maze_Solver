import pygame
import random
import math

def simulated_annealing_algorithm(draw, begin, end):
    temp= 100  # khởi tạo nhiệt độ
    alpha = 0.99       # làm mát nhiệt độ
    cameFrom = {}  
    current = begin
    currentCost = manhattan(current, end)

    while temp > 1:
        draw()
        # Đặt màu vàng cho các ô đã duyệt
        if current != begin and current != end:
            current.makePath()
        pygame.time.delay(50)  # Độ trễ để quan sát
        neighbors = current.neighbors#lấy các ô hàng xóm
        nextNode = random.choice(neighbors)#chọn ngẫu nhiên 1 ô hàng xóm
        nextCost = manhattan(nextNode, end)

        # chọn ô hàng xóm nếu nó có chi phí thấp hơn
        if nextCost < currentCost:
            cameFrom[nextNode] = current
            current = nextNode
            currentCost = nextCost
        else:
            # tính xác suất chọn ô hàng xóm
            probability = math.exp((currentCost - nextCost) / temp)
            if random.random() < probability:
                cameFrom[nextNode] = current
                current = nextNode
                currentCost = nextCost

        # Đánh dấu các ô đang duyệt
        if current != begin and current != end:
            current.makeOpen()

        # Làm mát nhiệt độ
        temp *= alpha

        # Nếu tìm đến đích
        if current == end:
            pygame.time.delay(2000)  # Chờ 2 giây sau khi hoàn thành
            return True

    return False


def manhattan(node, end):
    x1, y1 = node.getPos()
    x2, y2 = end.getPos()
    return abs(x1 - x2) + abs(y1 - y2)



