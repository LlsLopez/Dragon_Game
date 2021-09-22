import pygame
import time
import os
from random import randrange

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



#load images
fireballImage = pygame.image.load('Sprites/Dragon/Projectiles/fireball.png').convert_alpha()
spikeImage = pygame.image.load('Sprites/Objects/spikeUp.png').convert_alpha()

#player action variables
moveRight = False
moveLeft = False
ascend = False
descend = False
shoot = False


backgroundColor = (201,97,77)
background = pygame.image.load('Sprites/Background/cave2.jpg').convert_alpha()
background = pygame.transform.scale(background,(SCREEN_WIDTH*2,SCREEN_HEIGHT))
backgroundRect = background.get_rect()

'''   delete?????
def draw_background(bs):
    #screen.fill(backgroundColor)
    #screen.blit(background,(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    #screen.blit(background, (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (bs, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (bs+SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    #bs -= backgroundScrollSpeed
    #if(abs(bs)>SCREEN_WIDTH):
       # bs = 0
    background.rect.x -= backgroundScrollSpeed
    return bs

'''

#def check_position():
    # check if the position of the player is past the background mark to scroll


class Dragon(pygame.sprite.Sprite):
    def __init__(self,x,y,scale,speed,health):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.shotCD = 0
        self.bodyCD = 200  # time till body dissappears
        self.health = health
        self.maxHealth = 300
        self.damage = 20  # base damage, can be changed with powerups (future)
        self.invulTimer = 0 # time invulnerable

        self.animations = []
        self.animationIndex = 0
        self.frameIndex = 0
        self.update_time = pygame.time.get_ticks()


        animationType = ['Flying']
        for anim in animationType:
            #check file amount in folder
            fileNum = len(os.listdir(f'Sprites/Dragon/{anim}'))
            #RESET TEMP LIST
            tempList = []
            for i in range(fileNum):
                image = pygame.image.load(f'Sprites/Dragon/{anim}/{anim}{i}.png').convert_alpha()
                image = pygame.transform.scale(image,(int(image.get_width()*scale),int(image.get_height()*scale)))
                tempList.append(image)
            self.animations.append(tempList)

        self.image = self.animations[self.animationIndex][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def shoot(self):
        if (self.shotCD == 0):
            self.shotCD = 20
            fireshot = FireShot(player.rect.centerx + (1 * player.rect.size[0]), player.rect.centery, .2)
            fireballGroup.add(fireshot)

    def update_animation(self):
        animationCD = 100 # animation cooldown
        self.image = self.animations[self.animationIndex][self.frameIndex]
        if(pygame.time.get_ticks() - self.update_time) > animationCD:
            self.frameIndex += 1
            self.update_time = pygame.time.get_ticks()
            if(self.frameIndex >= len(self.animations[self.animationIndex])):
                 if(self.animationIndex == 0 and self.alive == False):
                        self.frameIndex = len(self.animations[self.animationIndex]) -1
                 else:
                     self.frameIndex = 0

    def update(self):
        self.update_animation()
        self.checkIfAlive()
        #update cd
        if self.shotCD > 0:
            self.shotCD -= 1
        if self.invulTimer > 0:
            self.invulTimer -= 1
    def move(self,moveLeft,moveRight,ascend,descend,dy1):
        dx = 0
        dy = dy1
        if(self.alive == True):
            if(moveLeft == True):
                dx = -self.speed
            if(moveRight == True):
                dx = self.speed
            if(ascend == True):
                dy = -self.speed
            if(descend == True):
                dy = self.speed

        #Collision Check for bounds (all sides)
        if(self.rect.bottom + dy >= SCREEN_HEIGHT):
            dy = 0
        if(self.rect.top + dy <= 0):
            dy = 0
        if(self.rect.right + dx >= SCREEN_WIDTH):
            dx = 0
        if(self.rect.left + dx <= 0):
            dx = 0
        #update position
        self.rect.x += dx
        self.rect.y += dy

    def checkIfAlive(self):
        if self.health <= 0:
            self.health = 0
            #self.speed = 0 # no continued movement, dies on spot
            self.alive = False
           #self.update_animation("death number")


    def draw(self):
        if(self.alive == True):
            screen.blit(pygame.transform.flip(self.image,False,False),self.rect)
        else:
            if(self.bodyCD >= 0): # cooldown before body dissappears after death
                screen.blit(pygame.transform.flip(self.image, False, False), self.rect)
                enemy.move(moveLeft, moveRight, ascend, descend, 4)
                self.bodyCD -= 1

class FireShot(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = fireballImage
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * (scale)), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        self.rect.x += (self.speed)
        #shot offscreen check (delete from memory)
        if(self.rect.right <0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

        #collision check (characters)
        if pygame.sprite.spritecollide(player,fireballGroup,False):
            if player.alive:
                self.kill()
        if pygame.sprite.spritecollide(enemy,fireballGroup,False):
            if enemy.alive:
                #enemy.health -= player.damage
                enemy.health -= player.damage
                print(enemy.health)
                self.kill()
        if (pygame.sprite.groupcollide(spikeGroup, fireballGroup, False, False)): #stop on impact of spike
            self.kill()
class spike(pygame.sprite.Sprite):
    def __init__(self,x,y,scale,layout,size):
        pygame.sprite.Sprite.__init__(self)
        self.image = spikeImage
        self.image = pygame.transform.scale(self.image, (
        int(self.image.get_width() * (scale)), int(self.image.get_height() * size * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.layout = layout
        self.damage = 20
        if(layout == 2):
            self.image = pygame.transform.flip(self.image,False,True)


    def update(self):
        self.rect.x -= backgroundScrollSpeed
        if(self.rect.right < 0):
            self.kill()
        if (pygame.sprite.spritecollide(player, spikeGroup, False)):
            if player.alive and player.invulTimer <= 0:
                player.invulTimer = FPS * 3 # time in secaonds
                print("hit")

fireballGroup = pygame.sprite.Group()
spikeGroup = pygame.sprite.Group()
player = Dragon(50,200,.65,5,100)
enemy = Dragon(400,600,.65,5,50)

runGame = True
while(runGame == True):
    clock.tick(FPS)
    #Draw Background with scrolling effect
    screen.blit(background,(backgroundScroll,0))
    backgroundScroll -= backgroundScrollSpeed
    if abs(backgroundScroll) > SCREEN_WIDTH:
        backgroundScroll = 0
    player.update()
    player.draw()
    enemy.update()
    enemy.draw()
    fireballGroup.update()
    fireballGroup.draw(screen)
    spikeGroup.draw(screen)

    if(player.alive == True):
        if(shoot == True):                      # 0 index = width
            player.shoot()

        player.move(moveLeft,moveRight,ascend,descend,0)

        currentTime = pygame.time.get_ticks()
        if(currentTime - lastSpike > spikeTimer):
            randLocation = randrange(2) # spawn at top or bottom of screen
            randSize = randrange(5) # spawn with a random height
            if(randLocation == 0):
                newSpike = spike(SCREEN_WIDTH, SCREEN_HEIGHT, .5,1,randSize)
            else:
                newSpike = spike(SCREEN_WIDTH,0, .5,2,randSize)
            spikeGroup.add(newSpike)
            #chance for spike to spawn earlier, random time for some variation
            rand3 = randrange(spikeTimerVary)
            lastSpike = currentTime + rand3
        spikeGroup.update()

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