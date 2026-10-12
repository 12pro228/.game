import math
import pygame

pygame.init()

WIDTH, HEIGHT = 1600, 1440
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

clock = pygame.time.Clock()

# Cube points in 3D space
vertices = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

clicked = False
cube_color = (255, 0, 0)
angle_x = 0.5
angle_y = 0.7


def rotate_point(point, ax, ay):
    x, y, z = point

    # Rotate around X axis
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    # Rotate around Y axis
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    return x, y, z


def project(point):
    x, y, z = point
    depth = 5
    scale = 50
    perspective = scale / (depth + z)
    return (
        WIDTH // 2 + int(x * perspective * 30),
        HEIGHT // 2 + int(y * perspective * 30),
    )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = not clicked
            cube_color = (255, 0, 0) if clicked else (0, 255, 0)

    screen.fill((20, 20, 30))

    angle_x += 0.03
    angle_y += 0.04

    projected = [project(rotate_point(v, angle_x, angle_y)) for v in vertices]

    for a, b in edges:
        pygame.draw.line(screen, cube_color, projected[a], projected[b], 2)

    # Draw a tiny marker so the user sees the click area
    pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), 4)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()