import random
import pygame
import time
import numpy as np
from pygame.locals import *
import json 
import csv
import pandas as pd
import os

pygame.init()
screen = pygame.display.set_mode((1150, 670))
pygame.display.set_caption("Mouse Game")
clock = pygame.time.Clock()
running = True
plugged = False
captured = False
color = (0, 0, 255)
trial = 1
game_data = []
start_time = time.time()
path = 'DaqCpp/record/pose.csv'
arr = []
arr1 = []




    #arr1 = next(reader)
#joystick


pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    plugged = True
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
else:
    joysticks = []


player_score = 0
defender_score = 0
a = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 945
textY = 120
timer = time.time()

randx = [67, 200]
randy = [67, 333, 598]
#m_arr = np.random.randint(0, 8, size=(2, 4))

#print(m_arr)


#m_arr = np.array([[3,0,7,5],[0,1,7,2]])
m_arr = np.array([[-5.33247879150843e-05,3.55507427725192e-05,-0.000668516195280432, -0.000631942988468327,	-0.00143781984715076,	-0.000691431808599448,	0.00276886989301726,	0.00395505401419451,	0.00355954996564003,	-3.74330758317242e-05,	0.00697306630302672,	0.00893695172258586,	0.00804325691094529,	7.00739928822353e-05,	0.00569227277209805,	0.00746988789276899,	0.00672289803153796,	-1.85044318698863e-05,	0.00504560935962856,	0.00635550797765998,	0.00571995714367466],[0.00136859144602875,	-0.000912386033903697,	0.0166398580212531,	0.0170947439600576,	0.0340428744699597,	0.00160655988197229,	-0.00393386205170458,	-0.00561862284449718,	-0.00505676166756256,	0.00249110872571687,	0.00729916518055413,	0.0119279744390449,	0.0107351844138503,	0.000686843168696682,	-0.00687439142765975,	-0.00889586604750950,	-0.00800629000198628,	7.84883340792437e-05,	0.00127624416230591,	0.00281448125397012,	0.00253303203980908]])
print(m_arr.shape)
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def checkMouse(self, pos):
        x , y = pos
        if np.linalg.norm(np.array([x, y]) - np.array([self.rect.centerx, self.rect.centery])) < 80:
            return True

block_group = pygame.sprite.Group()
# initial position of players
x = 700
y = 50
x1 = 700
y1 = 600
# initial velocity of players
v_x = 0
v_y = 0
v_x1 = 0
v_y1 = 0
player = pygame.rect.Rect(x, y, 25, 25)
player1 = pygame.rect.Rect(x1, y1, 25, 25)

def calc_newPos(v_x, v_y, x, y):

    return (x + v_x, y + v_y)

#record data of inputs every game in a list
#append data at every 10 ms to a list - joystick and velocity info and positions of the players
#posotion of flag and time it took to get it
#save data to a file

#change player1 to circle 
#add a circle radius around player and flag to show capture radius 
#time score should be 0 for losing player

# person whos capturing is the attacker/player
# person who is defending is defender 

# 4 scoring conditions 

# 1. player brought back flag (player full points, defender 0)
# 2. defender intercepts (defender full points, player 0)
# 3. time runs out (defender 75% of points, player 0) 
# 4. player captures flag but dont bring it back (player 25% of points, defender 0)

