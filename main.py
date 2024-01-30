import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1150, 670))
pygame.display.set_caption("Mouse Game")
clock = pygame.time.Clock()
running = True
plugged = False
import time
import numpy as np

#joystick
from pygame.locals import *

pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    plugged = True
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
else:
    joysticks = []


score_value = 0
a = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 945
textY = 120
timer = time.time()

randx = [67, 598]
randy = [67, 333, 598]
#m_arr = np.random.randint(0, 8, size=(2, 4))

#print(m_arr)


m_arr = np.array([[3,0,7,5],[0,1,7,2]])
m_arr = 3*m_arr
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def checkMouse(self, pos):
        if self.rect.collidepoint(pos):
            return True

block_group = pygame.sprite.Group()
x = 25
y = 25
x1 = 25
y1 = 25
v_x = 0
v_y = 0
v_x1 = 0
v_y1 = 0
player = pygame.rect.Rect(x, y, 25, 25)
player1 = pygame.rect.Rect(x1, y1, 25, 25)

def calc_newPos(v_x, v_y, x, y):
    return (x + v_x, y + v_y)

def draw_grid():
    blockSize = 133  # Set the size of the grid block
    for x in range(0, 665, blockSize):
        for y in range(666 - blockSize, -1, -blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    #pygame.draw.rect(screen, (91, 219, 68), (532, 666, 134, 134), 2)
    pygame.draw.rect(screen, (91, 219, 68), (665, 532, 134, 134), 2)
    pygame.draw.rect(screen, (91, 219, 68), (665, 0, 134, 134), 2)
def fill_grid():
    # Fill the grid with the colors
    blockSize = 132  # Set the size of the grid block
    new_block = Block((255, 0, 0), blockSize, blockSize, random.choice(randx), random.choice(randy))
    block_group.add(new_block)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))

def calc_score():
    x, y = player.topleft
    blockPosx, blockPosy = block_group.sprites()[0].rect.center
    # norm
    dist = np.linalg.norm(np.array([blockPosx, blockPosy]) - np.array([x, y]))
    return int(100-dist)

def calc_score1():
    x, y = player1.topleft
    blockPosx, blockPosy = block_group.sprites()[0].rect.center
    # norm
    dist = np.linalg.norm(np.array([blockPosx, blockPosy]) - np.array([x, y]))
    return int(100-dist)

def checkSafe(topleft):
    a, b= topleft
    if a > 532 and b > 532:
        return True
    else:
        return False 
    

while(1==1):
    screen.fill((255, 255, 255))
    fill_grid()
    draw_grid()
    block_group.draw(screen)
    break

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def combine_inputs(arr):
    return m_arr @ arr


while running:


    s = block_group.sprites()[0]
    #control mouse with joystick
    draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("black"), 900, 10)
    x, y = player.topleft
    player.topleft = calc_newPos(v_x, v_y, x, y)
    player1.topleft = (x1, y1)
    block_group.draw(screen)
    draw_grid()
    pygame.draw.rect(screen, (0, 128, 255), player)
    pygame.draw.rect(screen, (0, 255, 0), player1)
    """x = x + joysticks[0].get_axis(0)*8
    y = y + joysticks[0].get_axis(1)*8
    x1 = x1 + joysticks[0].get_axis(2)*8
    y1 = y1 + joysticks[0].get_axis(3)*8 """
    # make a 4 by 1 matrix of the joystick inputs
    if plugged:
        arr = np.array([joysticks[0].get_axis(0), joysticks[0].get_axis(1), joysticks[0].get_axis(2), joysticks[0].get_axis(3)])
        arr1 = np.array([joysticks[1].get_axis(0), joysticks[1].get_axis(1), joysticks[1].get_axis(2), joysticks[1].get_axis(3)])

    # make x and y the outputs of the matrix multiplication
    if plugged:
        v_x, v_y = combine_inputs(arr)
        v_x1, v_y1 = combine_inputs(arr1)
    """x *= 50
    y *= 50
    x1 *= 50
    y1 *= 50
    x = max(x, 0)
    x = min(x, 640)
    y = max(y, 0)
    y = min(y, 640)
    x1 = max(x1, 0)
    x1 = min(x1, 640)
    y1 = max(y1, 0)
    y1 = min(y1, 640)"""
    """if x < 0:
        x = 0
    if x > 775:
        x = 775
    if y < 0:
        y = 0
    if y > 775:
        y = 775
    if x1 < 0:
        x1 = 0
    if x1 > 775:
        x1 = 775
    if y1 < 0:
        y1 = 0
    if y1 > 775:
        y1 = 775"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == JOYDEVICEADDED:
            print("Joystick connected")

    # problem, block spawns in the same place as the last one
    if (s.checkMouse(player.topleft)):
        if (time.time()-timer > 5):
            print(time.time()-timer)
            timer = time.time()
            sc = calc_score()
            s.kill()
            screen.fill((255, 255, 255))
            a = 0
            draw_grid()
            fill_grid()
            block_group.draw(screen)
            score_value += sc

    if (s.checkMouse(player1.topleft)):
        if (time.time()-timer > 5):
            print(time.time()-timer)
            timer = time.time()
            sc = calc_score1()
            s.kill()
            screen.fill((255, 255, 255))
            a = 0
            draw_grid()
            fill_grid()
            block_group.draw(screen)
            score_value += sc
    # second controller
    # safe zone
    

    clock.tick(60)
    point = pygame.mouse.get_pos()
    show_score(textX, textY)
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()