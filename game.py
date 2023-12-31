import pygame
import os
import xlwings as xw
pygame.font.init()
pygame.mixer.init()

wb = xw.Book('scores.xls')
sheet = wb.sheets('scores')

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

BUTTON_BULLETS_RED = pygame.Rect(WIDTH / 2 + 30, 5, 64, 64)
BUTTON_BULLETS_YELLOW = pygame.Rect(WIDTH / 2 - 96, 5, 64, 64)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Shoot.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SCORE_FONT = pygame.font.SysFont('comicsans', 20)

FPS = 60
VEL = 5
BULLETS_VEL = 7
MAX_BULLET_RED = 3
MAX_BULLET_YELLOW = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

BULLET_UPGRADE_BUTTON_IMG = pygame.image.load(os.path.join('Assets', 'bulletUpgrades.png'))

def draw_window(red, yellow, red_bullets, yellow_bullets , red_health, yellow_health, red_score, yellow_score):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    red_score_text = SCORE_FONT.render("Score " + str(red_score), 1, WHITE)
    yellow_score_text = SCORE_FONT.render("Score " + str(yellow_score), 1, WHITE)
    WIN.blit(red_score_text, (WIDTH - red_score_text.get_width()- 10, 60))
    WIN.blit(yellow_score_text, (10, 60))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    WIN.blit(BULLET_UPGRADE_BUTTON_IMG, (WIDTH / 2 + 30, 5))
    WIN.blit(BULLET_UPGRADE_BUTTON_IMG, (WIDTH / 2 - 96, 5))

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_q] and yellow.x - VEL > 0: #LEFT
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGTH
        yellow.x += VEL
    if keys_pressed[pygame.K_z] and yellow.y -VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGTH
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y -VEL > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    bullet_upgrade_red = []
    bullet_upgrade_yellow = []

    red_health = 10
    yellow_health = 10

    red_score = sheet['B1'].value
    yellow_score = sheet['B2'].value
    
    clock = pygame.time.Clock()
    run = True
    hovered_red = False
    hovered_yellow = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sheet['B1'].value = 0
                sheet['B2'].value = 0
                wb.save()
                wb.close()
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                if BUTTON_BULLETS_RED.collidepoint(event.pos):
                    hovered_red = True
                    hovered_yellow = False
                elif BUTTON_BULLETS_YELLOW.collidepoint(event.pos):
                    hovered_yellow = True
                    hovered_red = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if red_score == 5:
                    if hovered_red:
                        print("Geklikt")
                        red_score = sheet['B1'].value - 5
                        bullet_upgrade_red.append()
                        wb.save()
                elif red_score <= 5:
                    if hovered_red:
                        print("Niet genoeg")
                if yellow_score == 5:
                    if hovered_yellow:
                        print("Geklikt")
                        yellow_score = sheet['B2'].value - 5
                        bullet_upgrade_red.append()
                        wb.save()
                elif yellow_score <= 5:
                    if hovered_yellow:
                        print("Niet genoeg")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET_YELLOW + bullet_upgrade_yellow:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                #TODO Zorg ervoor dat je het max aantal bullets kan omhoog doen met de upgrade.
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET_RED + bullet_upgrade_red:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
        
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
            sheet['B2'].value += 1
        if yellow_health <= 0:
            winner_text = "Red Wins!"
            sheet['B1'].value += 1
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)  
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, red_score, yellow_score)
        
    main()

if __name__ == "__main__":
    main()