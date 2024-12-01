import matplotlib.pyplot as plt
import csv
import os
def save_results_to_csv(results):
    dataset_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset")
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    filename = 'maze_solver_results.csv'
    filepath = os.path.join(dataset_folder, filename)
    file_exists = os.path.exists(filepath)
    
    with open(filepath, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Algorithms', 'Run(s)', 'Moves(square)'])
        
        for algo_name, data in results.items():
            writer.writerow([
                algo_name,
                f"{data['time']:.3f}",
                data['path_length']
            ])

def plot_comparison(results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    algorithms = list(results.keys())
    times = [results[algo]['time'] for algo in algorithms]
    path_lengths = [results[algo]['path_length'] for algo in algorithms]
    
    # Plot thời gian thực thi
    bars1 = ax1.bar(algorithms, times, color=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])
    ax1.set_title('Thời gian thực thi', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Thời gian (giây)', fontsize=10)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}s',
                ha='center', va='bottom')
    
    # Plot độ dài đường đi
    bars2 = ax2.bar(algorithms, path_lengths, color=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])
    ax2.set_title('Độ dài đường đi', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Số ô', fontsize=10)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)} ô',
                ha='center', va='bottom')
    
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax2.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    fig.suptitle('So sánh hiệu suất các thuật toán', fontsize=14, fontweight='bold', y=1.05)
    plt.show()
