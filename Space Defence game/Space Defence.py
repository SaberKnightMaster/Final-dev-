

#######################
## Faris MARVANAĞA   ##
#######################
## ÖĞR.NO: 221980112 ##
#######################


# importing libraries
from pygame import mixer
import pygame
import math
import random
import time


# Intialize pygame
pygame.init()


# create the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# game over music
game_overSound = mixer.Sound("game_over.wav")# Touch - Mattia Cupelli

# main menu Background
mainMenu = pygame.image.load('main menu.png')

# in game background
background = pygame.image.load('background.png').convert()
background_y = 0

# Caption and icon
pygame.display.set_caption("Space Defense")
icon = pygame.image.load('meteor.png')
pygame.display.set_icon(icon)

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
dark_red = (200,0,0)
yellow = (250,250,100)
dark_yellow = (200,200,75)
cyan = (0,250,250)
dark_cyan = (0,200,200)

# Score value and font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# global variables
pause = False
g_over = True
clock = pygame.time.Clock()


# creating text
def text_objects(text,font,color):
    
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# text blit modification
def message_dispaly(text,size,x,y,color):
    
    subText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, subText,color)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()


# buttons modification
def button(msg,x,y,w,h,ic,ac,action=None):

    # get mouse coordinates
    mouse = pygame.mouse.get_pos()
    # get mouse press
    click = pygame.mouse.get_pressed()
    # button rect
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    # button text
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(msg, smallText,white)
    TextRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(TextSurf, TextRect)


# score blit
def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, white)
    screen.blit(score, (x, y))


# live blit
def show_lives(x,y):
    lives = font.render("lives : " + str(lives_value), True, white)
    screen.blit(lives, (x, y))


# game's main menu
def main_menu():
    
    # in menu music
    mixer.music.load("menu.wav")# Action Background Music
    mixer.music.play(-1)
    game_overSound.stop()
    # time dalay for preventing missclick
    time.sleep(0.1)
    
    # main menu Background Image
    screen.blit(mainMenu, (0, 0))
    # game start and how to play texts
    message_dispaly("Welcome to Space Defense!",56,width/2,250,white)
    message_dispaly("< use arrows to move >",32,width/2,325,dark_yellow)
    message_dispaly("< use space bar to shoot >",32,width/2,375,dark_yellow)
    # main menu is active
    intro = True
    
    # actions while main menu is active
    while intro:
        
        # end game on exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        
        # buttons with action
        button("fight!",150,450,100,50,dark_cyan,cyan,game_loop)
        button("quit",550,450,100,50,dark_red,red,quitgame)
        
        # refresh display for cnstant blit
        pygame.display.update()
        clock.tick(60)


