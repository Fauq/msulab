from math import atan2
import math, random, pygame, time
import numpy as np
from pygame.locals import *
import json, csv, os, pickle

from calibrationASL import runCalibration_ASL

# Setting game sessions and parameters
calib_flag = 0
gameplay_flag = 1



#======================= Calibration Phase ====================================
if calib_flag:
    C_glove, p0, synergies, scaling, dxy, calibFlag = runCalibration_ASL(calibSigns=33, subject='001', joint_dim=21, expDay=1)
else:
    C_glove= np.array([[-0.03132698,  0.02051033,  0.03498236,  0.03498232,  0.08300048, -0.08430041,  0.40687442,  0.58010444,  0.52293686, -0.14560099, 0.88047125,  1.23860548,  1.11474462,  0.0058947,  0.62157013, 0.88795741,  0.79916169,  0.03217047,  0.52628314,  0.74993886, 0.6766496 ],
                     [ 0.46436904, -0.30624316,  2.06743546,  2.06743242,  4.37282329, 0.70592261, -2.05631285, -2.90577053, -2.64021756, -1.69479561, 1.8350689 ,  2.74689286,  2.47220197, -0.40117436, -0.8480112, -1.2114465 , -1.09030442, -0.27762784, -0.83292699, -1.19548129, -1.07090373]])
    p0 = np.array([[  34.06299109],
                   [-180.81036949]])

C_joy = 3 * np.array([[3,0,7,5],[0,1,7,2]])
    
#======================= Gameplay Phase =======================================
pygame.init()
screen = pygame.display.set_mode((1150, 670))
pygame.display.set_caption("Capture The Flag")
clock = pygame.time.Clock()
running = True
plugged = False
attackerColor = (0, 0, 255)
game_data = []
start_time = time.time()
filePath_gloveData = 'DaqCpp/record/pose.csv'

# flags for condition checking
flagCaptured = False
attackerCaptured = False
flagReturned = False 
returnHome_flag = False
trialEnd_flag = False
hasFlag = False

# trials and sessions
trial = 1
session = 1 

# Checking joystick connection and creating the joystick object
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    plugged = True
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
else:
    joysticks = []


player_score = 0
defender_score = 0
a = 0
font = pygame.font.Font('freesansbold.ttf', 26)
textX = 945
textY = 120
timer = time.time()

randx = [67, 200]
randy = [67, 333, 598]

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
x  =  np.array([700])
y  = np.array([50])
x1 = np.array([710])
y1 = np.array([600])
actualX = 0
actualY = 0
# initial velocity of players
v_x = 0
v_y = 0
v_x1 = 0
v_y1 = 0
attacker = pygame.rect.Rect(x.item(), y.item(), 25, 25)
defender = pygame.rect.Rect(x1.item(), y1.item(), 25, 25)

#record data of inputs every game in a list
#append data at every 10 ms to a list - joystick and velocity info and positions of the players
#posotion of flag and time it took to get it
#save data to a file

#change defender to circle 
#add a circle radius around attacker and flag to show capture radius 
#time score should be 0 for losing player

# person whos capturing is the attacker/player
# person who is defending is defender 

# 4 scoring conditions 

# 1. attacker brought back flag (attacker full points, defender 0)
# 2. defender intercepts (defender full points, attacker 0)
# 3. time runs out (defender 75% of points, attacker 0) 
# 4. attacker captures flag but dont bring it back (attacker 25% of points, defender 0)

#timing score 
# attacker score: 20 - time it took for attacker to capture flag 
# defender: the time elapsed (or trial time)



#============================ Function Space ==================================
# Move to a separate file with class and its methods ==========================

def vel_to_pos(v_x, v_y, x, y):
    return np.array([x + v_x]), np.array([y + v_y])

def draw_grid():
    blockSize = 133  # Set the size of the grid block
   # for x in range(0, 665, blockSize):
       # for y in range(666 - blockSize, -1, -blockSize):
            #rect = pygame.Rect(x, y, blockSize, blockSize)
            #pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    #pygame.draw.rect(screen, (91, 219, 68), (532, 666, 134, 134), 2)
    pygame.draw.rect(screen, (0,0,0), (665, 0, 2, 665), 1)
    pygame.draw.rect(screen, (0,0,0), (0, 0, 665, 2), 1)
    pygame.draw.rect(screen, (0,0,0), (0, 0, 2, 670), 1)
    pygame.draw.rect(screen, (0,0,0), (0, 668, 665, 2), 1)
    pygame.draw.rect(screen, (91, 219, 68), (665, 532, 134, 139), 2)
    pygame.draw.rect(screen, (0, 128, 255), (665, 0, 134, 134), 2)
    pygame.draw.arc(screen, (0, 255, 0), (466, -198, 400, 400), math.pi, (3*math.pi)/2, 2)
def fill_grid():
    # Fill the grid with the colors
    blockSize = 50  # Set the size of the grid block
    x = random.choice(randx)
    y = random.choice(randy)
    global blockX
    global blockY
    blockX = x
    blockY = y
    new_block = Block((255, 0, 0), blockSize, blockSize, x, y)
    block_group.add(new_block)
    
    

