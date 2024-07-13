import pygame, sys
from pygame.locals import *
import random

pacman_image = pygame.image.load("Pacman.png")
background_image = pygame.image.load("Background.jpg")
background_height = background_image.get_height()
background_width = background_image.get_width()

# Screen size constants
WIDTH = 735
HEIGHT = 386

# Initialize
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Game')
orange_image = pygame.image.load("Orange.png")
pink_image = pygame.image.load("Pink.png")
blue_image = pygame.image.load("Blue.png")
red_image = pygame.image.load("Red.png")


class Enemy:
    # load enemies
    def __init__(self, color, x, y, active, starting_direction, speed):
        self.image_r = pygame.transform.scale(red_image, (25, 25))
        self.image_b = pygame.transform.scale(blue_image, (25, 25))
        self.image_p = pygame.transform.scale(pink_image, (35, 25))
        self.image_o = pygame.transform.scale(orange_image, (25, 25))

        self.image = None

        if color == "red":
            self.image = self.image_r
        if color == "blue":
            self.image = self.image_b
        if color == "pink":
            self.image = self.image_p
        if color == "orange":
            self.image = self.image_o

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = active

        self.direction = starting_direction
        self.speed = speed

    def change_direction(self):
        self.direction = random.choice([0, 1, 2, 3])

    def fix_stutter(self):
        if self.direction == 0:
            self.rect.x -= 10
        elif self.direction == 1:
            self.rect.x += 10
        elif self.direction == 2:
            self.rect.y -= 10
        elif self.direction == 3:
            self.rect.y += 10

    def update(self):
        if self.active:
            if self.direction == 1:
                self.rect.x += self.speed
            if self.direction == 0:
                self.rect.x -= self.speed
            if self.direction == 2:
                self.rect.y -= self.speed
            if self.direction == 3:
                self.rect.y += self.speed

            # Change direction if close to screen boundaries
            if self.rect.x < 10:
                self.direction = random.choice([1, 2, 3])
                self.fix_stutter()
            if self.rect.x + self.image.get_width() > 725:
                self.direction = random.choice([0, 2, 3])
                self.fix_stutter()
            if self.rect.y + self.image.get_height() > 376:
                self.direction = random.choice([0, 1, 2])
                self.fix_stutter()
            if self.rect.y < 10:
                self.direction = random.choice([0, 1, 3])
                self.fix_stutter()

            # Change direction if colliding with walls
            increase = [[5, 0], [-5, 0], [0, 5], [0, -5]]
            for i in boundaries.rects:
                if self.direction == 0:
                    self.rect.x -= 10
                    if pygame.Rect.colliderect(self.rect, i):
                        self.direction = random.choice([1, 2, 3])
                        self.fix_stutter()
                    self.rect.x += 10
                elif self.direction == 1:
                    self.rect.x += 10
                    if pygame.Rect.colliderect(self.rect, i):
                        self.direction = random.choice([0, 2, 3])
                        self.fix_stutter()
                    self.rect.x -= 10
                elif self.direction == 2:
                    self.rect.y -= 10
                    if pygame.Rect.colliderect(self.rect, i):
                        self.direction = random.choice([0, 1, 3])
                        self.fix_stutter()
                    self.rect.y += 10
                elif self.direction == 3:
                    self.rect.y += 10
                    if pygame.Rect.colliderect(self.rect, i):
                        self.direction = random.choice([0, 1, 2])
                        self.fix_stutter()
                    self.rect.y -= 10

    def render(self):
        SCREEN.blit(self.image, self.rect)


