import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pudge breakout")
clock = pygame.time.Clock()
game_over = False
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

for x, y in positions:
    rect = pygame.Rect(x, y, 50, 15)
    if random.random() < 0.05:        
        gold_platforms.append(rect)
    elif random.random() < 0.0005:  
        secret_platforms.append(rect)
    elif random.random() < 0.1:  
        shield_platforms.append(rect)
    elif random.random() < 0.3:  
        neon_platforms.append(rect)
    elif random.random() < 0.1:  
        void_platforms.append(rect)
    elif random.random() < 0.02:  
        candy_platforms.append(rect)
    else:
        platforms.append(rect)

platform_hp = [1] * len(platforms)
gold_platform_hp = [2] * len(gold_platforms)
secret_platform_hp = [15] * len(secret_platforms)
shield_platform_hp = [4] * len(shield_platforms)
neon_platform_hp = [2] * len(neon_platforms)
void_platform_hp = [5] * len(void_platforms)
candy_platform_hp = [1] * len(candy_platforms)

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
    pygame.draw.rect(screen, (0, 200, 100), player)
    pygame.draw.rect(screen, (255, 255, 0), ball)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()