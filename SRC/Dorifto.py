import sys, pygame, time, asyncio, threading, math, os
from datetime import datetime, timedelta

score = 0
score_increment = 1
score_increment_fast = 2

pygame.init()

font = pygame.font.Font(None, 25)
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

size = width, height = 1729, 800

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pygame Driftmaster (Space +  Direction to drift)")

bg_image = pygame.image.load("Grass.png")

bg_rect = bg_image.get_rect()

needle_image = pygame.image.load("Needle.png")
speedometer_image = pygame.image.load("Speedometer.png")
car_image = pygame.image.load("Lidl_car.png")
crash = pygame.image.load("crash.png")


class Car:
    def __init__(self, image):
        self.x = 57
        self.y = 43
        self.image = image
        self.perm_image = image
        self.angle = 1
        self.direction = 180
        self.speed = 1.5
        self.antispeed = 1
        self.x_shift = 0
        self.y_shift = 0
        self.speed2 = 1.25
        self.acc_mult = 0.25
        self.drift = False
        self.drift_distance = 0
        self.colliding = True 

    def display(self, screen):
        direction = self.direction*-1
        direction += self.drift_distance
        self.image = pygame.transform.rotate(self.perm_image, direction)
        screen.blit(self.image, self.image.get_rect(center=[self.x, self.y]))


    def rotate(self, angle):
        self.direction -= angle
        self.direction = self.direction % 360

    def check_wall_collision(self, needle):
        collision = False
        if self.x > 1520:
            self.speed = 1.5
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8
            self.x -= self.speed

        if self.x < 25:
            self.speed = 1
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8
            self.x += self.speed


        if self.y > 745:
            self.speed = 1
            self.y -= self.speed
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8

        if self.y < 20:
            self.speed = 1
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8
            self.y += self.speed


        if self.y < 35 or self.y > 1500 or self.x < 35 or self.x > 1500:
            collision = True

        self.colliding = collision
        
        car.drive()
        car.rotate(rotation_shift)
        screen.blit(bg_image, bg_rect)
        car.display(screen)
        screen.blit(score_text,(1590,700))
                
        if self.y < 40 :
            screen.blit(crash, (0,0))
        
        if self.y > 740 :
            screen.blit(crash, (0,0))
        
        
        if self.x < 50 :
            screen.blit(crash, (0,0))
            
        if self.x > 1488:
            screen.blit(crash, (0,0))
            
    def drive(self):
        if self.speed == 0:
            self.speed = 0
        change_x = math.cos(math.radians(int(90 - self.direction))) * self.speed
        change_y = math.sin(math.radians(int(90 - self.direction))) * self.speed

        self.x += change_x
        self.y -= change_y

        self.antispeed = 1 / self.speed

    def accelerate(self, needle):
        self.speed2 = self.speed
        if self.speed < 1:
            self.acc_mult = 10.025
        elif self.speed < 3:
            self.acc_mult = 1.025
        elif self.speed < 4:
            self.acc_mult = 1.025
        elif self.speed < 5:
            self.acc_mult = 1.005
        elif self.speed < 6:
            self.acc_mult = 1.005
        elif self.speed < 7:
            self.acc_mult = 1.001
        elif self.speed < 8:
            self.acc_mult = 1.0005
        else:
            self.acc_mult = 1.005


        if self.speed < 12:
            self.speed *= self.acc_mult
            if needle.degrees_from_0 > 1 and not self.colliding:
                needle.degrees_from_0 -= self.acc_mult/2

    def drop_speed(self, needle):
        self.speed = self.speed / 1.005
        if self.speed < 0.5:
            self.speed = 0.5
        else:
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 0.3


    def brake(self):
        self.speed = self.speed / 1.02
        if self.speed < 0.5:
            self.speed = 0.5
        else:
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 1
class Data_Sign:
    def __init__(self, x, y, text, color, size):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(name="Calibri", size=size, bold=True)
        self.text_obj = self.font.render(self.text, True, (self.color))

    def display(self, screen):
        self.text_obj = self.font.render(self.text, True, (self.color))
        print("display", self.x, self.y)
        screen.blit(self.text_obj, ((self.x - self.text_obj.get_width() // 2, self.y - self.text_obj.get_height() // 2)))
class Speedometer:
    def __init__(self, image):
        self.x = 30
        self.y = 30
        self.image = image

    def display(self, screen):
        screen.blit(pygame.transform.scale(surface=self.image, size=(200, 200)), (self.x, self.y))
class Needle:
    def __init__(self,x ,y, image):
        self.x = x
        self.y = y
        self.degrees_from_0 = 120
        self.image = image
        self.perm_image = image

    def display(self, screen):
        self.image = pygame.transform.rotate(self.perm_image, self.degrees_from_0)
        screen.blit(self.image, self.image.get_rect(center=[self.x, self.y]))


needle = Needle(x=125, y=130, image=needle_image)
car = Car(image=car_image)
speedometer = Speedometer(speedometer_image)
fps = Data_Sign(x=1729, y=800, text="FPS", color = (255, 255, 255), size=20)
speed_text = Data_Sign(x= 1729, y=800, text=f"6", color=(255, 255, 255), size=80)
    

rotation_shift = 1
x_shift = 1
y_shift = 1

prev = datetime.utcnow()
prev_fps_switch = datetime.utcnow()
FPS = 120
fps_toggle = True 


    

while True:
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        pygame.QUIT
        exit()
        
    FPS += 1
    if datetime.utcnow() - prev > timedelta(seconds=1):
        prev = datetime.utcnow()
        fps.text = f"FPS: {FPS}"
        FPS = 0

    if keys[pygame.K_l] and keys[pygame.K_t]:
        if datetime.utcnow() - prev_fps_switch > timedelta(seconds=0.3):
            prev_fps_switch = datetime.utcnow()
            if fps_toggle == True:
                fps_toggle = False
            else:
                fps_toggle = True

    event = pygame.event.poll()


    if event.type == pygame.QUIT:
        exit()


    if keys[pygame.K_a]:        
        if car.speed > 3:
            rotation_shift = 1.5
        elif car.speed > 5:
            rotation_shift = 2
        elif car.speed > 7:
            rotation_shift = 3
        else:
            rotation_shift = 0.7
    elif keys[pygame.K_d]:
        if car.speed > 3:
            rotation_shift = -1.5
        elif car.speed > 5:
            rotation_shift = -2
        elif car.speed > 7:
            rotation_shift = -3
        else:
            rotation_shift = -0.7
    else:
        rotation_shift = 0

    if keys[pygame.K_w]:
        car.speed = 4
    else:
        car.drop_speed(needle)

    if keys[pygame.K_s]:
        car.brake()
    if keys[pygame.K_w] and keys[pygame.K_LSHIFT]:
        car.speed = 7.25
    
    if (keys[pygame.K_SPACE] and keys[pygame.K_a] or keys[pygame.K_d]) or (car.speed > 6 and keys[pygame.K_a] or keys[pygame.K_d]) and not keys[pygame.K_s]:
        if keys[pygame.K_a] and car.drift_distance < 50:
            car.drift_distance += 1.5
        elif keys[pygame.K_d] and car.drift_distance > -50:
            car.drift_distance -= 1.5
    else:
        if car.drift_distance > 0:
            car.drift_distance -= 1
            if car.speed > 1:
                car.speed -= 0.1
            if car.drift_distance < 0:
                car.drift_distance = 0
        elif car.drift_distance < 0:
            car.drift_distance += 1
            if car.speed > 1:
                car.speed -= 0.1

            if car.drift_distance > 0:
                car.drift_distance = 0
    
    
    if keys[pygame.K_SPACE] and keys[pygame.K_d]:
        score += score_increment
    
    if keys[pygame.K_SPACE] and keys[pygame.K_a]:
        score += score_increment
    
    if keys[pygame.K_LSHIFT] and keys[pygame.K_SPACE] and keys[pygame.K_a]:
        score + score_increment_fast
    
    if keys[pygame.K_LSHIFT] and keys[pygame.K_SPACE] and keys[pygame.K_d]:
        score + score_increment_fast
        
    
    score_text = font.render(f"Score: {score}", True , (255,255,255))
    
    ach1 = font.render(f"Achievment 1: Nice (69 score)", True, (255,255,255))
    ach2 = font.render(f"Achievment 2: Real drifter (1000 score)", True, (255,255,255))
    ach3 = font.render(f"Achievment 3: Get a life, please (10 000 score)", True, (255,255,255))
    ach4 = font.render(f"Achievment 4: stop (100 000 score)", True, (255,255,255))
    
    car.check_wall_collision(needle)
   
    if score >= 69:
        screen.blit(ach1,(25,780))
    if score >= 1000:
         screen.blit(ach2,(280,780))
    if score >= 10000:
        screen.blit(ach3,(620,780))
    if score >= 100000:
        screen.blit(ach4,(1018,780))

        
    pygame.display.update()
