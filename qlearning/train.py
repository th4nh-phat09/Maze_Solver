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
                    
                    # Lưu actions xuống file
                    np.save(f'episode_{episode}_actions.npy', np.array(current_episode_actions))
                    # Lưu reward riêng
                    np.save(f'episode_{episode}_reward.npy', np.array([ep_reward]))
            else:
                current_car_pos = env.current_pos
                if not grid[current_car_pos[0]][current_car_pos[1]].checkEnd():
                    grid[current_car_pos[0]][current_car_pos[1]].makeStart()
            
                if draw_function:
                    draw_function()
                    pygame.time.delay(50)
                agent.learn(state, action, reward, next_state, list(range(4)))
                state = next_state

    # In kết quả cuối cùng
    print("\nKết quả training:")
    if first_success_actions is not None:
        print(f"Actions đầu tiên thành công: {first_success_actions}")
        print(f"Actions tốt nhất (reward = {best_episode_reward}): {best_episode_actions}")
        
        # Lưu kết quả tốt nhất
        np.save('best_actions.npy', np.array(best_episode_actions))
        np.save('first_success_actions.npy', np.array(first_success_actions))
    else:
        print("Không tìm thấy đường đi thành công nào!")
    
    start_node.makeStart()
    if draw_function:
        draw_function()
    
    print("Hoàn thành training!")
    return agent