#timing score 
# player score: 20 - time it took for player to capture flag 
# defender: the time elapsed (or trial time)
def draw_grid():
    blockSize = 133  # Set the size of the grid block
    for x in range(0, 665, blockSize):
        for y in range(666 - blockSize, -1, -blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    #pygame.draw.rect(screen, (91, 219, 68), (532, 666, 134, 134), 2)
    pygame.draw.rect(screen, (91, 219, 68), (665, 532, 134, 134), 2)
    pygame.draw.rect(screen, (0, 128, 255), (665, 0, 134, 134), 2)
def fill_grid():
    # Fill the grid with the colors
    blockSize = 50  # Set the size of the grid block
    new_block = Block((255, 0, 0), blockSize, blockSize, random.choice(randx), random.choice(randy))
    block_group.add(new_block)

def show_score1(x, y):
    score = font.render("Player Score: " + str(player_score), True, (255, 0, 0))
    screen.blit(score, (x-75, y))

def show_score2(x, y):
    score = font.render("Defender Score: " + str(defender_score), True, (255, 0, 0))
    screen.blit(score, (x-95, y+50))

def show_time():
    score = font.render("Time: " + str(int(time.time() - timer)), True, (0, 0, 0))
    screen.blit(score, (textX, textY-50))

def show_trial():
    score = font.render("Trial: " + str(trial), True, (0, 0, 0))
    screen.blit(score, (textX, 500))

def calc_time():
    return int(time.time() - timer)

def calc_scorePlayer(senario, time):
    timeScore = (20-int(time.time() - timer))
    if senario == 1:
        return 20 + timeScore
    if senario == 2 or senario == 3:
        return timeScore 
    if senario == 4:
        return timeScore + 0.25*20

def calc_scoreDefender(senario, time):
    timeScore = int(time.time() - timer)
    if senario == 1:
        return timeScore
    if senario == 2:
        return 20 + timeScore
    if senario == 3:
        return 0.75*20 + timeScore
    if senario == 4:
        return timeScore     

def checkSafe(topleft):
    a, b= topleft
    if a > 532 and b > 532:
        return True
    else:
        return False 
    
def readValues():
    if os.path.getsize(path) == 0:
        print("Error")
    else: 
        with open (path, "r") as file: 
            reader = csv.reader(file)
            for row in reader:
                return row

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
    print(m_arr @ arr)
    return m_arr @ arr

def checkDrift(axis):
    if abs(axis) < 0.1:
        return 0
    else:
        return axis

    
def isSafe_player(x, y):
    if x > 700 and y < 108 and captured == True:
        return True
    else:
        return False
    
    
def checkBounds(x, y, player):
    if player:
        if x < 0:
            x = 0
        if x > 774 and y <= 108:
            x = 774
        if x > 687 and y > 108:
            y = 108
        if x > 774:
            x = 774
        if y < 0:
            y = 0
        if y > 115 and x > 640:
            x = 640
        if y > 640:
            y = 640
    else: 
        if x < 0:
            x = 0
        if y < 532 and x > 640:
            x = 640
        if x > 687 and y < 532:
            y = 532
        if x > 774:
            x = 774
        if y < 0:
            y = 0
        if y > 640:
            y = 640
        
    return (x, y)


while running:
    arr = readValues()
    arr = np.array(arr)
    arr = arr.astype(np.float64)

    if (arr.shape == (21,)):
        newarr = arr.reshape(21, 1)
    if plugged and time.time() - timer >= 0.01:
        game_data.append( {
            'joystick': [joysticks[0].get_axis(0), joysticks[0].get_axis(1), joysticks[0].get_axis(2), joysticks[0].get_axis(3)],
            'velocity': [v_x, v_y, v_x1, v_y1],
            'position': [(x, y), (x1, y1)],
            'flag': block_group.sprites()[0].rect.center,
        })
    
    start_time = time.time()

    if block_group.sprites():
        s = block_group.sprites()[0]
    #control mouse with joystick
    draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("black"), 900, 10)
    ##x, y = calc_newPos(v_x, v_y, x, y)
    ##x1, y1 = calc_newPos(v_x1, v_y1, x1, y1)


    #print(joysticks[0].get_axis(0), joysticks[0].get_axis(1))
    #stick drift 

    # Restrict players within the playing area


    # Update player positions
    
    player.topleft = (x, y)
    player1.topleft = (x1, y1)
    if not captured:
        block_group.draw(screen)
    draw_grid()
    pygame.draw.rect(screen, color, player)
    pygame.draw.rect(screen, (0, 255, 0), player1)

    # make a 4 by 1 matrix of the joystick inputs
    """if plugged:
        arr = np.array([checkDrift(joysticks[0].get_axis(0)), checkDrift(joysticks[0].get_axis(1)), checkDrift(joysticks[0].get_axis(2)), checkDrift(joysticks[0].get_axis(3))])
        arr1 = np.array([checkDrift(joysticks[1].get_axis(0)), checkDrift(joysticks[1].get_axis(1)), checkDrift(joysticks[1].get_axis(2)), checkDrift(joysticks[1].get_axis(3))])
"""
    # make x and y the outputs of the matrix multiplication
   
    if (newarr.shape == (21, 1)):
        x, y = combine_inputs(newarr)
        x = x*150
        y = y*150
        
        #v_x1, v_y1 = combine_inputs(arr1)
    
    x, y = checkBounds(x, y, True)
    x1, y1 = checkBounds(x1, y1, False)
    print(x, y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == JOYDEVICEADDED:
            print("Joystick connected")

    # problem, block spawns in the same place as the last one
    if (s.checkMouse(player.topleft)):
        if not captured:
            captured = True
            color = (255, 0, 0)
            s.kill()
            screen.fill((255, 255, 255))
            a = 0
            draw_grid()
            fill_grid()

    """if (np.linalg.norm(np.array([x, y]) - np.array([x1, y1])) < 30):
        captured = False
        color = (0, 0, 255)
        timer = time.time()
        x = 700
        y = 50
        x1 = 700
        y1 = 600
        trial += 1"""

    """sc = calc_score1()
        s.kill()
        screen.fill((255, 255, 255))
        a = 0
        draw_grid()
        fill_grid()
        score_value += sc"""
    # second controller
    # safe zone
    if isSafe_player(x, y):
        trial += 1
        player_score += (20-int(time.time() - timer))
        x1 = 700
        y1 = 600
        game_data.append({
            'time_to_capture': int(time.time() - timer),
        })
        captured = False
        timer = time.time()
        color = (0, 0, 255)
        a = 0
        block_group.draw(screen)

    # time doesnt start counting until both players leave the safe zone
    if (x > 665 and y < 134 and x1 > 665 and y1 > 532):
       timer = time.time()


    if (calc_time() > 20):
        x = 700
        y = 50
        player.topleft=(x,y)
        
        x1 = 700
        y1 = 600
        captured = False
        color = (0, 0, 255)
        time.sleep(5)
        timer = time.time()
    
    clock.tick(60)
    point = pygame.mouse.get_pos()
    show_score1(textX, textY)
    show_score2(textX, textY)
    show_time()
    show_trial()
    pygame.display.flip()
    screen.fill((255, 255, 255))

pygame.quit()



# Saving data 
# Calibration ()
# Manual home position 
# Bounds for Flag and Home position of player 
# Actual x,y and displayed x,y 
# No time limit for trial, message to tell both players to go back to home position before new trial starts 
# Circle around flag and attacker 
