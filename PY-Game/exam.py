import pygame, random, math

# Window, clock, colors, fonts setup
pygame.init()
WIDTH, HEIGHT = 1500, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Relic")
clock = pygame.time.Clock()

BACKGROUND, GRID, WHITE, BLACK = (10,12,25),(25,30,50),(240,245,255),(0,0,0)
CYAN,BLUE,PURPLE,RED = (40,230,255),(70,120,255),(180,70,255),(255,70,90)
ORANGE,GREEN,YELLOW,PINK = (255,150,50),(70,255,150),(255,230,60),(255,80,190)

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 80)


# CLASS 1
class Player:
    # Starting position, stats, and cooldown timers
    def __init__(self):
        self.radius, self.speed = 20, 280
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.color = CYAN
        self.max_health = self.health = 100
        self.shoot_cooldown = self.dash_cooldown = self.dash_timer = self.portal_power = 0
        self.dash_direction = pygame.Vector2(0, 0)
        self.alive = True
        self.ult_charging = False
        self.ult_charge_timer = 0
        self.ult_charge_duration = 0.2
        self.ult_cooldown = 0
        self.ult_max_cooldown = 10.0

    # WASD movement, dash override, cooldown countdowns
    def update(self, dt, keys, speed_mult=1.0):
        if not self.alive: return
        movement = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: movement.y -= 1
        if keys[pygame.K_s]: movement.y += 1
        if keys[pygame.K_a]: movement.x -= 1
        if keys[pygame.K_d]: movement.x += 1
        if movement.length() > 0: movement = movement.normalize()

        if self.dash_timer <= 0:
            self.x += movement.x * self.speed * speed_mult * dt
            self.y += movement.y * self.speed * speed_mult * dt
        else:
            self.x += self.dash_direction.x * 750 * dt
            self.y += self.dash_direction.y * 750 * dt
            self.dash_timer -= dt

        # Clamp position to screen bounds
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        for attr in ('shoot_cooldown','dash_cooldown','portal_power','ult_cooldown'):
            if getattr(self, attr) > 0: setattr(self, attr, getattr(self, attr) - dt)
        if self.ult_charging: self.ult_charge_timer += dt

    # Starts ult charge if off cooldown
    def trigger_ult_charge(self):
        if not self.alive or self.ult_cooldown > 0 or self.ult_charging: return
        self.ult_charging, self.ult_charge_timer = True, 0

    # Fires bullet ring and damages nearby enemies
    def check_and_detonate_ult(self, bullets, enemies):
        if self.ult_charging and self.ult_charge_timer >= self.ult_charge_duration:
            self.ult_charging, self.ult_charge_timer, self.ult_cooldown = False, 0, self.ult_max_cooldown
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                bullets.append(Bullet(self.x, self.y, math.cos(rad), math.sin(rad), powered=True, color=self.color))
            for enemy in enemies:
                if math.dist((self.x, self.y), (enemy.x, enemy.y)) < 250: enemy.health -= 5

    # Fires one bullet toward a target point
    def shoot(self, target_pos):
        if not self.alive or self.shoot_cooldown > 0: return None
        direction = pygame.Vector2(target_pos[0] - self.x, target_pos[1] - self.y)
        if direction.length() > 0:
            direction = direction.normalize()
            self.shoot_cooldown = 0.12 if self.portal_power > 0 else 0.25
            return Bullet(self.x, self.y, direction.x, direction.y, self.portal_power > 0, self.color)
        return None

    # Starts a short burst dash in held direction
    def dash(self, keys):
        if not self.alive or self.dash_cooldown > 0: return
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w]: direction.y -= 1
        if keys[pygame.K_s]: direction.y += 1
        if keys[pygame.K_a]: direction.x -= 1
        if keys[pygame.K_d]: direction.x += 1
        if direction.length() > 0:
            self.dash_direction = direction.normalize()
            self.dash_timer, self.dash_cooldown = 0.18, 1.2

    # Draws player plus ult/portal status rings
    def draw(self, surface):
        if not self.alive: return
        pos = (int(self.x), int(self.y))
        if self.ult_charging:
            ratio = self.ult_charge_timer / self.ult_charge_duration
            r = int(self.radius + ratio * 60)
            pygame.draw.circle(surface, RED, pos, r, 2)
            pygame.draw.circle(surface, ORANGE, pos, int(r*0.7), 1)
        if self.portal_power > 0: pygame.draw.circle(surface, PURPLE, pos, self.radius + 10)
        pygame.draw.circle(surface, self.color, pos, self.radius)
        pygame.draw.circle(surface, WHITE, pos, 7)


