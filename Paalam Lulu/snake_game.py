import pygame, sys
from random import randint

class Snake:
    def __init__(self):
        self.moves = [None]
        self.surf = pygame.Surface((50,50))
        self.rect = self.surf.get_rect(center = (150,150))
        self.tail_surfs, self.tail_rects = [], []
        self.tail_rects.append(self.rect)
        self.extrama = {}
    
    def get_keypressed(self):# w = 119, d = 100, a = 97, s = 115 (keyboard input)
        for event in pygame.event.get(eventtype = pygame.KEYDOWN):
            if event.type == pygame.KEYDOWN:
                if event.key == 119: self.moves[0] = "up"
                elif event.key == 115: self.moves[0] = 'down'
                elif event.key == 97: self.moves[0] = 'left'
                elif event.key == 100: self.moves[0] = 'right'
                extrama = pygame.Rect((0,0), (50,50))
                extrama.center = self.rect.center
                self.extrama[self.moves[0]] = extrama
    
    def movement(self, rect, i):
        if i == 0: speed = 3
        else: speed = 2.9
        if self.moves[i] == 'up': rect.top -= speed
        elif self.moves[i] == 'down': rect.bottom += speed
        elif self.moves[i] == 'left': rect.left -= speed
        elif self.moves[i] == 'right': rect.right += speed
    
    def add_tail(self):
        tail_surf = pygame.Surface((50,50))
        tail_surf.fill('Green')
        self.tail_surfs.append(tail_surf)
        self.tail_rects.append(tail_surf.get_rect())
        self.idk()
    
    def idk(self):
        oft = 100
        i = len(self.tail_rects) - 1
        if self.moves[i - 1] == 'up':
            self.tail_rects[i].center = (self.tail_rects[i-1].centerx, self.tail_rects[i-1].centery + oft)
        elif self.moves[i - 1] == 'down':
            self.tail_rects[i].center = (self.tail_rects[i-1].centerx, self.tail_rects[i-1].centery - oft)
        elif self.moves[i - 1] == 'left':
            self.tail_rects[i].center = (self.tail_rects[i-1].centerx + oft, self.tail_rects[i-1].centery)
        elif self.moves[i - 1] == 'right':
            self.tail_rects[i].center = (self.tail_rects[i-1].centerx - oft, self.tail_rects[i-1].centery)
        self.moves.append(self.moves[i - 1])

    def tail_movement(self):
        oft = 30
        for i, rect in enumerate(self.tail_rects):
            if i == 0:
                self.movement(rect, i)
                continue
            flag = 0
            while flag <= len(self.extrama):
                try:
                    direc, ex = list(self.extrama.items())[flag]
                except IndexError: break
                if ex.collidepoint(rect.center):
                    self.moves[i] = direc
                    if self.tail_rects[i] == self.tail_rects[-1] and i != 0:
                        print(self.extrama)
                        self.extrama.pop(direc)
                        print(self.extrama)
                flag += 1
                    
            self.movement(rect, i)
                
    def update(self):
        self.tail_movement()
        screen.blit(self.surf, self.rect)
        for i, tail in enumerate(self.tail_surfs[0:]):
            screen.blit(tail, self.tail_rects[i+1])
            
class Apple:
    def __init__(self):
        self.apple = pygame.Surface((50,50))
        self.apple.fill('Red')
    def make_rect(self):
        x, y = randint(35, 605), randint(30, 450)
        self.rect = self.apple.get_rect(center = (x,y))
        
    def spawn(self):
        screen.blit(self.apple, self.rect)
        
pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
test_surf = pygame.Surface((570, 420)) #35, 30 ("boarder distance")
test_rect = test_surf.get_rect(center = (320, 240))
snake = Snake()
apple = Apple()
apple.make_rect()
while True:
    screen.fill("Blue")
    snake.get_keypressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if snake.rect.colliderect(apple.rect):
        snake.add_tail()
        apple.make_rect()
    else: snake.update()
    apple.spawn()
    #screen.blit(test_surf, test_rect)
    pygame.display.flip()
    
    clock.tick(60)