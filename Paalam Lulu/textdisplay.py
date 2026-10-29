import pygame, sys


class Text:
    def __init__(self, font, screen, clock):
        self.font = font
        self.timers = {}
        self.screen = screen
        self.dont_display = set([]) #set for faster lookup with "in"
        self.clock = clock
        
    def render(self, text, pos, time, color): #(text, position to blit, amount of time to display, text color)
        """Blits text onto screen"""
        if text in self.dont_display: return
        if text not in self.timers.keys():
            self.timers[text] = time
            
        text_list = text.split('\n') #how bad is this for performance? 
        text_surf = self.font.render(text_list[0], None, color)
        text_rect = text_surf.get_rect(center = pos)
        
        if len(text_list) >= 2 and self.timers[text] > 0 :
            """If text has new lines"""
            self.screen.blit(text_surf, text_rect)
            for text_line in text_list[1:]: #messy..fix?
                text_rect = text_surf.get_rect(left = text_rect.left, top = text_rect.bottom)
                text_surf = self.font.render(text_line, None, color)
                self.screen.blit(text_surf, text_rect)
            self.timers[text] = self.timers[text] - self.clock.get_time() / 1000
        
        elif self.timers[text] > 0:
            """if text doesnt have newlines"""
            self.screen.blit(text_surf, text_rect)
            self.timers[text] = self.timers[text] - self.clock.get_time() / 1000
        
        else:
            """When timer hits 0, text is deleted from self.timers"""
            self.dont_display.add(text)
            del self.timers[text]
            
# pygame.init()
# clock = pygame.time.Clock()
# font = pygame.font.Font(None, 50)
# screen = pygame.display.set_mode((500,500))
# text = Text(font, screen)
# time = 0
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#             
#     screen.fill('Black')
#     text.render("Hello", (250,250), 6)
#     text.render("Hiiiii", (150, 250), 4)
#     if time >= 8:
#         text.render("Uhhhh", (250,250), 4)
#     text.render("I did\nit but idk how\ngood this is for\nperformance", (100, 300), 2)
#     pygame.display.flip()
#     print(clock.get_time())
#     time += clock.get_time() / 1000
#     clock.tick(60)