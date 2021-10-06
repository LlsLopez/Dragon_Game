import pygame
import os
#imports
# dragon class -------------------------------------------
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
            fileNum = len(os.listdir(f'../Sprites/Dragon/{anim}'))
            #RESET TEMP LIST
            tempList = []
            for i in range(fileNum):
                image = pygame.image.load(f'../Sprites/Dragon/{anim}/{anim}{i}.png').convert_alpha()
                image = pygame.transform.scale(image,(int(image.get_width()*scale),int(image.get_height()*scale)))
                tempList.append(image)
            self.animations.append(tempList)

        self.image = self.animations[self.animationIndex][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def shoot(self,player,fireballGroup,fireballImage):
        if (self.shotCD == 0):
            self.shotCD = 20
            fireshot = FireShot(fireballImage,player.rect.centerx + (1 * player.rect.size[0]), player.rect.centery, .2)
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
    def move(self,moveLeft,moveRight,ascend,descend,dy1,SCREEN_WIDTH,SCREEN_HEIGHT):
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


    def draw(self,enemy,moveLeft,moveRight,ascend,descend,screen,SCREEN_HEIGHT,SCREEN_WIDTH):
        if(self.alive == True):
            screen.blit(pygame.transform.flip(self.image,False,False),self.rect)
        else:
            if(self.bodyCD >= 0): # cooldown before body dissappears after death
                screen.blit(pygame.transform.flip(self.image, False, False), self.rect)
                enemy.move(moveLeft, moveRight, ascend, descend, 4,SCREEN_HEIGHT,SCREEN_WIDTH)
                self.bodyCD -= 1
# END dragon class -------------------------------------------

# START Fireshot Class-------------------------------------------
class FireShot(pygame.sprite.Sprite):
    def __init__(self,fireballImage,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = fireballImage
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * (scale)), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self,player,enemy,fireballGroup,spikeGroup,SCREEN_WIDTH):
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
# END Fireshot Class-------------------------------------------

#START spike class --------------------------------------------------
class spike(pygame.sprite.Sprite):
    def __init__(self,spikeImage,x,y,scale,layout,size):
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

    def update(self,backgroundScrollSpeed,player,spikeGroup,FPS):
        self.rect.x -= backgroundScrollSpeed
        if (self.rect.right < 0):
            self.kill()
        if (pygame.sprite.spritecollide(player, spikeGroup, False)):
            if player.alive and player.invulTimer <= 0:
                player.invulTimer = FPS * 3  # time in secaonds
                print("hit")
#END spike class --------------------------------------------------
class Collectible(pygame.sprite.Sprite):
    def __init__(self,image,code,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.code = code
        if(code == 1): #CannonBall
            self.image = pygame.transform.scale(self.image, (
                int(self.image.get_width() * (.1)), int(self.image.get_height() * .1)))  # temporarily smaller
            self.healthEffect = -20
        elif(code == 2): # Health
            self.image = pygame.transform.scale(self.image, (
                int(self.image.get_width() * (.2)), int(self.image.get_height() * .2)))  # temporarily smaller
            self.healthEffect = +25
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self,backgroundScrollSpeed,player,cGroup,FPS):
        self.rect.x -= backgroundScrollSpeed
        if(self.rect.right <0):
            self.kill()
        if (pygame.sprite.spritecollide(player, cGroup, False)):
            if(self.healthEffect > 0 or player.invulTimer <= 0 ): #if a heal OR damaging attack w/ no invulnerability
                player.health += self.healthEffect
            if(player.health > 100):
                player.health = 100 # prevent going over max health
            if(player.health < 0):
                player.health = 0
            self.kill()
            print(self.healthEffect)
            print(player.health)

