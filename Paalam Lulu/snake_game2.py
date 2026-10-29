import pygame, sys, math
from pygame import math as m
from random import randint

class Apple:
    def __init__(self):
        self.apple = pygame.image.load('island.png')
        
    def make_rect(self):
        x, y = randint(35, 605), randint(30, 450)
        self.rect = self.apple.get_rect(center = (x,y))
        
    def spawn(self):
        screen.blit(self.apple, self.rect)
    
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640,480))
surf = pygame.image.load('chinese_ship.png') #surf gets transformed and saved to surf1
surf1 = pygame.image.load('chinese_ship.png')

tail = pygame.image.load('head.png')
tail.fill('Red')


rect = surf.get_rect(center = (320,240))
angle, direction = "Idk", (0,0)
speed = 5
surfs = []
positions = [(-100, -100)]
apple = Apple()
apple.make_rect()
game_on = True
pygame.mouse.set_visible(False)
tail_number = 1

while game_on:
    screen.fill('Blue')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            distance = [event.pos[1] - rect.centery, event.pos[0] - rect.centerx]
            #rotation of surface
            angle = -math.degrees(math.atan2(distance[0], distance[1])) # angle between head n mouse
            surf1 = pygame.transform.rotate(surf, angle)
            rect = surf1.get_rect(center = rect.center)
            
            #movement of surface to mouse
           
            angle = math.radians(-angle)
            direction = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed
            if math.sqrt(math.pow(distance[0], 2) + math.pow(distance[1], 2)) <= 75:
                mouse_newpos = event.pos + direction * 5
                if mouse_newpos[0] < 0 or mouse_newpos[1] < 0:
                    pass
                else:
                    pygame.mouse.set_pos(mouse_newpos) #prevents mouse n head from colliding
    
    if angle != 'Idk':
        rect.center = rect.center + direction
        if m.Vector2(rect.center).distance_to(positions[-1]) > 20: #only append new surf if distance from prev is far enough
            positions.append(m.Vector2(rect.center))
    
    if len(positions) > tail_number:
        positions.pop(0)
    
    
    #displaying of snake
    for i, position in enumerate(positions):
        if i == len(positions) - 1:
            screen.blit(surf1, position)
        else:
            distance = (positions[i+1][0] - position[0], positions[i+1][1] - position[1])
            angle = -math.degrees(math.atan2(distance[1], distance[0]))
            surf1 = pygame.transform.rotate(surf, angle)
            screen.blit(surf1, position)
            #pygame.draw.circle(screen, 'Green', position, 25)
            
    if rect.colliderect(apple.rect):
        apple.make_rect()
        tail_number += 1
        
    
    for position in positions[:-3]:
        position = m.Vector2(position)
        if position.distance_to(rect.center) <= 30:
            print('game over')
            game_on = False
            
    apple.spawn()
    pygame.display.flip()
    clock.tick(60)
    print(len(positions))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()