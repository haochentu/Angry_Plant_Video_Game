# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:24:57 2022

@author: Haochen Tu

Angry Plants Game Manager
"""
import pygame
from .basicManager import BasicManager
import pygame 
import os
import random
import json
import sys
import time, threading
from modules.vector2D import Vector2
from modules.frameManager import FrameManager
from modules.buttonManager import ButtonManager
from modules.soundManager import SoundManager
from modules.sunflower import Sunflower
from modules.animals import Fox, Otter, Cat, Panda, Dragon, AbstractAnimal
from modules.weapons import FoxWeapon, OtterWeapon, CatWeapon, PandaWeapon, DragonWeapon
from modules.enemy import Cactus, Mushroom, Pumpkin, Flower, Dandelion
from .drawable import Drawable

class GameManager(BasicManager):
    
   def __init__(self, screenSize, loadFile):
   
       self._loadFile = loadFile
       self._screenSize = screenSize
   
   def load(self):
              
       filePtr = open(os.path.join("resources", "levels", self._loadFile))      
       info = json.load(filePtr)
       filePtr.close()
       
       self._cactusAppearTimes = info["cactus"]
       self._pumpkinAppearTime = info["pumpkins"]
       self._mushroomAppearTime = info["mushrooms"]
       self._flowerAppearTime = info["flowers"]
       self._dandelionAppearTime = info["dandelions"]
       
       self._fm = FrameManager().getInstance()
       
       if self._loadFile == "jsonLevel0.txt":
           self._background = self._fm.getFrame("background.png")
       
       elif self._loadFile == "jsonLevel1.txt":
            self._background = self._fm.getFrame("background1.png")
      
       elif self._loadFile == "jsonLevel2.txt":
            self._background = self._fm.getFrame("background2.png")
           
       
       self._sunflower1 = Sunflower(Vector2(386,15))
       self._sunflower2 = Sunflower(Vector2(386,85))
       self._sunflower3 = Sunflower(Vector2(386,155))
       
       self._bm = ButtonManager()
       
       self._drawObj = None
       
       # animals list
       self._foxes = [] 
       self._otters = []
       self._cats = []
       self._pandas = []
       self._dragons = []
       self._buttons = []
       self._animalCollection = []
       self._animalCount = len(self._foxes)+ len(self._otters) + len(self._cats) + len(self._pandas) + len(self._dragons) 
       
       self._skulls = []
       
       # weapons list
       self._foxWeapon = []
       self._otterWeapon = []
       self._catWeapon = []
       self._pandaWeapon = []
       self._dragonWeapon = []
       self._allWeapon = []

       # enemy list
       self._cactuses  = []
       self._mushrooms = []
       self._pumpkins = []
       self._flowers = []
       self._dandelions = []
       
       self._dx = 0
       
       self._enemyCollection = []

       self._enemyNumber = 0 
       
       self._totalTime = 0
      
       self._enemyCount = len(self._cactusAppearTimes) + len(self._pumpkinAppearTime) + len(self._mushroomAppearTime) + len(self._flowerAppearTime) + len(self._dandelionAppearTime)
       
       self._enemyCountB = self._enemyCount
       
       self._progress = self._enemyNumber/self._enemyCountB

       self._moving = False
       
       # money left 
       if self._loadFile == "jsonLevel2.txt":
           self._money = 2000
       else: 
           self._money = 1500
       self._font = pygame.font.Font("freesansbold.ttf", 12)
       
       if self._loadFile == "jsonLevel2.txt":
           self._foxMoney = self._font.render("150" , True, (255,255,0))     
           self._otterMoney = self._font.render("100" , True, (255,255,0))
           self._catMoney = self._font.render("200" , True, (255,255,0))
           self._pandaMoney = self._font.render("350" , True, (255,255,0))
           self._dragonMoney = self._font.render("500" , True, (255,255,0))
       
       else: 
       #self._moneyleft = self._font.render("Money: " + str(self._money), True, (2,7,93))
           self._foxMoney = self._font.render("150" , True, (2,7,93))     
           self._otterMoney = self._font.render("100" , True, (2,7,93))
           self._catMoney = self._font.render("200" , True, (2,7,93))
           self._pandaMoney = self._font.render("350" , True, (2,7,93))
           self._dragonMoney = self._font.render("500" , True, (2,7,93))
       
       #sound effect 
       self._bulletNoise = SoundManager.getInstance()
       
       #bgm
       self._bgm = SoundManager.getInstance()
       
       #level star
       self._star = Drawable ("star.png", (160,90))
       
       self._winStar = False 
   
   def draw(self, drawSurface):
      # draw everything
      drawSurface.blit(self._background, (0,0))
      self._percentage = "{:.0%}".format(self._progress)
      
      if self._loadFile == "jsonLevel2.txt":
          self._moneyleft = self._font.render("Money: " + str(self._money), True, (255,255,0))
          self._moneyReserve = self._font.render("(Max: 1500) ", True, (255,255,204))
          self._animalCounts = self._font.render("Denfenders: " + str(self._animalCount), True, (255, 0, 0))
          self._animalCap = self._font.render("(Max: 25) ", True, (255,255,204))
          self._printPercentage = self._font.render("Progress: " + str(self._percentage), True, (255,0,0))

      else: 
          self._moneyleft = self._font.render("Money: " + str(self._money), True, (2,7,93))
          self._moneyReserve = self._font.render("(Max: 1500) ", True, (153,255,255))
          self._animalCounts = self._font.render("Denfenders: " + str(self._animalCount), True, (2,7,93))
          self._animalCap = self._font.render("(Max: 25) ", True, (153,255,255))
          self._printPercentage = self._font.render("Progress: " + str(self._percentage), True, (2,7,93))
      
      drawSurface.blit(self._moneyleft, (360, 252))
      drawSurface.blit(self._moneyReserve, (362, 265))
      drawSurface.blit(self._animalCounts, (145, 5))
      drawSurface.blit(self._animalCap, (235, 5))
      drawSurface.blit(self._printPercentage, (350, 5))
      drawSurface.blit(self._foxMoney, (61, 296))
      drawSurface.blit(self._otterMoney, (16, 296))
      drawSurface.blit(self._catMoney, (110, 296))
      drawSurface.blit(self._pandaMoney, (157, 296))
      drawSurface.blit(self._dragonMoney, (206, 296))
      
      self._sunflower1.draw(drawSurface)
      self._sunflower2.draw(drawSurface)
      self._sunflower3.draw(drawSurface)
      
      # initiate the buttom manager so it can draw the animals buttoms
      self._bm.draw(drawSurface)

      if self._moving:
          self._drawObj.draw(drawSurface)
      
      # animals 
      for fightFox in self._foxes:
          fightFox.draw(drawSurface)
      for fightOtter in self._otters:
          fightOtter.draw(drawSurface)
      for fightCat in self._cats:
          fightCat.draw(drawSurface)
      for fightPanda in self._pandas:
          fightPanda.draw(drawSurface)
      for fightDragon in self._dragons:
          fightDragon.draw(drawSurface)
          
        
      # weapons
      for bullet in self._foxWeapon: 
          bullet.draw(drawSurface)
      for bullet in self._otterWeapon: 
          bullet.draw(drawSurface)
      for bullet in self._catWeapon: 
          bullet.draw(drawSurface)
      for bullet in self._pandaWeapon: 
          bullet.draw(drawSurface)
      for bullet in self._dragonWeapon: 
          bullet.draw(drawSurface)

      # enemy
      for cactus in self._cactuses:
          cactus.draw(drawSurface)
      for mushroom in self._mushrooms:
          mushroom.draw(drawSurface)
      for pumpkin in self._pumpkins:
          pumpkin.draw(drawSurface)
      for flower in self._flowers:
          flower.draw(drawSurface)
      for dandelion in self._dandelions:
          dandelion.draw(drawSurface)
          
      if self._enemyCount == 0 and self._loadFile != "jsonLevel2.txt":
          self._star.draw(drawSurface)
   
   def handleEvent(self, event):
       # when clicked down the buttom, the correct animal image will be created 
       SCALE = 2
       
       if event.type == pygame.MOUSEBUTTONDOWN and self._money > 0 and self._animalCount <25:

              adjustedPos = list([int(x / SCALE) for x in event.pos])
              result = self._bm.handleEvent(event, adjustedPos, self._money)
              if result != None:
                  self._moving = True
                  self._buttons.append(result)
                  self._drawObj = result
                  
              elif self._star.getCollisionRect().collidepoint(adjustedPos):
                  self._winStar = True 
                  
       #when the user lift the mouse, we will create a new image at the place where the drawObj is
       elif event.type == pygame.MOUSEBUTTONUP and self._animalCount <25:
             self._moving = False
             
             if type(self._drawObj) == Fox and self._drawObj.getPosition()[1] > 0 and self._drawObj.getPosition()[1] < 200:
                 self._foxes.append(Fox(self._drawObj.getPosition()))
                 self._money = self._money - 150
                 self._foxes[-1]._animate = True
                 self._foxes[-1].snap()
              
             elif type(self._drawObj) == Otter and self._drawObj.getPosition()[1] > 0 and self._drawObj.getPosition()[1] < 200:
                 self._otters.append(Otter(self._drawObj.getPosition()))
                 self._money = self._money - 100
                 self._otters[-1]._animate = True
                 self._otters[-1].snap()

             elif type(self._drawObj) == Cat and self._drawObj.getPosition()[1] > 0 and self._drawObj.getPosition()[1] < 200:
                 self._cats.append(Cat(self._drawObj.getPosition()))
                 self._money = self._money - 200
                 self._cats[-1]._animate = True
                 self._cats[-1].snap()

             elif type(self._drawObj) == Panda and self._drawObj.getPosition()[1] > 0 and self._drawObj.getPosition()[1] < 200:
                 self._pandas.append(Panda(self._drawObj.getPosition()))
                 self._money = self._money - 350
                 self._pandas[-1]._animate = True
                 self._pandas[-1].snap()

             elif type(self._drawObj) == Dragon and self._drawObj.getPosition()[1] > 0 and self._drawObj.getPosition()[1] < 200:
                 self._dragons.append(Dragon(self._drawObj.getPosition()))
                 self._money = self._money - 500
                 self._dragons[-1]._animate = True
                 self._dragons[-1].snap()
             
             # make drawObj disappear so only one animal is at that place
             self._drawObj = None

       # when the mouse is moving, the animal will move with the mouse 
       elif event.type == pygame.MOUSEMOTION and self._moving:
             adjustedPos = list([int(x / SCALE) for x in event.pos])
             if type(self._drawObj) == Fox: 
                 self._drawObj.setPosition(Vector2(adjustedPos[0] - 45//2,
                                            adjustedPos[1] - 54//2))
             elif type(self._drawObj) == Otter:
                 self._drawObj.setPosition(Vector2(adjustedPos[0] - 38//2,
                                              adjustedPos[1] - 54//2))
             elif type(self._drawObj) == Cat:
                 self._drawObj.setPosition(Vector2(adjustedPos[0] - 68//2,
                                              adjustedPos[1] - 56//2))
             elif type(self._drawObj) == Panda:
                 self._drawObj.setPosition(Vector2(adjustedPos[0] - 65//2,
                                              adjustedPos[1] - 53//2))
             
             elif type(self._drawObj) == Dragon:
                 self._drawObj.setPosition(Vector2(adjustedPos[0] - 51//2,
                                              adjustedPos[1] - 62//2))
                   
   def update(self, seconds, screenSize):
       
       # update sunflower to get it moving 
       self._sunflower1.update(seconds)
       self._sunflower2.update(seconds)
       self._sunflower3.update(seconds)
       
       self._animalCollection = self._foxes + self._otters + self._cats + self._pandas + self._dragons

       self._animalCount = len(self._foxes)+ len(self._otters) + len(self._cats) + len(self._pandas) + len(self._dragons)
       
       # update animals to make them move and create bullet
       for fightFox in self._foxes:
           fightFox.update(seconds)
           if fightFox._canMakeBullet:
               bulletPosition = fightFox.getPosition()  
               fightFox._canMakeBullet = False
               fightFox._coolDown = 3
               self._foxWeapon.append(FoxWeapon(Vector2(bulletPosition[0] + 17, bulletPosition[1] + 11)))
               self._bulletNoise.playSound("bullet.wav")
     
           for enemy in self._enemyCollection:
               enemy_rect = enemy.getCollisionRect()
               if fightFox.getSCollisionRect().colliderect(enemy_rect):
                   fightFox._life -= enemy._attack/500
                   enemy_rect = (0,0,0,0)
                   if fightFox._life <0:
                       self._foxes.remove(fightFox)
                   break
               
       for otter in self._otters:
           otter.update(seconds)
           if otter._canMakeBullet:
              
               bulletPosition = otter.getPosition() 
               otter._canMakeBullet = False
               otter._coolDown = 4
               self._otterWeapon.append(OtterWeapon(Vector2(bulletPosition[0] + 5,bulletPosition[1] + 14)))
               self._bulletNoise.playSound("otter.wav")
               
           for enemy in self._enemyCollection:
               enemy_rect = enemy.getCollisionRect()
               if otter.getSCollisionRect().colliderect(enemy_rect):
                   otter._life -= enemy._attack/500
                   enemy_rect = (0,0,0,0)
                   if otter._life <0:
                       self._otters.remove(otter)
                   break
               
       for cat in self._cats:
           cat.update(seconds)
           if cat._canMakeBullet:
               bulletPosition = cat.getPosition() 
               cat._canMakeBullet = False
               cat._coolDown = 3
               self._catWeapon.append(CatWeapon(Vector2(bulletPosition[0] + 5, bulletPosition[1] + 24)))
               self._bulletNoise.playSound("catSword.wav")
    
           for enemy in self._enemyCollection:
               enemy_rect = enemy.getCollisionRect()
               if cat.getSCollisionRect().colliderect(enemy_rect):
                   cat._life -= enemy._attack/500
                   enemy_rect = (0,0,0,0)
                   if cat._life <0:
                       self._cats.remove(cat)
                   break
               
       for panda in self._pandas:
           panda.update(seconds)
           if panda._canMakeBullet:
               bulletPosition = panda.getPosition() 
               panda._canMakeBullet = False
               panda._coolDown = 4.5
               self._pandaWeapon.append(PandaWeapon(Vector2(bulletPosition[0] + 8, bulletPosition[1] + 11)))
               self._bulletNoise.playSound("panda.wav") 
               
           for enemy in self._enemyCollection:
               enemy_rect = enemy.getCollisionRect()
               if panda.getSCollisionRect().colliderect(enemy_rect):
                   panda._life -= enemy._attack/500
                   enemy_rect = (0,0,0,0)
                   if panda._life <0:
                       self._pandas.remove(panda)
                   break
          
       for dragon in self._dragons:
           dragon.update(seconds)
           if dragon._canMakeBullet:
               bulletPosition = dragon.getPosition() 
               dragon._canMakeBullet = False
               dragon._coolDown = 4.5
               self._dragonWeapon.append(DragonWeapon(Vector2(bulletPosition[0] - 5, bulletPosition[1] + 16)))
               self._bulletNoise.playSound("fireball.wav")
               
           for enemy in self._enemyCollection:
               enemy_rect = enemy.getCollisionRect()
               if dragon.getSCollisionRect().colliderect(enemy_rect):
                   dragon._life -= enemy._attack/500
                   enemy_rect = (0,0,0,0)
                   
                   if dragon._life <0:
                       self._dragons.remove(dragon)
                   
                   break

       self._allWeapon = self._foxWeapon + self._otterWeapon + self._catWeapon + self._pandaWeapon + self._dragonWeapon
           
       
        
      #check if skull should be removed
       for skull in self._skulls:
           if skull._life <0:
               self._skulls.remove(skull)
        
       
       # update the weapons to make them move and if it collide with animals it will disappear 
       for bullet in self._foxWeapon:
           bullet.update(seconds)
           for enemy in self._enemyCollection:
             enemy_rect = enemy.getCollisionRect()
             if bullet.getCollisionRect().colliderect(enemy_rect) and type(enemy) != Dandelion:
                 self._foxWeapon.remove(bullet)
                 break
       for bullet in self._otterWeapon:
           bullet.update(seconds)
           for enemy in self._enemyCollection:
             enemy_rect = enemy.getCollisionRect()
             if bullet.getCollisionRect().colliderect(enemy_rect) and type(enemy) != Dandelion:
                 self._otterWeapon.remove(bullet)
                 break
       for bullet in self._catWeapon:
           bullet.update(seconds)
           for enemy in self._enemyCollection:
             enemy_rect = enemy.getCollisionRect()
             if bullet.getCollisionRect().colliderect(enemy_rect) and type(enemy) != Dandelion:
                 self._catWeapon.remove(bullet)
                 break
       for bullet in self._pandaWeapon:
           bullet.update(seconds)
           for enemy in self._enemyCollection:
             enemy_rect = enemy.getCollisionRect()
             if bullet.getCollisionRect().colliderect(enemy_rect) and type(enemy) != Dandelion:
                 self._pandaWeapon.remove(bullet)
                 break
       for bullet in self._dragonWeapon:
           bullet.update(seconds, self._dandelions)
           for enemy in self._enemyCollection:
             enemy_rect = enemy.getCollisionRect()
             if bullet.getCollisionRect().colliderect(enemy_rect):
                 self._dragonWeapon.remove(bullet)
                 break
         
         
       self._totalTime += seconds
       
       
       if len(self._cactusAppearTimes) > 0 and self._totalTime> self._cactusAppearTimes[0]:
           cactus_random = random.choice([20, 65, 108, 152, 196])
           self._cactuses.append(Cactus(Vector2(0, cactus_random)))
           self._enemyNumber += 1 
           self._cactusAppearTimes.pop(0)

       if len(self._mushroomAppearTime) > 0 and self._totalTime> self._mushroomAppearTime[0]:
           mushroom_random = random.choice([27, 74, 118, 162, 204])
           self._mushrooms.append(Mushroom(Vector2(0,mushroom_random)))
           self._enemyNumber += 1 
           self._mushroomAppearTime.pop(0)
     
       if len(self._pumpkinAppearTime) > 0 and self._totalTime > self._pumpkinAppearTime[0]:
           pumpkin_random = random.choice([13, 60, 104, 148, 192])
           self._pumpkins.append(Pumpkin(Vector2(0, pumpkin_random)))
           self._enemyNumber += 1 
           self._pumpkinAppearTime.pop(0)
        
       if len(self._flowerAppearTime) > 0 and self._totalTime > self._flowerAppearTime[0]:
           flower_random = random.choice([22, 69, 113, 157, 200])
           self._flowers.append(Flower(Vector2(0, flower_random)))
           self._enemyNumber += 1 
           self._flowerAppearTime.pop(0)
           
       if len(self._dandelionAppearTime) > 0 and self._totalTime > self._dandelionAppearTime[0]:
           dandelion_random = random.randint(60, 170)
           self._dandelions.append(Dandelion(Vector2(0, dandelion_random)))
           self._enemyNumber += 1 
           self._dandelionAppearTime.pop(0)
       
       # update the enemy to make them move
       for cactus in self._cactuses:
             cactus_rect = cactus.getCollisionRect()
             collided = False
             if cactus._lifeValue <=0:
                 self._cactuses.remove(cactus)
                 self._bulletNoise.playSound("enemyDeath.wav")
                 if (self._money + 100) <= 1500:
                     self._money += 100
                 self._enemyCount -= 1
             for animal in self._animalCollection:
                 animal_rect = animal.getSCollisionRect()
                 if cactus_rect.colliderect(animal_rect):
                     collided = True 
                     break
                 
             if collided:
                 cactus.froze()
             else:
                 cactus.recover()   
                 
             cactus.update(seconds)
             
       for dandelion in self._dandelions:
             if dandelion._lifeValue <=0:
                 self._dandelions.remove(dandelion)
                 self._bulletNoise.playSound("enemyDeath.wav")
                 if (self._money + 450) <= 1500:
                     self._money += 450
                 
                 self._enemyCount -= 1 
             
             dandelion.update(seconds, self._dx)
             self._dx += 1 
                 
                     
       for mushroom in self._mushrooms:
             mushroom_rect = mushroom.getCollisionRect()
             collided = False
             if mushroom._lifeValue <=0:
                 self._mushrooms.remove(mushroom)
                 self._bulletNoise.playSound("enemyDeath.wav")
                 if (self._money + 130) <= 1500:
                     self._money += 130
                 
                 self._enemyCount -= 1
             for animal in self._animalCollection:
                 animal_rect = animal.getSCollisionRect()
                 if mushroom_rect.colliderect(animal_rect):
                     collided = True
                     break 
             if collided:
                 mushroom.froze()
             else:
                 mushroom.recover() 
                 
             mushroom.update(seconds)
             
       for pumpkin in self._pumpkins:
             pumpkin_rect = pumpkin.getCollisionRect()
             collided = False
             for animal in self._animalCollection:
                 animal_rect = animal.getSCollisionRect()
                 if pumpkin_rect.colliderect(animal_rect):
                     collided = True
                     break 
             if collided:
                 pumpkin.froze()
             else:
                 pumpkin.recover() 

             pumpkin.update(seconds) 
             
             if pumpkin._state.getState() == "died":
                 self._pumpkins.remove(pumpkin)
                 self._bulletNoise.playSound("enemyDeath.wav")
                 if (self._money + 180) <= 1500:
                     self._money += 180
                 self._enemyCount -= 1

       for flower in self._flowers:
             flower_rect = flower.getCollisionRect()
             collided = False
             for animal in self._animalCollection:
                 animal_rect = animal.getSCollisionRect()
                 if flower_rect.colliderect(animal_rect):
                     collided = True
                     break 
             if collided:
                 flower.froze()
             else:
                 flower.recover() 

             flower.update(seconds) 
             
             if flower._state.getState() == "died":
                 self._flowers.remove(flower)
                 self._bulletNoise.playSound("enemyDeath.wav")
                 if (self._money + 80) <= 1500:
                     self._money += 80 
                 self._enemyCount -= 1
                 
       self._enemyCollection = self._cactuses + self._mushrooms + self._pumpkins + self._flowers + self._dandelions
       
       for enemy in self._enemyCollection:
           if enemy.getCollisionRect().colliderect(self._sunflower1.getCollisionRect()):
               return "dead"
           elif enemy.getCollisionRect().colliderect(self._sunflower2.getCollisionRect()):
               return "dead"
           elif enemy.getCollisionRect().colliderect(self._sunflower3.getCollisionRect()):
               return "dead"
        
       # check if bullet hit any enemy, if does, the enemy's life value will drop accordingly 
       for bullet in self._allWeapon:
         bullet_rect = bullet.getCollisionRect()
         for enemy in self._enemyCollection:
             enemy_rect = enemy.getCollisionRect()
             if bullet_rect.colliderect(enemy_rect):
                if type(enemy) == Dandelion and type(bullet) == DragonWeapon:
                    enemy._lifeValue -= bullet.power
                elif type(enemy) == Dandelion and type(bullet) != DragonWeapon:
                    enemy._lifeValue -= 0
                else: 
                    enemy._lifeValue -= bullet.power
          
       if self._loadFile == "jsonLevel2.txt" and self._enemyCount == 0:
           return "nextLevel"
       elif self._enemyCount == 0 and self._winStar == True:
           return "nextLevel"
           

       self._progress = self._enemyNumber/self._enemyCountB

       
      
      

