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

if n == 0:
    print(-1)
else:
    edges = {}
    for i in range(1, n + 1):
        edges[i] = []
    for i in range(m):
        a,b,c= input().split()
        a,b ,c= int(a), int(b), int(c)
        edges[a].append((b,c))
    print(fpath(n, edges))