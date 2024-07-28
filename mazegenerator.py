import pygame
import AStar
from random import choice

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
    global grid_cells, current_cell, stack, colors, color, maze_array,path 
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 10
    path = []

def drawAStarPath(path):
    for step in path:
            x, y = step
            pygame.draw.rect(sc, pygame.Color('#FF0000'),
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

while True:
    sc.fill(pygame.Color('#FFFFFF'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
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
                posicaoNoGrid -= 18
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if current_cell.walls["bottom"] == False:
                posicaoNoGrid += 18
                current_cell = grid_cells[posicaoNoGrid]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if path:
                drawAStarPath(path)

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
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

    if not stack and not next_cell and not path:
        nodes = AStar.create_graph_from_maze(grid_cells)
        start = nodes[(0, 0)]
        goal = nodes[(cols - 1, rows - 1)]
        path = AStar.a_star(start, goal,nodes)
        if path:
            print("Path found:", path)
        else:
            print("No path found")

    pygame.display.flip()
    clock.tick(30) 