# CLASS 2
class Enemy:
    # Spawn position and stats scaled by difficulty
    def __init__(self, difficulty):
        side = random.randint(0, 3)
        self.x, self.y = [(random.randint(0,WIDTH),-30),(WIDTH+30,random.randint(0,HEIGHT)),
                           (random.randint(0,WIDTH),HEIGHT+30),(-30,random.randint(0,HEIGHT))][side]
        self.radius = random.randint(14, 22)
        self.speed = random.randint(80, 125) + difficulty * 5
        self.health = 2 if difficulty <= 12 else 3
        self.damage_cooldown = 0

    # Moves straight toward the player
    def update(self, dt, player, speed_mult=1.0):
        if not player.alive: return
        direction = pygame.Vector2(player.x - self.x, player.y - self.y)
        if direction.length() > 0: direction = direction.normalize()
        self.x += direction.x * self.speed * speed_mult * dt
        self.y += direction.y * self.speed * speed_mult * dt
        if self.damage_cooldown > 0: self.damage_cooldown -= dt

    # Damages player on contact, on cooldown
    def damage_player(self, player):
        if not player.alive: return
        if math.dist((self.x,self.y),(player.x,player.y)) < self.radius + player.radius and self.damage_cooldown <= 0:
            player.health -= 12
            if player.health <= 0: player.health, player.alive = 0, False
            self.damage_cooldown = 0.8

    # Draws a layered circle enemy
    def draw(self, surface):
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, RED, pos, self.radius)
        pygame.draw.circle(surface, ORANGE, pos, self.radius - 6)
        pygame.draw.circle(surface, BLACK, pos, 4)


# CLASS 3
class Bullet:
    # Position, direction, and powered stat block
    def __init__(self, x, y, direction_x, direction_y, powered, color=YELLOW):
        self.x, self.y = x, y
        self.direction_x, self.direction_y = direction_x, direction_y
        self.powered = powered
        self.color = PURPLE if powered and color == YELLOW else color
        self.speed = 750 if powered else 600
        self.damage = 2 if powered else 1
        self.radius = 8 if powered else 6
        self.alive = True

    # Moves forward, dies off-screen
    def update(self, dt):
        self.x += self.direction_x * self.speed * dt
        self.y += self.direction_y * self.speed * dt
        if self.x < -50 or self.x > WIDTH+50 or self.y < -50 or self.y > HEIGHT+50: self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# CLASS 4
class Crystal:
    # Random spawn point and rotation
    def __init__(self):
        self.x, self.y = random.randint(50, WIDTH-50), random.randint(80, HEIGHT-50)
        self.radius = 12
        self.rotation = random.random() * 360

    def update(self, dt): self.rotation += 180 * dt

    # Heals player, adds score on contact
    def collect(self, player, score):
        if not player.alive: return False, score
        if math.dist((self.x,self.y),(player.x,player.y)) < self.radius + player.radius:
            player.health = min(player.max_health, player.health + 8)
            return True, score + 5
        return False, score

    # Draws a rotating diamond shape
    def draw(self, surface):
        points = [(self.x + math.cos(math.radians(a+self.rotation))*self.radius,
                   self.y + math.sin(math.radians(a+self.rotation))*self.radius) for a in range(0,360,90)]
        pygame.draw.polygon(surface, GREEN, points)
        pygame.draw.polygon(surface, WHITE, points, 2)


