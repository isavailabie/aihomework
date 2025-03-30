import heapq

def dijkstra(start):
    target = "12345678x"
    states = set()  
    pq = [(0, start)]  

    while pq:
        steps, state = heapq.heappop(pq)
        
        if state == target:
            return steps  

        xx = state.index('x')
        x, y = xx // 3, xx % 3
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                np = nx * 3 + ny
                new_state = list(state)
                new_state[xx], new_state[np] = new_state[np], new_state[xx] 
                new_state = ''.join(new_state)  

                if new_state not in states:  
                    states.add(new_state) 
                    heapq.heappush(pq, (steps + 1, new_state))

    return -1  

start = input().replace(" ", "")
print(dijkstra(start))
