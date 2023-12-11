import pygame
import random

pygame.init()
win = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("First Game")
bg = pygame.image.load('assets/platform 9.jpeg')
background_image = pygame.transform.scale(bg, win.get_size())
char = pygame.image.load('assets/no_anim_0.png')
clock = pygame.time.Clock()

walkRight = [pygame.image.load('assets/run.right1.png'), pygame.image.load('assets/run.right2.png'),
             pygame.image.load('assets/run.right3.png'), pygame.image.load('assets/run.right4.png')]
walkLeft = [pygame.image.load('assets/run.left1.png'), pygame.image.load('assets/run.left2.png'),
            pygame.image.load('assets/run.left3.png'), pygame.image.load('assets/run.left4.png')]

shock = pygame.image.load('assets/1_0.png')
sprite_sheet = pygame.image.load('assets/sprite.png')
score = 0
MagS = pygame.mixer.Sound('assets/magic sound.wav')
SnH = pygame.mixer.Sound('assets/snake.hit.wav')
SnD = pygame.mixer.Sound('assets/snake.death.wav')
MkH = pygame.mixer.Sound('assets/mask.hit.wav')
MkD = pygame.mixer.Sound('assets/mask.death.wav')
# McH =
music = pygame.mixer.music.load('assets/game sound.mp3')
pygame.mixer.music.play(-1)


def get_image(sheet, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (0, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image


frame_0 = get_image(sprite_sheet, 64, 96, 3)


class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 8
        self.standing = True
        self.hitbox = (self.x, self.y, 64, 96)
        self.health = 10
        self.visible = True

    def hit(self):
        self.isJump = False
        self.jumpCount = 8
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

        if self.walkCount + 1 >= 16:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x, self.y, 64, 96)


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(pygame.sprite.Sprite):
    walkRight = [pygame.image.load('assets/er1.png'), pygame.image.load('assets/er2.png'),
                 pygame.image.load('assets/er3.png'), pygame.image.load('assets/er4.png')]
    walkLeft = [pygame.image.load('assets/el1.png'), pygame.image.load('assets/el2.png'),
                pygame.image.load('assets/el3.png'), pygame.image.load('assets/el4.png')]

    def __init__(self, x, y, width, height, end):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x, self.y, 64, 96)
        self.health = 10
        self.visible = True

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 16:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x, self.y, 64, 96)
        else:
            self.remove()
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


class Snake(pygame.sprite.Sprite):
    walkRight = [pygame.image.load('assets/sr1.png'), pygame.image.load('assets/sr2.png'),
                 pygame.image.load('assets/sr3.png'), pygame.image.load('assets/sr4.png')]
    walkLeft = [pygame.image.load('assets/sl1.png'), pygame.image.load('assets/sl2.png'),
                pygame.image.load('assets/sl3.png'), pygame.image.load('assets/sl4.png')]

    def __init__(self, x, y, width, height, end):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = -3
        self.hitbox = (self.x, self.y, 64, 96)
        self.health = 10
        self.visible = True

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 16:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x, self.y, 64, 96)
        else:
            self.remove()

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


def redrawGameWindow():
    win.blit(background_image, (0, 0))
    mc.draw(win)
    mask.draw(win)
    snake.draw(win)
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (1435, 10))
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

# mainloop
font = pygame.font.SysFont('comicsans', 30, True, False)
winnerfont = pygame.font.SysFont('comicsans', 100, True, False)
winner = winnerfont.render('YOU WIN', 1, (0, 0, 0))
mc = player(50, 720, 64, 96)
shootLoop = 0
bullets = []
mask = enemy(250, 720, 64, 96, 1000)
snake = Snake(500, 720, 64, 96, 1000)
run = True

while run:

    clock.tick(60)
    win.blit(frame_0, (0, 0))

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 4:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if mask.visible:
            if bullet.y - bullet.radius < mask.hitbox[1] + mask.hitbox[3] and bullet.y + bullet.radius > mask.hitbox[1]:
                if bullet.x + bullet.radius > mask.hitbox[0] and bullet.x - bullet.radius < mask.hitbox[0] + \
                        mask.hitbox[2]:
                    MkH.play()
                    mask.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if snake.visible:
            if bullet.y - bullet.radius < snake.hitbox[1] + snake.hitbox[3] and bullet.y + bullet.radius > snake.hitbox[1]:
                if bullet.x + bullet.radius > snake.hitbox[0] and bullet.x - bullet.radius < snake.hitbox[0] + \
                        snake.hitbox[2]:
                    SnH.play()
                    snake.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 1600 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        MagS.play()
        if mc.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(
                projectile(round(mc.x + mc.width // 2), round(mc.y + mc.height // 2), 6, (244, 61, 182), facing))
        shootLoop = 1
    if keys[pygame.K_LEFT] and mc.x > mc.vel:
        mc.x -= mc.vel
        mc.left = True
        mc.right = False
        mc.standing = False
    elif keys[pygame.K_RIGHT] and mc.x < 1600 - mc.width - mc.vel:
        mc.x += mc.vel
        mc.right = True
        mc.left = False
        mc.standing = False
    else:
        mc.standing = True
        mc.walkCount = 0

    if not (mc.isJump):
        if keys[pygame.K_UP]:
            mc.isJump = True
            mc.right = False
            mc.left = False
            mc.walkCount = 0
    else:
        if mc.jumpCount >= -8:
            neg = 1
            if mc.jumpCount < 0:
                neg = -1
            mc.y -= (mc.jumpCount ** 2) * 0.5 * neg
            mc.jumpCount -= 1
        else:
            mc.isJump = False
            mc.jumpCount = 8
    redrawGameWindow()
    if score == 22:
        win.blit(winner,((550),(400)))
        pygame.display.update()
pygame.quit()
