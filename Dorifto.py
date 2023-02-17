import pygame
import time
import math
from  tools import blit_rotate_center

logo = pygame.image.load("logo.PNG")
pygame.display.set_icon(logo)

GROUND = pygame.image.load("background.png")
TRACK = pygame.image.load("Track.png")
CAR = pygame.image.load("Lidl_car.png")

REX_X = 800
RES_Y = 600

WIDTH, HEIGHT = GROUND.get_width(), GROUND.get_height()
WIN = pygame.display.set_mode((REX_X, RES_Y))
pygame.display.set_caption("Dorifto")

FPS = 120
RACER = ()

class AbstractCar:   
    def __init__(self ,max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 180
        self.x , self.y = self.START_POS
        self.acceleration = 0.5
 
    def rotate(self, left=False , right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
            
    def draw(self,win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

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
    
class PlayerCar(AbstractCar):
    IMG = CAR
    START_POS = (50,27)
    
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
   
    player_car.draw(win)
    pygame.display.update()
 
run = True
clock = pygame.time.Clock()
images = [(GROUND, (0,0)), (TRACK, (0,0))]
player_car = PlayerCar(5,5)

while run:
    clock.tick(FPS)
    
    draw(WIN, images, player_car)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
  
    keys = pygame.key.get_pressed()
    moved = False 
    
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True )
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True 
        player_car.move_forward()
        
    if not moved:
        player_car.reduce_speed()



clock.tick(FPS)
pygame.QUIT