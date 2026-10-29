import pygame, sys, time, threading, json
#Notes >> dtime: display time, pos: position, animation=[in, out, bool]
class Text:
    """A text system, an attempt to model one"""
    def __init__(self, dias): #dias: {text:[pos, dtime, animation]}
        self.active_texts = {}
        self.threads = [threading.Thread(target=self.add_active,args=(dia,dias[dia][0],dias[dia][1],dias[dia][2])) for dia in dias.keys()]
        self.dont_clears = []
    
    def blit_active(self):
        '''blits all current active texts to screen'''
        for surf, rect in self.active_texts.items():
            screen.blit(surf, rect)
    
    def display_text(self, text_index):
        '''method to add text to active texts'''
        try: self.threads[text_index].start()
        except RuntimeError: pass
        
    def add_active(self, text, pos, dtime, animation):
        '''Makes text surf and rect, and handles display time n animation'''
        text_surfs = [font.render(content, None, 'White') for content in text.split('\n')]
        text_rects = []
        for index, value in enumerate(text_surfs):
            if index == 0: text_rects.append(value.get_rect(center=(pos)))
            else: text_rects.append(value.get_rect(center=(pos)))
            pos = (text_rects[index].centerx, text_rects[index].centery + 30) #makes pos for next text
            text_rects[index].left = text_rects[0].left #aligns
            self.active_texts[value] = text_rects[index]
        self.in_animation(text_surfs, animation[0])
        if True in animation: #if a text is not to be cleared from screen
            self.dont_clears.append(text_surfs)
            return
        time.sleep(dtime)
        self.out_animation(text_surfs, animation[1])
        for content in text_surfs:#clears text from screen after time
            del self.active_texts[content]
    
    def in_animation(self, text_surfs, animation):
        timer = 0
        if animation == 'None': return
        elif animation == "fadein":
            while timer <= 255:
                for text_surf in text_surfs:
                    text_surf.set_alpha(timer)
                timer += 51
                time.sleep(0.1)
                
    def out_animation(self, text_surfs, animation):
        timer = 255
        if animation == 'None': return
        elif animation == 'fadeout':
            while timer >= 0:
                for text_surf in text_surfs:
                    text_surf.set_alpha(timer)
                timer -= 51
                time.sleep(0.1)
    
    def clear(self, index=None):
        """clears text that previously were not to be cleared"""
        if index: #clear one specific
            del self.active_texts[self.dont_clears[index]]
            del self.dont_clears[index]
        else: #clear all
            for surf_list in self.dont_clears:
                for surf in surf_list: del self.active_texts[surf]
            self.dont_clears = []
            
                
            
        

    
pygame.init()

screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
with open("LuluDialogues.json", "r") as file:
    text = Text(json.load(file))

while True:
    screen.fill('grey')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            text.clear()
    text.display_text(1)
    text.display_text(5)
    text.blit_active()
    pygame.display.flip()
    clock.tick(60)