def show_score1(x, y):
    _scoreStr = font.render("Player Score: ", True, (0,0,0))
    score = font.render(str(player_score), True, (0, 0, 255))
    screen.blit(score, (x+80, y+2))
    screen.blit(_scoreStr,(x-100, y))

def show_score2(x, y):
    _scoreStr = font.render("Defender Score: ", True, (0,0,0))
    score = font.render(str(defender_score), True, (0, 255, 0))
    screen.blit(score, (x+120, y+52))
    screen.blit(_scoreStr, (x-100, y+50))

def show_time():
    _time = int(time.time() - timer)
    _timeStr = font.render("Time Elapsed: ", True, (0,0,0))
    if (_time < 20):
        score = font.render(str(int(time.time() - timer)), True, (0, 0, 0))
    else:
        score = font.render(str(int(time.time() - timer)), True, (255, 0, 0))
    screen.blit(score, (1040, textY-50))
    screen.blit(_timeStr, (textX-100, textY-50))

def show_trial():
    score = font.render("Trial: " + str(trial), True, (0, 0, 0))
    screen.blit(score, (844, 22))

def show_warning(): 
    font1 = pygame.font.Font('freesansbold.ttf', 22)
    score = font1.render("Please Return to Home Position", True, (0, 140, 140))
    screen.blit(score, (800, 400))

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
    
def readGloveData():
    if os.path.getsize(filePath_gloveData) == 0:
        print("Error")
    else: 
        with open (filePath_gloveData, "r") as file: 
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

def mapGlove_cursor(joint_angles, C_glove, p0):
    return C_glove @ joint_angles - p0


def mapJoy_cursor(joyInput):
    return C_joy @ joyInput

def checkDrift(axis):
    if abs(axis) < 0.1:
        return 0
    else:
        return axis

    
def isSafe_attacker(x, y):
    if x > 666 and y < 108:
        return True
    else:
        return False
    
def isSafe_defender(x, y):
    if x>666 and y>532:
        return True
    else:
        return False
    

def chkBoundsArr(X, attacker):
    if attacker:
        if X[0] < 0:
            X[0] = 0

def checkBounds(x_arr, y_arr, attacker):
    x = x_arr.item()
    y = y_arr.item()
    if attacker:
        if x < 0:
            x = 13
        if x > 774 and y <= 121:
            x = 774
        if x > 680 and y > 121:
            y = 121
        if x > 774:
            x = 774
        if y < 0:
            y = 13
        if y >= 141 and x > 654:
            x = 654
        if y > 640:
            y = 656
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
        
    return np.array([x]), np.array([y])


