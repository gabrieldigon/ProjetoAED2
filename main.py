import pygame
import AStar
import suportingFile
from random import choice
# Definindo o tamanho do grid e o tamanho das celulas, pode aumentar o tamanho do grid mas o ideal e que seja multiplo de 50
RES = WIDTH, HEIGHT = 900, 900
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE
# Carregando as imagens
character = pygame.image.load(suportingFile.characters.codibentinho.value)
character = pygame.transform.scale(character, (TILE - 2, TILE - 2))

endGame = pygame.image.load(suportingFile.characters.Estrela.value)
endGame = pygame.transform.scale(endGame, (TILE - 2, TILE - 2))

# definicao da classe de celula e suas funções de apoio
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {suportingFile.orientation.top.value: True, suportingFile.orientation.right.value: True,
                        suportingFile.orientation.bottom.value: True, suportingFile.orientation.left.value: True}
        self.visited = False
    
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        sc.blit(character, (x + 2, y + 2))
    
    def draw_end(self):
        x, y = self.x * TILE, self.y * TILE
        sc.blit(endGame, (x + 2, y + 2))
        
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color(suportingFile.Color.backgroundColor.value),
                             (x, y, TILE, TILE))
        if self.walls[suportingFile.orientation.top.value]:
            pygame.draw.line(sc, pygame.Color(suportingFile.Color.lineColor.value), 
                             (x, y), (x + TILE, y), 6)
        if self.walls[suportingFile.orientation.right.value]:
            pygame.draw.line(sc, pygame.Color(suportingFile.Color.lineColor.value), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 6)
        if self.walls[suportingFile.orientation.bottom.value]:
            pygame.draw.line(sc, pygame.Color(suportingFile.Color.lineColor.value), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 6)
        if self.walls[suportingFile.orientation.left.value]:
            pygame.draw.line(sc, pygame.Color(suportingFile.Color.lineColor.value), 
                             (x, y + TILE), (x, y), 6)
            
    def check_cell(self, x, y):
        
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        
        return grid_cells[find_index(x, y)] 
    # checa os vizinhos pra atualizar a stack
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
# Remove as paredes na hora do backtracking
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls[suportingFile.orientation.left.value] = False
        next.walls[suportingFile.orientation.right.value] = False
    elif dx == -1:
        current.walls[suportingFile.orientation.right.value] = False
        next.walls[suportingFile.orientation.left.value] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls[suportingFile.orientation.top.value] = False
        next.walls[suportingFile.orientation.bottom.value] = False
    elif dy == -1:
        current.walls[suportingFile.orientation.bottom.value] = False
        next.walls[suportingFile.orientation.top.value] = False 

# Reseta o jogo deinindo as variaveis pra posicoes iniciais e refazendo o grid
def reset_game_state():
    global grid_cells, current_cell, stack, colors, color, maze_array,path,end_place
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    end_place = grid_cells[323]
    stack = []
    colors, color = [], 10
    path = []

def drawAStarPath(path):
    for step in path:
            x, y = step
            pygame.draw.rect(sc, pygame.Color(suportingFile.Color.pathColor.value),
                             (x * TILE + TILE // 4, y * TILE + TILE // 4,
                              TILE // 2, TILE // 2))
    
    pygame.display.flip()
    clock.tick(30)
    
# Logica do jogo

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption('Maze generator')
clock = pygame.time.Clock()
reset_game_state() 
posicaoNoGrid = 0
shouldShowPath = False

while True:
    sc.fill(pygame.Color(suportingFile.Color.backgroundColor.value))
    
    # Movimentação e controles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game_state()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            if current_cell.walls[suportingFile.orientation.right.value] == False:
                posicaoNoGrid += 1
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            if current_cell.walls[suportingFile.orientation.left.value] == False:
                posicaoNoGrid -= 1
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            if current_cell.walls[suportingFile.orientation.top.value] == False:
                posicaoNoGrid -= 18
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if current_cell.walls[suportingFile.orientation.bottom.value] == False:
                posicaoNoGrid += 18
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if shouldShowPath:
                shouldShowPath = False
            else:
                shouldShowPath = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            character = pygame.image.load(suportingFile.characters.Professor.value)
            character = pygame.transform.scale(character, (TILE - 2, TILE - 2))
    # começo da logica do DFS apos o resetGameState()
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    end_place.draw_end()
    
    [pygame.draw.rect(sc, colors[i], 
                      (cell.x * TILE + 2, cell.y * TILE + 2,
                       TILE - 1, TILE - 1), border_radius=8) for i,
                       cell in enumerate(stack)] 
    
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 0, 103))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell=next_cell
    elif stack: 
        current_cell = stack.pop()

    # Se o algoritmo de geração acabou ou seja se n tem nada na stack ,gere um grafo e descubra se existe um caminho

    if not stack  :
        nodes = AStar.create_graph_from_maze(grid_cells)
        start = nodes[(0, 0)]
        goal = nodes[(cols - 1, rows - 1)]
        path = AStar.a_star(start, goal,nodes)
    # Se a tecla for apertada mostre o caminho
    if shouldShowPath:
        drawAStarPath(path)

    # Uma otima maneira de enxergar o dfs em ação e limitar o fps pra 1
    pygame.display.flip()
    clock.tick(60) 