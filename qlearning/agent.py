import numpy as np

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, epsilon=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995  
        self.q_table = {} # Khởi tạo Q-table
    
    def get_action(self, state, valid_actions):
        """Chọn action dựa trên epsilon-greedy policy"""
        # Chọn ngẫu nhiên action với xác suất epsilon (khám phá)
        if np.random.rand() <= self.epsilon:
            return np.random.choice(valid_actions)
        
        # Lấy Q-values cho state hiện tại
        state_q_values = self.q_table.get(state, {})
        
        # Chọn action có Q-value cao nhất trong số các action hợp lệ
        max_q = float('-inf')
        best_action = valid_actions[0]
        
        for action in valid_actions:
            q_value = state_q_values.get(action, 0)
            if q_value > max_q:
                max_q = q_value
                best_action = action
                
        return best_action
    
    def learn(self, state, action, reward, next_state, next_valid_actions):
        """Cập nhật Q-value dựa trên trải nghiệm"""
        # Khởi tạo state trong Q-table nếu chưa tồn tại
        if state not in self.q_table:
            self.q_table[state] = {}
        
        # Tính toán max Q-value cho state tiếp theo
        next_max_q = 0
        if next_state in self.q_table:
            next_q_values = [self.q_table[next_state].get(a, 0) for a in next_valid_actions]
            if next_q_values:
                next_max_q = max(next_q_values)
        
        # Cập nhật Q-value
        old_q = self.q_table[state].get(action, 0)
        new_q = (1 - self.learning_rate) * old_q + \
            self.learning_rate * (reward + self.discount_factor * next_max_q)
        self.q_table[state][action] = new_q
        
        # Giảm epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def choose_action(self, state):
        """Chọn action dựa trên epsilon-greedy policy"""
        valid_actions = list(range(self.action_size))  # [0,1,2,3] cho 4 hướng
        return self.get_action(state, valid_actions)
