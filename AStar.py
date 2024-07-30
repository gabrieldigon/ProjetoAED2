class Node:
    def __init__(self, name, neighbors=None):
        self.name = name
        self.neighbors = neighbors or {}
        self.g = float('inf')  # Custo di inicio ate o no
        self.h = float('inf')  # Heurística 
        self.f = float('inf')  # g + h
        self.parent = None  

    def __lt__(self, other):
        return self.f < other.f
# Nossa heuristica pro A&
def heuristic(node, goal):
    
    return abs(goal[0] - node[0]) + abs(goal[1] - node[1])
#heap para implementar o A*
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
# Função que transforma as coordenadas do grid em um grafo pra poder utilizar o A*
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
# Implementação do A*
def a_star(start, goal,nodes):
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


