import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Moves")
clock = pygame.time.Clock()
player = pygame.Rect(375, 500, 50, 50)
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
    if player.right > screen.get_width():
        player.right = screen.get_width()

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 100), player)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()