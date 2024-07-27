import pygame
import random

# Configurações
CELL_SIZE = 30
GRID_SIZE = 11
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Node:
    def __init__(self, name, neighbors=None):
        self.name = name
        self.neighbors = neighbors or {}
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def generate_maze(height, width):
    maze = [[0 for _ in range(width)] for _ in range(height)]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    
    def in_bounds(y, x):
        return 0 <= y < height and 0 <= x < width
    
    def get_neighbors(y, x):
        neighbors = []
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if in_bounds(ny, nx) and maze[ny][nx] == 0:
                neighbors.append((ny, nx))
        return neighbors
    
    def carve_maze(y, x):
        maze[y][x] = 1
        neighbors = get_neighbors(y, x)
        random.shuffle(neighbors)
        for ny, nx in neighbors:
            if maze[ny][nx] == 0:
                maze[(y + ny) // 2][(x + nx) // 2] = 1
                carve_maze(ny, nx)
    
    start_y, start_x = 1, 1
    carve_maze(start_y, start_x)
    
    return maze

def draw_maze(window, maze, path=None):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = WHITE if maze[y][x] == 1 else BLACK
            pygame.draw.rect(window, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    if path:
        for (y, x) in path:
            pygame.draw.rect(window, GREEN, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def create_graph_from_maze(maze):
    height = len(maze)
    width = len(maze[0]) if height > 0 else 0
    nodes = {}
    
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                node_name = (y, x)
                nodes[node_name] = Node(node_name)
    
    for (y, x), node in nodes.items():
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if (ny, nx) in nodes:
                node.neighbors[(ny, nx)] = 1
    
    return nodes

def heuristic(node, goal):
    return abs(goal[0] - node[0]) + abs(goal[1] - node[1])

def min_heapify(a, heap_size, i):
    l = 2 * i + 1
    r = 2 * i + 2
    smallest = i

    if l < heap_size and a[l].f < a[i].f:
        smallest = l

    if r < heap_size and a[r].f < a[smallest].f:
        smallest = r

    if smallest != i:
        a[i], a[smallest] = a[smallest], a[i]
        min_heapify(a, heap_size, smallest)

def build_min_heap(a):
    heap_size = len(a)
    for i in range(heap_size // 2 - 1, -1, -1):
        min_heapify(a, heap_size, i)

def extract_min(heap):
    min_elem = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    min_heapify(heap, len(heap), 0)
    return min_elem

def a_star(start, goal, nodes):
    open_list = [start]
    closed_list = set()

    start.g = 0
    start.h = heuristic(start.name, goal.name)
    start.f = start.g + start.h

    while open_list:
        build_min_heap(open_list)
        current_node = extract_min(open_list)

        if current_node.name == goal.name:
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return path[::-1]

        closed_list.add(current_node)

        for neighbor_name, cost in current_node.neighbors.items():
            neighbor = nodes[neighbor_name]
            if neighbor in closed_list:
                continue

            tentative_g = current_node.g + cost

            if tentative_g < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor.name, goal.name)
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Maze Solver")
    
    maze = generate_maze(GRID_SIZE, GRID_SIZE)
    nodes = create_graph_from_maze(maze)
    
    start = nodes.get((1, 1))
    goal = nodes.get((GRID_SIZE - 2, GRID_SIZE - 2))

    if not start or not goal:
        raise ValueError("Ponto inicial ou objetivo não estão no labirinto!")

    path = a_star(start, goal, nodes)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        window.fill(BLACK)
        draw_maze(window, maze, path)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
