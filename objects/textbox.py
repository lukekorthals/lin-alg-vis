from utils.draw import draw_text
from settings.colors import *
from pygame.font import Font

class Textbox:

    def __init__(self, pos: tuple, text: str, font: Font, color: tuple = BLACK, bg_color: tuple = WHITE):
        self.pos = pos
        self.text = text
        self.font = font
        self.color = color
        self.bg_color = bg_color
    
    def draw(self, surface):
        draw_text(surface, self.font, self.text, self.pos, self.color, self.bg_color)
