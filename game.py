import pygame
import random
from pathlib import Path

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
        elif roll < 0.15:
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

def load_block(name):
    image_path = Path(__file__).resolve().parent / f"{name}.png"
    image = pygame.image.load(str(image_path)).convert_alpha()
    return pygame.transform.scale(image, (50, 15))

block_images = {
    "normal": load_block("platform"),
    "gold": load_block("golden_platform"),
    "secret": load_block("secret_platform"),
    "shield": load_block("shield_platform"),
    "neon": load_block("neon_platform"),
    "void": load_block("void_platform"),
    "candy": load_block("candy_platform"),
}

build_normal_level()

ball_stuck = True          
ball_speed_x = 0
ball_speed_y = 0

#MAIN GAME LOOP |(NONONO TOCH)

speed = 5
hp_font = pygame.font.Font(None, 18)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == "menu" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                menu_choice = 1 - menu_choice
            elif event.key == pygame.K_RETURN:
                if menu_choice == 1:
                    build_secret_level()
                    ball_stuck = True
                    ball_speed_x = 0
                    ball_speed_y = 0
                    state = "secret"
                else:
                    build_normal_level()
                    ball_stuck = True
                    state = "playing"

    if not running:
        break

    if state == "menu":
        draw_secret_menu()
        clock.tick(60)
        continue

    if state == "game_over" or state == "won":
        screen.fill((30, 30, 30))
        result = "Boss defeated!" if state == "won" else "Game Over"
        result_color = (0, 255, 0) if state == "won" else (255, 0, 0)
        result_text = menu_font.render(result, True, result_color)
        screen.blit(result_text, result_text.get_rect(center=(400, 400)))
        score_text = menu_font.render(f"Points: {points}", True, (255, 255, 0))
        screen.blit(score_text, score_text.get_rect(center=(400, 480)))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

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

    if not ball_stuck and ball.colliderect(player) and ball_speed_y > 0:
            hit_offset = max(-1, min(1, (ball.centerx - player.centerx) / (player.width / 2)))
            ball_speed_x = round(hit_offset * 7)
            ball_speed_y = -abs(ball_speed_y)

    if ball_stuck and keys[pygame.K_SPACE]:
        ball_stuck = False
        ball_speed_x = 0
        ball_speed_y = -5

    if not ball_stuck and ball.top > screen.get_height():
        game_hp -= 1
        if game_hp <= 0:
            state = "game_over"
        ball_stuck = True
        ball_speed_x = 0
        ball_speed_y = 0
        continue

    if ball.top <= 0:
        ball.top = 0
        ball_speed_y = abs(ball_speed_y)

    if state == "secret" and boss_hp > 0 and ball.colliderect(boss):
        boss_hp -= 1
        ball.top = boss.bottom
        ball_speed_y = abs(ball_speed_y)
        if boss_hp == 0:
            state = "won"

    platform_groups = (
        (platforms, platform_hp, 5, "normal"),
        (gold_platforms, gold_platform_hp, 50, "gold"),
        (secret_platforms, secret_platform_hp, 1000, "secret"),
        (shield_platforms, shield_platform_hp, 5, "shield"),
        (neon_platforms, neon_platform_hp, 70, "neon"),
        (void_platforms, void_platform_hp, 100, "void"),
        (candy_platforms, candy_platform_hp, 30, "candy"),
    )
    if not ball_stuck and ball.top <= 700:
        for blocks, hp_values, point_value, _ in platform_groups:
            hit_index = next(
                (
                    index for index, block in enumerate(blocks)
                    if hp_values[index] > 0 and ball.colliderect(block)
                ),
                None,
            )
            if hit_index is not None:
                hit_platform = blocks[hit_index]
                hp_values[hit_index] -= 1
                if hp_values[hit_index] == 0:
                    points += point_value
                ball_speed_y = -ball_speed_y
                if ball_speed_y > 0:
                    ball.top = hit_platform.bottom
                else:
                    ball.bottom = hit_platform.top
                break

    if state == "playing" and secret_platforms and not any(
        hp > 0 for hp in secret_platform_hp
    ):
        state = "menu"
        draw_secret_menu()
        clock.tick(60)
        continue

    screen.fill((30, 30, 30))
    for blocks, hp_values, _, image_key in platform_groups:
        image = block_images[image_key]
        for platform, hp in zip(blocks, hp_values):
            if hp > 0:
                screen.blit(image, platform)
                hp_label = hp_font.render(str(hp), True, (0, 0, 0))
                screen.blit(hp_label, hp_label.get_rect(center=platform.center))
    if state == "secret" and boss_hp > 0:
        pygame.draw.rect(screen, (255, 0, 0), boss)
        boss_label = menu_font.render(f"Boss HP: {boss_hp}", True, (255, 255, 255))
        screen.blit(boss_label, boss_label.get_rect(center=boss.center))
    pygame.draw.rect(screen, (0, 200, 100), player)
    pygame.draw.rect(screen, (255, 255, 0), ball)
    hud = hp_font.render(f"Lives: {game_hp}   Points: {points}", True, (255, 255, 255))
    screen.blit(hud, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()