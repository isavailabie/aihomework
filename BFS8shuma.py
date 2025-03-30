def bfs(start):
    queue = [(start, 0)]  
    states_list = {start}

    front = 0
    while front < len(queue):
        state, steps = queue[front]
        front += 1

        if state == "12345678x":
            return steps 
        
        x_index = state.index('x')
        xx = x_index // 3  
        xy = x_index % 3
        state_list = list(state) 
        change = [(-1, 0), (1, 0), (0, -1), (0, 1)]     
        for dx, dy in change:
            newx, newy = xx + dx, xy + dy
            if 0 <= newx < 3 and 0 <= newy < 3: 
                new_x = newx * 3 + newy
                state_list[x_index], state_list[new_x] = state_list[new_x], state_list[x_index]
                new_state = ''.join(state_list) 

                if new_state not in states_list:
                    states_list.add(new_state)
                    queue.append((new_state, steps + 1))  
                state_list[x_index], state_list[new_x] = state_list[new_x], state_list[x_index]

    return -1


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
    print(bfs(start))
else:
    print("-1")