# CLASS 5
class Portal:
    # Random spawn point and countdown timer
    def __init__(self):
        self.x, self.y = random.randint(100, WIDTH-100), random.randint(120, HEIGHT-100)
        self.radius, self.timer, self.rotation, self.active = 30, 10, 0, True

    def update(self, dt):
        self.timer -= dt
        self.rotation += 180 * dt
        if self.timer <= 0: self.active = False

    # Grants a temporary rapid-fire buff
    def use(self, player):
        if not player.alive: return
        if math.dist((self.x,self.y),(player.x,player.y)) < self.radius + player.radius:
            player.portal_power, self.active = 7, False

    # Draws spinning spokes around a ring
    def draw(self, surface):
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, PURPLE, pos, self.radius, 5)
        pygame.draw.circle(surface, PINK, pos, self.radius - 10, 4)
        for angle in range(0, 360, 60):
            rad = math.radians(angle + self.rotation)
            end = (self.x + math.cos(rad)*self.radius, self.y + math.sin(rad)*self.radius)
            pygame.draw.line(surface, PINK, pos, end, 3)


# ===================== Helper functions =====================
# Draws background and grid overlay
def draw_background():
    screen.fill(BACKGROUND)
    for x in range(0, WIDTH, 50): pygame.draw.line(screen, GRID, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, 50): pygame.draw.line(screen, GRID, (0,y), (WIDTH,y))


AUTO_SHOOT_RANGE = 380

# Finds closest enemy for auto-shoot
def find_nearest_target(p, enemies):
    nearest, nearest_dist = None, AUTO_SHOOT_RANGE
    for e in enemies:
        d = math.dist((p.x,p.y),(e.x,e.y))
        if d < nearest_dist: nearest, nearest_dist = e, d
    return nearest


# Resets all state to a fresh run
def reset_game():
    player = Player()
    return (player, [], [], [Crystal(), Crystal()], None,
            0, 0, 0, 25, 0, False, "")


# ===================== Game initialization =====================
(player, enemies, bullets, crystals, portal,
 enemy_timer, crystal_timer, game_time,
 portal_score, score, game_over, winner_text_str) = reset_game()

running, paused = True, False
auto_shoot = False

