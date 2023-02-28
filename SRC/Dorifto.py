import sys, pygame, time, asyncio, threading, math
from datetime import datetime, timedelta

pygame.init()

logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

size = width, height = 1545, 800

screen = pygame.display.set_mode(size)

pygame.display.set_caption("D is for Drift")

bg_image = pygame.image.load("background.png")
Track = pygame.image.load("Track.png")

bg_rect = bg_image.get_rect()
T_rect = Track.get_rect()


needle_image = pygame.image.load("Needle.png")
speedometer_image = pygame.image.load("Speedometer.png")
car_image = pygame.image.load("Lidl_car.png")

class Car:
    def __init__(self, image):
        self.x = 58
        self.y = 43
        self.image = image
        self.perm_image = image
        self.angle = 1
        self.direction = 180
        self.speed = 0.1
        self.antispeed = 1
        self.x_shift = 0
        self.y_shift = 0
        self.speed2 = 1.25
        self.acc_mult = 0.25
        self.drift = False
        self.drift_distance = 0
        self.colliding = False

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
        if self.x > 2175:
            self.speed = 0.5
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8
            self.x -= self.speed

        if self.x < 25:
            self.speed = 1
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8
            self.x += self.speed


        if self.y > 1175:
            self.speed = 1
            self.y -= self.speed
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8

        if self.y < 25:
            self.speed = 1
            if needle.degrees_from_0 < 120:
                needle.degrees_from_0 += 8
            self.y += self.speed


        if self.y < 35 or self.y > 1165 or self.x < 35 or self.x > 2165:
            collision = True

        self.colliding = collision



    def drive(self):
        if self.speed == 0:
            self.speed = 0.2
        change_x = math.cos(math.radians(int(90 - self.direction))) * self.speed
        change_y = math.sin(math.radians(int(90 - self.direction))) * self.speed

        self.x += change_x
        self.y -= change_y

        self.antispeed = 1 / self.speed

    def accelerate(self, needle):
        self.speed2 = self.speed
        if self.speed < 1:
            self.acc_mult = 1.025
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
fps = Data_Sign(x=2150, y=30, text="FPS", color = (255, 255, 255), size=20)
speed_text = Data_Sign(x= 130, y=125, text=f"6", color=(255, 255, 255), size=80)


rotation_shift = 0
x_shift = 0
y_shift = 0

prev = datetime.utcnow()
prev_fps_switch = datetime.utcnow()
FPS = 60
fps_toggle = False




while True:
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        pygame.QUIT
    
    FPS += 1
    if datetime.utcnow() - prev > timedelta(seconds=1):
        prev = datetime.utcnow()
        fps.text = f"FPS: {FPS}"
        FPS = 0

    if keys[pygame.K_LSUPER] and keys[pygame.K_LALT]:
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
        car.accelerate(needle)
    else:
        car.drop_speed(needle)

    if keys[pygame.K_s]:
        car.brake()


    if (keys[pygame.K_SPACE] and keys[pygame.K_a] or keys[pygame.K_d]) or (car.speed > 6 and keys[pygame.K_a] or keys[pygame.K_d]) and not keys[pygame.K_s]:
        if keys[pygame.K_a] and car.drift_distance < 50:
            car.drift_distance += 1
        elif keys[pygame.K_d] and car.drift_distance > -50:
            car.drift_distance -= 1
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
    if keys[pygame.K_ESCAPE]:
        pygame.QUIT
        

    if int(car.speed*10) % 2 == 0:
        speed_text.text = f"{int(car.speed*10)}"

    car.check_wall_collision(needle)

    car.drive()
    car.rotate(rotation_shift)
    screen.blit(bg_image, bg_rect)
    screen.blit(Track, T_rect)
    car.display(screen)



    if fps_toggle:
        fps.display(screen)

    pygame.display.update()

