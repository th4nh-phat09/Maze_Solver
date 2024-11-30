import sys
import os
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qlearning.environment import MazeEnvironment
from qlearning.agent import QLearningAgent

def train_agent(grid, start_pos, end_pos, num_episodes=500, draw_function=None):
    print(f"\nBắt đầu training với {num_episodes} episodes...")
    
    env = MazeEnvironment(grid, start_pos, end_pos)
    agent = QLearningAgent(state_size=(len(grid), len(grid[0])), action_size=4)
    
    # Lưu trữ node start để khôi phục sau
    start_node = grid[start_pos[0]][start_pos[1]]
    start_image = start_node.image  # Lấy hình ảnh START từ node
    
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        
        # Reset màu của tất cả các ô (trừ end và barriers)
        for row in grid:
            for node in row:
                if not (node.checkEnd() or node.checkBarrier()):
                    node.reset()
        
        # Đặt xe tại vị trí bắt đầu
        current_car_pos = start_pos
        grid[current_car_pos[0]][current_car_pos[1]].makeStart()
        
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            
            # Xóa xe ở vị trí cũ
            grid[current_car_pos[0]][current_car_pos[1]].reset()
            
            # Di chuyển xe đến vị trí mới
            current_car_pos = env.current_pos
            if not grid[current_car_pos[0]][current_car_pos[1]].checkEnd():
                grid[current_car_pos[0]][current_car_pos[1]].makeStart()
            
            if draw_function:
                draw_function()
                pygame.time.delay(50)
            
            agent.learn(state, action, reward, next_state, list(range(4)))
            state = next_state
        
        if episode % 10 == 0:
            print(f"Hoàn thành episode {episode}/{num_episodes}")
    
    # Khôi phục điểm start sau khi training xong
    start_node.makeStart()
    if draw_function:
        draw_function()
    
    print("Hoàn thành training!")
    return agent