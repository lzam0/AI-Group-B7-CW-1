def path_IDDFS(start, end):
    from collections import deque
    if start.numHingers() > 0 or end.numHingers() > 0:
        return None
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        for neighbor in current.moves():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None
    

def path_astar(start,end):
    import heapq
    if start.numHingers() > 0 or end.numHingers() > 0:
        return None

    open_list = []
    heapq.heappush(open_list, (0, 0, start, [start]))  # (f, g, state, path)
    g_score = {start: 0}
    visited = set()

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            return path

        for next_state in current.moves():
            if next_state and next_state.numHingers() == 0:
                tentative_g = g + 1
                h = next_state.mDist(end)
                f_score = tentative_g + h

                if next_state not in g_score or tentative_g < g_score[next_state]:
                    g_score[next_state] = tentative_g
                    heapq.heappush(open_list, (f_score, tentative_g, next_state, path + [next_state]))

    return None



def tester():
    pass