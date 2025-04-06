import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from collections import deque
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

def bfs_search(maze):
    """执行BFS搜索算法并返回搜索过程和最短路径"""
    n, m = len(maze), len(maze[0])
    start, end = (0, 0), (n-1, m-1)
    
    # 初始化状态矩阵
    state = np.where(np.array(maze) == 1, 1, 0)  # 1是墙，0是路
    
    # 存储搜索过程和路径历史
    history = [state.copy()]
    path_history = [[]]
    came_from = {}  # 用于路径回溯
    
    queue = deque([(start[0], start[1], 0)])  # 使用deque提高性能
    visited = set()
    visited.add(start)
    
    found = False
    steps = -1
    
    while queue and not found:
        x, y, steps = queue.popleft()
        
        # 到达终点
        if (x, y) == end:
            found = True
            break
        
        # 标记当前点为浅青色(正在处理)
        state[x, y] = 3
        history.append(state.copy())
        path_history.append([])
        
        # 标记为已访问(淡青色)
        state[x, y] = 2
        history.append(state.copy())
        path_history.append([])
        
        # 探索四个方向
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                came_from[(nx, ny)] = (x, y)
                queue.append((nx, ny, steps + 1))
                
                # 显示候选点(浅青色)
                temp_state = state.copy()
                temp_state[nx, ny] = 3
                history.append(temp_state.copy())
                path_history.append([])
    
    # 回溯路径
    if found:
        path = []
        current = end
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        
        # 添加路径动画帧
        for i in range(len(path)):
            temp_state = state.copy()
            # 标记已找到的路径部分为黄色
            for px, py in path[:i+1]:
                temp_state[px, py] = 4
            history.append(temp_state.copy())
            path_history.append(path[:i+1])
    
    return history, path_history, steps if found else -1

def visualize_search(history, path_history, maze, algorithm_name="BFS"):
    """BFS可视化，与A*风格一致"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 颜色定义：0=空地(白), 1=墙(黑), 2=已访问(淡青), 3=当前点(浅青), 4=路径(黄)
    cmap = ListedColormap(['white', 'black', '#88CCEE', '#44AA99', 'gold'])
    
    # 初始化图像
    img = ax.imshow(history[0], cmap=cmap, vmin=0, vmax=4)
    
    # 添加网格线
    n, m = len(maze), len(maze[0])
    ax.set_xticks(np.arange(-0.5, m, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", size=0)
    
    # 设置标题
    ax.set_title(f'{algorithm_name}算法迷宫寻路\n(白色:空地, 黑色:障碍, 青色:已访问, 黄色:最短路径)')
    
    # 动画更新函数
    def update(frame):
        img.set_array(history[frame])
        # 清除之前的路径线
        while len(ax.lines) > 0:
            ax.lines[0].remove()
        # 绘制当前路径
        if frame < len(path_history) and path_history[frame]:
            path = path_history[frame]
            y_coords = [p[0] for p in path]
            x_coords = [p[1] for p in path]
            ax.plot(x_coords, y_coords, color='gold', linewidth=3, 
                    marker='o', markersize=8, markerfacecolor='gold')
        return [img]
    
    # 创建动画
    ani = FuncAnimation(fig, update, frames=len(history), 
                       interval=300, blit=False, repeat=True)
    
    # 保存为GIF
    print("正在保存GIF动画...")
    writer = PillowWriter(
        fps=10,
        bitrate=1800,
        metadata={
            'title': 'BFS Pathfinding',
            'artist': 'Matplotlib'
        }
    )
    ani.save(
        "bfs_pathfinding.gif",
        writer=writer,
        dpi=100,
        savefig_kwargs={'facecolor': 'white'}
    )
    print("GIF动画已保存为 bfs_pathfinding.gif")
    
    plt.show()

# 主程序
n, m = map(int, input().split())
maze = []
for i in range(n):
    maze.append(list(map(int, input().split())))
  
# 执行搜索和可视化
history, path_history, path_length = bfs_search(maze)
print(f"最短路径长度: {path_length}")
visualize_search(history, path_history, maze, "BFS")