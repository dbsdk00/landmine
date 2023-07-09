import pygame
import random

pygame.init()

boardWidth = 16
boardHeight = 25
screenWidth = 400
screenHeight = 600
cursorLocationX = 0
cursorLocationY = 0
placed = False


white = ( 255, 255, 255 )
green = ( 0, 150, 0 )
red = ( 200, 0, 0 )
beige = ( 252, 231, 177 )
yellow = ( 200, 150, 0 )
black = ( 0, 0, 0 )

def createBoard(width: int, height: int, filledWith: int) -> list[list[int]]:
    return [ [ filledWith for x in range(width) ] for y in range(height) ]

board = createBoard(boardWidth, boardHeight, 0)
opened = createBoard(boardWidth, boardHeight, 0)
warned = createBoard(boardWidth, boardHeight, 0)

def printBoard(board: list[list[int]]) -> None:
    width = len(board[0])
    height = len(board)

    for y in range(height):
        for x in range(width):
            print(f"{board[y][x]:2d}", end = " ")
        print()

def placeLandMine(board: list[list[int]], ratio: int, excludeX: int, excludeY: int) -> list[list[int]]:

    width = len(board[0])
    height = len(board)

    def plus(x: int, y: int):

        for nearY in range(y - 1, y + 2):
            for nearX in range(x - 1, x + 2):
                if nearX < 0 or nearX >= width or nearY < 0 or nearY >= height: continue
                if x == nearX and y == nearY: continue
                if board[nearY][nearX] == -1: continue

                board[nearY][nearX] += 1


    for y in range(height):
        for x in range(width):
            percent = random.randint(1, 100)

            if percent > ratio: continue
            if excludeX - 1 <= x and x <= excludeX + 1 and excludeY - 1 <= y and y <= excludeY + 1: continue

            board[y][x] = -1
            plus(x, y)

    return board

def moveCursor(board: list[list[int]], x: int, y: int):
    global cursorLocationX, cursorLocationY

    width = len(board[0])
    height = len(board)

    cursorLocationX += x
    cursorLocationY += y

    if cursorLocationX < 0: cursorLocationX += width
    if cursorLocationY < 0: cursorLocationY += height

    cursorLocationX %= width
    cursorLocationY %= height

def renderBoard(board: list[list[int]], cubeSize: int, gap: int, borderWeight: int):
    global cursorLocationX, cursorLocationY

    width = len(board[0])
    height = len(board)

    for y in range(height):
        for x in range(width):
            rectValue = ( borderWeight + x * cubeSize + x * gap, borderWeight + y * cubeSize + y * gap, cubeSize, cubeSize )
            if x == cursorLocationX and y == cursorLocationY: pygame.draw.rect(displaySurface, white, ( x * cubeSize + x * gap, y * cubeSize + y * gap, cubeSize + 2 * borderWeight, cubeSize + 2 * borderWeight ))
            if opened[y][x] == 0:
                if warned[y][x] == 0: pygame.draw.rect(displaySurface, green, rectValue)
                else: pygame.draw.rect(displaySurface, yellow, rectValue)
            elif board[y][x] == -1: pygame.draw.rect(displaySurface, red, rectValue)
            else:
                pygame.draw.rect(displaySurface, beige, rectValue)
                text = font.render(str(board[y][x]), True, black)
                displaySurface.blit(text, (borderWeight + x * cubeSize + x * gap, borderWeight + y * cubeSize + y * gap))

def digBoard(board: list[list[int]], x: int, y: int):
    width = len(board[0])
    height = len(board)

    if x < 0 or x >= width or y < 0 or y >= height: return True
    if warned[y][x] == 1: return True
    if opened[y][x] == 1: 
        nearWarns = 0
        for nearY in range(y - 1, y + 2):
            for nearX in range(x - 1, x + 2):
                if nearX < 0 or nearX >= width or nearY < 0 or nearY >= height: continue
                if warned[nearY][nearX] == 1:
                    nearWarns += 1
        
        success = True

        if nearWarns != board[y][x]: return True

        for nearY in range(y - 1, y + 2):
            for nearX in range(x - 1, x + 2):
                if nearX < 0 or nearX >= width or nearY < 0 or nearY >= height: continue
                if opened[nearY][nearX] == 1: continue
                if x == nearX and y == nearY: continue
                success = success and digBoard(board, nearX, nearY)
        
        return success



    opened[y][x] = 1

    if board[y][x] == -1: return False


    hasNearLandMine = False

    for nearY in range(y - 1, y + 2):
        for nearX in range(x - 1, x + 2):
            if nearX < 0 or nearX >= width or nearY < 0 or nearY >= height: continue
            if board[nearY][nearX] == -1:
                hasNearLandMine = True
                break
    
    if hasNearLandMine: return True

    for nearY in range(y - 1, y + 2):
        for nearX in range(x - 1, x + 2):
            if x == nearX and y == nearY: continue
            digBoard(board, nearX, nearY)

    return True

def warnBoard(board: list[list[int]], x: int, y: int):
    if opened[y][x] == 1: return
    warned[y][x] += 1
    warned[y][x] %= 2

moveDelay = [ 0, 0, 0, 0, 5 ]
delay = 5
displaySurface = pygame.display.set_mode((screenWidth, screenHeight))
font = pygame.font.SysFont("arial", 15)
pygame.display.set_caption("지뢰 찾기")

running = True
clock = pygame.time.Clock()

while running:

    clock.tick(30)

    moveDelay[0] = max(moveDelay[0] - 1, 0)
    moveDelay[1] = max(moveDelay[1] - 1, 0)
    moveDelay[2] = max(moveDelay[2] - 1, 0)
    moveDelay[3] = max(moveDelay[3] - 1, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and moveDelay[0] == 0: 
        moveDelay[0] = delay
        moveCursor(board, -1, 0)
    if keys[pygame.K_RIGHT] and moveDelay[1] == 0: 
        moveDelay[1] = delay
        moveCursor(board, 1, 0)
    if keys[pygame.K_UP] and moveDelay[2] == 0: 
        moveDelay[2] = delay
        moveCursor(board, 0, -1)
    if keys[pygame.K_DOWN] and moveDelay[3] == 0: 
        moveDelay[3] = delay
        moveCursor(board, 0, 1)

    if not keys[pygame.K_LEFT]: moveDelay[0] = 0
    if not keys[pygame.K_RIGHT]: moveDelay[1] = 0
    if not keys[pygame.K_UP]: moveDelay[2] = 0
    if not keys[pygame.K_DOWN]: moveDelay[3] = 0

    if keys[pygame.K_RETURN]:
        if not placed: 
            placeLandMine(board, 15, cursorLocationX, cursorLocationY)
            placed = True
        success = digBoard(board, cursorLocationX, cursorLocationY)
        if not success:
            for y in range(boardHeight):
                for x in range(boardWidth):
                    if board[y][x] == -1: opened[y][x] = 1
            
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and moveDelay[4] == 0:
        moveDelay[4] = 1
        warnBoard(board, cursorLocationX, cursorLocationY)
    if not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]): moveDelay[4] = 0

    displaySurface.fill(( 0, 0, 0 ))
    renderBoard(board, 20, 2, 2)
    pygame.display.update()

pygame.quit()