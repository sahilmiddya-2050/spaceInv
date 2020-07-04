import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("BG.jpg")

# Title And Icon
pygame.display.set_caption("Space War")

# Background Music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# Player Image And Information
playerImg = pygame.image.load('ufo.png')
playerX = 370
playerY = 480
player_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy Image
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
number_of_enemy = 15
for i in range(number_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemy_changeX.append(3)
    enemy_changeY.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet Image
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_changeX = 0
bullet_changeY = 18
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Showing Score
score_value = 0
font = pygame.font.Font('Boochain.ttf', 38)
textX = 10
textY = 10
RED = (255, 0, 0)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, RED)
    screen.blit(score, (x, y))


# GAME OVER
GameOverText = pygame.font.Font('Boochain.ttf', 64)


def game_over_text():
    GameOver = GameOverText.render(" GAME OVER ", 1, RED)
    screen.blit(GameOver, (280, 250))


# HANDLING HIGH SCORE
with open("highscore.txt", "r") as f:
    HighScore = f.read()

# SHOWING HIGH SCORE ON THE SCREEN
highscoretext = pygame.font.Font('Boochain.ttf', 32)


def show_highscore(x, y):
    high_score = highscoretext.render("HIGH SCORE : " + HighScore, True, RED)
    screen.blit(high_score, (x, y))


# UPDATING HIGH SCORE
def update_highscore():
    with open("highscore.txt", "w") as f:
        f.write(HighScore)


# Game Loop
running = True
while running:
    # To Fill The Display With Color With RGB
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_highscore()
            running = False

        # Handling The Keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_change = 4
            if event.key == pygame.K_LEFT:
                player_change = -4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            # bullet_state = "ready"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_change = 0

    playerX += player_change
    # Boundary For Player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(number_of_enemy):
        # Game Over
        if enemyY[i] > 435:
            for j in range(number_of_enemy):
                enemyY[j] = 2000
                update_highscore()
            game_over_text()
            show_highscore(325, 310)
            break
        enemyX[i] += enemy_changeX[i]
        # Boundary For Enemy
        if enemyX[i] <= 0:
            enemy_changeX[i] = 3
            enemyY[i] += enemy_changeY[i]
        elif enemyX[i] >= 736:
            enemy_changeX[i] = -3
            enemyY[i] += enemy_changeY[i]

        # Collision
        collision1 = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision1:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            score_value += 1
            if score_value > int(HighScore):
                HighScore = str(score_value)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_changeY

    player(playerX, playerY)
    show_score(textX, textY)
    show_highscore(620, 10)
    pygame.display.update()
