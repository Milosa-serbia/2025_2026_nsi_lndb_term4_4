import pygame
from brbr_data import *

class UI :
    def __init__(self) :
        self.menu_open = False
        self.px_id = None
        self.status_rect = pygame.rect.Rect(20, 20, 500, 810)
        self.infos = {}
        for id in STATES.keys() :
            self.infos[id] = KinderState( \
                STATES[id]['name'], \
                STATES[id]['population'], \
                STATES[id]['vegetable_production'], \
                STATES[id]['obesity_rate'], \
                STATES[id]['importations'], \
                STATES[id]['exportations'] \
                    )
    
    def draw(self, screen) :
        if self.menu_open :
            pygame.draw.rect(screen, (240, 240, 240), self.status_rect)
            