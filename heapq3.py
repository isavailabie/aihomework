import heapq

def fpath(n, edges):
    queue = [(0, 1)] 
    juli = {}
    for i in range(1, n + 1):
        juli[i] = -1        
    juli[1] = 0 

    while queue:
        dist, node = heapq.heappop(queue) 
        for neighbor, weight in edges[node]:  
            if juli[neighbor] == -1 or dist + weight < juli[neighbor]:  
                juli[neighbor] = dist + weight 
                heapq.heappush(queue, (juli[neighbor], neighbor))  
    return juli[n]



n, m = map(int, input().split())
graph = {}
for i in range(1, n + 1):
    graph[i] = []
for _ in range(m):
    a, b, w = map(int, input().split())
    graph[a].append((b, w))

print(fpath(n, graph))