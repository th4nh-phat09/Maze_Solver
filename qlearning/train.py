import numpy as np
import sys
import os
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qlearning.environment import MazeEnvironment
from qlearning.agent import QLearningAgent

# Biến toàn cục để lưu actions
current_episode_actions = []
best_episode_actions = []
best_episode_reward = -float('inf')
first_success_actions = None

def train_agent(grid, start_pos, end_pos, num_episodes=500, draw_function=None):
    print(f"\nBắt đầu training với {num_episodes} episodes...")
    
    env = MazeEnvironment(grid, start_pos, end_pos)
    agent = QLearningAgent(state_size=(len(grid), len(grid[0])), action_size=4)
    start_node = grid[start_pos[0]][start_pos[1]]
    
    global current_episode_actions, best_episode_actions, best_episode_reward, first_success_actions
    
    # Tạo file để ghi kết quả
    with open('training_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== KẾT QUẢ TRAINING ===\n\n")
        
    for episode in range(num_episodes):
        print(f"Đang training episode {episode}/{num_episodes}")
        state = env.reset()
        done = False
        ep_reward = 0
        current_episode_actions = []  # Reset actions cho episode mới
        
        # Reset grid
        for row in grid:
            for node in row:
                if not (node.checkEnd() or node.checkBarrier()):
                    node.reset()
        
        current_car_pos = start_pos
        grid[current_car_pos[0]][current_car_pos[1]].makeStart()
        
        while not done:
            action = agent.choose_action(state)
            current_episode_actions.append(action)  # Lưu action
            next_state, reward, done = env.step(action)
            ep_reward += reward
            
            grid[current_car_pos[0]][current_car_pos[1]].reset()

            if done:
                if next_state == env.goal_pos:
                    print(f"Đã đến đích tại ep = {episode}, reward = {ep_reward}")
                    # Lưu actions đầu tiên thành công
                    if first_success_actions is None:
                        first_success_actions = current_episode_actions.copy()
                    # Lưu actions tốt nhất
                    if ep_reward > best_episode_reward:
                        best_episode_reward = ep_reward
                        best_episode_actions = current_episode_actions.copy()
                    
                    # Ghi kết quả vào file
                    with open('training_results.txt', 'a', encoding='utf-8') as f:
                        directions = {0: "LÊN", 1: "PHẢI", 2: "XUỐNG", 3: "TRÁI"}
                        f.write(f"\nEpisode {episode}:\n")
                        f.write(f"Reward: {ep_reward}\n")
                        f.write("Actions: ")
                        for act in current_episode_actions:
                            f.write(f"{directions[act]} -> ")
                        f.write("ĐÍCH\n")
                        f.write("-" * 50 + "\n")
            else:
                current_car_pos = env.current_pos
                if not grid[current_car_pos[0]][current_car_pos[1]].checkEnd():
                    grid[current_car_pos[0]][current_car_pos[1]].makeStart()
            
                if draw_function:
                    draw_function()
                    pygame.time.delay(50)
                agent.learn(state, action, reward, next_state, list(range(4)))
                state = next_state

    # Ghi kết quả tổng kết vào cuối file
    with open('training_results.txt', 'a', encoding='utf-8') as f:
        f.write("\n=== TỔNG KẾT ===\n")
        if first_success_actions is not None:
            directions = {0: "LÊN", 1: "PHẢI", 2: "XUỐNG", 3: "TRÁI"}
            
            f.write("\nĐường đi đầu tiên thành công:\n")
            for act in first_success_actions:
                f.write(f"{directions[act]} -> ")
            f.write("ĐÍCH\n")
            
            f.write(f"\nĐường đi tốt nhất (reward = {best_episode_reward}):\n")
            for act in best_episode_actions:
                f.write(f"{directions[act]} -> ")
            f.write("ĐÍCH\n")
        else:
            f.write("\nKhông tìm thấy đường đi thành công nào!\n")
    
    start_node.makeStart()
    if draw_function:
        draw_function()
    
    print("Hoàn thành training!")
    return agent