def fpath(n, edges):
    queue = [1] 
    juli = {}
    for i in range(1, n + 1):
        juli[i] = -1        
    juli[1] = 0 

    while queue:
        node = queue.pop(0) 
        for neighbor in edges[node]:  
            if juli[neighbor] == -1:  
                juli[neighbor] = juli[node] + 1 
                queue.append(neighbor)  
    return juli[n] 


n, m = map(int, input().split())

if n == 0:
    print(-1)
else:
    edges = {}
    for i in range(1, n + 1):
        edges[i] = []
    for i in range(m):
        a, b = input().split()
        a, b = int(a), int(b)
        edges[a].append(b)
    print(fpath(n, edges))
