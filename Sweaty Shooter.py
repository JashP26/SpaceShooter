#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
#game art by kenney.nl
import pygame
import random
from os import path

WIDTH = 480
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 100, 10)
PURPLE = (102, 0, 102)

game_folder = path.dirname(__file__)
imgs_folder = path.join(game_folder, "img")
snds_folder = path.join(game_folder, "snd")

all_sprites = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
lasers_boss = pygame.sprite.Group()
boss = pygame.sprite.Group()

difficulty = 0
bosses = 0
boss_phase = False
health_height = int(HEIGHT - 30)
pow_height = health_height - 30

def load_img(img):
    return pygame.image.load(path.join(imgs_folder, str(img))).convert()

def load_snd(snd):
    return pygame.mixer.Sound(path.join(snds_folder, (snd)))

def draw_text(surf, text, size, font, color, x, y):
    wanted_font = pygame.font.match_font(str(font))
    font = pygame.font.Font(wanted_font, size)
    text_surface = font.render(text, True, color) #true means that the font is anti-aliased and makes letter look smoother
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def spawn_enemies():
    m = Mob()
    all_sprites.add(m)
    enemies.add(m)

def draw_health(x, y, line):
    if line < 0:
        line = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    FILL = line
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, FILL, BAR_HEIGHT)
    pygame.draw.rect(screen, WHITE, outline_rect, 3)
    pygame.draw.rect(screen, GREEN, fill_rect)

