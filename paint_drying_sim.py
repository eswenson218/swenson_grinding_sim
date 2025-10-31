# Emmanuel Swenson

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
        self.game_duration = 60

        self.max_mobs = 10
        self.spawn_timer = 0
        self.spawn_delay = 650

        self.coin_spawn_timer = 0
        self.coin_spawn_delay = 3000
        self.coin_spawn_chance = 0.5
        self.max_coins = 2
        self.game_start_time = 0

    # sets up a game folder directory path using the current folder containing THIS file
    # give the Game class a map property which uses the Map class to parse the level1.txt file
    # loads image file from images folder
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.map = Map(path.join(self.game_folder, 'paint_drying_arena.txt'))
        self.player_img = pg.image.load(path.join(self.img_folder, 'Drill_Off.png')).convert_alpha()
        self.player_img_2 = pg.image.load(path.join(self.img_folder, 'Drill_On.png')).convert_alpha()

        self.pig_img = pg.image.load(path.join(self.img_folder, 'Pig_Not_Moving.png')).convert_alpha()
        self.cow_img = pg.image.load(path.join(self.img_folder, 'Cow_Not_Moving.png')).convert_alpha()
        self.chicken_img = pg.image.load(path.join(self.img_folder, 'Chicken_Not_Moving.png')).convert_alpha()

        self.pig_moving_img = pg.image.load(path.join(self.img_folder, 'Pig_Moving.png')).convert_alpha()
        self.cow_moving_img = pg.image.load(path.join(self.img_folder, 'Cow_Moving.png')).convert_alpha()
        self.chicken_moving_img = pg.image.load(path.join(self.img_folder, 'Chicken_Moving.png')).convert_alpha()
        self.sun_powerup_img = pg.image.load(path.join(self.img_folder, 'Sun_Powerup.png')).convert_alpha()

        self.painting_1_img = pg.image.load(path.join(self.img_folder, 'Painting_1.png')).convert_alpha()
        self.painting_2_img = pg.image.load(path.join(self.img_folder, 'Painting_2.png')).convert_alpha()
        self.painting_3_img = pg.image.load(path.join(self.img_folder, 'Painting_3.png')).convert_alpha()
        self.painting_4_img = pg.image.load(path.join(self.img_folder, 'Painting_4.png')).convert_alpha()
        self.painting_1_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_1_damaged.png')).convert_alpha()
        self.painting_2_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_2_damaged.png')).convert_alpha()
        self.painting_3_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_3_damaged.png')).convert_alpha()
        self.painting_4_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_4_damaged.png')).convert_alpha()
        self.painting_1_badly_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_1_badly_damaged.png')).convert_alpha()
        self.painting_2_badly_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_2_badly_damaged.png')).convert_alpha()
        self.painting_3_badly_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_3_badly_damaged.png')).convert_alpha()
        self.painting_4_badly_damaged_img = pg.image.load(path.join(self.img_folder, 'Painting_4_badly_damaged.png')).convert_alpha()

        self.background_img = pg.image.load(path.join(self.img_folder, 'paint_drying_sim_bg.png')).convert()
        self.background_img = pg.transform.scale(self.background_img, (WIDTH, HEIGHT))

    def new(self):
        # the sprite Groups allow us to update and draw sprites in grouped batches
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_targets = pg.sprite.Group()
        self.game_start_time = pg.time.get_ticks()
        
        self.spawn_points = []
        map_width = len(self.map.data[0])
        map_height = len(self.map.data)
        
        for x in range(map_width):
            self.spawn_points.append((x, 0))
            self.spawn_points.append((x, map_height - 1))
        
        for y in range(map_height):
            self.spawn_points.append((0, y))
            self.spawn_points.append((map_width - 1, y))

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
                elif tile == 'T':
                    Target_Object(self, col, row)

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
                self.playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_pos = pg.mouse.get_pos()
                # Check if any mob was clicked
                for mob in self.all_mobs:
                    if mob.rect.collidepoint(mouse_pos):
                        mob.kill()
                # Check if any coin (powerup) was clicked
                for coin in list(self.all_coins):
                    if coin.rect.collidepoint(mouse_pos):
                        # Activate powerup and remove it
                        coin.activate()

    def update(self):
        # update all sprites
        self.all_sprites.update()
        
        current_time = pg.time.get_ticks()
        elapsed_seconds = (current_time - self.game_start_time) // 1000
        self.time = max(0, self.game_duration - elapsed_seconds)
        
        if self.time <= 0:
            if len(self.all_targets.sprites()) > 0:
                self.draw_text(self.screen, "YOU WIN!", 100, GREEN, WIDTH // 2, (HEIGHT // 2) - 50)
                pg.display.flip()
                pg.time.wait(3000)
            self.playing = False
            return
        
        if (current_time - self.spawn_timer >= self.spawn_delay and len(self.all_mobs) < self.max_mobs):
            spawn_x, spawn_y = random.choice(self.spawn_points)
            Mob(self, spawn_x, spawn_y)
            self.spawn_timer = current_time

        if (current_time - self.coin_spawn_timer >= self.coin_spawn_delay and
            len(self.all_coins) < self.max_coins):
            rolled = random.random()
            if rolled < self.coin_spawn_chance:
                spawn_px = random.randint(0, WIDTH - TILESIZE[0])
                Coin(self, spawn_px, -TILESIZE[1], falling=True)
            self.coin_spawn_timer = current_time

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))

        self.draw_text(self.screen, f"Time Left: {str(self.time)}s", 24, WHITE, WIDTH // 2, 20)
        
        painting = self.all_targets.sprites()[0] if self.all_targets else None
        if painting:
            health_text = f"Painting Health: {painting.health}"
            health_color = RED if painting.health < 30 else (ORANGE if painting.health < 60 else GREEN)
            self.draw_text(self.screen, health_text, 32, health_color, WIDTH // 2, HEIGHT - 40)
        
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    # creating an instance or instantiating the Game class
    g = Game()
    g.new()
    g.run()