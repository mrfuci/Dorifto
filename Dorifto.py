import pygame
import time
import math
from  tools import blit_rotate_center

logo = pygame.image.load("logo.PNG")
pygame.display.set_icon(logo)

GROUND = pygame.image.load("background.png")
TRACK = pygame.image.load("Track.png")
CAR = pygame.image.load("Lidl_car.png")

WIDTH, HEIGHT = GROUND.get_width(), GROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dorifto")

FPS = 60


class AbstractCar:   
    def __init__(self ,max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x , self.y = self.START_POS
<<<<<<< Updated upstream
=======
        self.acceleration = 0.25
>>>>>>> Stashed changes
        
    def rotate(self, left=False , right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
            
    def draw(self,win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
<<<<<<< Updated upstream

=======
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
    
        self.y -= vertical
        self.x -= horizontal
        
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
    
>>>>>>> Stashed changes
class PlayerCar(AbstractCar):
    IMG = CAR
    START_POS = (50,50)
    
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
   
    player_car.draw(win)
    pygame.display.update()
 
run = True
clock = pygame.time.Clock()
images = [(GROUND, (0,0)), (TRACK, (0,0))]
player_car = PlayerCar(4,4)

while run:
    clock.tick(FPS)
    
    draw(WIN, images, player_car)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
<<<<<<< Updated upstream
=======
    
    keys = pygame.key.get_pressed()
    moved = False 
    
    if keys[pygame.K_a]:
        player_car.rotate(left=True )
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True 
        player_car.move_forward()
        
    if not moved:
        player_car.reduce_speed()
>>>>>>> Stashed changes


clock.tick(FPS)
pygame.QUIT