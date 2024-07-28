import pygame
from random import choice

# Maze generation settings
RES = WIDTH, HEIGHT = 900, 900
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#228b22'),
                         (x + 2, y + 2, TILE - 2, TILE - 2))
        
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#FFFFFF'),
                             (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#000000'), 
                             (x, y), (x + TILE, y), 6)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#000000'), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 6)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#000000'), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 6)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#000000'), 
                             (x, y + TILE), (x, y), 6)
            
    def check_cell(self, x, y):
        
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        
        return grid_cells[find_index(x, y)] 
    
    def check_neighbors(self):
        neighbors = []
        
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        
        return choice(neighbors) if neighbors else False   
    
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False 

def reset_game_state():
    global grid_cells, current_cell, stack, colors, color, path
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 10
    path = []

# Logic for A* algorithm
class Node:
    def __init__(self, name, neighbors=None):
        self.name = name
        self.neighbors = neighbors or {}
        self.g = float('inf')  # Cost from start to this node
        self.h = float('inf')  # Heuristic cost from this node to goal
        self.f = float('inf')  # g + h
        self.parent = None  # For path reconstruction

    def __lt__(self, other):
        return self.f < other.f

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
            return path[::-1]  # Inverting the path

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

    return None  # If there is no path

def create_graph_from_maze(grid_cells):
    nodes = {}
    for cell in grid_cells:
        name = (cell.x, cell.y)
        neighbors = {}
        if not cell.walls['top']:
            neighbors[(cell.x, cell.y - 1)] = 1
        if not cell.walls['right']:
            neighbors[(cell.x + 1, cell.y)] = 1
        if not cell.walls['bottom']:
            neighbors[(cell.x, cell.y + 1)] = 1
        if not cell.walls['left']:
            neighbors[(cell.x - 1, cell.y)] = 1
        nodes[name] = Node(name, neighbors)
    return nodes

# Initialize pygame and create maze
pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption('Maze generator')
clock = pygame.time.Clock()
reset_game_state()

posicaoNoGrid = 0
path = []

while True:
    sc.fill(pygame.Color('#FFFFFF'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game_state()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if current_cell.walls["right"] == False:
                posicaoNoGrid += 1
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            if current_cell.walls["left"] == False:
                posicaoNoGrid -= 1
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            if current_cell.walls["top"] == False:
                posicaoNoGrid -= cols
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if current_cell.walls["bottom"] == False:
                posicaoNoGrid += cols
                current_cell = grid_cells[posicaoNoGrid]

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 0, 103))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    # Run A* and draw path once maze generation is complete
    if not stack and not next_cell and not path:
        nodes = create_graph_from_maze(grid_cells)
        start = nodes[(0, 0)]
        goal = nodes[(cols - 1, rows - 1)]
        path = a_star(start, goal,nodes)
        if path:
            print("Path found:", path)
        else:
            print("No path found")

    # Draw the path found by A* algorithm
    if path:
        for step in path:
            x, y = step
            pygame.draw.rect(sc, pygame.Color('#FF0000'),
                             (x * TILE + TILE // 4, y * TILE + TILE // 4,
                              TILE // 2, TILE // 2))

    pygame.display.flip()
    clock.tick(30)  # Adjusted frame rate
