import random
import math
import pygame


class Game:
    pygame.mixer.init()

    def __init__(self, id):
        self.playersX = [100, 400]
        self.playersY = [700, 700]
        self.playersXchange = [0, 0]
        self.playersYchange = [0, 0]
        self.playersLives = [4, 4]
        self.ready = False
        self.id = id
        self.stage = {"level": 1,
                      "numOfEnemies": 5,
                      "Xchange": [1, 5],
                      "Ychange": [10, 20]}
        self.bulletImg = [0, 0]
        self.bulletX = [0, 0]
        self.bulletY = [0, 0]
        self.bulletYchange = [4, 4]
        self.bulletState = [0, 0]
        self.score = 0
        self.moneyPlayers = [0, 0]
        self.textX = [100, 450]
        self.textY = [770, 770]
        self.moneyX = []
        self.moneyY = []
        self.moneyYchange = 1
        self.enemyImg = [random.randint(0, 3)
                         for _ in range(self.stage["numOfEnemies"])]
        self.enemyX = [random.randint(20, 516)
                       for _ in range(self.stage["numOfEnemies"])]
        self.enemyY = [random.randint(1, 100)
                       for _ in range(self.stage["numOfEnemies"])]
        self.enemyXchange = [random.randint(self.stage["Xchange"][0], self.stage["Xchange"][1])
                             for _ in range(self.stage["numOfEnemies"])]
        self.enemyYchange = [random.randint(self.stage["Ychange"][0], self.stage["Ychange"][1])
                             for _ in range(self.stage["numOfEnemies"])]
        self.bossX = 268
        self.bossY = 50
        self.bossXchange = 7
        self.bossYchange = 20
        self.bossLives = 8

    def connected(self):
        return self.ready

    def shotPlayer(self, players):
        if self.bulletState[players] == 0:
            laser = pygame.mixer.Sound("sound/laser.wav")
            laser.play()
            self.bulletState[players] = 1
            self.bulletX[players] = self.playersX[players]
            self.bulletY[players] = self.playersY[players]

    def movmentBullet(self, players):
        if self.bulletY[players] <= 0:
            self.bulletY[players] = self.playersY[players]
            self.bulletState[players] = 0
        if self.bulletState[players] == 1:
            self.bulletY[players] -= self.bulletYchange[players]

    def moneyMovment(self):
        for money in range(len(self.moneyX)):
            self.moneyY[money] += self.moneyYchange
            if self.moneyY[money] >= 800:
                self.moneyX.remove(self.moneyX[money])
                self.moneyY.remove(self.moneyY[money])
                break

    def bossMovment(self):
        self.bossX += self.bossXchange
        if self.bossX <= 0:
            self.bossXchange = -self.bossXchange
            self.bossY += self.bossYchange
        elif self.bossX >= 536:
            self.bossXchange = -self.bossXchange
            self.bossY += self.bossYchange
        elif self.bossY >= 700:
            self.stage["level"] = 'LOSE'

    def enemy_Movment(self):
        for enemy in range(self.stage["numOfEnemies"]):
            self.enemyX[enemy] += self.enemyXchange[enemy]
            if self.enemyX[enemy] <= 0:
                self.enemyXchange[enemy] = -self.enemyXchange[enemy]
                self.enemyY[enemy] += self.enemyYchange[enemy]
            elif self.enemyX[enemy] >= 536:
                self.enemyXchange[enemy] = -self.enemyXchange[enemy]
                self.enemyY[enemy] += self.enemyYchange[enemy]

    def upgrade(self, player):
        if self.bulletImg[player] < 3:
            if self.moneyPlayers[player] >= 10:
                self.bulletImg[player] += 1
                self.bulletYchange[player] += 2
                self.moneyPlayers[player] -= 10

    def movmentPlayer(self, players, move):
        self.borderPlayer(players)
        if move == 'L':
            self.playersXchange[players] = -2
            self.playersX[players] += self.playersXchange[players]
        if move == 'R':
            self.playersXchange[players] = 2
            self.playersX[players] += self.playersXchange[players]
        if move == 'U':
            self.playersYchange[players] = -2
            self.playersY[players] += self.playersYchange[players]
        if move == 'D':
            self.playersYchange[players] = 2
            self.playersY[players] += self.playersYchange[players]

    def borderPlayer(self, player):
        if self.playersX[player] <= -20:
            self.playersX[player] = -20
        elif self.playersX[player] >= 556:
            self.playersX[player] = 556
        if self.playersY[player] <= 600:
            self.playersY[player] = 600
        elif self.playersY[player] >= 756:
            self.playersY[player] = 756

    def isCollision(self, enemyX, enemyY, bulletX, bulletY, sizeenemy, sizebullet):
        Rect1 = pygame.Rect(enemyX, enemyY, sizeenemy, sizeenemy)
        Rect2 = pygame.Rect(bulletX, bulletY, sizebullet, sizebullet)

        if Rect1.colliderect(Rect2):
            return True
        else:
            return False

    def checkStage(self):
        levels = self.stage["level"]
        if self.score == 15*levels:
            self.stage["level"] += 1
            self.stage["numOfEnemies"] += 1
            self.stage["Xchange"][1] += 1
            self.stage["Ychange"][0] += 1
            self.stage["Ychange"][1] += 2
            self.enemyX.append(random.randint(20, 516))
            self.enemyY.append(random.randint(1, 100))
            self.enemyXchange.append(random.randint(
                self.stage["Xchange"][0], self.stage["Xchange"][1]))
            self.enemyYchange.append(random.randint(
                self.stage["Ychange"][0], self.stage["Ychange"][1]))
            self.enemyImg.append(random.randint(0, 3))

        if self.stage["level"] == 10:
            self.stage["level"] = "BOSS"
            self.stage["numOfEnemies"] = 0
            self.enemyX = []
            self.enemyY = []
            self.enemyXchange = []
            self.enemyYchange = []
            self.enemyImg = []
        if self.stage["level"] == "BOSS":
            self.bossMovment()
            self.playerHitBoss()
            for i in range(2):
                collision = self.isCollision(
                    self.bossX, self.bossY, self.playersX[i], self.playersY[i], 128, 64)
                if collision:
                    self.stage["level"] = "LOSE"

    def checkCollision(self):
        for i in range(2):
            for j in range(self.stage["numOfEnemies"]):
                collision = self.isCollision(
                    self.enemyX[j], self.enemyY[j], self.bulletX[i], self.bulletY[i], 64, 32)
                if self.bulletState[i] == 1:
                    if collision:
                        explosion = pygame.mixer.Sound("sound/explosion.wav")
                        explosion.play()
                        self.bulletY[i] = self.playersY[i]
                        self.bulletState[i] = 0
                        self.score += 1
                        x = random.random()
                        if x > 0.7:
                            self.moneyX.append(self.enemyX[j]+32)
                            self.moneyY.append(self.enemyY[j]+48)
                        self.enemyX[j] = random.randint(20, 516)
                        self.enemyY[j] = random.randint(1, 100)
                        self.enemyXchange[j] = random.randint(
                            self.stage["Xchange"][0], self.stage["Xchange"][1])
                        self.enemyYchange[j] = random.randint(
                            self.stage["Ychange"][0], self.stage["Ychange"][1])
                        self.enemyImg[j] = random.randint(0, 3)

    def playerCollision(self):
        for i in range(2):
            for j in range(self.stage["numOfEnemies"]):
                collision = self.isCollision(
                    self.enemyX[j], self.enemyY[j], self.playersX[i], self.playersY[i], 64, 64)
                if collision:
                    if self.playersLives[i] == 1:
                        self.stage["level"] = "LOSE"
                    else:
                        explosion = pygame.mixer.Sound("sound/explosion.wav")
                        explosion.play()
                        self.playersLives[i] -= 1
                        self.enemyX[j] = random.randint(20, 516)
                        self.enemyY[j] = random.randint(1, 100)
                        self.enemyXchange[j] = random.randint(
                            self.stage["Xchange"][0], self.stage["Xchange"][1])
                        self.enemyYchange[j] = random.randint(
                            self.stage["Ychange"][0], self.stage["Ychange"][1])
                        self.enemyImg[j] = random.randint(0, 3)

    def playerHitBoss(self):
        for i in range(2):
            collision = self.isCollision(
                self.bossX, self.bossY, self.bulletX[i], self.bulletY[i], 128, 32)
            if collision:
                self.bossLives -= 1
                if self.bossLives == 0:
                    self.stage["level"] = "WIN"
                self.bulletY[i] = self.playersY[i]
                self.bulletState[i] = 0

    def playerTakeMoney(self):
        for i in range(2):
            for money in range(len(self.moneyX)):
                collision = self.isCollision(
                    self.moneyX[money], self.moneyY[money], self.playersX[i], self.playersY[i], 24, 64)
                if collision:
                    moneytake = pygame.mixer.Sound("sound/coincollect.wav")
                    moneytake.play()
                    self.moneyPlayers[i] += 1
                    self.moneyX.remove(self.moneyX[money])
                    self.moneyY.remove(self.moneyY[money])
                    break

    def drawHealthyBarPlayers(self, window):
        for i in range(len(self.playersX)):
            pygame.draw.rect(window, (255, 0, 0),
                             (self.playersX[i], self.playersY[i]+64, 64, 5))
            pygame.draw.rect(window, (0, 255, 0),
                             (self.playersX[i], self.playersY[i]+64, self.playersLives[i]*16, 5))
