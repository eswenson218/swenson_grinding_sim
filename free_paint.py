# Emmanuel Swenson

# importing necessary modules
import pygame as pg
from settings import *
import settings
from sprites import *
from utils import *
from os import path

class Game:
    def __init__(self):
        pg.init() # initializing pygame
        self.clock = pg.time.Clock() # creating the game clock
        self.screen = pg.display.set_mode((FP_W, FP_H)) # screen dimentions
        pg.display.set_caption("Free Paint")
        self.screen.fill(WHITE)
        self.playing = True
        self.is_drawing = False
        self.color = BLACK
        self.draw_size = 10

    def load_data(self):
        # where to get images
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')

        # where to get sounds
        self.sound_folder = path.join(self.game_folder, 'sounds')

        pg.mixer.music.load(path.join(self.sound_folder, "fp bg music.mp3"))
        pg.mixer.music.set_volume(settings.VOL_MULT * 0.4)
        pg.mixer.music.play(-1)

    def new(self):
        # the sprite Groups allow us to update and draw sprites in grouped batches
        self.load_data()

        # creating sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_targets = pg.sprite.Group()
        self.game_start_time = pg.time.get_ticks()

        pg.draw.rect(self.screen, LIGHT_GREY, (0, 0, 1200, 70))
        pg.draw.rect(self.screen, DARK_GREY, (0, 70, 1200, 10))

        # color selectors
        pg.draw.rect(self.screen, BLACK, (100, 20, 30, 30))
        pg.draw.rect(self.screen, BROWN, (150, 20, 30, 30))
        pg.draw.rect(self.screen, RED, (200, 20, 30, 30))
        pg.draw.rect(self.screen, ORANGE, (250, 20, 30, 30))
        pg.draw.rect(self.screen, YELLOW, (300, 20, 30, 30))
        pg.draw.rect(self.screen, LIME, (350, 20, 30, 30))
        pg.draw.rect(self.screen, GREEN, (400, 20, 30, 30))
        pg.draw.rect(self.screen, DARK_GREEN, (450, 20, 30, 30))
        pg.draw.rect(self.screen, NAVY, (500, 20, 30, 30))
        pg.draw.rect(self.screen, BLUE, (550, 20, 30, 30))
        pg.draw.rect(self.screen, LIGHT_BLUE, (600, 20, 30, 30))
        pg.draw.rect(self.screen, CYAN, (650, 20, 30, 30))
        pg.draw.rect(self.screen, LIGHT_PURPLE, (700, 20, 30, 30))
        pg.draw.rect(self.screen, PURPLE, (750, 20, 30, 30))
        pg.draw.rect(self.screen, MAGENTA, (800, 20, 30, 30))
        pg.draw.rect(self.screen, PINK, (850, 20, 30, 30))
        pg.draw.rect(self.screen, GREY, (900, 20, 30, 30))
        pg.draw.rect(self.screen, DARK_GREY, (950, 20, 30, 30))
        pg.draw.rect(self.screen, NOT_QUITE_BLACK, (1000, 20, 30, 30))

    def run(self):
        while self.playing:
            # game clock
            self.dt = self.clock.tick(10000) / 1000
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
                self.playing = False
            elif event.type == pg.MOUSEBUTTONDOWN and list(pg.mouse.get_pos())[1] > 80 + (self.draw_size / 2):
                self.is_drawing = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.is_drawing = False
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key == pg.K_d: # draw function
                    self.color = BLACK
                elif event.key == pg.K_e: # eraser function
                    self.color = WHITE
                # drawing size
                elif event.key == pg.K_1:
                    self.draw_size = 10
                elif event.key == pg.K_2:
                    self.draw_size = 20
                elif event.key == pg.K_3:
                    self.draw_size = 30
                elif event.key == pg.K_4:
                    self.draw_size = 40
                elif event.key == pg.K_5:
                    self.draw_size = 50
                elif event.key == pg.K_6:
                    self.draw_size = 60
                elif event.key == pg.K_7:
                    self.draw_size = 70
                elif event.key == pg.K_8:
                    self.draw_size = 80
                elif event.key == pg.K_9:
                    self.draw_size = 90
                elif event.key == pg.K_0:
                    self.draw_size = 100
                # can draw thinner lines if holding left alt and choose a number
                if keys[pg.K_LALT]:
                    if event.key == pg.K_1:
                        self.draw_size = 1
                    elif event.key == pg.K_2:
                        self.draw_size = 2
                    elif event.key == pg.K_3:
                        self.draw_size = 3
                    elif event.key == pg.K_4:
                        self.draw_size = 4
                    elif event.key == pg.K_5:
                        self.draw_size = 5
                    elif event.key == pg.K_6:
                        self.draw_size = 6
                    elif event.key == pg.K_7:
                        self.draw_size = 7
                    elif event.key == pg.K_8:
                        self.draw_size = 8
                    elif event.key == pg.K_9:
                        self.draw_size = 9
                    elif event.key == pg.K_0:
                        self.draw_size = 10
                # color choosing
                if keys[pg.K_LCTRL]:
                    if event.key == pg.K_q:
                        self.color = BLACK
                    elif event.key == pg.K_w:
                        self.color = BROWN
                    elif event.key == pg.K_e:
                        self.color = RED
                    elif event.key == pg.K_r:
                        self.color = ORANGE
                    elif event.key == pg.K_t:
                        self.color = YELLOW
                    elif event.key == pg.K_y:
                        self.color = LIME
                    elif event.key == pg.K_u:
                        self.color = GREEN
                    elif event.key == pg.K_i:
                        self.color = DARK_GREEN
                    elif event.key == pg.K_o:
                        self.color = NAVY
                    elif event.key == pg.K_t:
                        self.color = YELLOW
                    elif event.key == pg.K_p:
                        self.color = BLUE
                    elif event.key == pg.K_a:
                        self.color = LIGHT_BLUE
                    elif event.key == pg.K_s:
                        self.color = CYAN
                    elif event.key == pg.K_d:
                        self.color = LIGHT_PURPLE
                    elif event.key == pg.K_f:
                        self.color = PURPLE
                    elif event.key == pg.K_g:
                        self.color = MAGENTA
                    elif event.key == pg.K_h:
                        self.color = PINK
                    elif event.key == pg.K_j:
                        self.color = GREY
                    elif event.key == pg.K_k:
                        self.color = DARK_GREY
                    elif event.key == pg.K_l:
                        self.color = NOT_QUITE_BLACK


            # draws continuously while mouse is being held down, but stops when it gets too close to the menu
            if list(pg.mouse.get_pos())[1] <= 80 + (self.draw_size / 2):
                self.is_drawing = False
            if self.is_drawing:
                self.mouse_pos = list(pg.mouse.get_pos())
                self.mouse_x = self.mouse_pos[0]
                self.mouse_y = self.mouse_pos[1]
                pg.draw.rect(self.screen, self.color, (self.mouse_x - (self.draw_size // 2), self.mouse_y - (self.draw_size // 2), self.draw_size, self.draw_size))

    def update(self):
        # update all sprites
        self.all_sprites.update()

    def draw_text(self, surface, text, size, color, x, y): # makes drawing text easier
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.draw_text(self.screen, "CTRL +", 26, BLACK, 52, 18)
        # drawing the letters on top of the color samples
        self.draw_text(self.screen, "Q", 18, WHITE, 115, 24)
        self.draw_text(self.screen, "W", 18, WHITE, 165, 24)
        self.draw_text(self.screen, "E", 18, WHITE, 215, 24)
        self.draw_text(self.screen, "R", 18, WHITE, 265, 24)
        self.draw_text(self.screen, "T", 18, WHITE, 315, 24)
        self.draw_text(self.screen, "Y", 18, WHITE, 365, 24)
        self.draw_text(self.screen, "U", 18, WHITE, 415, 24)
        self.draw_text(self.screen, "I", 18, WHITE, 465, 24)
        self.draw_text(self.screen, "O", 18, WHITE, 515, 24)
        self.draw_text(self.screen, "P", 18, WHITE, 565, 24)
        self.draw_text(self.screen, "A", 18, WHITE, 615, 24)
        self.draw_text(self.screen, "S", 18, WHITE, 665, 24)
        self.draw_text(self.screen, "D", 18, WHITE, 715, 24)
        self.draw_text(self.screen, "F", 18, WHITE, 765, 24)
        self.draw_text(self.screen, "G", 18, WHITE, 815, 24)
        self.draw_text(self.screen, "H", 18, WHITE, 865, 24)
        self.draw_text(self.screen, "J", 18, WHITE, 915, 24)
        self.draw_text(self.screen, "K", 18, WHITE, 965, 24)
        self.draw_text(self.screen, "L", 18, WHITE, 1015, 24)

        self.draw_text(self.screen, "no. keys for sizes", 18, BLACK, 1090, 6)
        self.draw_text(self.screen, "d = draw", 18, BLACK, 1090, 24)
        self.draw_text(self.screen, "e = eraser", 18, BLACK, 1090, 42)

        self.all_sprites.draw(self.screen)

        pg.display.flip() # updates the screen


if __name__ == "__main__":
    # creating an instance or instantiating the Game class
    g = Game()
    g.new()
    g.run()