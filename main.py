import pygame
pygame.init()

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
grey = pygame.Color(200, 200, 200)
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mine Sweeper')

running = True
gameState = -1

mouse_state = 0
mouse_x = 0
mouse_y = 0

class Box():
    def __init__(self):
        textBoxes = {}

    def clickedIn(self, x, y, w, h):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x >= x and mouse_x <= (x + w) and mouse_y >= y and mouse_y <= (y + h): return True
        return False

    def hovering(self, x, y, w, h):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x >= x and mouse_x <= (x + w) and mouse_y >= y and mouse_y <= (y + h): return True

class Tile():
    def __init__(self, x, y, rows, cols):
        self.rows = rows
        self.cols = cols
        self.x = (x * (size[0] / self.cols))
        self.y = (y * ((size[1] - 100) / self.rows)) + 100
        self.mine = False
        self.neighbors = 0

    def show(self):
        if self.mine == True:
            pygame.draw.rect(screen, red, (self.x, self.y, (size[0] / self.cols), ((size[1] - 100) / self.rows)))
        else:
            pygame.draw.rect(screen, grey, (self.x, self.y, (size[0] / self.cols),((size[1] - 100) / self.rows)), 2)


class Board():
    def __init__ (self, cols, rows, mine):
        self.cols = cols
        self.rows = rows
        self.mine = mine
        self.board = []
        self.mines = []
        self.numOfMines = len(self.mines)
        self.numOfNeighbors = 0
        self.foundedMines = 0

    def createBoard(self):
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(Tile(i, j, self.cols, self.rows))

    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].show()

board = Board(5, 5, 5)

while running:
    board.createBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    board.draw()
    pygame.display.flip()

pygame.quit()


