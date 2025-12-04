# Emmanuel Swenson

'''
Sources:
Mr. Cozort's code (https://github.com/ccozort/cozort__tower_of_the_apprentice)
'''

# brings the map defined in the text files into a defined map
from settings import *
import pygame as pg

# print(pg.font.get_fonts())

# Object or class

class Map:
    def __init__(self, filename):
        # creates empty list for map data
        self.data = []
        # open a specific file and close with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        # properties of Map that allow us to define length and width
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE[0]
        self.height = self.tileheight * TILESIZE[1]

# loads an image file and creates an image surface for blitting or drawing images on surface
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height)) # blit draws a source surface onto this surface
        #image = pg.transform.scale(image, (width // 2, height // 2))
        return image