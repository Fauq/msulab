import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1150, 800))
pygame.display.set_caption("Mouse Game")
clock = pygame.time.Clock()
running = True
import time
import numpy as np

#joystick
from pygame.locals import *

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


score_value = 0
a = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 860
textY = 200
timer = time.time()

randx = [80, 720]
randy = [80, 400, 720]
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
player = pygame.rect.Rect(x, y, 25, 25)
player1 = pygame.rect.Rect(x1, y1, 25, 25)

def draw_grid():
    blockSize = 160  # Set the size of the grid block
    for x in range(0, 800, blockSize):
        for y in range(0, 800, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
def fill_grid():
    # Fill the grid with the colors
    blockSize = 159  # Set the size of the grid block
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
    draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("black"), 850, 10)
    player.topleft = (x, y)
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
    arr = np.array([joysticks[0].get_axis(0), joysticks[0].get_axis(1), joysticks[0].get_axis(2), joysticks[0].get_axis(3)])
    arr1 = np.array([joysticks[1].get_axis(0), joysticks[1].get_axis(1), joysticks[1].get_axis(2), joysticks[1].get_axis(3)])

    # make x and y the outputs of the matrix multiplication
    x, y = combine_inputs(arr)
    x1, y1 = combine_inputs(arr1)
    x = x*50
    y= y*50
    x1 = x1*50
    y1 = y1*50
    if x < 0:
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
        y1 = 775
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