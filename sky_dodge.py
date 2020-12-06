import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self, hp):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.hp = hp
        self.score = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            flame.visible = True
        else:
            flame.visible = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Flame(pygame.sprite.Sprite):
    def __init__(self):
        super(Flame, self).__init__()
        self.surf = pygame.image.load("images/flame2.png").convert()
        self.surf.set_colorkey((254, 254, 254), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.visible = False

    def update(self):
        self.rect.x = player.rect.x - 40
        self.rect.y = player.rect.y - 10


class Text(pygame.sprite.Sprite):
    def __init__(self, font, size, text, color, bg):
        super(Text, self).__init__()
        self.font = font
        self.size = size
        self.text = text
        self.color = color
        self.bg = bg
        txt = pygame.font.SysFont(self.font, self.size)
        self.text_r = txt.render(self.text, True, self.color, self.bg)
        self.rect = self.text_r.get_rect()

    def update(self, pos_x, pos_y):
        self.rect.x = player.rect.x + pos_x
        self.rect.y = player.rect.y + pos_y


try:
    f = open("score.txt", "r")
    hi_sc = int(f.read())
    f.close()
except FileNotFoundError:
    hi_sc = 0

pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('haha xd')

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

ADDSCORE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSCORE, 1000)

player = Player(3)
flame = Flame()

hp_txt = Text('arial', 15, f'   HP: {player.hp}   ', 'black', 'white')
hp_txt.update(10, -50)

score_txt = Text('arial', 15, f'   SCORE: {player.score} ({hi_sc})   ', 'black', 'white')
score_txt.update(-15, -30)

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.01)

move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")

move_up_sound.set_volume(0.1)
move_down_sound.set_volume(0.1)
collision_sound.set_volume(0.3)


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # print(f"{event.key}")
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDSCORE:
            player.score += 1
            score_txt = Text('arial', 15, f'   SCORE: {player.score} ({hi_sc})   ', 'black', 'white')
            score_txt.update(-10, -30)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if flame.visible:
        flame.update()
        screen.blit(flame.surf, flame.rect)

    screen.blit(hp_txt.text_r, hp_txt.rect)
    screen.blit(score_txt.text_r, score_txt.rect)

    hp_txt.update(10, -50)
    score_txt.update(-15, -30)

    if pygame.sprite.spritecollideany(player, enemies):
        if player.hp > 1:
            player.hp -= 1
            hp_txt = Text('arial', 15, f'   HP: {player.hp}   ', 'black', 'white')
            hp_txt.update(15, -50)
            player.rect.x = 5
            player.rect.y = 5

        else:
            player.kill()
            hp_txt.kill()
            score_txt.kill()

            move_up_sound.stop()
            move_down_sound.stop()
            pygame.mixer.music.stop()
            pygame.time.delay(50)
            collision_sound.play()
            pygame.time.delay(500)

            if hi_sc < player.score:
                f = open("score.txt", "w")
                f.write(str(player.score))
                f.close()

            running = False

    if pygame.sprite.spritecollideany(player, clouds):
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(200)
        s.fill((255, 255, 255))
        screen.blit(s, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.quit()
