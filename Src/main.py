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
difficulty = 1 #default is normal difficulty


#load images
fireballImage = pygame.image.load('../Sprites/Dragon/Projectiles/fireball.png').convert_alpha()
spikeImage = pygame.image.load('../Sprites/Objects/spikeUp.png').convert_alpha()
healthImage = pygame.image.load('../Sprites/Collectibles/heart.png').convert_alpha()
cannonBallImage = pygame.image.load('../Sprites/Collectibles/cannonball.png').convert_alpha()

backgroundColor = (201,97,77)
background = pygame.image.load('../Sprites/Background/cave2.jpg').convert_alpha()
background = pygame.transform.scale(background,(SCREEN_WIDTH*2,SCREEN_HEIGHT))
backgroundRect = background.get_rect()

#def check_position():
    # check if the position of the player is past the background mark to scroll

fireballGroup = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
collectibleGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()

#Define Text Colors
white = (255,255,255)
red = (255,0,0)
test = [False,False,False] #


def difficulty_screen(): # retrieves difficulty settings
    print("test")
    run = True
    click = False
    red = (255, 0, 0)
    mainMenu = classes.Button("Main Menu", white, screen, 85, SCREEN_HEIGHT - 30, 30,red,True, True)
    easy = classes.Button("easy", white, screen, SCREEN_WIDTH / 2, 4 * SCREEN_HEIGHT / 10, 50,red,True, True)
    normal = classes.Button("normal", white, screen, SCREEN_WIDTH / 2, 5 * SCREEN_HEIGHT / 10, 50,red,True, True)
    hard = classes.Button("hard", white, screen, SCREEN_WIDTH / 2, 6 * SCREEN_HEIGHT / 10, 50,red,True, True)
    harder = classes.Button("harder", white, screen, SCREEN_WIDTH / 2, 7 * SCREEN_HEIGHT / 10, 50,red,True, True)
    difficultyValue = difficulty

    while run:
        mouseX, mouseY = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        screenTitle = classes.Button("Difficulty Settings", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 50,red,True, False)

        easy.to_screen()
        normal.to_screen()
        hard.to_screen()
        harder.to_screen()

        screenTitle.to_screen()
        mainMenu.to_screen()

        if mainMenu.button.collidepoint((mouseX, mouseY)):
            mainMenu.hover_button()
            if click:
                #run = False  # back to main menu, ends loop
                return difficultyValue
        elif easy.button.collidepoint((mouseX,mouseY)):
            easy.hover_button()
            desTest = "Decreased enemy health, damage, spawns"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH / 2, 8 * SCREEN_HEIGHT / 10, 30,red,True, False)
            description.to_screen()
            if click:
               print("easy")
               difficultyValue = 0
        elif normal.button.collidepoint((mouseX,mouseY)):
            normal.hover_button()
            desTest = "Normal enemy health, damage, spawns"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH / 2, 8 * SCREEN_HEIGHT / 10, 30,red,True, False)
            description.to_screen()
            if click:
               print("normal")
               difficultyValue = 1
        elif hard.button.collidepoint((mouseX,mouseY)):
            hard.hover_button()
            desTest = "Increased enemy health, damage, hostile spawns, decreased health spawn"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH/2, 8 * SCREEN_HEIGHT / 10, 30,red,True, False)
            description.to_screen()
            if click:
               print("hard")
               difficultyValue = 2
        elif harder.button.collidepoint((mouseX,mouseY)):
            harder.hover_button()
            desTest = "Heavily increased enemy health, damage, spawns, decreased health and health spawn"
            description = classes.Button(desTest, white, screen, SCREEN_WIDTH / 2, 8 * SCREEN_HEIGHT / 10, 30,red,True, False)
            description.to_screen()
            if click:
               print("harder")
               difficultyValue = 3
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


