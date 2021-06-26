import pygame
from network import Network

from game import Game
pygame.font.init()

width = 600
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
moneyImg = pygame.image.load("img/money.png")
bossImg = pygame.image.load(
    "img/boss.png")
playersImg = [pygame.image.load(
    "img/spaceship0.png"), pygame.image.load("img/spaceship1.png")]
bulletImg = [pygame.image.load(
    "img/bullet.png"), pygame.image.load(
    "img/bullet1.png"), pygame.image.load(
    "img/bullet2.png"), pygame.image.load(
    "img/bullet3.png")]
enemyImg = []
background = pygame.image.load('img/background.png')
loadingscreen = pygame.image.load('img/loading_screen.png')
winScreen = pygame.image.load('img/WIN.png')
gameOverScreen = pygame.image.load('img/GameOver.png')
for x in range(4):
    enemyImg.append(pygame.image.load('img/monster_' + str(x)+'.png'))


def enemydraw(game, win):
    for i in range(game.stage["numOfEnemies"]):
        win.blit(enemyImg[game.enemyImg[i]],
                 (game.enemyX[i], game.enemyY[i]))


def drawMoney(game, win):
    font = pygame.font.SysFont("comicsans", 48)
    text = font.render("Score : "+str(game.score),
                       True, (255, 255, 255))
    win.blit(text, (300-text.get_width()/2, 750))
    for i in range(2):
        if game.bulletImg[i] < 3:
            if game.moneyPlayers[i] < 10:
                font = pygame.font.SysFont("comicsans", 24)
                text = font.render(" X "+str(game.moneyPlayers[i]),
                                   True, (255, 255, 255))
                win.blit(moneyImg, (game.textX[i],
                                    game.textY[i]))
                win.blit(text, (game.textX[i]+24,
                                game.textY[i]+6))
            elif game.moneyPlayers[i] >= 10:
                font = pygame.font.SysFont("comicsans", 27)
                text = font.render("UPGRADE [U] ",
                                   True, (255, 0, 255))
                win.blit(
                    text, (game.textX[i]-20, game.textY[i]))


def moneydraw(game, win):
    for i in range(len(game.moneyX)):
        win.blit(moneyImg,
                 (game.moneyX[i], game.moneyY[i]))


def redrawBOSS(game, window):
    window.blit(bossImg, (game.bossX, game.bossY))
    pygame.draw.rect(window, (255, 0, 0),
                     (game.bossX, game.bossY+128, 128, 8))
    pygame.draw.rect(window, (0, 255, 0),
                     (game.bossX, game.bossY+128, game.bossLives*16, 8))


def draw(game, win):
    win.blit(playersImg[0],
             (game.playersX[0], game.playersY[0]))
    win.blit(playersImg[1],
             (game.playersX[1], game.playersY[1]))


def drawShot(game, win):
    for i in range(2):
        if game.bulletState[i] == 1:
            win.blit(bulletImg[game.bulletImg[i]],
                     (game.bulletX[i]+16, game.bulletY[i]))


def redrawWindow(win, game):
    win.blit(background, (0, 0))
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load('img/project.png')
    pygame.display.set_icon(icon)
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width() /
                 2, height/2 - text.get_height()/2))

    else:
        if game.stage["level"] == "LOSE":
            win.fill((255, 255, 255))
            win.blit(gameOverScreen, (0, 0))
        elif game.stage["level"] == "WIN":
            win.fill((123, 123, 3))
            win.blit(winScreen, (0, 0))
        else:
            font = pygame.font.SysFont("comicsans", 48)
            text = font.render(
                "Poziom : "+str(game.stage["level"]), 1, (0, 255, 0))
            win.blit(text, (width/2 - text.get_width() /
                            2, 10))
            draw(game, win)
            if game.stage["level"] == "BOSS":
                redrawBOSS(game, win)
            drawShot(game, win)
            enemydraw(game, win)
            moneydraw(game, win)
            drawMoney(game, win)
            game.drawHealthyBarPlayers(win)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    while run:
        clock.tick(30)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            n.send('L')
        if keys[pygame.K_RIGHT]:
            n.send('R')
        if keys[pygame.K_UP]:
            n.send('U')
        if keys[pygame.K_DOWN]:
            n.send('D')
        if keys[pygame.K_SPACE]:
            n.send('shot')
        if keys[pygame.K_u]:
            n.send('upgrade')
        redrawWindow(win, game)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        win.fill((128, 128, 128))
        win.blit(loadingscreen, (0, 0))
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load('img/project.png')
        pygame.display.set_icon(icon)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
