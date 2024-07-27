import random

# Tamanhos do labirinto
WIDTH, HEIGHT = 10, 10

# Definição das direções (N, S, E, W)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def create_maze(width, height):
    # Inicializa a matriz do labirinto com paredes (True para paredes)
    maze = [[True for _ in range(width)] for _ in range(height)]

    # Função recursiva para realizar a DFS
    def dfs(x, y):
        # Marca a célula atual como visitada (remove a parede)
        maze[y][x] = False

        # Embaralha as direções para garantir a aleatoriedade
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx]:
                maze[y + dy][x + dx] = False  # Remove a parede entre as células
                dfs(nx, ny)  # Visita a próxima célula

    # Inicia o DFS a partir de um ponto aleatório
    start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
    dfs(start_x, start_y)
    
    return maze

# Função para imprimir o labirinto
def print_maze(maze):
    for row in maze:
        print("".join("█" if cell else " " for cell in row))

# Gera e imprime o labirinto
maze = create_maze(WIDTH, HEIGHT)
print_maze(maze)
