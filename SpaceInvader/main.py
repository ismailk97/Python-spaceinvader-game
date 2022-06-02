import random
import pygame
import math


#  Initializing the pygame
import pygame.display

pygame.init()
#  creating the screen width and height
screen = pygame.display.set_mode((800, 600))

# Title and Icon change
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceinvadericon.png')
pygame.display.set_icon(icon)


#background loading
background = pygame.image.load('background.jpg')


# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (0,255,255))
    screen.blit(score,(textY,textX))



#Enemy
enemyImg = pygame.image.load('enemy.png')
#have to set it to 700 else it bugs and spawn
# outside and falls of screen when hit multiple times
enemyX = random.randint(0, 700)
enemyY = random.randint(0,50)
enemyX_change = 0.5
enemyY_change = 40

# bullet
# ready meaning you cant see the bullet yet
# fire the bullet is visible
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def enemy(x, y):
    screen.blit(enemyImg, (enemyX, enemyY))


# creating a function for player easier to call it in the loop
# .blit() means to draw
# x y coordinates desides where it spawns on the screen.
def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+18, y))

#we are gonna use this to detect when bullet hit enemy
# the distance formula is picked from googling "distance between two coordinates"
def isCollision(enemyX, enemyY, bulletX, bulletY):
    #math.pow is the exponent function in python
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# to be able to close the program we make a variable acting as a switch here
running = True
# if we do not have a loop here the program screen will close after executing
# setting it so when we close the program it wil quit.
while running:
    screen.fill((211, 55, 0))
    # background loading
    screen.blit(background, (0, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    #controller for movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                #set the value to playerx here and change it in movement
                #to bulletX soo bullet does not follow spaceship movement
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # adding boundaries so player cant go outside of map
    # 736 because player is 64bit 800-64
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


#boundaries for enemy + adding movement
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change



    # put it over the update else it will not be shown
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX,textY)

    # bullet movement:
    # if the bullet reaches frame 480 it resets and bullet change becomes ready
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #collission detection, setting bullet back to start point and
    #ready to fire
    collision = isCollision(enemyX,enemyY,bulletX,bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score_value += 10
        print(score_value)
        #setting the enemy to respawn when hit
        enemyX = random.randint(0, 700)
        enemyY = random.randint(0, 50)

    # updating the screen color
    pygame.display.update()






