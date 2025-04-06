import heapq

def h(state):
    dist = 0
    for i in range(9):
        if state[i] != 'x':
            num = int(state[i]) - 1
            target_x, target_y = num // 3, num % 3
            x, y = i // 3, i % 3
            dist += abs(x - target_x) + abs(y - target_y)
    return dist

def astar(start):
    dist, prev = {}, {}
    heap = []
    dist[start] = 0
    heapq.heappush(heap, (h(start), start))
    end="12345678x"
    directions = [(-1, 0, 'u'), (0, 1, 'r'), (1, 0, 'd'), (0, -1, 'l')]

    while heap:
        _, state = heapq.heappop(heap)

        if state == end:
            break

        idx = state.index('x')
        x, y = idx // 3, idx % 3
        for dx,dy,moves in directions:
            a, b = x + dx, y + dy
            if 0 <= a < 3 and 0 <= b < 3:
                nx_index = a * 3 + b
                x_index = x * 3 + y
                state_list = list(state)
                state_list[x_index], state_list[nx_index] = state_list[nx_index], state_list[x_index]
                new_state = ''.join(state_list)
                
                if new_state not in dist or dist[new_state] > dist[state] + 1:
                    dist[new_state] = dist[state] + 1
                    prev[new_state] = (moves, state)
                    heapq.heappush(heap, (dist[new_state] + h(new_state), new_state))

    road, current = "", end
    while current != start:
        if current in prev:
            move, prev_state = prev[current]
            road += move
            current = prev_state
        else:
            return "unsolvable"
    
    return road[::-1]  

def countin(co):
    count = 0
    for i in range(8):  
        for j in range(i + 1, 8):
            if co[i] > co[j]:
                count += 1
    return count

li = input().split()
start = ''.join(li)
co = start.replace('x', '') 
inv_count = countin(co)

if inv_count % 2 == 0:
    print(astar(start))
else:
    print("unsolvable")
