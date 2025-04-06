import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

def h(x, y, end_x, end_y):
    return abs(x - end_x) + abs(y - end_y)

def astar_search(maze):
    n, m = len(maze), len(maze[0])
    start, end = (0, 0), (n-1, m-1)
    
    # 初始状态：0=空地，1=墙
    state = np.where(np.array(maze) == 1, 1, 0)
    history = [state.copy()]  # 历史状态记录
    path_history = [[]]      # 路径历史记录
    came_from = {}           # 路径回溯
    
    # 优先队列：(f_score, g_score, position)
    pq = [(0 + h(*start, *end), 0, start)]
    visited = set()
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    
    found = False
    steps = -1
    
    while pq and not found:
        _, steps, (x, y) = heapq.heappop(pq)
        
        if (x, y) == end:
            found = True
            break
            
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        # 创建新状态（基于上一帧）
        new_state = history[-1].copy()
        
        # 标记当前点为正在处理(浅青色=3)
        new_state[x, y] = 3
        history.append(new_state.copy())
        path_history.append([])
        
        # 标记为已访问(淡青色=2)
        new_state[x, y] = 2
        history.append(new_state.copy())
        path_history.append([])
        
        # 探索四个方向
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 0 and (nx, ny) not in visited:
                came_from[(nx, ny)] = (x, y)
                f = steps + 1 + h(nx, ny, *end)
                heapq.heappush(pq, (f, steps + 1, (nx, ny)))
                
                # 显示候选点(浅青色=3)
                temp_state = new_state.copy()
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
            # 基于最后的状态，不要覆盖已访问区域
            temp_state = history[-1].copy()
            for px, py in path[:i+1]:
                temp_state[px, py] = 4  # 4=路径(黄色)
            history.append(temp_state.copy())
            path_history.append(path[:i+1])
    
    return history, path_history, steps if found else -1

# 读取输入
n, m = map(int, input().split())
maze = []
for i in range(n):
    row = list(map(int, input().split()))
    maze.append(row)

# 执行A*搜索
history, path_history, path_length = astar_search(maze)
print(f"最短路径长度: {path_length}")

# 创建可视化
plt.rcParams['font.sans-serif'] = ['SimHei']
fig, ax = plt.subplots(figsize=(10, 8))

# 颜色定义：0=空地(白), 1=墙(黑), 2=已访问(淡青), 3=当前点(浅青), 4=路径(黄)
cmap = ListedColormap(['white', 'black', '#88CCEE', '#44AA99', 'gold'])
img = ax.imshow(history[0], cmap=cmap, vmin=0, vmax=4)

# 设置网格线
ax.set_xticks(np.arange(-0.5, m, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
ax.tick_params(which="minor", size=0)
ax.set_title('A*算法迷宫寻路 (白色:空地, 黑色:障碍, 青色:已访问, 黄色:路径)')

# 动画更新函数
def update(frame):
    img.set_array(history[frame])
    
    # 清除之前的路径绘制
    while len(ax.lines) > 0:
        ax.lines[0].remove()
        
    # 绘制当前路径
    if frame < len(path_history) and path_history[frame]:
        path = path_history[frame]
        y_coords = [p[0] for p in path]
        x_coords = [p[1] for p in path]
        ax.plot(x_coords, y_coords, color='gold', linewidth=3, 
                marker='o', markersize=8, markerfacecolor='gold')
    
    return img,

# 创建动画
ani = animation.FuncAnimation(
    fig, update, frames=len(history),
    interval=300, blit=False, repeat=True
)

# 保存为GIF（使用更高质量的设置）
print("正在保存GIF动画...")
writer = PillowWriter(
    fps=10,
    bitrate=1800,
    metadata={
        'title': 'A* Pathfinding',
        'artist': 'Matplotlib'
    }
)
ani.save(
    "astar_pathfinding.gif",
    writer=writer,
    dpi=100,
    savefig_kwargs={'facecolor': 'white'}
)
print("GIF动画已保存为 astar_pathfinding.gif")

# 显示动画
plt.show()