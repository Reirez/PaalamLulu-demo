import pygame, sys
from random import choice, randint

class Roach:
    def __init__(self):
        self.roaches = {} #{surf:[rect, horizontal d, vertical d]} d=direction
        self.speed = [] #[xspeed,, yspeed]
        self.score = 0
        self.deads = []
        self.dead = [pygame.image.load('dead1.png'), pygame.image.load('dead2.png')]
        """makes roaches"""
        while len(self.roaches.keys()) < 15:
            self.roaches[pygame.image.load_sized_svg(choice(['fries12.svg', 'egg13.svg']), (choice([(100,70),(100,70),(200,140)])))] = []
            self.speed.append([randint(7,15), randint(2,5)])
        for roach in self.roaches:
            self.roaches[roach].append(roach.get_rect())
            self.roach_direction(roach)
            
    def roach_direction(self, roach):
        """assigns direction to roaches"""
        x, y = choice([-10, 650, -20, 670]), choice(range(0, 480))
        self.roaches[roach][0].center = (x,y)
        if self.roaches[roach][0].centerx < 0: self.roaches[roach].append('R')
        else: self.roaches[roach].append('L')
        self.roaches[roach].append(choice(["T", 'B']))
                
    def move_roach(self):
        """moves the roaches"""
        for index, roach in enumerate(self.roaches):
            if len(self.roaches[roach]) >= 4: continue
            if "T" in self.roaches[roach]: self.roaches[roach][0].top -= self.speed[index][1]
            else: self.roaches[roach][0].bottom += self.speed[index][1]
            if 'R' in self.roaches[roach]: self.roaches[roach][0].right += self.speed[index][0]
            else: self.roaches[roach][0].left -= self.speed[index][0]
            """gives roach new direction and speed after going off-screen"""
            if self.roaches[roach][0].left > 650 or self.roaches[roach][0].right < 0:
                self.roaches[roach].pop(1)
                self.roaches[roach].pop(1)
                self.speed[index] = [randint(7,15), randint(2,5)]
                self.roach_direction(roach)
    
    def squish_roach(self):
        for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONUP):
            if self.squish_again(event): return #squishes again
            for roach_val in self.roaches.values(): #squishes
                if roach_val[0].collidepoint(event.pos) and True not in roach_val:
                    roach_val.append(True)
                    return

    def squish_again(self, event):
        for surf, roach_val in self.roaches.items():
            if True not in roach_val: continue
            if roach_val[0].collidepoint(event.pos) and "squished" not in roach_val:
                roach_val.append('squished')
                surf.set_alpha(0)
                surface = pygame.transform.scale(choice(self.dead), surf.get_size())
                self.deads.append([surface, roach_val[0]])
                self.score += 1
                return True
                    
    def update_roach(self):
        if self.deads:
            for ded in self.deads:
                screen.blit(ded[0], ded[1])
        for roach in self.roaches:
            screen.blit(roach, self.roaches[roach][0])
    
    def display_score(self):
        score = font.render(str(self.score), None, 'Purple')
        score_rect = score.get_rect(center = (320, 100))
        screen.blit(score, score_rect)

pygame.init()
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640,480))
ads = Roach()
while True:
    screen.fill('Gray')
    ads.squish_roach()
    for event in pygame.event.get(eventtype=pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
           
    ads.move_roach()
    
    ads.update_roach()
    ads.display_score()
    pygame.display.flip()
    print(clock.get_fps())
    clock.tick(60)
    
    