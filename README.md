# Maze Solver Game

## Giới thiệu

Maze Solver là một ứng dụng minh họa các thuật toán tìm đường đi trong mê cung, được phát triển bởi:

- Nguyễn An Thành Phát (22110197)
- Phan Văn Thuận (22110240)

## Tính năng

- Tạo mê cung ngẫu nhiên
- Hỗ trợ nhiều thuật toán tìm đường:
  - A\* (A-star)
  - BFS (Breadth-First Search)
  - Backtracking
  - Simulated Annealing
  - Q-Learning
- Hiển thị trực quan quá trình tìm đường
- So sánh hiệu suất giữa các thuật toán
- Giao diện đồ họa thân thiện

## Yêu cầu hệ thống

- Python 3.7 trở lên
- Các thư viện Python:
  ```bash
  pip install pygame
  pip install tkinter
  pip install matplotlib
  pip install numpy
  ```

## Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/th4nh-phat09/Maze_Solver.git
   ```
2. Di chuyển vào thư mục project:
   ```bash
    cd maze-solver
   ```
3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

## Chạy ứng dụng

```bash
python maze_solver.py
```

### Hướng dẫn sử dụng

- Click chuột trái để đặt:
  - Click đầu tiên: điểm bắt đầu
  - Click thứ hai: điểm đích
  - Các click tiếp theo: tạo chướng ngại vật
- Click chuột phải để xóa ô đã đặt
- Nhấn SPACE để bắt đầu tìm đường
- Nhấn C để xóa toàn bộ mê cung

## Đóng góp

Mọi đóng góp và góp ý đều được hoan nghênh. Vui lòng tạo issue hoặc pull request.

## Giấy phép

[MIT License](LICENSE)

## Liên hệ

- Nguyễn An Thành Phát - 22110197@student.hcmute.edu.vn
- Phan Văn Thuận - 22110240@student.hcmute.edu.vn
