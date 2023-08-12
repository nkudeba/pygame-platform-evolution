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


# Function to load and scale image
def load_and_scale_image(image_path, width, height):
    picture = pygame.image.load(image_path)
    return pygame.transform.scale(picture, (width, height))


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.elapsedTime = pygame.time.get_ticks()
        self.rect.x = x
        self.rect.y = y
        self.velocity = [0, 0]
        self.on_moving_bar = False
        self.score = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.basicUpdate()

    def basicUpdate(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

# Stickman class
class Stickman(Character):
    def __init__(self, x, y):
        image = load_and_scale_image('player2.png', 30, 55) 
        super().__init__(x, y, image)
    def update(self):
        self.basicUpdate()        
        self.velocity[1] += 1  # Gravity
        self.elapsedTime = pygame.time.get_ticks()


class Fish(Character):
    def __init__(self, x, y, velocity = [0, 0], name = fish_count + 1):  
        fishWidth = 30
        fishHeight = 30
        self.elapsedTime = pygame.time.get_ticks()        
        self.fish_image(fishWidth, fishHeight)        
        self.name = "fish " + str(name)   
        super().__init__(x, y, self.image)
        self.score = 0

    def fish_image(self, fishWidth, fishHeight):
        random_red    = random.randint( 50, 250 )
        random_green  = random.randint( 50, 250 )
        random_blue   = random.randint( 50, 250 )
        random_colour = ( random_red, random_green, random_blue )
        self.image = load_and_scale_image('fish_image.png', fishWidth, fishHeight)
        self.rect = self.image.get_rect()
        fish_scales= pygame.Surface( ( fishWidth, fishHeight ) )
        fish_scales.fill( random_colour )
        fish_scales.blit( self.image, (0,0) )
        self.image = fish_scales
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
        self.basicUpdate()
        # self.velocity[1] += 1  # Gravity

class Projectile(Character):
    def __init__(self, x, y, velocity = [4, 0]):
        self.image = pygame.Surface((10, 2))
        self.image.fill(BLACK)
        super().__init__(x, y, self.image)
        self.velocity = velocity
        self.on_moving_bar = False


# Platform class
class Platform(Character):
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        super().__init__(x, y, self.image)

# Star class
class Star(Character):
    def __init__(self, x, y, velocity = [0, 0]):
        self.image = load_and_scale_image('star.png', 30, 30)
        super().__init__(x, y, self.image)
        self.velocity = velocity

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
              

def check_collision(object, platform):
    if isinstance(object, Stickman):
        collision = pygame.sprite.spritecollide(object, platform, False)
    else:
        collision = pygame.sprite.groupcollide(object, platform, False, False, pygame.sprite.collide_mask)
    if collision:
        if isinstance(object, Stickman):
            platform_collisions(object, platform)
        else:
            for object, myplatform in collision.items():
                platform_collisions(object, platform)

def platform_collisions(object, platform):
    if platform is horiplatforms:                
        object.velocity[1] = 0
        object.rect.y = HEIGHT - object.height - 10
    elif platform is topplatforms:
        object.velocity[1] = 0
        object.rect.y = 10
    elif platform is vertplatforms:
        object.velocity[0] = 0
        object.rect.x = 10
    elif platform is rightplatforms:
        object.velocity[0] = 0
        object.rect.x = WIDTH - object.width - 10


def barCollision(object, moving_bars):
    if isinstance(object,Stickman):
        bar_collision = pygame.sprite.spritecollide(object, moving_bars, False)
    else:
        bar_collision = pygame.sprite.groupcollide(object, moving_bars, False, False, pygame.sprite.collide_mask)
    if bar_collision:
        if isinstance(object, Stickman):
            bar = bar_collision[0]
            handleBarCollision(object, bar_collision, bar)
        else:
            for object, bars in bar_collision.items():
                print('fish bar collide')
                bar = bars[0]
                handleBarCollision(object, bar_collision, bar)
                

def handleBarCollision(object, bar_collision, bar):
    if object.on_moving_bar and bar_collision:
        object.rect.x += bar.speed # Move with the bar
        object.velocity[0] += bar.speed
        print('moving on bar')
    if object.velocity[1] > 0:  # Landing on the bar
        object.rect.y = bar.rect.y - object.rect.height
        object.velocity[1] = 0
        object.on_moving_bar = True
        print('landed on bar')
    elif object.velocity[1] < 0:  # Hitting the bar from below
        object.rect.y = bar.rect.y + bar.rect.height + 5
        object.velocity[1] = 0
        print('hit bar from below')

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

    if keys[pygame.K_LEFT]:
        stickman.velocity[0] = -5
    elif keys[pygame.K_RIGHT]:
        stickman.velocity[0] = 5
    else:
        stickman.velocity[0] = 0

    if keys[pygame.K_SPACE]:
        stickman.velocity[1] = -15
        stickman.on_moving_bar = False


    # Check for collisions with platforms
    check_collision(stickman, horiplatforms)
    check_collision(stickman, topplatforms)
    check_collision(stickman, vertplatforms)
    check_collision(stickman, rightplatforms)
    check_collision(fishes, horiplatforms)
    check_collision(fishes, vertplatforms)
    check_collision(fishes, rightplatforms)
    check_collision(fishes, topplatforms)
    

    bars_right_collision = pygame.sprite.groupcollide(moving_bars, rightplatforms, False, False, pygame.sprite.collide_mask)
    if bars_right_collision:
        for bar, platform in bars_right_collision.items():
            bar.rect.x = platform[0].rect.x - bar.width
    
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
    barCollision(stickman, moving_bars)
    barCollision(fishes, moving_bars) # Need to make this work - Group object has no attribute 'rect'


    # Draw game objects
    screen.fill(WHITE)
    screen.blit(stickman.image, stickman.rect)
    tobuild = [horiplatforms, vertplatforms, rightplatforms, topplatforms, moving_bars, stars, fishes, projectiles]
    for group in tobuild:
        for object in group:
            screen.blit(object.image, object.rect)           
    score_text = font.render("Score: " + str(stickman.score), True, Text_Color)
    time_text = font.render("Time: " + str(stickman.elapsedTime), True, Text_Color)
    screen.blit(score_text, (WIDTH - 170, 10))
    screen.blit(time_text, (WIDTH - 170, 40))
    pygame.display.flip()
    clock.tick(FPS)

    # Update game objects
    toupdate = [stickman, moving_bars, stars, projectiles, fishes]
    for object in toupdate:
        object.update()
