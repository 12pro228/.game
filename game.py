import pygame
import random
import math
from pathlib import Path
from game_data import get_player_name, record_score, save_player_name

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.key.start_text_input()
pygame.display.set_caption("Pudge breakout")
clock = pygame.time.Clock()
secret_lvl = False
game_over = False
state = "name_entry"
player_name_input = ""
player_name_error = ""
boss = pygame.Rect(310, 90, 180, 170)
boss_hp = 0
boss_max_hp = 50
hook_active = False
hook_returning = False
hook_origin = pygame.Vector2()
hook_position = pygame.Vector2()
hook_target = pygame.Vector2()
hook_cooldown = 180
hook_cooldown_timer = hook_cooldown
hook_damage_applied = False
menu_choice = 0         
menu_font = pygame.font.Font(None, 56)
game_hp = 3
points = 0
player = pygame.Rect(375, 600, 100, 15)
ball = pygame.Rect(419, 580, 15, 15)
ball_trail = []
ball_angle = 0
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
        elif roll < 0.26:
            neon_platforms.append(rect)
        elif roll < 0.36:
            void_platforms.append(rect)
        elif roll < 0.48:
            candy_platforms.append(rect)
        else:
            platforms.append(rect)
    if not secret_platforms and platforms:
        secret_platforms.append(platforms.pop())
    platform_hp[:] = [1] * len(platforms)
    gold_platform_hp[:] = [2] * len(gold_platforms)
    secret_platform_hp[:] = [1] * len(secret_platforms)
    shield_platform_hp[:] = [4] * len(shield_platforms)
    neon_platform_hp[:] = [2] * len(neon_platforms)
    void_platform_hp[:] = [5] * len(void_platforms)
    candy_platform_hp[:] = [1] * len(candy_platforms)

def build_secret_level():
    global boss_hp, hook_active, hook_returning, hook_cooldown_timer
    for lst in (platforms, gold_platforms, secret_platforms, shield_platforms,
                neon_platforms, void_platforms, candy_platforms):
        lst.clear()
    for hp_list in (platform_hp, gold_platform_hp, secret_platform_hp, shield_platform_hp,
                    neon_platform_hp, void_platform_hp, candy_platform_hp):
        hp_list.clear()
    boss_hp = boss_max_hp
    hook_active = False
    hook_returning = False
    hook_cooldown_timer = hook_cooldown

def draw_secret_menu():
    screen.fill((20, 20, 40))
    title = menu_font.render("Secret block defender ", True, (255, 0, 255))
    screen.blit(title, title.get_rect(center=(400, 250)))
    for i, text in enumerate(("Continue level", "Secret level")):
        color = (255, 255, 0) if i == menu_choice else (200, 200, 200)
        label = menu_font.render(text, True, color)
        screen.blit(label, label.get_rect(center=(400, 380 + i * 70)))
    pygame.display.flip()

def load_block(filename):
    image_path = Path(__file__).resolve().parent / filename
    image = pygame.image.load(str(image_path)).convert_alpha()
    return pygame.transform.scale(image, (50, 15))

def load_texture(filename):
    image_path = Path(__file__).resolve().parent / filename
    return pygame.image.load(str(image_path)).convert_alpha()

block_images = {
    "normal": load_block("platform (3).png"),
    "gold": load_block("golden_platform (3).png"),
    "secret": load_block("secret_platform (3).png"),
    "shield": load_block("shield_platform.png"),
    "neon": load_block("neon_platform.png"),
    "void": load_block("void_platform (3).png"),
    "candy": load_block("candy_platform (3).png"),
}
player_image = pygame.transform.scale(load_texture("player.png"), (100, 22))
ball_image = pygame.transform.scale(load_texture("ball (2).png"), (15, 25))
player.size = player_image.get_size()
ball.size = ball_image.get_size()
ball_mask = pygame.mask.Mask(ball.size, fill=True)
heart_path = Path(__file__).resolve().parent / "hp.png"
heart_image = pygame.image.load(str(heart_path)).convert_alpha()
heart_image = pygame.transform.scale(heart_image, (24, 24))
boss_path = Path(__file__).resolve().parent / "big_pudge_x4.png"
boss_image = pygame.image.load(str(boss_path)).convert_alpha()
boss_image = pygame.transform.smoothscale(boss_image, boss.size)
boss_mask = pygame.mask.from_surface(boss_image)
hook_image = pygame.transform.scale(load_texture("hook_x8.png"), (64, 64))
chain_strip = load_texture("chain_strip_x8.png")
chain_frame_width = chain_strip.get_width() // 8
if chain_frame_width * 8 != chain_strip.get_width():
    raise ValueError("chain_strip_x8.png must contain 8 equally sized frames.")