# game's loop
def game_loop():

    # player blit
    def player(x, y):
        screen.blit(playerImg, (x, y))

    # enemy blit
    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    # bullet blit
    def fire_bullet(x, y):
        screen.blit(bulletImg, (x + 16, y + 10))

    # collision between enemy and bullet on hit
    def isCollision_B(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 50:
            return True
        else:
            return False

    # collision between enemy and player on hit
    def isCollision_P(enemyX, enemyY, playerX, playerY):
        distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
        if distance < 50:
            return True
        else:
            return False

    # load variables
    global pause
    global score_value
    global lives_value
    global background_y
    # reset score and lives
    score_value = 0
    lives_value = 3

    # in_game music
    mixer.music.load("battle.wav")# Break the Sword of Justice
    mixer.music.play(-1)
    game_overSound.fadeout(500)

    # Player
    playerImg = pygame.image.load('spaceship.png')
    playerX =  width/2-32
    playerY =  height-64
    playerX_change = 0

    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    num_of_enemies = 5
    speed = 2

    # popup (num_of_enemies) enemies randomly
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(-100, -80))

    # Bullet
    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletY_change = 30
    # bullet ready to fire
    bullet_state = "ready"


    # game's loop is active
    running = True

    # actions while game's loop is active
    while running:

        # background image scrolling algorithm
        rel_y = background_y % background.get_rect().height
        screen.blit(background, (0, rel_y -background.get_rect().height))
        if rel_y < height:
            screen.blit(background, (0, rel_y))
        background_y += 1

        # recognizing events
        for event in pygame.event.get():
            # end game on exit
            if event.type == pygame.QUIT:
                quitgame()
            
            # if any key is pressed
            if event.type == pygame.KEYDOWN:
                # pause game
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()
                # move right
                if event.key == pygame.K_RIGHT:
                    playerX_change = 10
                # move left
                if event.key == pygame.K_LEFT:
                    playerX_change = -10
                #shoot bullet when its ready
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        # play sound efect when firing bullet
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        # fire the bullet at the exact coordinates of the spaceship's x coordinates
                        fire_bullet(playerX, bulletY)
                        bullet_state = "fire"
            
            # stop moving if key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # moving through screen sides
        playerX += playerX_change
        if playerX < 0:
            playerX = 736
        elif playerX > 736:
            playerX = 0

        # Enemy Movement
        for i in range(num_of_enemies):

            #show enemy
            enemy(enemyX[i], enemyY[i], i)

            # move enemy
            enemyY[i] += speed

            # collision algorithms load
            collision_B = isCollision_B(enemyX[i], enemyY[i], bulletX, bulletY)
            collision_P = isCollision_P(enemyX[i], enemyY[i], playerX, playerY)

            # check for collision between enemy and bullet
            if collision_B:
                # reloading bullet, scoring and respawn enemy after collision
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 0)

            # check for collision between enemy and player
            if collision_P:
                # respawn enemy after collision
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 50)

            # check for enemy is passed the screen
            if enemyY[i] > 536:
                # loose live and respawn emeny
                lives_value -= 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 0) 
            
            # game over in loosing all lives
            if  lives_value < 0:
                game_over()

        # check if bullet is fired
        if bullet_state == "fire":
            # fire bullet
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # check if bullet reached the top
        if bulletY <= 0:
            # reload the bullet
            bulletY = 480
            bullet_state = "ready"

        # step up to the next level every 10 score
        if  score_value % 10 is 0 and score_value != 0:
            # earn 1 live, 1 score and increase enemy speed
            lives_value +=1
            score_value +=1
            speed += 0.2

        # show player, score and lives in screen
        player(playerX, playerY)
        show_score(10, 10)
        show_lives(width-130,10)
        # refresh display for cnstant blit
        pygame.display.update()
        clock.tick(60)


# game pause
def paused():

    global show_score
    global show_lives
    # show score and lives while paused
    show_score(10, 10)
    show_lives(width-130,10)
    # paused texts
    message_dispaly("paused",100,(width/2),(200),white)
    # actions while game is paused
    while pause:
        # recognizing events
        for event in pygame.event.get():
            # end game on exit
            if event.type == pygame.QUIT:
                quitgame()
            # if escape key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # unpause
                unpause()
        # buttons with action
        button("restart",150,450,100,50,dark_cyan,cyan,game_loop)
        button("menu",550,450,100,50,dark_yellow,yellow,main_menu)

        # refresh display for cnstant blit 
        pygame.display.update()
        clock.tick(60)


# unpause
def unpause():

    # load variables 
    global pause
    pause = False


# game over
def game_over():

    # stop game music
    mixer.music.fadeout(500)
    # play game over music
    game_overSound.play()
    # load variables for game over loop,score reset and background image
    global g_over
    global score_value
    global background_y

    # actions while game over loop is active
    while g_over:
        
        # background image scrolling algorithm
        rel_y = background_y % background.get_rect().height
        screen.blit(background, (0, rel_y -background.get_rect().height))
        if rel_y < height:
            screen.blit(background, (0, rel_y))
        background_y += 0.5

        # recognizing events
        for event in pygame.event.get():
            # end game on exit
            if event.type == pygame.QUIT:
                quitgame()

        # buttons with action
        button("restart",150,450,100,50,dark_cyan,cyan,game_loop)
        button("menu",550,450,100,50,dark_yellow,yellow,main_menu)
        # show score after game over
        show_score(10, 10)
        # game over text
        message_dispaly("GAME OVER",100,width/2,height/2,white)

        # refresh display for cnstant blit 
        pygame.display.update()
        clock.tick(60)

# game quit
def quitgame():
    
    pygame.quit()
    quit()


main_menu()
game_loop()
quitgame()
