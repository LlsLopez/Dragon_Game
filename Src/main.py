import pygame
import time
import os
from random import randrange


import classes

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * .6)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Dragon Game")

clock = pygame.time.Clock()
FPS = 60

# temp
backgroundScroll = 0
backgroundScrollSpeed = 5
spikeTimer = 2000
spikeTimerVary = 1500
lastSpike = pygame.time.get_ticks()
mainTimer = 0
cannonBallTimer = 0
nextCannonBall = 300 # shoot first cannon ball 300 frames in
healthTimer = 0
nextHealth = 600 # first health 600 frames in


#load images
fireballImage = pygame.image.load('../Sprites/Dragon/Projectiles/fireball.png').convert_alpha()
spikeImage = pygame.image.load('../Sprites/Objects/spikeUp.png').convert_alpha()
healthImage = pygame.image.load('../Sprites/Collectibles/heart.png').convert_alpha()
cannonBallImage = pygame.image.load('../Sprites/Collectibles/cannonball.png').convert_alpha()

#player action variables
moveRight = False
moveLeft = False
ascend = False
descend = False
shoot = False


backgroundColor = (201,97,77)
background = pygame.image.load('../Sprites/Background/cave2.jpg').convert_alpha()
background = pygame.transform.scale(background,(SCREEN_WIDTH*2,SCREEN_HEIGHT))
backgroundRect = background.get_rect()

#def check_position():
    # check if the position of the player is past the background mark to scroll

fireballGroup = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
player = classes.Dragon(50,200,.65,5,100,0)
enemy = classes.Dragon(400,600,.65,5,50,1)
collectibleGroup = pygame.sprite.Group()

#delete after
test = True


runGame = True
while(runGame == True):
    clock.tick(FPS)
    mainTimer += 1
    #Draw Background with scrolling effect
    screen.blit(background,(backgroundScroll,0))
    backgroundScroll -= backgroundScrollSpeed
    if abs(backgroundScroll) > SCREEN_WIDTH:
        backgroundScroll = 0
    player.update()
    player.draw(moveLeft,moveRight,ascend,descend,screen,SCREEN_HEIGHT,SCREEN_WIDTH)
    enemy.update()
    enemy.draw(moveLeft,moveRight,ascend,descend,screen,SCREEN_HEIGHT,SCREEN_HEIGHT)
    fireballGroup.update(player,enemy,fireballGroup,spikeGroup,SCREEN_WIDTH)
    fireballGroup.draw(screen)
    spikeGroup.draw(screen)
    collectibleGroup.draw(screen)

    if(player.alive == True):
        if(shoot == True):                      # 0 index = width
            player.shoot(player,fireballGroup,fireballImage)

        player.move(moveLeft,moveRight,ascend,descend,0,SCREEN_WIDTH,SCREEN_HEIGHT)

        currentTime = pygame.time.get_ticks()
        if(currentTime - lastSpike > spikeTimer):
            randLocation = randrange(2) # spawn at top or bottom of screen
            randSize = randrange(5) # spawn with a random height
            if(randLocation == 0):
                newSpike = classes.spike(spikeImage,SCREEN_WIDTH, SCREEN_HEIGHT, .5,1,randSize)
            else:
                newSpike = classes.spike(spikeImage,SCREEN_WIDTH,0, .5,2,randSize)
            spikeGroup.add(newSpike)
            #chance for spike to spawn earlier, random time for some variation
            rand3 = randrange(spikeTimerVary)
            lastSpike = currentTime + rand3
        spikeGroup.update(backgroundScrollSpeed,player,spikeGroup,FPS)

        if(cannonBallTimer == nextCannonBall): # CannonBall Generator : Range #200 -
            nextCannonBall = randrange(200)
            cannonBallTimer = 0
            randX = randrange(400) + 200 # X coordinate
            newC = classes.Collectible(cannonBallImage,1,SCREEN_WIDTH,randX)
            collectibleGroup.add(newC)
        cannonBallTimer += 1
        if(healthTimer == nextHealth):
            healthTimer = 0
            nextHealth = randrange(1000) + 1500
            randX = randrange(400) + 200  # X coordinate
            newC = classes.Collectible(healthImage, 2, SCREEN_WIDTH, randX)
            collectibleGroup.add(newC)
        healthTimer += 1
        collectibleGroup.update(backgroundScrollSpeed, player, collectibleGroup, FPS)

#movement section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveLeft = True;
            if event.key == pygame.K_d:
                moveRight = True;
            if event.key == pygame.K_w:
                ascend = True
            if event.key == pygame.K_s:
                descend = True
            if event.key == pygame.K_SPACE:
                shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False;
            if event.key == pygame.K_d:
                moveRight = False;
            if event.key == pygame.K_w:
                ascend = False
            if event.key == pygame.K_s:
                descend = False
            if event.key == pygame.K_SPACE:
                shoot = False




    pygame.display.update()
pygame.quit()