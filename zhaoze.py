import heapq
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

# 判断位置是否有效
def is_valid(x, y, m, n):
    return 0 <= x < m and 0 <= y < n

# 保存每一步的帧
def save_frame(grid, visited, current, path, m, n, frame_dir, frames):
    img = np.ones((m, n, 3))  # 白色背景
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                img[i][j] = [0.7, 0.7, 0.7]  # 灰色沼泽
            else:
                img[i][j] = [1, 1, 1]  # 白色通路

    fig, ax = plt.subplots()
    ax.imshow(img, interpolation='none')
    ax.set_xticks([])  # 去除坐标轴
    ax.set_yticks([])

    # 小圆点标记访问过的点（棕色）
    for x, y in visited:
        ax.plot(y, x, 'o', color=(0.6, 0.4, 0.2), markersize=10)

    # 当前点（蓝色）
    if current:
        x, y = current
        ax.plot(y, x, 'o', color='blue', markersize=15)

    # 路径（红线）
    if path:
        path_y = [y for x, y in path]
        path_x = [x for x, y in path]
        ax.plot(path_y, path_x, color='gold', linewidth=2)

    plt.tight_layout()
    frame_path = f"{frame_dir}/frame_{len(frames):04d}.png"
    plt.savefig(frame_path)
    plt.close()
    frames.append(frame_path)

# 重建路径
def reconstruct_path(parent, end_x, end_y):
    path = []
    x, y = end_x, end_y
    while (x, y) != (0, 0):
        path.append((x, y))
        x, y = parent[x][y]
    path.append((0, 0))
    path.reverse()
    return path

# Dijkstra 算法
def dijkstra(grid, m, n, swamp_penalty=2):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = []
    heapq.heappush(heap, (0, 0, 0))  # (cost, x, y)
    cost_map = [[float('inf')] * n for _ in range(m)]
    cost_map[0][0] = 0
    visited = set()
    parent = [[None] * n for _ in range(m)]
    path = []
    frames = []
    
    # 创建输出目录
    frame_dir = "frames"
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)
    
    while heap:
        cost, x, y = heapq.heappop(heap)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        save_frame(grid, visited, (x, y), path, m, n, frame_dir, frames)

        if x == m - 1 and y == n - 1:
            path = reconstruct_path(parent, x, y)
            for _ in range(5):  # 重复几帧强调最终路径
                save_frame(grid, visited, None, path, m, n, frame_dir, frames)
            return cost, frames

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, m, n):
                new_cost = cost + 1 + (swamp_penalty if grid[nx][ny] == 1 else 0)
                if new_cost < cost_map[nx][ny]:
                    cost_map[nx][ny] = new_cost
                    parent[nx][ny] = (x, y)
                    heapq.heappush(heap, (new_cost, nx, ny))

    return -1, frames

# 保存 GIF 使用 Pillow
def save_gif_with_pillow(frames, output_path="maze_solution.gif"):
    images = [Image.open(f) for f in frames]
    # 使用 Pillow 创建 GIF, 设置 duration 单位为毫秒
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=500, loop=0)  # duration=500ms
    print(f"GIF saved as {output_path}")

    # 清理临时帧
    for f in frames:
        os.remove(f)
    os.rmdir("frames")

# 读取输入
n, m = map(int, input().split())  # 输入行数 n 和列数 m
maze = []
for i in range(n):
    row = list(map(int, input().split()))  # 输入每一行的数字
    maze.append(row)

# 调用 Dijkstra 算法
result, frames = dijkstra(maze, n, m)
print("Dijkstra result:", result)

# 保存 GIF
save_gif_with_pillow(frames)