class Pacman:

    def __init__(self):
        # Initialize Pacman images and attributes
        self.image_r = pygame.transform.scale(
            pacman_image,
            (pacman_image.get_width() // 65, pacman_image.get_height() // 65))
        self.image_l = pygame.transform.flip(self.image_r, True, False)
        self.image_u = pygame.transform.rotate(self.image_r, 90)
        self.image_d = pygame.transform.rotate(self.image_r, 270)

        self.image = self.image_r
        self.direction = "None"
        self.rect = self.image_r.get_rect()
        self.rect.x = 14
        self.rect.y = 178

    def update(self):
        # Move Pacman based on keyboard input
        self.keyboard()

        # Ensure Pacman stays within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def keyboard(self):
        # Keyboard input handling for Pacman movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.image = self.image_l
            self.direction = "Left"
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.image = self.image_r
            self.direction = "Right"
        if keys[pygame.K_UP]:
            self.rect.y -= 5
            self.image = self.image_u
            self.direction = "Up"
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
            self.image = self.image_d
            self.direction = "Down"

    def render(self):
        # Render Pacman on the screen
        SCREEN.blit(self.image, self.rect)


class Boundaries:

    def __init__(self, width, height, thickness=10, color=(0, 0, 255)):
        self.rects = []

        # Additional boundaries for Pacman maze layout (customize as needed)
        center_h = height // 2
        center_v = width // 2
        quarter_h = height // 4
        quarter_v = width // 4
        three_quarter_h = height * 3 // 4
        three_quarter_v = width * 3 // 4

        # Add lines based on your desired maze layout
        # Here are some examples:

        # Top left corner (modify positions and sizes as needed)
        self.rects.append(pygame.Rect(quarter_v, 0, thickness, quarter_h))
        self.rects.append(pygame.Rect(0, quarter_h, quarter_v, thickness))

        # Top right corner
        self.rects.append(pygame.Rect(three_quarter_v, 0, thickness,
                                      quarter_h))
        self.rects.append(
            pygame.Rect(width - quarter_v, quarter_h, quarter_v, thickness))

        # Bottom left corner
        self.rects.append(
            pygame.Rect(quarter_v, three_quarter_h, thickness, quarter_h))
        self.rects.append(
            pygame.Rect(0, three_quarter_h - thickness, quarter_v, thickness))

        # Bottom right corner
        self.rects.append(
            pygame.Rect(three_quarter_v, three_quarter_h, thickness,
                        quarter_h))
        self.rects.append(
            pygame.Rect(width - quarter_v, three_quarter_h - thickness,
                        quarter_v, thickness))

        # Center sections (adjust positions and sizes)
        self.rects.append(
            pygame.Rect(quarter_v, center_h - thickness // 2,
                        three_quarter_v - quarter_v, thickness))
        self.rects.append(
            pygame.Rect(quarter_v, center_h + thickness // 2,
                        three_quarter_v - quarter_v, thickness))
        self.rects.append(
            pygame.Rect(center_v - thickness // 2, quarter_h, thickness,
                        center_h - quarter_h))
        self.rects.append(
            pygame.Rect(center_v + thickness // 2, quarter_h, thickness,
                        center_h - quarter_h))
        self.rects.append(
            pygame.Rect(center_v - thickness // 2, three_quarter_h, thickness,
                        center_h - quarter_h))
        self.rects.append(
            pygame.Rect(center_v + thickness // 2, three_quarter_h, thickness,
                        center_h - quarter_h))

        self.box = pygame.Rect(259, 200, 225, 50)
        self.color = color

    def update(self):
        # Check for screen boundaries and adjust Pacman's position if needed
        if pacman.rect.left < 0:
            pacman.rect.left = 0
        if pacman.rect.right > WIDTH:
            pacman.rect.right = WIDTH
        if pacman.rect.top < 0:
            pacman.rect.top = 0
        if pacman.rect.bottom > HEIGHT:
            pacman.rect.bottom = HEIGHT

        # Checking if pacman collides with blue boundaries
        for i in self.rects:
            if pygame.Rect.colliderect(pacman.rect, i):
                if pacman.direction == "Right":
                    pacman.rect.x -= 5
                if pacman.direction == "Left":
                    pacman.rect.x += 5
                if pacman.direction == "Up":
                    pacman.rect.y += 5
                if pacman.direction == "Down":
                    pacman.rect.y -= 5

    def render(self):
        """Draws all the boundaries on the given screen surface."""
        for rect in self.rects:
            pygame.draw.rect(SCREEN, self.color, rect)
        pygame.draw.rect(SCREEN, self.color, self.box, 5)


def ghostHandler(blinky, pinky, clyde):
    if pygame.time.get_ticks() >= 10000:
        blinky.active = True
    if pygame.time.get_ticks() >= 20000:
        pinky.active = True
    if pygame.time.get_ticks() >= 30000:
        clyde.active = True


class Dots:
    def __init__(self):
        self.dots = []
        self.make_dots()
         
    def make_dots(self):
        y = 200
        ycount = 0
        while ycount < 14:
            xcount = 0
            x = 0
            while xcount < 7:
                dot = Rect(y, x, 12, 12)
                self.dots.append(dot)
                x += 25
                xcount += 1

            ycount += 1
            y += 25

        # x: 200-340, y: 275-365
        x = 200
        y = 275
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25 
       
        x = 200
        y = 300
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25 
            
        x = 200
        y = 325
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25 
           
        x = 200
        y = 350
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 200
        y = 375
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 110
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 135
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 160
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 185
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 210
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 235
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 0
        y = 260
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 110
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 135
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 160
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 185
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 210
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 235
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 552
        y = 260
        for i in range(8):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 394
        y = 275
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 394
        y = 300
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 394
        y = 325
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 394
        y = 350
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25

        x = 394
        y = 375
        for i in range(6):
            dot = Rect(x, y, 12, 12)
            self.dots.append(dot)
            x += 25
  

        
            
        

    def update(self):
        for i in self.dots:
            if pygame.Rect.colliderect(i, pacman.rect):
                self.dots.remove(i)
             
                

    def render(self):
        for i in self.dots:
            pygame.draw.rect(SCREEN, (255, 255, 255), i)
            
        
    
    

    

pacman = Pacman()
boundaries = Boundaries(WIDTH, HEIGHT)

blinky = Enemy("red", 271, 221, False, 0, 1)
pinky = Enemy("pink", 350, 221, False, 1, 1)
clyde = Enemy("orange", 450, 221, False, 3, 1)
dots = Dots()

enemies = [blinky, pinky, clyde]
run = True

while run:
    CLOCK.tick(60)
    SCREEN.fill((0, 0, 0))
    boundaries.render()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pacman.update()
    pacman.render()
    
    ghostHandler(blinky, pinky, clyde)

    for enemy in enemies:
        enemy.update()
        enemy.render()

    dots.update()
    dots.render()

    # Check for player collision with ghosts
    for i in enemies:
        if pygame.Rect.colliderect(pacman.rect, i.rect):
            run = False




    pygame.display.update()
