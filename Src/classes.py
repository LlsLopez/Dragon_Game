from random import randrange

import pygame
import os
#imports
# dragon class -------------------------------------------
class Dragon(pygame.sprite.Sprite):
    def __init__(self,x,y,scale,speed,health,dragonType):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.dragonType = dragonType # 0 = player, 1 = normal enemy
        self.enemyMov = "up"
        self.speed = speed
        self.shotCD = 0
        if dragonType == 1:
            self.shotCD = 50 # start with a delayed shot if enemy
        self.bodyCD = 200  # time till body dissappears # update in def shoot aswell
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

    def shoot(self,fireballGroup,fireballImage):
        if (self.shotCD == 0):
            if self.dragonType == 0:
                self.shotCD = 20
                fireshot = FireShot(fireballImage,self.rect.centerx + (1 * self.rect.size[0]), self.rect.centery, .2,True)
                fireballGroup.add(fireshot)
            elif self.dragonType == 1 and self.bodyCD == 200:
                self.shotCD = 50 + randrange(200)
                fireballImage = pygame.transform.flip(fireballImage, True, False)
                fireshot = FireShot(fireballImage, self.rect.centerx - (1 * self.rect.size[0]), self.rect.centery, .2,False)
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
    def enemy_ai(self,fireballGroup,fireballImage):
        # btwn 100-700 X or Y
        # MOVEMENT
        if(self.enemyMov == "down"):
            if(self.rect.bottom <= 700):
                asc = False
                dec = True
            else:
                asc = True
                dec = False
                self.enemyMov = "up"
        if(self.enemyMov == "up"):
            if(self.rect.top >= 100):
                asc = True
                dec = False
            else:
                asc = False
                dec = True
                self.enemyMov = "down"
        if self.alive:
            self.enemy_move(asc,dec)

        # SHOOTING
        self.shoot(fireballGroup,fireballImage)

    def enemy_move(self,ascend,descend):
        dy = 0
        if (ascend == True):
            dy = -self.speed
        elif (descend == True and self.rect.bottom <= 750):
            dy = self.speed
        self.rect.y += dy
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
            if self.bodyCD == 0 : #dont kill player avatar
                self.kill()
           #self.update_animation("death number")


    def draw(self,moveLeft,moveRight,ascend,descend,screen,SCREEN_HEIGHT,SCREEN_WIDTH):
        if(self.alive == True):
            if self.dragonType == 0:
                screen.blit(pygame.transform.flip(self.image,False,False),self.rect)
            elif self.dragonType == 1:
                screen.blit(pygame.transform.flip(self.image,True,False),self.rect)
        else:
            if(self.bodyCD >= 0): # cooldown before body dissappears after death
                self.enemy_move(False,True)
                screen.blit(pygame.transform.flip(self.image, False, False), self.rect)
                #enemy.move(moveLeft, moveRight, ascend, descend, 4,SCREEN_HEIGHT,SCREEN_WIDTH) ???
                self.bodyCD -= 1
    def reset_positon(self): # resets the players position to start
        self.rect.center = (50, 200)
# END dragon class -------------------------------------------

# START Fireshot Class-------------------------------------------
class FireShot(pygame.sprite.Sprite):
    def __init__(self,fireballImage,x,y,scale,playerShot):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = fireballImage
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * (scale)), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.playerShot = playerShot # is it the player's shot?

    def update(self,player,enemyGroup,fireballGroup,spikeGroup,SCREEN_WIDTH):
        if self.playerShot == True: # if player shoot towards right
            self.rect.x += (self.speed)
        elif self.playerShot == False:
            self.rect.x -= self.speed
        #shot offscreen check (delete from memory)
        if(self.rect.right <0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

        #collision check (characters)
        if pygame.sprite.spritecollide(player,fireballGroup,False) and self.playerShot == False:
            if player.alive and player.invulTimer == 0:
                self.kill()
                print("shot hit")
                player.invulTimer = 50
        for enemy in enemyGroup:
            if pygame.sprite.spritecollide(enemy,fireballGroup,False) and self.playerShot == True:
                if enemy.alive:
                    #enemy.health -= player.damage
                    enemy.health -= player.damage
                    print(enemy.health)
                    self.kill()
        if (pygame.sprite.groupcollide(spikeGroup, fireballGroup, False, False) and self.playerShot == True): #stop on impact of spike if player
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

#button Class
class Button():
    def __init__(self,text,color,surface,x,y,size,rectColor,hasRect,isButton):
        self.surface = surface
        self.isButton = isButton
        self.hasRect = hasRect
        self.button = 0 # for collide check in menu
        self.font = pygame.font.Font('../Font/AvQest.ttf',size)
        self.x = x
        self.y = y
        self.size = size
        self.textColor = color
        self.text = text
        self.textO = self.font.render(text,1,color)
        self.textRec = self.textO.get_rect()
        self.textRec = self.textO.get_rect(center = (x,y))
        self.buttonColor = rectColor


    def to_screen(self):
        if self.isButton: #ignores if only a text ; buttonless
            self.button = pygame.Rect(self.textRec.left, self.textRec.top, self.textRec.width, self.textRec.height)
            if self.hasRect:
                pygame.draw.rect(self.surface, self.buttonColor, self.button)
        self.surface.blit(self.textO,self.textRec)

    def hover_button(self):
        self.buttonColor = (0,0,0)
        self.textO = self.font.render(self.text,1,(200,100,30))

    def unhover_button(self): # return to original color
        self.buttonColor = (255,0,0)
        self.textO = self.font.render(self.text, 1, self.textColor)

    def update_text(self,newText):
            self.text = newText
            self.textO = self.font.render(self.text, 1, self.textColor)