import numpy as np

class MazeEnvironment:
    def __init__(self, grid, start_pos, end_pos):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.start_pos = start_pos
        self.goal_pos = end_pos
        self.current_pos = start_pos
        
    def reset(self):
        """Reset môi trường về trạng thái ban đầu"""
        self.current_pos = self.start_pos
        return self._get_state()
    
    def _get_state(self):
        """Chuyển đổi vị trí hiện tại thành state"""
        return self.current_pos
    
    def step(self, action):
        """
        Thực hiện action và trả về (state mới, reward, done)
        action: 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT
        """
        # Ánh xạ action sang hướng di chuyển
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        row, col = self.current_pos
        new_row = row + directions[action][0]
        new_col = col + directions[action][1]
        
        # Kiểm tra va chạm vật cản hoặc ra ngoài grid
        if (new_row < 0 or new_row >= self.rows or 
            new_col < 0 or new_col >= self.cols or 
            self.grid[new_row][new_col].checkBarrier()):
            return self._get_state(), -10, False
        # Cập nhật vị trí mới
        self.current_pos = (new_row, new_col)
        # Kiểm tra đến đích
        if self.current_pos == self.goal_pos:
            return self._get_state(), 100, True
        
        # Reward nhỏ cho mỗi bước đi hợp lệ
        return self._get_state(), -1, False
    
   