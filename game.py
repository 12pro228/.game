import pygame
# Initialize Pygame
pygame.init()
# Set up the display
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pudge breakout")
clock = pygame.time.Clock()
player = pygame.Rect(375, 600, 100, 15)
ball = pygame.Rect(419, 580, 15, 15)
platform = pygame.Rect(100, 50, 50, 15)
platform2 = pygame.Rect(170, 50, 50, 15)
platform3 = pygame.Rect(240, 50, 50, 15)
platform4 = pygame.Rect(310, 50, 50, 15)
platform5 = pygame.Rect(380, 50, 50, 15)
platform6 = pygame.Rect(450, 50, 50, 15)
platform7 = pygame.Rect(520, 50, 50, 15)
platform8 = pygame.Rect(590, 50, 50, 15)

ball_stuck = True          
ball_speed_x = 0
ball_speed_y = 0


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

    if ball.top > 600:
            ball_stuck = True

    if ball_stuck and keys[pygame.K_SPACE]:
        ball_stuck = False
        ball_speed_x = 0
        ball_speed_y = -5

    if ball.top <= 610:
        if ball.colliderect(platform):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform2):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform3):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform4):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform5):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform6):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform7):
            ball_speed_y = -ball_speed_y
        if ball.colliderect(platform8):
            ball_speed_y = -ball_speed_y


    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (255, 0, 0), platform)
    pygame.draw.rect(screen, (0, 200, 100), platform2)
    pygame.draw.rect(screen, (0, 200, 100), platform3)
    pygame.draw.rect(screen, (0, 200, 100), platform4)
    pygame.draw.rect(screen, (0, 200, 100), platform5)
    pygame.draw.rect(screen, (0, 200, 100), platform6)
    pygame.draw.rect(screen, (0, 200, 100), platform7)
    pygame.draw.rect(screen, (0, 200, 100), platform8)
    pygame.draw.rect(screen, (0, 200, 100), player)
    pygame.draw.rect(screen, (255, 255, 0), ball)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()