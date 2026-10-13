import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pudge breakout")
clock = pygame.time.Clock()
secret_lvl = False
game_over = False
state = "playing"       
boss = pygame.Rect(300, 100, 200, 70)   
boss_hp = 0
menu_choice = 0         
menu_font = pygame.font.Font(None, 56)
game_hp = 3
points = 0
player = pygame.Rect(375, 600, 100, 15)
ball = pygame.Rect(419, 580, 15, 15)
positions = [
    (x, y)
    for x in (0, 100, 170, 240, 310, 380, 450, 520, 590, 660, 730)
    for y in (100, 130, 160, 190)
]

platforms = []
gold_platforms = []
secret_platforms = []
shield_platforms = []
neon_platforms = []
void_platforms = []
candy_platforms = []
platform_hp = []
gold_platform_hp = []
secret_platform_hp = []
shield_platform_hp = []
neon_platform_hp = []
void_platform_hp = []
candy_platform_hp = []

def build_normal_level():
    for lst in (platforms, gold_platforms, secret_platforms, shield_platforms,
                neon_platforms, void_platforms, candy_platforms):
        lst.clear()
    for x, y in positions:
        rect = pygame.Rect(x, y, 50, 15)
        roll = random.random()
        if roll < 0.05:
            gold_platforms.append(rect)
        elif roll < 0.06:
            secret_platforms.append(rect)
        elif roll < 0.065:
            shield_platforms.append(rect)
        elif roll < 0.36:
            neon_platforms.append(rect)
        elif roll < 0.46:
            void_platforms.append(rect)
        elif roll < 0.48:
            candy_platforms.append(rect)
        else:
            platforms.append(rect)
    if not secret_platforms and platforms:
        secret_platforms.append(platforms.pop())
    platform_hp[:] = [1] * len(platforms)
    gold_platform_hp[:] = [2] * len(gold_platforms)
    secret_platform_hp[:] = [15] * len(secret_platforms)
    shield_platform_hp[:] = [4] * len(shield_platforms)
    neon_platform_hp[:] = [2] * len(neon_platforms)
    void_platform_hp[:] = [5] * len(void_platforms)
    candy_platform_hp[:] = [1] * len(candy_platforms)

def build_secret_level():
    global boss_hp
    for lst in (platforms, gold_platforms, secret_platforms, shield_platforms,
                neon_platforms, void_platforms, candy_platforms):
        lst.clear()
    for hp_list in (platform_hp, gold_platform_hp, secret_platform_hp, shield_platform_hp,
                    neon_platform_hp, void_platform_hp, candy_platform_hp):
        hp_list.clear()
    boss_hp = 50

def draw_secret_menu():
    screen.fill((20, 20, 40))
    title = menu_font.render("Secret block defender ", True, (255, 0, 255))
    screen.blit(title, title.get_rect(center=(400, 250)))
    for i, text in enumerate(("Continue level", "Secret level")):
        color = (255, 255, 0) if i == menu_choice else (200, 200, 200)
        label = menu_font.render(text, True, color)
        screen.blit(label, label.get_rect(center=(400, 380 + i * 70)))
    pygame.display.flip()

build_normal_level()

ball_stuck = True          
ball_speed_x = 0
ball_speed_y = 0

#MAIN GAME LOOP |(NONONO TOCH)

speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state == "menu" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                menu_choice = 1 - menu_choice
            if event.key == pygame.K_RETURN:
                if menu_choice == 1:
                    build_secret_level()
                    ball_stuck = True
                    state = "secret"
                else:
                    build_normal_level()
                    state = "playing"

    if state == "menu":
        draw_secret_menu()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += speed

    if player.left < 0:
        player.left = 0
    if player.right > 800:
        player.right = 800

    if ball_stuck:
        ball.centerx = player.centerx
        ball.bottom = player.top
    else: 
        ball.x += ball_speed_x
        ball.y += ball_speed_y

    if ball.left <= 0:
     ball.left = 0
     ball_speed_x = abs(ball_speed_x)
    if ball.right >= 800:
     ball.right = 800
     ball_speed_x = -abs(ball_speed_x)

    if ball.colliderect(player) and ball_speed_y > 0:
            hit_offset = max(-1, min(1, (ball.centerx - player.centerx) / (player.width / 2)))
            ball_speed_x = round(hit_offset * 7)
            ball_speed_y = -abs(ball_speed_y)

    if ball_stuck and keys[pygame.K_SPACE]:
        ball_stuck = False
        ball_speed_x = 0
        ball_speed_y = -5

    #game hp
    if ball.top > 800:
            game_hp -= 1
            if game_hp <= 0:
                game_over = True
            ball_stuck = True

    if game_over:
        screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(400, 400))
        screen.blit(text, text_rect)
        stats_font = pygame.font.Font(None, 48)
        points_text = stats_font.render(f"Points: {points}", True, (255, 255, 0))
        points_rect = points_text.get_rect(center=(400, 500))
        screen.blit(points_text, points_rect)
        pygame.display.flip()
        pygame.time.wait(3000) #clouse time 
        running = False
        continue

    if ball.top <= 0:
        ball.top = 0
        ball_speed_y = abs(ball_speed_y)

    if ball.top <= 700:
        for index, platform in enumerate(platforms):
            if platform_hp[index] > 0 and ball.colliderect(platform):
                platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 5
                break

        for index, platform in enumerate(gold_platforms):
            if gold_platform_hp[index] > 0 and ball.colliderect(platform):
                gold_platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 50
                break
        for index, platform in enumerate(secret_platforms):
            if secret_platform_hp[index] > 0 and ball.colliderect(platform):
                secret_platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 1000
                break
        for index, platform in enumerate(shield_platforms):
            if shield_platform_hp[index] > 0 and ball.colliderect(platform):
                shield_platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 5
                break
        for index, platform in enumerate(neon_platforms):
            if neon_platform_hp[index] > 0 and ball.colliderect(platform):
                neon_platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 70
                break
        for index, platform in enumerate(void_platforms):
            if void_platform_hp[index] > 0 and ball.colliderect(platform):
                void_platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 100
                break
        for index, platform in enumerate(candy_platforms):
            if candy_platform_hp[index] > 0 and ball.colliderect(platform):
                candy_platform_hp[index] -= 1
                ball_speed_y = -ball_speed_y
                points += 30
                break

    if state == "playing" and secret_platforms and not any(
        hp > 0 for hp in secret_platform_hp
    ):
        state = "menu"
        draw_secret_menu()
        clock.tick(60)
        continue

    if state == "secret" and boss_hp > 0 and ball.colliderect(boss):
        boss_hp -= 1
        ball.top = boss.bottom
        ball_speed_y = abs(ball_speed_y)

    screen.fill((30, 30, 30))
    for index, platform in enumerate(platforms):
        if platform_hp[index] > 0:
            color = (255, 0, 0) if index == 0 else (0, 200, 100)
            pygame.draw.rect(screen, color, platform)
    for index, platform in enumerate(gold_platforms):
        if gold_platform_hp[index] > 0:
            pygame.draw.rect(screen, (255, 255, 0), platform)
    for index, platform in enumerate(secret_platforms):
        if secret_platform_hp[index] > 0:
            pygame.draw.rect(screen, (255, 0, 255), platform)        
            half = pygame.Rect(platform.x + platform.width // 2, platform.y,
                               platform.width // 2, platform.height)
            pygame.draw.rect(screen, (0, 255, 255), half)
    for index, platform in enumerate(shield_platforms):
        if shield_platform_hp[index] > 0:
            pygame.draw.rect(screen, (0, 255, 255), platform)
    for index, platform in enumerate(neon_platforms):
        if neon_platform_hp[index] > 0:
            pygame.draw.rect(screen, (255, 255, 255), platform)
    for index, platform in enumerate(void_platforms):
        if void_platform_hp[index] > 0:
            pygame.draw.rect(screen, (0, 0, 0), platform)
    for index, platform in enumerate(candy_platforms):
        if candy_platform_hp[index] > 0:
            pygame.draw.rect(screen, (255, 182, 193), platform)
    if state == "secret" and boss_hp > 0:
        pygame.draw.rect(screen, (255, 0, 0), boss)
        boss_label = menu_font.render(f"Boss HP: {boss_hp}", True, (255, 255, 255))
        screen.blit(boss_label, boss_label.get_rect(center=boss.center))
    pygame.draw.rect(screen, (0, 200, 100), player)
    pygame.draw.rect(screen, (255, 255, 0), ball)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()