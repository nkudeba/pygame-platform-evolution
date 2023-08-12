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
    def __init__(self, x, y, c1ax, c2ax, c3ax, c1ay, c2ay, c3ay, velocity = [0, 0], name = fish_count + 1):  
        fishWidth = 30
        fishHeight = 30
        self.elapsedTime = pygame.time.get_ticks()        
        self.fish_image(fishWidth, fishHeight)        
        self.name = "fish " + str(name)   
        super().__init__(x, y, self.image)
        self.score = 0
        self.c1ax = c1ax
        self.c2ax = c2ax
        self.c3ax = c3ax
        self.c1ay = c1ay
        self.c2ay = c2ay
        self.c3ay = c3ay

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


    def update(self):
        # self.automate_movement()
        c1ax = self.c1ax
        c2ax = self.c2ax
        c3ax = self.c3ax
        c1ay = self.c1ay
        c2ay = self.c2ay
        c3ay = self.c3ay
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

platformNames = [['horiplatforms', [0, HEIGHT - 10, WIDTH, 10]], ['topplatforms',[0, 0, WIDTH, 10]], ['vertplatforms', [-40, 0, 50, HEIGHT]], ['rightplatforms',[WIDTH - 10, 0, 50, HEIGHT]]]
for platform in platformNames:
    globals()[platform[0]] = pygame.sprite.Group()
    globals()[platform[0]].add(Platform( platform[1][0], platform[1][1], platform[1][2], platform[1][3]))

moving_bars = pygame.sprite.Group()
moving_bars.add(MovingBar(100, HEIGHT - 100, 100, 10, 3))
moving_bars.add(MovingBar(150, HEIGHT - 300, 100, 10, 2.5))
stars = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
starlist = [[100, 100], [150, 50], [100, 471], [500, 200], [120, 421]]
for star in starlist:
    stars.add(Star(star[0], star[1], [0, 0]))

players = pygame.sprite.Group()
# players.add(Stickman(100, HEIGHT - 50))
fishes = pygame.sprite.Group()
fishlist = [540, 100, 200, 300]
for fish in fishlist:
    fishes.add(Fish(fish, HEIGHT-50, random.randint (-5, 5) * 0.001, random.randint (-5, 5) * 0.001, random.randint (-5, 5) * 0.001, random.randint (-5, 5) * 0.001, random.randint (-5, 5) * 0.001, random.randint (-5, 5) * 0.001))

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
                bar = bars[0]
                handleBarCollision(object, bar_collision, bar)
                

def handleBarCollision(object, bar_collision, bar):
    if object.on_moving_bar and bar_collision:
        object.rect.x += bar.speed # Move with the bar
        object.velocity[0] += bar.speed
    if object.velocity[1] > 0:  # Landing on the bar
        object.rect.y = bar.rect.y - object.rect.height
        object.velocity[1] = 0
        object.on_moving_bar = True
    elif object.velocity[1] < 0:  # Hitting the bar from below
        object.rect.y = bar.rect.y + bar.rect.height + 5
        object.velocity[1] = 0

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
    platforms = [horiplatforms, topplatforms, vertplatforms, rightplatforms]
    for platform in platforms:
        check_collision(stickman, platform)
        check_collision(fishes, platform)
    

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
    barCollision(fishes, moving_bars) 


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
