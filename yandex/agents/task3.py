def optimal_path():
    from collections import deque

    n, k = map(int, input().split())

    allowed = [False] * (n + 1)
    allowed[0] = True

    if k > 0:
        platforms = list(map(int, input().split()))
        for x in platforms:
            allowed[x] = True

    allowed[n] = True

    dist = [-1] * (n + 1)
    parent = [-1] * (n + 1)
    step = [''] * (n + 1)

    q = deque([0])
    dist[0] = 0

    while q:
        x = q.popleft()

        for jump in (1, 2):
            nx = x + jump
            if nx <= n and allowed[nx] and dist[nx] == -1:
                dist[nx] = dist[x] + 1
                parent[nx] = x
                step[nx] = str(jump)
                q.append(nx)

    if dist[n] == -1:
        print(-1)
        return

    ans = []
    cur = n
    while cur != 0:
        ans.append(step[cur])
        cur = parent[cur]

    print(dist[n])
    print(''.join(reversed(ans)))
optimal_path()