##################################### Run Game
def game_run(difficulty):

    if (difficulty == 0):
        print("easy selected")
        cannonVariableTime = +250
        healthVariableTime = +800
        enemyVariableTime = +300
        player = classes.Dragon(50, 200, .65, 5, 200,200, 0)
    elif (difficulty == 1):
        print("normal selected")
        cannonVariableTime = +180
        healthVariableTime = +1200
        enemyVariableTime = + 220
        player = classes.Dragon(50, 200, .65, 5, 120,120, 0)
    elif (difficulty == 2):
        print("hard selected")
        cannonVariableTime = +110
        healthVariableTime = +1500
        enemyVariableTime = + 120
        player = classes.Dragon(50, 200, .65, 5,100,100,0)
    elif (difficulty == 3):
        print("harder selected")
        cannonVariableTime = +40
        healthVariableTime = +2000
        enemyVariableTime = + 50
        player = classes.Dragon(50, 200, .65, 5,75,75, 0)
    else:
        print("error")

    # Timers
    spikeTimer = 2000
    spikeTimerVary = 1500
    lastSpike = pygame.time.get_ticks()
    mainTimer = 0
    cannonBallTimer = 0

    nextCannonBall = 300  # shoot first cannon ball 300 frames in
    healthTimer = 0
    nextHealth = 600  # first health 600 frames in
    enemySpawn = 0

    backgroundScroll = 0
    backgroundScrollSpeed = 5

    score = 0

    # player action variables
    moveRight = False
    moveLeft = False
    ascend = False
    descend = False
    shoot = False

    # Text and buttons
    scale = 20
    healthUI = classes.Button("Health:" + str(player.health), white, screen, scale * 3, scale , scale,red,True, True)
    scoreUI = classes.Button("Score:"+str(score),white,screen,SCREEN_WIDTH/2,scale,scale,red,False,True)
    #determine diff here

    print("Test")
    print(player.health)



    runGame = True
    while(runGame == True):
        #print(test)
        #print(difficulty)
        clock.tick(FPS)
        mainTimer += 1
        #Draw Background with scrolling effect
        screen.blit(background,(backgroundScroll,0))
        backgroundScroll -= backgroundScrollSpeed
        if abs(backgroundScroll) > SCREEN_WIDTH:
            backgroundScroll = 0
        player.update()
        player.draw(moveLeft,moveRight,ascend,descend,screen,SCREEN_HEIGHT,SCREEN_WIDTH)

        #UI
        healthUI.update_text("Health:" + str(player.health))
        healthUI.to_screen()
        scoreUI.update_text("Score:"+str(score))
        scoreUI.to_screen()

        for enemy in enemyGroup:
            enemy.update()
            enemy.enemy_ai(fireballGroup,fireballImage)
            enemy.draw(moveLeft, moveRight, ascend, descend, screen, SCREEN_HEIGHT, SCREEN_HEIGHT)
            score += enemy.killed() # add score for enemy killed
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
                nextCannonBall = randrange(100) + cannonVariableTime
                cannonBallTimer = 0
                randX = randrange(400) + 200 # X coordinate
                newC = classes.Collectible(cannonBallImage,1,SCREEN_WIDTH,randX)
                collectibleGroup.add(newC)
            cannonBallTimer += 1
            if(healthTimer == nextHealth): # Health spawn timer
                healthTimer = 1
                nextHealth = randrange(1000) + healthVariableTime
                randX = randrange(400) + 200  # X coordinate
                newC = classes.Collectible(healthImage, 2, SCREEN_WIDTH, randX)
                collectibleGroup.add(newC)
            healthTimer += 1
            collectibleGroup.update(backgroundScrollSpeed, player, collectibleGroup, FPS)

            #Enemy Spawner
            #NOTE: make game harder, decrease timers ( turn flat numbers into multipliers? multiplier * 100)
            if(enemySpawn <= 0):
                enemySpawn = randrange(300) + enemyVariableTime
                randX = SCREEN_WIDTH - randrange(200) - 40
                randY = randrange(2) # 0 player, 1 enemy classic
                print(randY)
                if randY == 0:
                    randY = 0
                elif randY == 1:
                    randY = SCREEN_HEIGHT

                if difficulty >= randrange(6): #easy never spawns high level
                    spawnType = 2
                    healthType = 100
                else:
                    spawnType = 1
                    healthType = 60
                enemy = classes.Dragon(randX,randY,.65,5,healthType,healthType,spawnType)
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


        if(player.alive == False):
            runGame = False  # stop the game
            # RESET ALL VARAIBLES FOR NEXT GAME
            # Kill all units in game for next game
            enemyGroup.empty()
            spikeGroup.empty()
            collectibleGroup.empty()
            fireballGroup.empty()
            player.alive = True
            player.health = 100
            # reset player position
            player.reset_positon()


            return

        score += 1 # increase score counter by frame
        pygame.display.update()


    pygame.quit()

def menu():
    click = False
    run = True
    tempArray = [difficulty,0,0]

    # Menu Options and Title Screen
    gameTitle = classes.Button("Dragon Game", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 50,red,True, False)

    difficultyButton = classes.Button("Difficulty", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 100, 30,red,True,True)
    optionButton = classes.Button("Options", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 150, 30,red,True, True)
    helpButton = classes.Button("Help", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 200, 30,red,True, True)
    startButton = classes.Button("Start Game", white, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 250, 30,red,True, True)


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
                game_run(tempArray[0])

        elif difficultyButton.button.collidepoint((mouseX,mouseY)):
            difficultyButton.hover_button()
            if click:
                tempArray[0] = difficulty_screen() # get difficulty value
                print(tempArray)
        else:
            startButton.unhover_button()
            difficultyButton.unhover_button()

        ## NOTE: ADD OPTIONS AND HELP LATER

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

menuData = menu() # get difficulty settings
settings = menuData
difficulty = menuData[0]


