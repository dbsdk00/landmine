import random
import pygame

pygame.init()

clock = pygame.time.Clock()

green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 30, True, False)

screenWidth = 400
screenHeight = 600
iconSize = 20
gap = 3
first = True

displaySurface = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("지뢰찾기 게임")
displaySurface.fill(black)

width = 10
height = 10
ratio = 30

locationX = 0
locationY = 0

land = [[0 for x in range(width)] for y in range(height)]
opened = [[0 for x in range(width)] for y in range(height)]

def move(x, y):
    global locationX, locationY

    locationX += x
    locationY += y

    if locationX < 0: locationX = width - 1
    if locationY < 0: locationY = height - 1

    locationX %= width
    locationY %= height

def mine(x, y):
    opened[y][x] = 1

def printMap(map):
    for y in range(height):
        for x in range(width):
            if opened[y][x] == 0:
                pygame.draw.rect(displaySurface, white if x == locationX and y == locationY else green, (x * iconSize + x * gap, y * iconSize + y * gap, iconSize, iconSize))
            else:
                if map[y][x] == -1: pygame.draw.rect(displaySurface, white if x == locationX and y == locationY else red, (x * iconSize + x * gap, y * iconSize + y * gap, iconSize, iconSize))
                else:
                    pygame.draw.rect(displaySurface, white if x == locationX and y == locationY else (255, 255, 0), (x * iconSize + x * gap, y * iconSize + y * gap, iconSize, iconSize))
                    textSurface = font.render(str(land[y][x]), True, black)
                    displaySurface.blit(textSurface, (x * iconSize + x * gap, y * iconSize + y * gap))
        print()

for y in range(height):
    for x in range(width):
        percent = random.randint(1, 100)

        if percent <= ratio:
            land[y][x] = -1

for y in range(height):
    for x in range(width):

        if land[y][x] == -1: continue

        count = 0

        for _nearY in range(3):
            for _nearX in range(3):
                nearY = y - 1 + _nearY
                nearX = x - 1 + _nearX
                
                if nearX < 0: continue
                if nearX > width - 1: continue
                if nearY < 0: continue
                if nearY > height - 1: continue

                if nearX == x and nearY == y: continue

                if land[nearY][nearX] == -1: count += 1
        
        land[y][x] = count

running = True

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        move(1, 0)
    if keys[pygame.K_LEFT]:
        move(-1, 0)
    if keys[pygame.K_UP]:
        move(0, -1)
    if keys[pygame.K_DOWN]:
        move(0, 1)
    if keys[pygame.K_RETURN]:
        if not mine(locationX, locationY):
            print("실패")

    printMap(land)

    pygame.display.flip()
            


pygame.quit()