chain_frames = [
    pygame.transform.scale(
        chain_strip.subsurface(
            pygame.Rect(
                index * chain_frame_width,
                0,
                chain_frame_width,
                chain_strip.get_height(),
            )
        ),
        (24, 32),
    )
    for index in range(8)
]
boss_bar_back_image = pygame.transform.scale(load_texture("bar_back.png"), (152, 32))
boss_bar_fill_image = pygame.transform.scale(load_texture("bar_fill.png"), (152, 32))
boss_bar_frame_image = pygame.transform.scale(load_texture("bar_frame.png"), (152, 32))
boss_portrait_normal_image = pygame.transform.scale(
    load_texture("portrait_normal.png"), (40, 40)
)
boss_portrait_hurt_image = pygame.transform.scale(
    load_texture("portrait_hurt.png"), (40, 40)
)
point_path = Path(__file__).resolve().parent / "point.png"
point_image = pygame.image.load(str(point_path)).convert_alpha()
point_image = pygame.transform.scale(point_image, (24, 24))
menu_image_path = Path(__file__).resolve().parent / "menu (1).png"
menu_image = pygame.image.load(str(menu_image_path)).convert_alpha()
menu_image = pygame.transform.scale(menu_image, (448, 704))
menu_rect = menu_image.get_rect(center=(400, 400))
start_button = pygame.Rect(
    menu_rect.x + 32,
    menu_rect.y + 528,
    384,
    176,
)

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
        elif state == "name_entry" and event.type == pygame.TEXTINPUT:
            if len(player_name_input) + len(event.text) <= 16:
                player_name_input += event.text
                player_name_error = ""
        elif state == "name_entry" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                player_name_input = player_name_input[:-1]
                player_name_error = ""
            elif event.key == pygame.K_RETURN:
                player_name = player_name_input.strip()
                if player_name:
                    save_player_name(player_name)
                    pygame.key.stop_text_input()
                    state = "title"
                else:
                    player_name_error = "Please enter a nickname."
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
        elif (
            state == "title"
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and start_button.collidepoint(event.pos)
        ):
            state = "playing"
        elif state == "title" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                state = "playing"

    if not running:
        break

    if state == "name_entry":
        screen.fill((20, 20, 40))
        title = menu_font.render("Create your nickname", True, (255, 220, 80))
        screen.blit(title, title.get_rect(center=(400, 280)))
        hint = hp_font.render("Type 1-16 characters, then press Enter", True, (220, 220, 220))
        screen.blit(hint, hint.get_rect(center=(400, 340)))
        input_box = pygame.Rect(220, 380, 360, 54)
        pygame.draw.rect(screen, (45, 45, 70), input_box, border_radius=8)
        pygame.draw.rect(screen, (255, 220, 80), input_box, width=2, border_radius=8)
        typed_name = menu_font.render(player_name_input or "_", True, (255, 255, 255))
        screen.blit(typed_name, typed_name.get_rect(center=input_box.center))
        if player_name_error:
            error_text = hp_font.render(player_name_error, True, (255, 100, 100))
            screen.blit(error_text, error_text.get_rect(center=(400, 465)))
        pygame.display.flip()
        clock.tick(60)
        continue

    if state == "title":
        screen.fill((0, 0, 0))
        screen.blit(menu_image, menu_rect)
        pygame.display.flip()
        clock.tick(60)
        continue

    if state == "menu":
        draw_secret_menu()
        clock.tick(60)
        continue

    if state == "game_over" or state == "won":
        result = "Boss defeated" if state == "won" else "Game Over"
        record_score(get_player_name(), points, result)
        screen.fill((30, 30, 30))
        result_color = (0, 255, 0) if state == "won" else (255, 0, 0)
        result_text = menu_font.render(result, True, result_color)
        screen.blit(result_text, result_text.get_rect(center=(400, 400)))
        score_text = menu_font.render(
            f"{get_player_name()}: {points}", True, (255, 255, 0)
        )
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
        ball_trail.clear()
        ball_angle = 0
    else: 
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        ball_angle = (ball_angle + 12) % 360
        ball_trail.append(ball.center)
        if len(ball_trail) > 8:
            del ball_trail[0]

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
        ball_trail.clear()
        continue

    if ball.top <= 0:
        ball.top = 0
        ball_speed_y = abs(ball_speed_y)

    if state == "secret" and boss_hp > 0:
        if not hook_active:
            if hook_cooldown_timer > 0:
                hook_cooldown_timer -= 1
            else:
                hook_origin.update(boss.centerx, boss.bottom)
                hook_position.update(hook_origin)
                if ball.centery > hook_origin.y:
                    aim = pygame.Vector2(
                        ball.centerx - hook_origin.x,
                        ball.centery - hook_origin.y,
                    )
                    aim.normalize_ip()
                    distance_to_700 = (700 - hook_origin.y) / aim.y
                    hook_target.update(hook_origin + aim * distance_to_700)
                else:
                    hook_target.update(ball.centerx, 700)
                hook_target.x = max(32, min(768, hook_target.x))
                hook_active = True
                hook_returning = False
                hook_damage_applied = False
        else:
            destination = hook_origin if hook_returning else hook_target
            travel = destination - hook_position
            if travel.length() <= 10:
                hook_position.update(destination)
                if hook_returning:
                    hook_active = False
                    hook_cooldown_timer = hook_cooldown
                else:
                    hook_returning = True
            else:
                hook_position += travel.normalize() * 10

            hook_rect = pygame.Rect(0, 0, 48, 48)
            hook_rect.center = round(hook_position.x), round(hook_position.y)
            if not hook_damage_applied and hook_rect.colliderect(player):
                game_hp -= 1
                hook_damage_applied = True
                hook_returning = True
                if game_hp <= 0:
                    state = "game_over"

    boss_offset = (ball.left - boss.left, ball.top - boss.top)
    boss_hit = boss_mask.overlap(ball_mask, boss_offset) is not None
    if state == "secret" and boss_hp > 0 and not ball_stuck and boss_hit:
        boss_hp -= 1
        if ball_speed_y < 0:
            ball.top = boss.bottom
            ball_speed_y = abs(ball_speed_y)
        else:
            ball.bottom = boss.top
            ball_speed_y = -abs(ball_speed_y)
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

    if boss_hp <= 0 and state == "secret":
        state = "won but is not end"
        

    screen.fill((30, 30, 30))
    for blocks, hp_values, _, image_key in platform_groups:
        image = block_images[image_key]
        for platform, hp in zip(blocks, hp_values):
            if hp > 0:
                screen.blit(image, platform)
    if state == "secret" and boss_hp > 0:
        screen.blit(boss_image, boss)
        boss_bar = pygame.Rect(boss.centerx - 56, boss.top - 38, 152, 32)
        boss_portrait = pygame.Rect(
            boss_bar.left - 40, boss_bar.centery - 20, 40, 40
        )
        boss_label = hp_font.render(
            f"Boss HP: {boss_hp}/{boss_max_hp}", True, (255, 255, 255)
        )
        screen.blit(
            boss_label,
            boss_label.get_rect(midbottom=(boss.centerx, boss_bar.top - 3)),
        )
        health_ratio = max(0, min(1, boss_hp / boss_max_hp))
        health_width = round(boss_bar.width * health_ratio)
        screen.blit(boss_bar_back_image, boss_bar)
        if health_width > 0:
            screen.blit(
                boss_bar_fill_image,
                boss_bar,
                pygame.Rect(0, 0, health_width, boss_bar.height),
            )
        screen.blit(boss_bar_frame_image, boss_bar)
        portrait_image = (
            boss_portrait_normal_image
            if health_ratio >= 0.5
            else boss_portrait_hurt_image
        )
        screen.blit(portrait_image, boss_portrait)
    if hook_active:
        chain_vector = hook_position - hook_origin
        chain_length = chain_vector.length()
        if chain_length:
            chain_angle = math.degrees(
                math.atan2(chain_vector.y, chain_vector.x)
            )
            frame_offset = pygame.time.get_ticks() // 80
            for segment, distance in enumerate(range(12, int(chain_length), 22)):
                chain_image = chain_frames[(frame_offset + segment) % len(chain_frames)]
                rotated_chain = pygame.transform.rotate(
                    chain_image,
                    90 - chain_angle,
                )
                chain_center = hook_origin + chain_vector * (distance / chain_length)
                screen.blit(rotated_chain, rotated_chain.get_rect(center=chain_center))
        hook_vector = hook_target - hook_origin
        if hook_returning:
            hook_vector = -hook_vector
        hook_angle = math.degrees(math.atan2(hook_vector.y, hook_vector.x))
        rotated_hook = pygame.transform.rotate(hook_image, 180 - hook_angle)
        screen.blit(rotated_hook, rotated_hook.get_rect(center=hook_position))
    if not ball_stuck:
        trail_colors = (
            (100, 15, 5),
            (150, 25, 5),
            (190, 40, 5),
            (220, 65, 5),
            (240, 95, 5),
            (255, 125, 10),
            (255, 160, 20),
            (255, 205, 45),
        )
        for index, position in enumerate(ball_trail):
            radius = 2 + index // 3
            pygame.draw.circle(screen, trail_colors[index], position, radius)
    screen.blit(player_image, player)
    rotated_ball = pygame.transform.rotate(
        ball_image, ball_angle if not ball_stuck else 0
    )
    screen.blit(rotated_ball, rotated_ball.get_rect(center=ball.center))
    lives_label = hp_font.render("Lives:", True, (255, 255, 255))
    screen.blit(lives_label, (10, 14))
    for life in range(max(0, game_hp)):
        screen.blit(heart_image, (60 + life * 30, 8))
    screen.blit(point_image, (160, 8))
    score_label = hp_font.render(str(points), True, (255, 255, 255))
    screen.blit(score_label, (190, 14))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()