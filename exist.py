def countin(co):
    count = 0
    for i in range(8):  
        for j in range(i + 1, 8):
            if co[i] > co[j]:
                count += 1
    return count

li = input().split()
li.remove('x')  
incount = countin(li)
if incount % 2 == 0:
    print(1)
else:
    print(0)