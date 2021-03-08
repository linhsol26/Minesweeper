# pygame version to create UI
import pygame
import random
pygame.init()

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
grey = pygame.Color(200, 200, 200)
white = (255, 255, 255)

size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mine Sweeper')
gameState = 0
running = False
clock = pygame.time.Clock()
font = pygame.font.Font("HighlandGothicFLF.ttf", 20)
mouse_state = 0
mouse_x = 0
mouse_y = 0

class Box():
    def __init__(self):
        textBoxes = {}

    def showInfo():
        global gameState
        pygame.draw.rect(screen, grey, (0, 0, 500, 100))
        pygame.draw.line(screen, black, (0, 100), (500, 400), 4)

        if gameState == 0:
            text = font.render('Mines: ' + str(board.mine), True, white)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, 150 - (text_x / 2), 50 - (text_y / 2))
        elif gameState == 1:
            text = font.render('Win!' + str(board.mine), True, white)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, 150 - (text_x / 2), 50 - (text_y / 2))
        else:
            text = font.render('Lose!' + str(board.mine), True, white)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, 150 - (text_x / 2), 50 - (text_y / 2))

    def clickedIn(self, x, y, w, h):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x >= x and mouse_x <= (x + w) and mouse_y >= y and mouse_y <= (y + h): return True

    def clickedOut(self, x, y, w, h):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x < x or mouse_state == 1 and mouse_x > (x + w) or mouse_state == 1 and mouse_y < y or mouse_state == 1 and mouse_y > (y + h): return True
    

class Tile():
    def __init__(self, x, y, rows, cols):
        self.rows = rows
        self.cols = cols
        self.x = (x * (size[0] / self.cols))
        self.y = (y * ((size[1] - 100) / self.rows)) + 100
        self.mine = False
        self.neighbors = 0
        self.visible = False

    def update(self):
        global gameState
        if gameState == 0:
            if mouse_state == 1 and mouse_x >= self.x and mouse_x <= (self.x + (size[0] / self.columns)) and mouse_y >= self.y and mouse_y <= (self.y + ((size[1] - 100) / self.rows)):
                self.visible = True
            if self.visible == True and self.mine == True:
                gameState = 2

    def show(self):
        if self.visible == True:
            if self.mine == False:
                pygame.draw.rect(screen,GREY,(self.x, self.y, (size[0] / self.cols), ((size[1] - 100) / self.rows)))
                if self.neighbors > 0:
                    text = font.render(str(self.neighbors),True,BLACK)
                    text_x = text.get_rect().width
                    text_y = text.get_rect().heigh
                    screen.blit(text, ((self.x + ((size[0] / self.cols) / 2) - (text_x / 2)), (self.y + (((size[1] - 100) / self.rows) / 2) - (text_y / 2))))
            elif self.mine == True:
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
        self.numOfVisible = 0

        #create board 
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(Tile(j, i, self.cols, self.rows))
            
        #plant bombs
        while self.numOfMines < self.mine:
            self.mineLocation = [random.randrange(self.cols), random.randrange(self.rows)]
            if self.board[self.mineLocation[1]][self.mineLocation[0]] == False:
                self.mines.append(self.mineLocation)
                self.board[self.mineLocation[1]][self.mineLocation[0]] = True
            self.numOfMines = len(self.mines)
        
        # calc neighbors
        for i in range(self.rows):
            for j in range(self.cols):
                self.numOfNeighbors = 0
                if i > 0 and j > 0:
                    if self.board[i - 1][j - 1].mine == True:
                        self.numOfNeighbors += 1
                if i > 0:
                    if self.board[i - 1][j].mine == True:
                        self.numOfNeighbors += 1
                if i > 0 and j < (self.cols - 1):
                    if self.board[i - 1][j + 1].mine == True:
                        self.numOfNeighbors += 1
                if j > 0:
                    if self.board[i][j - 1].mine == True:
                        self.numOfNeighbors += 1
                if j < (self.cols - 1):
                    if self.board[i][j + 1].mine == True:
                        self.numOfNeighbors += 1
                if i < (self.rows - 1) and j > 0:
                    if self.board[i + 1][j - 1].mine == True:
                        self.numOfNeighbors += 1
                if j < (self.rows - 1):
                    if self.board[i + 1][j].mine == True:
                        self.numOfNeighbors += 1
                if i < (self.cols - 1) and j < (self.rows - 1):
                    if self.board[i + 1][j + 1].mine == True:
                        self.numOfNeighbors += 1
                self.board[i][j].neighbors = self.numOfNeighbors

    def update(self):
        global gameState
        self.numOfVisible = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].update()
                if self.board[i][j].neighbors == 0 and self.board[i][j].visible == True:
                    if i > 0 and j > 0:
                        self.board[i - 1][j - 1].visible = True
                    if i > 0:
                        self.board[i - 1][j].visible = True
                    if i > 0 and j < (self.cols - 1):
                        self.board[i - 1][j + 1].visible = True
                    if j > 0:
                        self.board[i][j - 1].visible = True
                    if j < (self.cols - 1):
                        self.board[i][j + 1].visible = True
                    if j > 0 and i < (self.rows - 1):
                        self.board[i + 1][j - 1].visible = True
                    if i < (self.rows - 1):
                        self.board[i + 1][j].visible = True
                    if j < (self.columns - 1) and i < (self.rows - 1):
                        self.board[i + 1][j + 1].visible = True
                if self.board[i][j].visible == True:
                    self.numOfVisible += 1
        if self.numOfVisible == ((self.cols * self.rows) - self.numOfMines):
            gameState = 1
        if gameState == 1:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.board[i][j].visible = True

    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].show()

board = Board(10, 10, 5)
box = Box()

while not running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_state = event.button
            pygame.mouse.set_pos(mouse_x, mouse_y + 1)
        else: mouse_state = 0
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    if gameState >= 0 and gameState <= 2:
        showInfo()
        board.update()
        board.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()


