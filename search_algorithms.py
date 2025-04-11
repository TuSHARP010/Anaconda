import random
from collections import deque
import heapq

# Directions (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Random movement algorithm (limited moves)
def random_move(start, goal, obstacles, rows, cols):
    path = []
    current = start
    for _ in range(1000):  # Limit to 1000 moves
        direction = random.choice(DIRECTIONS)
        new_pos = (current[0] + direction[0], current[1] + direction[1])
        if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and new_pos not in obstacles:
            path.append(direction)
            current = new_pos
        if current == goal:
            return path
    return []  # If it takes too long, return empty path

# Breadth First Search (BFS)
def bfs(start, goal, obstacles, rows, cols):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in obstacles:
                queue.append(((new_x, new_y), path + [(dx, dy)]))
    return []

# Depth First Search (DFS)
def dfs(start, goal, obstacles, rows, cols):
    stack = [(start, [])]
    visited = set()
    while stack:
        (x, y), path = stack.pop()
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in obstacles:
                stack.append(((new_x, new_y), path + [(dx, dy)]))
    return []

# Iterative Deepening Search (IDS)
def dls(start, goal, obstacles, rows, cols, depth_limit, visited):
    stack = [(start, [], 0)]
    while stack:
        (x, y), path, depth = stack.pop()
        if (x, y) == goal:
            return path
        if depth >= depth_limit or (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in obstacles:
                stack.append(((new_x, new_y), path + [(dx, dy)], depth + 1))
    return None

def ids(start, goal, obstacles, rows, cols, max_depth=50):
    for depth in range(max_depth):
        visited = set()
        result = dls(start, goal, obstacles, rows, cols, depth, visited)
        if result is not None:
            return result
    return []

# Uniform Cost Search (UCS)
def ucs(start, goal, obstacles, rows, cols):
    priority_queue = [(0, start, [])]
    visited = {}
    while priority_queue:
        cost, (x, y), path = heapq.heappop(priority_queue)
        if (x, y) == goal:
            return path
        if (x, y) in visited and visited[(x, y)] <= cost:
            continue
        visited[(x, y)] = cost
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in obstacles:
                heapq.heappush(priority_queue, (cost + 1, (new_x, new_y), path + [(dx, dy)]))
    return []

# Heuristic function (Manhattan Distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Greedy Best First Search
def greedy_bfs(start, goal, obstacles, rows, cols):
    priority_queue = [(heuristic(start, goal), start, [])]
    visited = set()
    while priority_queue:
        _, (x, y), path = heapq.heappop(priority_queue)
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in obstacles:
                heapq.heappush(priority_queue, (heuristic((new_x, new_y), goal), (new_x, new_y), path + [(dx, dy)]))
    return []

# A* Search
def astar(start, goal, obstacles, rows, cols):
    priority_queue = [(0, 0, start, [])]  # (total_cost, path_cost, position, path)
    visited = {}
    while priority_queue:
        total_cost, path_cost, (x, y), path = heapq.heappop(priority_queue)
        if (x, y) == goal:
            return path
        if (x, y) in visited and visited[(x, y)] <= path_cost:
            continue
        visited[(x, y)] = path_cost
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x, new_y) not in obstacles:
                new_path_cost = path_cost + 1
                new_total_cost = new_path_cost + heuristic((new_x, new_y), goal)
                heapq.heappush(priority_queue, (new_total_cost, new_path_cost, (new_x, new_y), path + [(dx, dy)]))
    return []
