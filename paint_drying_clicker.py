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
        self.screen = pg.display.set_mode((CLICKER_W, CLICKER_H))
        pg.display.set_caption("Paint Drying Clicker")
        self.playing = True
        self.dryness = 0
        self.dryness_per_click = 1
        self.dryness_per_second = 0.0
        self.upgrades = { # 2D dictionary using key value pairs to store data about upgrades
            "candle" : {
                "name": "Candle",
                "cost": 500,
                "dpc": 2,
                "purchased": False
            },
            "blow dryer": {
                "name": "Blow Dryer",
                "cost": 2000,
                "dpc": 4,
                "purchased": False
            },
            "heat pack": {
                "name": "Heat Pack",
                "cost": 8500,
                "dpc": 10,
                "purchased": False
            },
            "torch": {
                "name": "Torch",
                "cost": 20000,
                "dpc": 25,
                "purchased": False
            },
            "clothes iron": {
                "name": "Clothes Iron",
                "cost": 50000,
                "dpc": 100,
                "purchased": False
            },
            "laser": {
                "name": "Laser",
                "cost": 200000,
                "dpc": 500,
                "purchased": False
            },
            "blanket": {
                "name": "Blanket",
                "cost": 5,
                "dps bonus": 0.02,
                "count": 0,
                "purchased": False
            },
            "light bulb": {
                "name": "Light Bulb",
                "cost": 20,
                "dps bonus": 0.1,
                "count": 0,
                "purchased": False
            },
            "fan": {
                "name": "Fan",
                "cost": 100,
                "dps bonus": 1,
                "count": 0,
                "purchased": False
            },
            "lantern": {
                "name": "Lantern",
                "cost": 1200,
                "dps bonus": 4,
                "count": 0,
                "purchased": False
            },
            "mini heater": {
                "name": "Mini Heater",
                "cost": 5000,
                "dps bonus": 20,
                "count": 0,
                "purchased": False
            },
            "portable heater": {
                "name": "Portable Heater",
                "cost": 25000,
                "dps bonus": 100,
                "count": 0,
                "purchased": False
            },
            "campfire": {
                "name": "Campfire",
                "cost": 80000,
                "dps bonus": 500,
                "count": 0,
                "purchased": False
            },
            "lava bucket": {
                "name": "Lava Bucket",
                "cost": 200000,
                "dps bonus": 2500,
                "count": 0,
                "purchased": False
            }
        }
    
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.clicker_painting_img = pg.image.load(path.join(self.img_folder, 'mona_lisa.png')).convert_alpha()
        self.clicker_painting_img = pg.transform.scale(self.clicker_painting_img, (288, 372))
        self.bg_img = pg.image.load(path.join(self.img_folder, 'paint_drying_clicker_bg.png')).convert()
        self.bg_img = pg.transform.scale(self.bg_img, (CLICKER_W, CLICKER_H))
        self.og_clicker_painting_img = self.clicker_painting_img.copy()
    
    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_floating_text = pg.sprite.Group()
        
        self.clicker_painting_rect = self.clicker_painting_img.get_rect()
        self.clicker_painting_rect.center = (CLICKER_W // 4, CLICKER_H // 2)
        
        self.scale_timer = 0
        self.is_scaling = False
        self.scale_duration = 100
    
    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        pg.quit()
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.clicker_painting_rect.collidepoint(mouse_pos):
                    self.click_painting()
                for key in self.upgrades.keys():
                    upgrade_rect = self.get_upgrade_rect(key)
                    if upgrade_rect.collidepoint(mouse_pos):
                        self.buy_upgrade(key)
    
    def click_painting(self):
        self.dryness += self.dryness_per_click

        self.is_scaling = True
        self.scale_timer = pg.time.get_ticks()
        
        FloatingText(self, f"+{self.dryness_per_click}", 30, YELLOW, self.clicker_painting_rect.centerx, self.clicker_painting_rect.top)

    def buy_upgrade(self, key):
        upgrade = self.upgrades[key]
        is_dps_upgrade = "dps bonus" in upgrade
        
        if self.dryness >= upgrade["cost"]:
            self.dryness -= upgrade["cost"]
            
            if is_dps_upgrade:
                self.dryness_per_second += upgrade["dps bonus"]
                upgrade["count"] += 1
                
                new_cost = upgrade["cost"] * (1 + 0.05 * upgrade["count"])
                upgrade["cost"] = round(new_cost)
                
            elif not upgrade["purchased"]:
                self.dryness_per_click = upgrade["dpc"]
                upgrade["purchased"] = True

        elif upgrade["purchased"]:
            print(f"{upgrade['name']} already purchased.")
        else:
            print(f"Not enough dryness! Need {upgrade['cost']}. Have {self.dryness}.")
    
    def update(self):
        self.all_sprites.update()
        self.dryness += self.dryness_per_second * self.dt
        if self.is_scaling:
            elapsed = pg.time.get_ticks() - self.scale_timer
            
            if elapsed < self.scale_duration:
                scale_factor = 1.1 
                new_width = int(self.og_clicker_painting_img.get_width() * scale_factor)
                new_height = int(self.og_clicker_painting_img.get_height() * scale_factor)
                self.clicker_painting_img = pg.transform.scale(self.og_clicker_painting_img, (new_width, new_height))
                
                center = self.clicker_painting_rect.center
                self.clicker_painting_rect = self.clicker_painting_img.get_rect()
                self.clicker_painting_rect.center = center
            else:
                self.clicker_painting_img = self.og_clicker_painting_img.copy()
                center = self.clicker_painting_rect.center
                self.clicker_painting_rect = self.clicker_painting_img.get_rect()
                self.clicker_painting_rect.center = center
                self.is_scaling = False
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
    
    def get_upgrade_rect(self, key):
        UPGRADE_W = 180
        UPGRADE_H = 80
        PADDING = 15
        MAX_PER_ROW = 2
        
        keys = list(self.upgrades.keys())
        index = keys.index(key)
        
        row = index // MAX_PER_ROW
        col = index % MAX_PER_ROW

        UPGRADE_START_X = CLICKER_W * 0.65
        UPGRADE_START_Y = CLICKER_H * 0.08

        X = UPGRADE_START_X + col * (UPGRADE_W + PADDING)
        Y = UPGRADE_START_Y + row * (UPGRADE_H + PADDING)
        
        return pg.Rect(X, Y, UPGRADE_W, UPGRADE_H)
    
    def draw_upgrade_area(self):
        for key, upgrade_data in self.upgrades.items():
            rect = self.get_upgrade_rect(key)
            is_dps_upgrade = "dps bonus" in upgrade_data
            color = GREY 
            text_color = WHITE
            if not upgrade_data["purchased"]:
                if self.dryness >= upgrade_data["cost"]:
                    color = GREEN
                elif not is_dps_upgrade and upgrade_data["purchased"]:
                    color = GREY
                else:
                    color = RED

            pg.draw.rect(self.screen, color, rect, border_radius=10)

            name_text = upgrade_data["name"]
            
            if is_dps_upgrade:
                name_text = f"{upgrade_data['name']} (x{upgrade_data['count']})"
                
            self.draw_text(self.screen, name_text, 24, text_color, rect.centerx, rect.top + 10)

            if is_dps_upgrade:
                effect_text = f"+{upgrade_data['dps bonus']} /s"
            else:
                dpc_value = upgrade_data.get("dpc", 0) 
                if upgrade_data["purchased"]:
                    effect_text = "PURCHASED"
                else:
                    effect_text = f"{dpc_value} DPC"
            
            self.draw_text(self.screen, effect_text, 18, text_color, rect.centerx, rect.top + 35)
            
            self.draw_text(self.screen, effect_text, 18, text_color, rect.centerx, rect.top + 35)

            if is_dps_upgrade or not upgrade_data["purchased"]:
                self.draw_text(self.screen, f"Cost: {upgrade_data['cost']}", 18, text_color, rect.centerx, rect.top + 55)
    
    def draw(self):
        self.screen.blit(self.bg_img, (0, 0))

        self.screen.blit(self.clicker_painting_img, self.clicker_painting_rect)
        
        dryness_text = f"Dryness: {int(self.dryness)} (DPC: {self.dryness_per_click} | DPS: {self.dryness_per_second:.2f})"
        self.draw_text(self.screen, dryness_text, 36, WHITE, (CLICKER_W // 2) - 20, 10)
        
        self.draw_upgrade_area()

        self.all_floating_text.draw(self.screen) 

        pg.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()