def draw_bar(y, color, length, number, max):
    BAR_LENGTH = number
    BAR_HEIGHT = 10
    outline_rect = pygame.Rect(10, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(10, y, int((length / max) * number), BAR_HEIGHT)
    pygame.draw.rect(screen, WHITE, outline_rect, 3)
    if length > 0:
        pygame.draw.rect(screen, color, fill_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img.set_colorkey(BLACK)
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def start_over():
    all_sprites.empty()
    lasers.empty()
    enemies.empty()
    powerups.empty()
    boss.empty()
    lasers_boss.empty()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        spawn_enemies()
    difficulty = 0
    player.lives = 3
    player.score = 0
    player.shield = 100

def starting_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Sweaty Shooter", 50, 'arial black', ORANGE, int(WIDTH / 2), 50)
    draw_text(screen, "Press the spacebar to start your adventure", 21, 'calibri', YELLOW, int(WIDTH / 2), 150)
    draw_text(screen, "Use the left and right keys to move your ship", 18, "arial", YELLOW, 300, 250)
    draw_text(screen, "Use the spacebar to shoot lasers", 18, "arial", YELLOW, 300, 345)
    draw_text(screen, "Collect powerups to enhance your ship's abilities", 18, "arial", YELLOW, 300, 475)
    draw_text(screen, "Shoot down meteors and the three bosses to win!", 18, "arial", YELLOW, 300, 590)
    player_ship_rect.center = (75, 250)
    screen.blit(player_ship, player_ship_rect)
    laser_rect.center = (75, 350)
    screen.blit(laser, laser_rect)
    powerup_img_shield_rect.center = (50, 450)
    powerup_img_gun_rect.center = (100, 450)
    powerup_img_speed_rect.center = (75, 500)
    screen.blit(powerup_img_shield, powerup_img_shield_rect)
    screen.blit(powerup_img_gun, powerup_img_gun_rect)
    screen.blit(powerup_img_speed, powerup_img_speed_rect)
    meteor_brown_rect.center = (45, 575)
    meteor_grey_rect.center = (105, 575)
    boss_img_icon_rect.center = (75, 650)
    screen.blit(meteor_brown, meteor_brown_rect)
    screen.blit(meteor_grey, meteor_grey_rect)
    screen.blit(boss_img_icon, boss_img_icon_rect)
    pygame.display.flip()
    waiting = True
    sleep = True
    while waiting:
        clock.tick(FPS)
        if sleep:
            pygame.time.wait(1500)
            sleep = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False

def go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GAME OVER", 50, 'arial black', RED, int(WIDTH / 2), 50)
    draw_text(screen, "Player Score:     " + str(player.score), 25, 'arial', YELLOW, int(WIDTH / 2), 500)
    draw_text(screen, "Press the x button to quit", 20, "calibri", YELLOW, int(WIDTH / 2), 600)
    boss_img_icon_rect.center = (int(WIDTH / 2), 350)
    screen.blit(boss_img_icon, boss_img_icon_rect)
    meteor_brown_rect.center = (75, 200)
    meteor_brown2_rect.center = (300, 450)
    meteor_grey_rect.center = (150, 350)
    meteor_grey2_rect.center = (350, 250)
    screen.blit(meteor_brown, meteor_brown_rect)
    screen.blit(meteor_brown2, meteor_brown2_rect)
    screen.blit(meteor_grey, meteor_grey_rect)
    screen.blit(meteor_grey2, meteor_grey2_rect)
    pygame.display.flip()
    waiting = True
    sleep = True
    while waiting:
        clock.tick(FPS)
        if sleep:
            pygame.time.wait(1500)
            sleep = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_x:
                    pygame.quit()

def victory_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "VICTORY", 50, 'arial black', ORANGE, int(WIDTH / 2), 50)
    if player.lives == 1:
        draw_text(screen, "You won with " + str(player.lives) + " life remaining", 25, 'arial', YELLOW, int(WIDTH / 2),
                  575)
    else:
        draw_text(screen, "You won with " + str(player.lives) + " lives remaining", 25, 'arial', YELLOW, int(WIDTH / 2), 575)
        draw_text(screen, "Press the x button to quit", 20, "calibri", YELLOW, int(WIDTH / 2), 650)
    player_ship_rect.center = (int(WIDTH / 2), 300)
    powerup_img_gun_rect.center = (100, 450)
    powerup_img_speed_rect.center = (250, 500)
    powerup_img_shield_rect.center = (350, 400)
    screen.blit(player_ship, player_ship_rect)
    screen.blit(powerup_img_gun, powerup_img_gun_rect)
    screen.blit(powerup_img_speed, powerup_img_speed_rect)
    screen.blit(powerup_img_shield, powerup_img_shield_rect)
    pygame.display.flip()
    waiting = True
    sleep = True
    while waiting:
        clock.tick(FPS)
        if sleep:
            pygame.time.wait(1500)
            sleep = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_x:
                    pygame.quit()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_ship, (66, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.radius = 27
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = int(HEIGHT - 100)
        self.speedx = 0
        self.speed = 0
        self.upgrades = 0
        self.speed_time = -6000
        self.speedpow_time = 0
        self.shoot_time = -4000
        self.shootpow_time = 0
        self.shots = 1
        self.speed_upgrade = False
        self.shoot_upgrade = False
        self.shoot_now = pygame.time.get_ticks()
        self.shoot_delay = 300
        self.shoot_sabotage = False
        self.shoot_sabotagetime = pygame.time.get_ticks()
        self.sabotageradius = self.radius + 10
        self.shield = 100
        self.lives = 3
        self.hide = False
        self.invincibility = False
        self.last_respawn = 0
        self.score = 0
        self.now = pygame.time.get_ticks()

    def update(self):
        self.now = pygame.time.get_ticks()
        self.speedpow_time = self.now - self.speed_time
        self.shootpow_time = self.now - self.shoot_time
        self.speedx = 0
        if self.shoot_sabotage == True and self.now - self.shoot_sabotagetime <= 5000:
            self.shoot_delay = 400
        else:
            self.shoot_delay = 300

        keystate = pygame.key.get_pressed()
        if self.hide == False:
            if keystate[pygame.K_LEFT]:
                self.speedx = -5 - self.speed
            if keystate[pygame.K_RIGHT]:
                self.speedx = 5 + self.speed
            if self.rect.x <= 0:
                self.rect.x = 0
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
            self.rect.centerx += self.speedx
            if keystate[pygame.K_SPACE]:
                self.shoot()
        elif self.now - self.last_respawn >= 1000:
            self.hide = False
            self.shield = 100
            self.rect.bottom = int(HEIGHT - 60)
            self.rect.centerx = int(WIDTH / 2)
        if self.now - self.last_respawn <= 3000:
            self.radius = 37
        else:
            self.radius = 27
            self.invincibility = False
        if self.speed_upgrade == True and self.speedpow_time < 6000:
            self.speed = random.randrange(1, 4)
        elif self.now - self.speedpow_time == 6000:
            self.upgrades -= 1
        else:
            self.speed_upgrade = False
            self.speed = 0
        if self.shoot_upgrade == True and self.shootpow_time >= 4000:
            self.shoot_upgrade = False
            self.shots = 1

    def shoot(self):
        if pygame.time.get_ticks() - self.shoot_now >= self.shoot_delay:
            if self.shots == 1:
                bullet1 = Laser(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                lasers.add(bullet1)
                self.shoot_now = pygame.time.get_ticks()
                shoot_snd.play()
            if self.shots == 2:
                bullet1 = Laser(int(self.rect.centerx - 5), self.rect.top)
                bullet2 = Laser(int(self.rect.centerx + 5), int(self.rect.top + 10))
                all_sprites.add(bullet1, bullet2)
                lasers.add(bullet1, bullet2)
                self.shoot_now = pygame.time.get_ticks()
                shoot_snd.play()
            if self.shots >= 3:
                bullet1 = Laser(int(self.rect.centerx - 35), self.rect.top + 15)
                bullet2 = Laser(int(self.rect.centerx), self.rect.top)
                bullet3 = Laser(int(self.rect.centerx + 35), self.rect.top + 15)
                all_sprites.add(bullet1, bullet2, bullet3)
                lasers.add(bullet1, bullet2, bullet3)
                self.shoot_now = pygame.time.get_ticks()
                shoot_snd.play()

    def respawn(self):
        self.hide = True
        self.invincibility = True
        self.shoot_sabotage = False
        self.rect.centery = HEIGHT + 100
        self.last_respawn = pygame.time.get_ticks()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 8
        self.spawn = pygame.time.get_ticks()

    def update(self):
        if self.rect.bottom <= 0:
            self.kill()
        if player.shoot_sabotage == True and player.now - player.shoot_sabotagetime <= 5000:
            self.speed = 6
        else:
            self.speed = 8
        self.rect.y -= self.speed

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if random.random() > 0.8:
            self.image_og = random.choice(meteors_complex)
            self.multiplier = 2
            self.health = 2
        else:
            self.image_og = random.choice(meteors_basic)
            self.health = 1
            self.multiplier = 1
        self.image_og.set_colorkey(BLACK)
        self.image = self.image_og.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.87 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(-50, 530)
        self.rect.centery = random.randrange(-200, -100)
        self.xspeed = random.randrange(-4 - difficulty, 4 + difficulty)
        self.yspeed = random.randrange(4, 7)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.x >= WIDTH + 75 or self.rect.x <= -75 or self.rect.y >= 610:
            self.kill()
            spawn_enemies()

    def rotate(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.last_update > 50:
            self.last_update = self.now
            self.rot += self.rot_speed % 360
            new_image = pygame.transform.rotate(self.image_og, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
            pygame.sprite.Sprite.__init__(self)
            self.type = random.choice(['shield', 'gun', 'speed'])
            self.image = powerup_img[self.type]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.speedy = 4

    def update(self):
            self.rect.y += self.speedy
            if self.rect.top >= HEIGHT:
                self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if difficulty == 1:
            self.image = boss_img['level1']
            self.color = RED
        elif difficulty == 2:
            self.image = boss_img['level2']
            self.color = GREEN
        else:
            self.image = boss_img['level3']
            self.color = BLUE
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WIDTH / 2)
        self.rect.centery = -1000
        self.speed = 0
        self.shoot_now = pygame.time.get_ticks()
        self.shoot_delay = int(1000 - (difficulty * 75))
        self.now = pygame.time.get_ticks()
        self.health = int(40 + (difficulty * 10))
        self.invincibility = False
        self.spawn_time = pygame.time.get_ticks()
        self.hit_phase = False
        self.hit = pygame.time.get_ticks()
        self.speed_choices = (-8, -7, -6, -5, 5, 6, 7, 8)

    def update(self):
        self.now = pygame.time.get_ticks()
        if self.now - self.hit >= 1000:
            self.hit_phase = False
        if self.now - self.spawn_time <= 3650:
            self.entry()
        else:
            if self.hit_phase == True:
                self.speed = random.choice(self.speed_choices)
            elif self.rect.x <= player.rect.right and self.rect.x >= player.rect.left:
                self.speed = 0
            elif self.rect.x < player.rect.x:
                self.speed = 3
            else:
                self.speed = -3
            if self.now - self.shoot_now >= self.shoot_delay:
                self.shoot()
                self.shoot_now = pygame.time.get_ticks()
        self.rect.centerx += self.speed
        if self.rect.centerx <= 50:
            self.rect.centerx = 50
        elif self.rect.centerx >= int(WIDTH - 50):
            self.rect.centerx = int(WIDTH - 50)

    def shoot(self):
        self.laser = Laser_boss(self.rect.centerx, int(self.rect.centery - 15))
        all_sprites.add(self.laser)
        lasers_boss.add(self.laser)

    def entry(self):
        self.rect.centery += 5
        self.invincibility = True

class Laser_boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if difficulty == 1:
            self.image = boss_laser_img['laser_red']
        elif difficulty == 2:
            self.image = boss_laser_img['laser_green']
        else:
            self.image = boss_laser_img['laser_blue']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.kill()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sweaty Shooter")
clock = pygame.time.Clock()

background = pygame.transform.scale(load_img('blue.png'), (HEIGHT, HEIGHT))
background_rect = background.get_rect()
player_ship = load_img('playerShip1_blue.png')
player_ship.set_colorkey(BLACK)
player_ship_rect = player_ship.get_rect()
player_life = pygame.transform.scale(player_ship, (25, 19))
laser = load_img('laserBlue06.png')
laser.set_colorkey(BLACK)
laser_rect = laser.get_rect()
meteors_basic = (load_img('meteorBrown_big1.png'), load_img('meteorBrown_big3.png'), load_img('meteorBrown_med1.png'), load_img('meteorBrown_med3.png'), load_img('meteorBrown_small1.png'), load_img('meteorBrown_small2.png'))
meteors_complex = (load_img('meteorGrey_big1.png'), load_img('meteorGrey_med1.png'), load_img('meteorGrey_small1.png'))
meteor_brown = load_img('meteorBrown_med1.png')
meteor_brown.set_colorkey(BLACK)
meteor_brown_rect = meteor_brown.get_rect()
meteor_brown2 = meteor_brown.copy()
meteor_brown2_rect = meteor_brown2.get_rect()
meteor_grey = load_img('meteorGrey_med1.png')
meteor_grey.set_colorkey(BLACK)
meteor_grey_rect = meteor_grey.get_rect()
meteor_grey2 = meteor_grey.copy()
meteor_grey2_rect = meteor_grey2.get_rect()
powerup_img = {}
powerup_img['shield'] = load_img('powerupGreen_shield.png')
powerup_img['shield'].set_colorkey(BLACK)
powerup_img_shield = powerup_img['shield']
powerup_img_shield_rect = powerup_img_shield.get_rect()
powerup_img['gun'] = load_img('powerupBlue_bolt.png')
powerup_img['gun'].set_colorkey(BLACK)
powerup_img_gun = powerup_img['gun']
powerup_img_gun_rect = powerup_img_gun.get_rect()
powerup_img['speed'] = load_img('powerupYellow_bolt.png')
powerup_img['speed'].set_colorkey(BLACK)
powerup_img_speed = powerup_img['speed']
powerup_img_speed_rect = powerup_img_speed.get_rect()
boss_img = {}
boss_img['level1'] = load_img('enemyRed5.png')
boss_img_icon = boss_img['level1']
boss_img_icon.set_colorkey(BLACK)
boss_img_icon_rect = boss_img_icon.get_rect()
boss_img['level2'] = load_img('enemyGreen4.png')
boss_img['level3'] = load_img('enemyBlue1.png')
boss_laser_img = {}
boss_laser_img['laser_red'] = load_img('laserRed02.png')
boss_laser_img['laser_green'] = load_img('laserGreen04.png')
boss_laser_img['laser_blue'] = load_img('laserBlue02.png')


shoot_snd = load_snd("Laser_Shoot24.wav")
meteor_snd = load_snd("Explosion_meteor.wav")
meteor_damage_snd = load_snd("Explosion_meteor_damage.wav")
damage_snd = load_snd("Explosion_damage.wav")
explosion_snd = load_snd("Explosion_ship.wav")
powshield_snd = load_snd("Powerup_shield.wav")
powspeed_snd = load_snd("Powerup_speed.wav")
powshoot_snd = load_snd("Powerup_shoot.wav")
laser_klank_snd = load_snd("Laser_klank.wav")

player = Player()
all_sprites.add(player)
for i in range(8):
    spawn_enemies()

running = True
keystate = pygame.key.get_pressed()
starting_screen()

while running:
    clock.tick(FPS)

    #Process
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.score += 20
        if hit.type == 'shield':
            powshield_snd.play()
            player.shield += random.randrange(20, 40)
            if player.shield > 100:
                player.shield = 100
        if hit.type == 'speed':
            powspeed_snd.play()
            player.shoot_sabotage = False
            if player.speed_upgrade == False:
                player.upgrades += 1
            player.speed_upgrade = True
            player.speed_time = pygame.time.get_ticks()
        if hit.type == 'gun':
            powshoot_snd.play()
            player.shoot_upgrade = True
            player.shots += 1
            player.shoot_time = pygame.time.get_ticks()
    hits = pygame.sprite.groupcollide(enemies, lasers, False, True)
    for hit in hits:
        hit.health -= 1
        if hit.health == 1:
            meteor_damage_snd.play()
        if hit.health == 0:
            if random.random() > 0.9 and len(powerups) <= 2:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            meteor_snd.play()
            hit.kill()
            player.score += int((70 - hit.radius) * hit.multiplier)
    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    if player.invincibility == False:
        for hit in hits:
            if hit.multiplier == 2:
                player.speed_upgrade = False
                player.shoot_sabotagetime = pygame.time.get_ticks()
                player.shoot_sabotage = True
            player.shield -= int(hit.radius * 1.8)
            if player.shield < 0:
                player.shield = 0
            if player.shield == 0:
                explosion_snd.play()
                player.lives -= 1
                player.respawn()
                player.shoot_sabotage = False
                player.speed_upgrade = False
                player.shoot_upgrade = False
                if player.lives < 0:
                    running = False
            else:
                damage_snd.play()
    else:
        for hit in hits:
            damage_snd.play()
    if boss_phase == True:
        while len(enemies) < 4 + difficulty:
            spawn_enemies()
    else:
        while len(enemies) < 8 + difficulty:
            spawn_enemies()
    hits = pygame.sprite.groupcollide(boss, lasers, False, True)
    for hit in hits:
        damage_snd.play()
        boss1.hit_phase = True
        boss1.hit = pygame.time.get_ticks()
        boss1.health -= 1
        if boss1.health == 0:
            explosion_snd.play()
            boss1.kill()
            player.score += 1000
            boss_phase = False
            if difficulty == 3:
                victory_screen()
    hits = pygame.sprite.spritecollide(player, lasers_boss, True)
    for hit in hits:
        player.shield -= 25
        damage_snd.play()
        if player.shield <= 0:
            explosion_snd.play()
            player.lives -= 1
            player.respawn()
            player.shoot_sabotage = False
            player.speed_upgrade = False
            player.shoot_upgrade = False
            if player.lives < 0:
                go_screen()
            else:
                damage_snd.play()
    hits = pygame.sprite.groupcollide(lasers, lasers_boss, True, True)
    for hit in hits:
        laser_klank_snd.play()

    if player.score >= 30000:
        difficulty = 3
    elif player.score >= 20000:
        difficulty = 2
    elif player.score >= 10000:
        difficulty = 1
    else:
        difficulty = 0

    if bosses == 0 and player.score >= 10000:
        boss1 = Boss()
        all_sprites.add(boss1)
        boss.add(boss1)
        bosses += 1
        boss_phase = True
    elif bosses == 1 and player.score >= 20000:
        boss1 = Boss()
        all_sprites.add(boss1)
        boss.add(boss1)
        bosses += 1
        boss_phase = True
    elif bosses == 2 and player.score >= 30000:
        boss1 = Boss()
        all_sprites.add(boss1)
        boss.add(boss1)
        bosses += 1
        boss_phase = True

    #Update
    all_sprites.update()

    #Draw/Render
    screen.blit(background, background_rect)
    if player.invincibility == True:
        pygame.draw.circle(screen, WHITE, player.rect.center, player.radius)
    if player.shoot_sabotage == True and player.now - player.shoot_sabotagetime <= 5000:
        pygame.draw.circle(screen, RED, player.rect.center, int(player.sabotageradius - (4 * int((player.now - player.shoot_sabotagetime) / 1000))))
    if player.speed_upgrade == True:
        draw_bar(int(HEIGHT - 60), YELLOW, int((6000 - player.speedpow_time) / 60), 100, 100)
    if player.shoot_upgrade == True:
        draw_bar(int(HEIGHT - 90), BLUE, int((4000 - player.shootpow_time) / 40), 100, 100)
    if boss_phase == True:
        draw_bar(10, boss1.color, boss1.health, int(WIDTH - 20), int(40 + (difficulty * 10)))
    all_sprites.draw(screen)
    lasers.draw(screen)
    enemies.draw(screen)
    powerups.draw(screen)
    lasers_boss.draw(screen)
    boss.draw(screen)
    draw_bar(int(HEIGHT - 30), GREEN, player.shield, 100, 100)
    draw_lives(screen, 450, health_height, player.lives, player_life)
    draw_text(screen, str(player.score), 15, 'arial black', WHITE, int(WIDTH / 2), int(HEIGHT - 30))
    pygame.display.flip()