while running:
    
    # Read Glove data for attacker
    gloveInputRaw = readGloveData()
    if not gloveInputRaw == None:
        gloveInputArr = np.array(gloveInputRaw).astype(np.float64)[:, None]
        
    # print(gloveInputArr.shape)
    
    # Take joystick inputs and map to defender cursor's velocity -> position
    if plugged:
        joyInputArr = np.array([checkDrift(joysticks[0].get_axis(0)), checkDrift(joysticks[0].get_axis(1)), checkDrift(joysticks[0].get_axis(2)), checkDrift(joysticks[0].get_axis(3))])
        v_x1, v_y1 = mapJoy_cursor(joyInputArr)
        x1, y1 = vel_to_pos(v_x1, v_y1, x1, y1)
        
   # # saving data?
   #  if time.time() - timer >= 0.01 and block_group.sprites():
   #      game_data.append( {
   #          #'joystick': [joysticks[0].get_axis(0), joysticks[0].get_axis(1), joysticks[0].get_axis(2), joysticks[0].get_axis(3)],
   #          #'velocity': [v_x, v_y, v_x1, v_y1],
   #          'position': [(x, y), (x1, y1)],
   #          'flag': block_group.sprites()[0].rect.center,
   #          'trial': trial,
   #      })
    
   # make sure it only runs once per trial 
    start_time = time.time()

    # change name of variable
    if block_group.sprites():
        flagBlock = block_group.sprites()[0] 
        
    # drawing attacker and defender on screen
    pygame.draw.rect(screen, attackerColor, attacker)
    pygame.draw.rect(screen, (0, 255, 0), defender)
        
    # make x and y the outputs of the matrix multiplication    
    x, y = mapGlove_cursor(gloveInputArr, C_glove, p0)
    actualX, actualY = x, y
    print(x, y)
    # Ensuring player positions are in bounds
    x, y = checkBounds(x, y, attacker=True)
    x1, y1 = checkBounds(x1, y1, attacker=False)
    print(x, y)
    # print(x, y, x1, y1)
    # abc
    attacker.center = (x.item(), y.item())
    defender.center = (x1.item(), y1.item())


    # checking for game stop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == JOYDEVICEADDED:
            print("Joystick connected")
            

            
    # checking if defender has crossed their boundary
    if (np.linalg.norm(np.array([x1, y1]) - np.array([blockX, blockY])) < 150):
        print(x1, y1)
        _theta = atan2((y1-blockY),(x1-blockX))
        print(_theta)
        x1 = np.array([blockX + 151*math.cos(_theta)])
        print(x1)
        y1 = np.array([blockY + 151*math.sin(_theta)])
        print(y1)
    
    if (np.linalg.norm(np.array([x1, y1]) - np.array([666, 0])) < 200): 
        _theta = atan2((y1-0),(x1-666))
        x1 =np.array([666 + 201*math.cos(_theta)])
        y1 = np.array([0 + 201*math.sin(_theta)])
    
    # check for when attacker captures flag
    if (flagBlock.checkMouse(attacker.center) and not attackerCaptured):
        flagCaptured = True
        
        # if not captured:
        #     captured = True
        #     color = (255, 0, 0)
        #     s.kill()
        #     screen.fill((255, 255, 255))
        #     a = 0
        #     draw_grid()
        #     fill_grid()
            
    # checking if defender captures attacker
    if (np.linalg.norm(np.array([x1, y1]) - np.array([x, y])) < 25):
        attackerCaptured = True 
        flagCaptured = False
        
    
        
    # If attacker gets captured by defender 
    # if attackerCaptured: 
    #     print("test!")
    #     s.kill()
    #     screen.fill((255, 255, 255))
    #     draw_grid()
    #     show_warning()
    #     if isSafe_player(x, y) == True and isSafe_player1(x1, y1) == True:
    #         trial += 1
    #         player_score += (20-int(time.time() - timer))
    #         captured = False
    #         attackerCaptured = False
    #         timer = time.time()
    #         color = (0, 0, 255)
    #         a = 0
    #         block_group.draw(screen)
    #         print("wtf")
            
    # If attacker is not captured and flag is also not captured
    if not hasFlag:   
        block_group.draw(screen)
        pygame.draw.circle(screen, (0, 255, 0), (blockX, blockY), 150, 5)
        pygame.draw.circle(screen, (0, 0, 255), (blockX, blockY), 80, 3)
        draw_grid()
    

    
    # checks if both players are in safe zone, then resets trial
    # if isSafe_player(x, y) == True and isSafe_player1(x1, y1) == True:
    #     captured = False
    #     print("Test!")
    #     trial += 1
    #     player_score += (20-int(time.time() - timer))
    #     x1 = np.array([710])
    #     y1 = np.array([600])
    #     game_data.append({
    #         'time_to_capture': int(time.time() - timer),
    #     })
        
    #     timer = time.time()
    #     color = (0, 0, 255)
    #     a = 0
        

    # time doesnt start counting until both players leave the safe zone
    if (x > 665 and y < 134 and x1 > 665 and y1 > 532):
       timer = time.time()
    
    # checking conditions 
    if flagCaptured: 
        attackerColor = (255, 0, 0)
        flagBlock.kill()
        screen.fill((255, 255, 255))
        draw_grid()
        fill_grid()
        hasFlag = True
        flagCaptured = False
    
    if hasFlag: 
        draw_grid()
        attackerColor = (255, 0, 0)
        # checks if attacker returns to safe zone with flag 
        if isSafe_attacker(x.item(), y.item()) == True:
            print("TEST!!!!")
            attackerColor = (0, 0, 255)
            hasFlag = False
            returnHome_flag = True
        
    if attackerCaptured: 
        attackerColor = (0, 0, 255)
        flagBlock.kill()
        screen.fill((255, 255, 255))
        draw_grid()
        returnHome_flag = True
        
    if flagReturned:
        attackerColor = (0, 0, 255)
        returnHome_flag = True  
        
    if returnHome_flag: 
        print("Return home")
        screen.fill((255, 255, 255))
        draw_grid()
        show_warning()
        # checks if attacker and defender are both in safe zones 
        if isSafe_attacker(x.item(), y.item()) == True and isSafe_defender(x1.item(), y1.item()) == True:
            trialEnd_flag = True
            returnHome_flag = False
        
    if trialEnd_flag: 
        print("TEST")
        #save data 
        if trial < 59:
            print("test")
            trial += 1 
        else: 
            trial = 1 
            session += 1 
        
        #scoring stuff
        player_score += (20-int(time.time() - timer))
        
        #resets all flags
        flagCaptured = False
        attackerCaptured = False
        flagReturned = False 
        returnHome_flag = False
        trialEnd_flag = False
        
        timer = time.time()
        
    clock.tick(60)
    point = pygame.mouse.get_pos()
    show_score1(textX, textY)
    show_score2(textX, textY)
    show_time()
    show_trial()
    pygame.display.flip()
    
    screen.fill((255, 255, 255))
    
    # Trial end jobs: Save data, incrememnt trial number, select next flag position, compute the score to be displayed on next trial, reset other flags
    # if trialEnd_flag:
        

with open ('data.pkl', 'wb') as f:
    pickle.dump(game_data, f)
pygame.quit()



# Saving data 
# Calibration ()
# Manual home position 
# Bounds for Flag and Home position of player 
# Actual x,y and displayed x,y 
# No time limit for trial, message to tell both players to go back to home position before new trial starts 

# Circle around flag and attacker 
