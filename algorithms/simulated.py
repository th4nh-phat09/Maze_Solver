import pygame
import random
import math

def simulated_annealing_algorithm(draw, grid, begin, end):
    """
    Simulated Annealing algorithm with colored visualization for states.
    """
    temperature = 100  # Initial temperature
    alpha = 0.99       # Cooling rate
    cameFrom = {}  

    current = begin
    current_cost = manhattan_distance(current, end)

    while temperature > 1:
        draw()

        # Đặt màu vàng cho các ô đã duyệt
        if current != begin and current != end:
            current.makePath()

        pygame.time.delay(50)  # Độ trễ để quan sát

        # Randomly choose a neighbor
        neighbors = current.neighbors
        if not neighbors:
            break

        next_node = random.choice(neighbors)
        next_cost = manhattan_distance(next_node, end)

        # Accept the neighbor if it improves or based on probability
        if next_cost < current_cost:
            cameFrom[next_node] = current
            current = next_node
            current_cost = next_cost
        else:
            probability = math.exp((current_cost - next_cost) / temperature)
            if random.random() < probability:
                cameFrom[next_node] = current
                current = next_node
                current_cost = next_cost

        # Đánh dấu các ô đang duyệt
        if current != begin and current != end:
            current.makeOpen()

        # Cool down the temperature
        temperature *= alpha

        # Nếu tìm đến đích
        if current == end:
            pygame.time.delay(2000)  # Chờ 2 giây sau khi hoàn thành
            return True

    return False


def manhattan_distance(node, end):
    """Calculate Manhattan distance between two nodes."""
    x1, y1 = node.getPos()
    x2, y2 = end.getPos()
    return abs(x1 - x2) + abs(y1 - y2)