# ===================== Main game loop =====================
while running:
    dt = clock.tick(60) / 1000

    # Pause, dash, ult, and restart key handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_over: paused = not paused
            if paused and event.key == pygame.K_q: auto_shoot = not auto_shoot

            if not game_over and not paused:
                if event.key == pygame.K_SPACE: player.dash(pygame.key.get_pressed())
                if event.key == pygame.K_e: player.trigger_ult_charge()

            if event.key == pygame.K_ESCAPE and game_over:
                paused = False
                (player, enemies, bullets, crystals, portal,
                 enemy_timer, crystal_timer, game_time,
                 portal_score, score, game_over, winner_text_str) = reset_game()

    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()

    # Core game logic, skipped while paused/over
    if not game_over and not paused:
        game_time += dt
        speed_mult = min(3.0, 1.0 + game_time * 0.01)

        player.update(dt, keys, speed_mult)
        player.check_and_detonate_ult(bullets, enemies)

        # Manual click-fire, or auto-fire nearest enemy
        if mouse_buttons[0] and player.alive:
            b = player.shoot(mouse_position)
            if b: bullets.append(b)
        elif auto_shoot and player.alive:
            target = find_nearest_target(player, enemies)
            if target is not None:
                b = player.shoot((target.x, target.y))
                if b: bullets.append(b)

        # Timed enemy spawns, ramping up with score
        enemy_timer += dt
        spawn_speed = max(0.35, 1.3 - score * 0.01)
        if enemy_timer >= spawn_speed:
            enemies.append(Enemy(score // 10))
            enemy_timer = 0

        # Timed crystal spawns
        crystal_timer += dt
        if crystal_timer >= 6:
            crystals.append(Crystal())
            crystal_timer = 0

        # Portal spawn once score threshold hit
        if score >= portal_score and portal is None:
            portal = Portal()
            portal_score += 40

        # Move bullets, drop off-screen ones
        for bullet in bullets: bullet.update(dt)
        bullets = [b for b in bullets if b.alive]

        # Move enemies, apply contact damage
        for enemy in enemies:
            enemy.update(dt, player, speed_mult)
            enemy.damage_player(player)

        # Bullet-enemy collisions, award score
        for bullet in bullets:
            for enemy in enemies:
                if math.dist((bullet.x,bullet.y),(enemy.x,enemy.y)) < bullet.radius + enemy.radius:
                    enemy.health -= bullet.damage
                    bullet.alive = False
                    if enemy.health <= 0: score += 2

        enemies = [e for e in enemies if e.health > 0]
        bullets = [b for b in bullets if b.alive]

        # Update and check crystal pickups
        for crystal in crystals: crystal.update(dt)
        remaining_crystals = []
        for crystal in crystals:
            collected, score = crystal.collect(player, score)
            if not collected: remaining_crystals.append(crystal)
        crystals = remaining_crystals

        # Update portal, check use or expiry
        if portal is not None:
            portal.update(dt)
            portal.use(player)
            if not portal.active: portal = None

        # End game on player death
        if not player.alive:
            game_over = True
            winner_text_str = "GAME OVER"

    # Draw background, objects, and player
    draw_background()
    for crystal in crystals: crystal.draw(screen)
    if portal is not None: portal.draw(screen)
    for bullet in bullets: bullet.draw(screen)
    for enemy in enemies: enemy.draw(screen)
    player.draw(screen)

    # HUD: health bar, dash/ult status, score
    pygame.draw.rect(screen, (60,30,40), (25,25,200,20))
    h_w = (player.health / player.max_health) * 200
    pygame.draw.rect(screen, GREEN if player.alive else RED, (25,25,h_w,20))
    screen.blit(small_font.render(f"HP: {int(player.health)}", True, WHITE), (30,48))

    dash_status = "READY" if player.dash_cooldown <= 0 else f"{player.dash_cooldown:.1f}s"
    screen.blit(small_font.render(f"DASH: {dash_status}", True, CYAN if player.dash_cooldown <= 0 else (100,100,120)), (25,70))

    if player.ult_charging:
        ult_status, ult_col = f"CHARGING ({player.ult_charge_duration - player.ult_charge_timer:.1f}s)", ORANGE
    elif player.ult_cooldown <= 0:
        ult_status, ult_col = "READY [E]", RED
    else:
        ult_status, ult_col = f"COOLDOWN ({player.ult_cooldown:.1f}s)", (100,100,120)
    screen.blit(small_font.render(f"WAVE: {ult_status}", True, ult_col), (25,90))

    screen.blit(font.render(f"SCORE: {score}", True, WHITE), (WIDTH-180,25))
    screen.blit(small_font.render(f"ENEMY SPEED x{speed_mult:.2f}", True, ORANGE), (WIDTH-220,85))

    controls_str = "WASD Move | Mouse Shoot | SPACE Dash | E Wave | P Pause | Q (paused) Auto-Shoot"
    controls = small_font.render(controls_str, True, (170,180,210))
    screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT-25))

    # Game over / paused overlay screens
    if game_over:
        overlay = pygame.Surface((WIDTH,HEIGHT)); overlay.set_alpha(190); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        gt = big_font.render(winner_text_str, True, RED)
        screen.blit(gt, (WIDTH//2 - gt.get_width()//2, 200))
        fs = font.render(f"FINAL SCORE: {score}", True, WHITE)
        rt = font.render("PRESS ESC TO RESTART", True, CYAN)
        screen.blit(fs, (WIDTH//2 - fs.get_width()//2, 300))
        screen.blit(rt, (WIDTH//2 - rt.get_width()//2, 370))

    elif paused:
        overlay = pygame.Surface((WIDTH,HEIGHT)); overlay.set_alpha(190); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        pt = big_font.render("PAUSED", True, YELLOW)
        rt = font.render("PRESS P TO RESUME", True, CYAN)
        a1 = font.render(f"AUTO-SHOOT: {'ON' if auto_shoot else 'OFF'} [Q]", True, CYAN if auto_shoot else (150,150,170))
        screen.blit(pt, (WIDTH//2 - pt.get_width()//2, 200))
        screen.blit(rt, (WIDTH//2 - rt.get_width()//2, 300))
        screen.blit(a1, (WIDTH//2 - a1.get_width()//2, 350))

    pygame.display.flip()

pygame.quit()
