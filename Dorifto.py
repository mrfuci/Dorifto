import sys
import pygame

pygame.init()

logo = pygame.image.load("logo.PNG")
pygame.display.set_icon(logo)

ROZLISENI_X = 800
ROZLISENI_Y = 600
FPS = 60
CERNA_BARVA = (0, 0, 0)
BILA_BARVA = (255, 255, 255)
CERVENA_BARVA = (255, 0 , 0 )
ZELENA_BARVA = ( 0, 255 , 0 )
MODRA_BARVA = ( 0 , 0 , 255 )

velikost = 25
pozice_x = (ROZLISENI_X - velikost) / 2
pozice_y = (ROZLISENI_Y - velikost) / 2
rychlost = 10 

#class AbstractCar:
#    def __init__(self ,max_vel, rotation_vel):
#        self.max_vel = max_vel
#        self.vel = 0
#       self.rotation_vel = rotation_vel
#        self.angle = 0
        
#    def rotate(self, left=False , right=False):
#        if left:
#            self.angle += self.rotation_vel
#        elif right:
#            self.angle -= self.rotation_vel
        
hodiny = pygame.time.Clock()

car = pygame.image.load("Lidl_car.png")
BACKGROUND = pygame.image.load("background.png")

okno = pygame.display.set_mode((ROZLISENI_X, ROZLISENI_Y))
pygame.display.set_caption("Dorifo")


while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    klavesy = pygame.key.get_pressed()
    
    if klavesy[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()


    if klavesy[pygame.K_DOWN]:
        pozice_y += rychlost
    if klavesy[pygame.K_UP]:
        pozice_y -= rychlost
    if klavesy[pygame.K_LEFT]:
       car = pygame.transform.rotate(car, 5)
       pozice_x -= rychlost
    if klavesy[pygame.K_RIGHT]:
       car = pygame.transform.rotate(car, -5)
       pozice_x += rychlost
    
    if pozice_x > 800 - 50:
        pozice_x = 800 - 50
    if pozice_y > 600 - 50:
        pozice_y = 600 - 50
    if pozice_x < 0:
        pozice_x = 0
    if pozice_y < 0:
        pozice_y = 0
    
    class platform(pygame.sprite.Sprite):
    
        okno.fill(BILA_BARVA)
        okno.blit(car, (pozice_x, pozice_y))
                
    pygame.display.update()
    hodiny.tick(FPS)