from collections import deque

q = deque()

q.append(1)
q.append(2)
q.append(3)

print(q)

print(q.popleft())

q.appendleft(1)
q.appendleft(2)
q.appendleft(3)

print(q)

print(q.pop())