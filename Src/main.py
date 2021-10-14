import sys

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
difficulty = "Normal"

#Timers
spikeTimer = 2000
spikeTimerVary = 1500
lastSpike = pygame.time.get_ticks()
mainTimer = 0
cannonBallTimer = 0
nextCannonBall = 300 # shoot first cannon ball 300 frames in
healthTimer = 0
nextHealth = 600 # first health 600 frames in
enemySpawn = 0

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
#enemy = classes.Dragon(400,600,.65,5,50,1)
#enemy2 = classes.Dragon(300,400,.65,5,50,1)
collectibleGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
#enemyGroup.add(enemy)
#enemyGroup.add(enemy2)
#delete after

#Define Text Colors
white = (255,255,255)
red = (255,0,0)
test = [False,False,False] #


def difficulty_screen():
    print("test")
    run = True
    click = False
    mainMenu = classes.Button("Main Menu", white, screen, 85, SCREEN_HEIGHT - 30, 30, True)
    easy = classes.Button("easy", white, screen, SCREEN_WIDTH / 2, 4 * SCREEN_HEIGHT / 10, 50, True)
    normal = classes.Button("normal", white, screen, SCREEN_WIDTH / 2, 5 * SCREEN_HEIGHT / 10, 50, True)
    hard = classes.Button("hard", white, screen, SCREEN_WIDTH / 2, 6 * SCREEN_HEIGHT / 10, 50, True)
    harder = classes.Button("harder", white, screen, SCREEN_WIDTH / 2, 7 * SCREEN_HEIGHT / 10, 50, True)

    while run:
        mouseX, mouseY = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        screenTitle = classes.Button("Difficulty Settings", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 50, False)

        easy.to_screen()
        normal.to_screen()
        hard.to_screen()
        harder.to_screen()

        screenTitle.to_screen()
        mainMenu.to_screen()

        if mainMenu.button.collidepoint((mouseX, mouseY)):
            mainMenu.hover_button()
            if click:
                run = False # back to main menu, ends loop
        elif easy.button.collidepoint((mouseX,mouseY)):
            easy.hover_button()
            desTest = "Decreased enemy health, damage, spawns"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH / 2, 8 * SCREEN_HEIGHT / 10, 30, False)
            description.to_screen()
            if click:
               print("easy")
        elif normal.button.collidepoint((mouseX,mouseY)):
            normal.hover_button()
            desTest = "Normal enemy health, damage, spawns"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH / 2, 8 * SCREEN_HEIGHT / 10, 30, False)
            description.to_screen()
            if click:
               print("normal")
        elif hard.button.collidepoint((mouseX,mouseY)):
            hard.hover_button()
            desTest = "Increased enemy health, damage, hostile spawns, decreased health spawn"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH/2, 8 * SCREEN_HEIGHT / 10, 30, False)
            description.to_screen()
            if click:
               print("hard")
        elif harder.button.collidepoint((mouseX,mouseY)):
            harder.hover_button()
            desTest = "Heavily increased enemy health, damage, spawns, decreased health and health spawn"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH / 2, 8 * SCREEN_HEIGHT / 10, 30, False)
            description.to_screen()
            if click:
               print("harder")
        else:
            mainMenu.unhover_button()
            easy.unhover_button()
            normal.unhover_button()
            hard.unhover_button()
            harder.unhover_button()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


def menu():
    click = False
    run = True
    tempArray = [0,0,0]

    # Menu Options and Title Screen
    gameTitle = classes.Button("Dragon Game", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 50, False)

    difficultyButton = classes.Button("Difficulty", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 100, 30, True)
    optionButton = classes.Button("Options", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 150, 30, True)
    helpButton = classes.Button("Help", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 200, 30, True)
    startButton = classes.Button("Start Game", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 250, 30, True)

    while run:
        #Center text with screenwidth/2 screenheight/2
        screen.fill((0, 0, 0))

        mouseX, mouseY = pygame.mouse.get_pos()

        gameTitle.to_screen()
        difficultyButton.to_screen()
        optionButton.to_screen()
        helpButton.to_screen()
        startButton.to_screen()

        if startButton.button.collidepoint((mouseX, mouseY)):
            startButton.hover_button()
            if click:
                run = False # end the loop, jump to game
        elif difficultyButton.button.collidepoint((mouseX,mouseY)):
            difficultyButton.hover_button()
            if click:
                difficulty_screen()
        else:
            startButton.unhover_button()
            difficultyButton.unhover_button()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)
    return tempArray

menuData = menu()
test = menuData
runGame = True
while(runGame == True):
    print(test)
    clock.tick(FPS)
    mainTimer += 1
    #Draw Background with scrolling effect
    screen.blit(background,(backgroundScroll,0))
    backgroundScroll -= backgroundScrollSpeed
    if abs(backgroundScroll) > SCREEN_WIDTH:
        backgroundScroll = 0
    player.update()
    player.draw(moveLeft,moveRight,ascend,descend,screen,SCREEN_HEIGHT,SCREEN_WIDTH)

    for enemy in enemyGroup:
        enemy.update()
        enemy.enemy_ai(fireballGroup,fireballImage)
        enemy.draw(moveLeft, moveRight, ascend, descend, screen, SCREEN_HEIGHT, SCREEN_HEIGHT)
    fireballGroup.update(player,enemyGroup,fireballGroup,spikeGroup,SCREEN_WIDTH)
    fireballGroup.draw(screen)
    spikeGroup.draw(screen)
    collectibleGroup.draw(screen)

    if(player.alive == True):
        if(shoot == True):                      # 0 index = width
            player.shoot(fireballGroup,fireballImage)

        player.move(moveLeft,moveRight,ascend,descend,0,SCREEN_WIDTH,SCREEN_HEIGHT)

        currentTime = pygame.time.get_ticks()
        if(currentTime - lastSpike > spikeTimer): ## spike spawner
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
        if(healthTimer == nextHealth): # Health spawn timer
            healthTimer = 0
            nextHealth = randrange(1000) + 1500
            randX = randrange(400) + 200  # X coordinate
            newC = classes.Collectible(healthImage, 2, SCREEN_WIDTH, randX)
            collectibleGroup.add(newC)
        healthTimer += 1
        collectibleGroup.update(backgroundScrollSpeed, player, collectibleGroup, FPS)

        #Enemy Spawner
        #NOTE: make game harder, decrease timers ( turn flat numbers into multipliers? multiplier * 100)
        if(enemySpawn <= 0):
            enemySpawn = randrange(300) + 120
            randX = SCREEN_WIDTH - randrange(200) - 40
            randY = randrange(2) # 0 player, 1 enemy classic
            print(randY)
            if randY == 0:
                randY = 0
            elif randY == 1:
                randY = SCREEN_HEIGHT
            enemy = classes.Dragon(randX,randY,.65,5,50,1)
            enemyGroup.add(enemy)
        enemySpawn -= 1


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