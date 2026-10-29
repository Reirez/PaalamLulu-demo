import pygame, sys
from assets import *
from textdisplay import Text

def jail(rects, rod):
    """restricts hand from going off display"""
    for rect in rects:
        if rect.left < 0: rect.left = 0
        if rect.right > 640: rect.right = 640
        if rect.top < 0: rect.top = 0
        if rect.bottom > 480: rect.bottom = 480
    """adds a bit of resistance before hand comes off rod"""
    if rects[0].colliderect(rod) and rects[0].left > rod.left:
        surf_rect.left = rod.left
    if rects[0].colliderect(rod) and rects[0].right < rod.right:
        surf_rect.right = rod.right

class Score:
    """Handles the score bar"""
    def __init__(self, font, palm, rod, increment):
        self.font = font
        self.score = 0
        self.check1, self.check2 = False, False
        self.score_bg = pygame.Surface((300,30))
        self.palm, self.rod = palm, rod
        self.increment = increment
        
    def add_score(self, rodbase, rodtip):
        """Checks if a score should be added"""
        if self.palm.colliderect(rodtip): self.check1 = True
        if self.palm.colliderect(rodbase) and self.check1: self.check2 = True
        if self.check1 and self.check2:
            self.score += self.increment
            self.check1, self.check2 = False, False
    
    def decrease_score(self):
        """decreases the score. speed of decrease is based on collision"""
        if not self.palm.colliderect(self.rod): self.score -= 1
        else: self.score -= 0.3
        if self.score < 0: self.score = 0
            
    def display_score(self): 
        """Displays the score"""
        self.decrease_score()
        score_surf2 = pygame.Surface((self.score, 30))
        score_surf2.fill('Purple')
        screen.blit(self.score_bg, (100, 50))
        screen.blit(score_surf2, (100, 50))
        
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
pygame.mouse.set_visible(False)
pygame.display.set_caption("Paalam Lulu Test")
#assets
score = Score(font, surf_rect, rod_rect, 10)
score_increment = 7
textz = Text(font, screen, clock)
flagtest = False

while True:
    screen.fill('Blue')
    left_rect = left_surf.get_rect(right = surf_rect.left, bottom = surf_rect.bottom)
    right_rect = right_surf.get_rect(left = surf_rect.right, bottom = surf_rect.bottom)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #grip hand
            surf = pygame.Surface((60,50))
            #surf = pygame.image.load('palm.png')
            surf_rect = surf.get_rect(center = event.pos)
            score.palm, score_increment = surf_rect, 13
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #open hand
            #surf = pygame.Surface((100,50))
            surf = pygame.image.load('palm.png')
            surf = pygame.transform.scale_by(surf, 1.2)
            surf_rect = surf.get_rect(center = event.pos)
            score.palm, score_increment = surf_rect, 5
            
        if event.type == pygame.MOUSEMOTION: #hand movement
            surf_rect.center = event.pos
            if rod_rect.colliderect(surf_rect):
                score.add_score(rodbase, rodtip)
    
    jail([surf_rect, left_rect, right_rect], rod_rect)
    screen.blit(background)
    score.display_score()

    screen.blit(surf, surf_rect)
    screen.blit(rod, rod_rect)
#     screen.blit(rodsurf, rodbase)
    #screen.blit(rodsurf, rodtip)
#     screen.blit(left_surf, (surf_rect.x - 15, surf_rect.y))
#     screen.blit(right_surf, (surf_rect.x + 25, surf_rect.y))
    screen.blit(left_surf, (left_rect.x + 10, left_rect.y))
    screen.blit(right_surf, (right_rect.x - 50, right_rect.y))
    
    pygame.display.flip()
    print(rod_rect.top)
    print(rodbase.bottom)
    
    clock.tick(60)
    