import sys
import pygame

pygame.init()

ROZLISENI_X = 800
ROZLISENI_Y = 600
FPS = 60
CERNA_BARVA = (0, 0, 0)
BILA_BARVA = (255, 255, 255)
CERVENA_BARVA = (255, 0 , 0 )
ZELENA_BARVA = ( 0, 255 , 0 )
MODRA_BARVA = ( 0 , 0 , 255 )

velikost = 50
pozice_x = (ROZLISENI_X - velikost) / 2
pozice_y = (ROZLISENI_Y - velikost) / 2
rychlost = 10 

hodiny = pygame.time.Clock()

logo = pygame.image.load("G:\Vys\pyton/logo.png")

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
        image = pygame.image.load('Lidl_car.png')
        
    pygame.display.update()
    hodiny.tick(FPS)