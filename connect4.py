import numpy as np
import pygame
import sys
import math

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT =6
COLUMN_COUNT =7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def valid_location(board, column):
    return board[5][column] == 0

def get_next_open_row(board, column):
    for r in range(ROW_COUNT):
        if board[r][column] ==0:
            return r

def print_board(board):
     print(np.flip(board,0))
     
### REFACTOR FOR A MORE REUSABLE CODE
def winning_move(bord,piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    #verical check for winning move

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    #SLope Diagnols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

   #Negative slope Diagnols
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) )
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)),RADIUS )
            
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
           if board[r][c] == 1: 
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE + SQUARE_SIZE/2),height- int(r*SQUARE_SIZE + SQUARE_SIZE/2)),RADIUS )
           elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), height - int(r*SQUARE_SIZE +  SQUARE_SIZE/2)),RADIUS )
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn=0
pygame.init()

SQUARE_SIZE = 100
#Screen width
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
RADIUS = int((SQUARE_SIZE / 2) - 5)
size = (width,height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

### Main game LOOP
##
#
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #drawing based on position in the game
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn ==0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
            #Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx/SQUARE_SIZE))
                
                if valid_location(board,column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)

                    if winning_move(board,1):
                        label = myfont.render("Player 1 Wins", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

            #Ask for Player 2 Input
            else:
                posx = event.pos[0]
                column = int(math.floor(posx/SQUARE_SIZE))

                if valid_location(board,column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 2)

                    if winning_move(board,2):
                        label = myfont.render("Player 2 Wins", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True
            
            print_board(board)
            draw_board(board)
            turn +=1 
            turn = turn%2

            if game_over:
                pygame.time.wait(3000)