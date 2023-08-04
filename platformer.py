import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Text_Color = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36) 

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Platform Game")
fish_count = 0

# Stickman class
class Stickman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image.fill([random_red, random_green, random_blue])
        picture = pygame.image.load('player2.png')  # load the star image
        self.image = pygame.transform.scale(picture, (30.2, 55.9))
        self.rect = self.image.get_rect() 
        self.elapsedTime = pygame.time.get_ticks()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0, 0]
        self.on_moving_bar = False
        self.score = 0

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.velocity[1] += 1  # Gravity
        self.elapsedTime = pygame.time.get_ticks()

class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity = [0, 0], name = fish_count + 1):
        super().__init__()        
        random_red    = random.randint( 50, 250 )
        random_green  = random.randint( 50, 250 )
        random_blue   = random.randint( 50, 250 )
        random_colour = ( random_red, random_green, random_blue )
        picture = pygame.image.load('fish_image.png')  # load the fish image
        fishWidth = 30
        fishHeight = 30
        self.elapsedTime = pygame.time.get_ticks()
        self.image = pygame.transform.scale(picture, (fishWidth, fishHeight))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = "fish " + str(name)
        fish_scales= pygame.Surface( ( fishWidth, fishHeight ) )
        fish_scales.fill( random_colour )
        fish_scales.blit( self.image, (0,0) )
        self.image = fish_scales
        self.velocity = [0, 0]
        self.on_moving_bar = False
        self.score = 0
    def automate_movement(self, xvel = random.randint (-1, 1), yvel = random.randint (-1, 1)):
        self.velocity[0] += xvel
        self.velocity[1] += yvel

    c1ax = random.randint (-5, 5) * 0.001
    c2ax = random.randint (-5, 5) * 0.001
    c3ax = random.randint (-5, 5) * 0.001
    c1ay = random.randint (-5, 5) * 0.001
    c2ay = random.randint (-5, 5) * 0.001
    c3ay = random.randint (-5, 5) * 0.001
    print(str(c1ax) + " " + str(c2ax) + " " + str(c3ax) + " " + str(c1ay) + " " + str(c2ay) + " " + str(c3ay))

    def update(self, c1ax = c1ax, c2ax = c2ax, c3ax = c3ax, c1ay = c1ay, c2ay = c2ay, c3ay = c3ay):
        # self.automate_movement()
        t = self.elapsedTime = pygame.time.get_ticks() / 100
        self.velocity[0] = c1ax * t * t + c2ax * t * c3ax
        self.velocity[1] = c1ay * t * t + c2ay * t + c3ay
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # self.velocity[1] += 1  # Gravity

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity = [4, 0]):
        super().__init__()
        self.image = pygame.Surface((10, 2))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.on_moving_bar = False
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Star class
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity = [0, 0]):
        super().__init__()
        picture = pygame.image.load('star.png')  # load the star image
        self.image = pygame.transform.scale(picture, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.on_moving_bar = False
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


# Moving bar class
class MovingBar(Platform):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.width = width

    def update(self):
        self.rect.x += self.speed
        if self.rect.x + self.rect.width > WIDTH -10 or self.rect.x < 10:
            self.speed = -self.speed

# Create game objects
stickman = Stickman(40, HEIGHT-50)
horiplatforms = pygame.sprite.Group()
horiplatforms.add(Platform(0, HEIGHT - 10, WIDTH, 10))
topplatforms = pygame.sprite.Group()
topplatforms.add(Platform(0, 0, WIDTH, 10))
vertplatforms = pygame.sprite.Group()
vertplatforms.add(Platform(-40, 0, 50, HEIGHT))
rightplatforms = pygame.sprite.Group()
rightplatforms.add(Platform(WIDTH - 10, 0, 50, HEIGHT))
moving_bars = pygame.sprite.Group()
moving_bars.add(MovingBar(100, HEIGHT - 100, 100, 10, 3))
moving_bars.add(MovingBar(150, HEIGHT - 300, 100, 10, 2.5))
stars = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
stars.add(Star(100, 100, [0,0]))
stars.add(Star(150, 50, [0,0]))
stars.add(Star(100, 471, [0,0]))
stars.add(Star(500, 200, [0,0]))
stars.add(Star(120, 421, [0, 0]))
players = pygame.sprite.Group()
# players.add(Stickman(100, HEIGHT - 50))
fishes = pygame.sprite.Group()
fishes.add(Fish(540, HEIGHT-50))
fish_count += 1
fishes.add(Fish(100, HEIGHT-50))
fish_count += 1
fishes.add(Fish(200, HEIGHT-50))
fish_count += 1
fishes.add(Fish(300, HEIGHT-50))

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input handling
    keys = pygame.key.get_pressed()

    # Projectile shot when pressing 's'
    if keys[pygame.K_s]:
        projectiles.add(Projectile(stickman.rect.x, stickman.rect.y + 20, [(stickman.velocity[0]+ 0.0001)/abs(stickman.velocity[0] + 0.0001) * 20,0]))


    if stickman.on_moving_bar and bar_collision:
        stickman.velocity[0] += bar.speed
    else:
        if keys[pygame.K_LEFT]:
            stickman.velocity[0] = -5
        elif keys[pygame.K_RIGHT]:
            stickman.velocity[0] = 5
        else:
            stickman.velocity[0] = 0

    if keys[pygame.K_SPACE]:
        stickman.velocity[1] = -15
        stickman.on_moving_bar = False

    # Update game objects
    stickman.update()
    moving_bars.update()
    stars.update()
    projectiles.update()
    fishes.update()

    # Check for collisions with platforms
    horiplatform_collision = pygame.sprite.spritecollide(stickman, horiplatforms, False)
    if horiplatform_collision:
        # print("Hit bottom")
        stickman.rect.y = horiplatform_collision[0].rect.y - stickman.rect.height
        stickman.velocity[1] = 0

    topplatforms_collision = pygame.sprite.spritecollide(stickman, topplatforms, False)
    if topplatforms_collision:
        # print("Hit top")
        stickman.rect.y = 40
        stickman.velocity[1] = 0
    
    vertplatform_collision = pygame.sprite.spritecollide(stickman, vertplatforms, False)
    if vertplatform_collision:
        print("Hit side")
        stickman.rect.x = 10
        stickman.velocity[0] = 0
    # if stickman.rect.x == 0:
    #     stickman.velocity[0] = 0
    #     stickman.rect.x == 1
    rightplatform_collision = pygame.sprite.spritecollide(stickman, rightplatforms, False)
    if rightplatform_collision:
        print("Hit right side")
        stickman.rect.x = WIDTH - 40
        stickman.velocity[0] = 0

    platform_fish_collision = pygame.sprite.groupcollide(fishes, horiplatforms, False, False, pygame.sprite.collide_mask)
    if platform_fish_collision:
        for fish, platform in platform_fish_collision.items():
            fish.velocity[1] = 0
            fish.rect.y = HEIGHT - 40

    vertplatform_fish_collision = pygame.sprite.groupcollide(fishes, vertplatforms, False, False, pygame.sprite.collide_mask)
    if vertplatform_fish_collision:
        for fish, platform in vertplatform_fish_collision.items():
            fish.velocity[0] = 0
            fish.rect.x = 10
    rightplatform_fish_collision = pygame.sprite.groupcollide(fishes, rightplatforms, False, False, pygame.sprite.collide_mask)
    if rightplatform_fish_collision:
        for fish, platform in rightplatform_fish_collision.items():
            fish.velocity[0] = 0
            fish.rect.x = WIDTH - 40

    bars_right_collision = pygame.sprite.groupcollide(moving_bars, rightplatforms, False, False, pygame.sprite.collide_mask)
    if bars_right_collision:
        for bar, platform in bars_right_collision.items():
            bar.rect.x = platform[0].rect.x - bar.width

    topplatform_fish_collision = pygame.sprite.groupcollide(fishes, topplatforms, False, False, pygame.sprite.collide_mask)
    if topplatform_fish_collision:
        for fish, platform in topplatform_fish_collision.items():
            fish.velocity[1] = 0
            fish.rect.y = 30

    # Check for collision with edges
    if stickman.rect.x == 0:
        stickman.velocity[0] = 0
    
    star_collision = pygame.sprite.spritecollide(stickman, stars, True, pygame.sprite.collide_mask)
    if star_collision:
        stickman.rect.y = star_collision[0].rect.y - stickman.rect.height
        stickman.velocity[1] = 0
        print ("star collision")
        stickman.score += 100
    
    star_bar_collision = pygame.sprite.groupcollide(stars, moving_bars, False, False)
    if star_bar_collision:
        # print("star bar collision")
        for star, bar in star_bar_collision.items():
            star.velocity[0] = bar[0].speed
            star.on_moving_bar = True

    star_player_collision = pygame.sprite.groupcollide(players, stars, True, True)
    if star_player_collision:
        print("star player collision")

    # Check for collisions with moving bars
    bar_collision = pygame.sprite.spritecollide(stickman, moving_bars, False)
    if bar_collision:
        bar = bar_collision[0]
        if stickman.velocity[1] > 0:  # Landing on the bar
            stickman.rect.y = bar.rect.y - stickman.rect.height
            stickman.velocity[1] = 0
            stickman.on_moving_bar = True
        elif stickman.velocity[1] < 0:  # Hitting the bar from below
            stickman.rect.y = bar.rect.y + bar.rect.height + 5
            stickman.velocity[1] = 0

    # Move with the moving bar
    if stickman.on_moving_bar and bar_collision:
        stickman.rect.x += stickman.velocity[0] + bar.speed

    # Draw game objects
    screen.fill(WHITE)
    screen.blit(stickman.image, stickman.rect)
    for platform in horiplatforms:
        screen.blit(platform.image, platform.rect)
    for platform in vertplatforms:
        screen.blit(platform.image, platform.rect)
    for platform in rightplatforms:
        screen.blit(platform.image, platform.rect)
    for platform in topplatforms:
        screen.blit(platform.image, platform.rect)
    for moving_bar in moving_bars:
        screen.blit(moving_bar.image, moving_bar.rect)
    for star in stars:
        screen.blit(star.image, star.rect)
    for fish in fishes:
        screen.blit(fish.image, fish.rect)
    for projectile in projectiles:
        screen.blit(projectile.image, projectile.rect)             
    score_text = font.render("Score: " + str(stickman.score), True, Text_Color)
    time_text = font.render("Time: " + str(stickman.elapsedTime), True, Text_Color)
    screen.blit(score_text, (WIDTH - 170, 10))
    screen.blit(time_text, (WIDTH - 170, 40))
    pygame.display.flip()
    clock.tick(FPS)
