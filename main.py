# Created by Emmanuel Swenson with the help of ChatGPT

# yay I can use github from VS CODE!

# import necessary modules
import math
import random
import sys
import pygame as pg
from settings import *  # the starting values of variables and constants
from sprites import *  # defining the characters / objects (player, mob, etc.)
from utils import *  # defining the characteristics of the maps
from os import path

class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Emmanuel's awesome game!!!")
        self.playing = True

    # sets up a game folder directory path using the current folder containing THIS file
    # give the Game class a map property which uses the Map class to parse the level1.txt file
    # loads image file from images folder
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.map = Map(path.join(self.game_folder, 'level1.txt'))
        self.player_img = pg.image.load(path.join(self.img_folder, 'Drill_Off.png')).convert_alpha()
        self.player_img_2 = pg.image.load(path.join(self.img_folder, 'Drill_On.png')).convert_alpha()
        self.pig_img = pg.image.load(path.join(self.img_folder, 'Pig_Not_Moving.png')).convert_alpha()
        self.cow_img = pg.image.load(path.join(self.img_folder, 'Cow_Not_Moving.png')).convert_alpha()
        self.chicken_img = pg.image.load(path.join(self.img_folder, 'Chicken_Not_Moving.png')).convert_alpha()
        self.sun_powerup_img = pg.image.load(path.join(self.img_folder, 'Sun_Powerup.png')).convert_alpha()

    def new(self):
        # the sprite Groups allow us to update and draw sprites in grouped batches
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, "unmoveable")
                elif tile == '2':
                    Wall(self, col, row, "moveable")
                elif tile == '3':
                    Wall(self, col, row, "breakable")
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # process
            self.update()
            # output
            self.draw()
        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("Window closed — quitting game")
                self.playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print("Mouse clicked!")

    def update(self):
        # update all sprites
        self.all_sprites.update()
        seconds = pg.time.get_ticks() // 1000
        countdown = 10
        self.time = countdown - seconds

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(DARK_GREY)
        # HUD
        self.draw_text(self.screen, str(self.player.health), 24, BLACK, 100, 100)
        self.draw_text(self.screen, str(self.player.coins), 24, BLACK, 400, 100)
        self.draw_text(self.screen, str(self.time), 24, BLACK, 500, 100)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    # creating an instance or instantiating the Game class
    g = Game()
    g.new()
    g.run()