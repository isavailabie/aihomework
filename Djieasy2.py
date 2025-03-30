def fpath(n, graph):
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[1] = 0  
    vis = [0] * (n + 1)  
    
    for _ in range(n):
        # find 最近的点
        u = -1
        for i in range(1, n + 1):
            if not vis[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if dist[u] == INF:
            break
        
        vis[u] = True  
        # relax
        for v, w in graph[u]:
            dist[v] = min(dist[v], dist[u] + w)

    return dist[n] if dist[n] != INF else -1

n, m = map(int, input().split())
graph = {}
for i in range(1, n + 1):
    graph[i] = []
for _ in range(m):
    a, b, w = map(int, input().split())
    graph[a].append((b, w))

print(fpath(n, graph))
