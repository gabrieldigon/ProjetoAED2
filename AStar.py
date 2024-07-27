class Node:
    def __init__(self, name, neighbors=None):
        self.name = name
        self.neighbors = neighbors or {}
        self.g = float('inf')  # Custo do início até este nó
        self.h = float('inf')  # Heurística estimada do nó até o objetivo
        self.f = float('inf')  # g + h
        self.parent = None  # Para reconstruir o caminho

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal):
    # Usando a distância de Manhattan como exemplo de heurística
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

def a_star(start, goal):
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
            return path[::-1]  # Invertendo o caminho

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

    return None  # Se não houver caminho

# Exemplo de uso:
start = Node((0, 0), neighbors={(1, 0): 1, (0, 1): 1})
goal = Node((2, 2))

# Configurando o grafo:
nodes = {
    (0, 0): start,
    (1, 0): Node((1, 0), neighbors={(2, 0): 1}),
    (0, 1): Node((0, 1), neighbors={(0, 2): 1}),
    (2, 0): Node((2, 0), neighbors={(2, 1): 1}),
    (0, 2): Node((0, 2), neighbors={(1, 2): 1}),
    (2, 1): Node((2, 1), neighbors={(2, 2): 1}),
    (1, 2): Node((1, 2), neighbors={(2, 2): 1}),
    (2, 2): goal
}

# Ligando os nós
start.neighbors[(1, 0)] = 1
start.neighbors[(0, 1)] = 1
nodes[(1, 0)].neighbors[(2, 0)] = 1
nodes[(0, 1)].neighbors[(0, 2)] = 1
nodes[(2, 0)].neighbors[(2, 1)] = 1
nodes[(0, 2)].neighbors[(1, 2)] = 1
nodes[(2, 1)].neighbors[(2, 2)] = 1
nodes[(1, 2)].neighbors[(2, 2)] = 1

# Executando o algoritmo
caminho = a_star(start, goal)
print("Caminho encontrado:", caminho)
