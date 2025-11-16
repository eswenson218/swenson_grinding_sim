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

'''
Sources:
Mr. Cozort's code (https://github.com/ccozort/cozort__tower_of_the_apprentice)
Clicking code from Aldric
Buttons - https://www.youtube.com/watch?v=8SzTzvrWaAA
'''

class Game:
    def __init__(self):
        pg.init() # initializing pygame
        self.clock = pg.time.Clock() # creating the game clock
        self.screen = pg.display.set_mode((CLICKER_W, CLICKER_H)) # screen dimentions
        pg.display.set_caption("Paint Drying Clicker")
        self.playing = True

        self.current_screen = "game" # what screen to be showed

        # these will not be reset
        self.ascension_count = 0
        self.ascension_cost = 10000

        self.permanent_upgrades = { # 2D dictionary using key value pairs to store data about permanent upgrades
            # key is upgrade name, value is the dictionary inside the dictionary
            # that key is the name of data for the upgrades, its value is the data
            "Thermotropism": { # gives you 1% of your dps every click on top of your dpc
                "cost": 1000000,
                "purchased": False
                },
            "Incandescence": { # doubles light bulb dps
                "cost": 250000,
                "purchased": False
                },
            "Autoclicker": { # clicks (starting at) every 5 seconds
                "cost": 500000,
                "cooldown": 5.0,
                "purchased": False
            },
            "Superfans": { # doubles fan dps
                "cost": 400000,
                "purchased": False
            },
            "Heavy Blankets": { # increases blanket dps from 0.1 to 0.5
                "cost": 200000,
                "purchased": False
            },
            "Fan Heaters": { # increases the dps of mini heaters and portable heaters by 1% for every 5 fans there are
                "cost": 1000000,
                "purchased": False
            },
            "Bonfire": { # doubles campfire dps
                "cost": 4000000,
                "purchased": False
            },
            "Lava Chicken": { # for every 2 lava buckets, autoclicker cooldown goes down by 0.5s until 0.5s, then it goes to 0.3s and then 0.1s
                "cost": 10000000,
                "purchased": False
            },
            "Warmer Lamps": { # dps multiplied by half on total light bulbs
                "cost": 10000000,
                "purchased": False
            },
            "Better Dryers": { # dps increased by 1% of itself
                "cost": 20000000,
                "purchased": False
            }
        }

        self.autoclick_timer = 0.0
        
        # these will be reset every ascension
        self.dryness = 0
        self.dryness_per_click = 1
        self.dryness_per_second = 0.0
        self.upgrades = { # 2D dictionary using key value pairs to store data about upgrades
            # key is upgrade name, value is the dictionary inside the dictionary
            # that key is the name of data for the upgrades, its value is the data
            "candle": { # increases dpc to 2
                "name": "Candle",
                "base cost": 500,
                "cost": 500,
                "dpc": 2,
                "purchased": False
            },
            "blow dryer": { # increases dpc to 4
                "name": "Blow Dryer",
                "base cost": 2500,
                "cost": 2500,
                "dpc": 4,
                "purchased": False
            },
            "heat pack": { # increases dpc to 10
                "name": "Heat Pack",
                "base cost": 10000,
                "cost": 10000,
                "dpc": 10,
                "purchased": False
            },
            "torch": { # increases dpc to 25
                "name": "Torch",
                "base cost": 25000,
                "cost": 25000,
                "dpc": 25,
                "purchased": False
            },
            "clothes iron": { # increases dpc to 100
                "name": "Clothes Iron",
                "base cost": 150000,
                "cost": 150000,
                "dpc": 100,
                "purchased": False
            },
            "laser": { # increases dpc to 500
                "name": "Laser",
                "base cost": 750000,
                "cost": 750000,
                "dpc": 500,
                "purchased": False
            },
            "blanket": { # adds 0.1 dps per blanket
                "name": "Blanket",
                "base cost": 5,
                "cost": 5,
                "dps bonus": 0.1,
                "count": 0,
                "purchased": False
            },
            "light bulb": { # adds 1 dps per light bulb
                "name": "Light Bulb",
                "base cost": 25,
                "cost": 25,
                "dps bonus": 1,
                "count": 0,
                "purchased": False
            },
            "fan": { # adds 5 dps per fan
                "name": "Fan",
                "base cost": 100,
                "cost": 100,
                "dps bonus": 5,
                "count": 0,
                "purchased": False
            },
            "heat lamp": { # adds 25 dps per lamp
                "name": "Heat Lamp",
                "base cost": 1200,
                "cost": 1200,
                "dps bonus": 25,
                "count": 0,
                "purchased": False
            },
            "mini heater": { # adds 75 dps per mheater
                "name": "Mini Heater",
                "base cost": 5000,
                "cost": 5000,
                "dps bonus": 75,
                "count": 0,
                "purchased": False
            },
            "portable heater": { # adds 500 dps per pheater
                "name": "Portable Heater",
                "base cost": 25000,
                "cost": 25000,
                "dps bonus": 500,
                "count": 0,
                "purchased": False
            },
            "campfire": { # adds 2,500 dps per campfire
                "name": "Campfire",
                "base cost": 80000,
                "cost": 80000,
                "dps bonus": 2500,
                "count": 0,
                "purchased": False
            },
            "lava bucket": { # adds 10,000 dps per bucket
                "name": "Lava Bucket",
                "base cost": 200000,
                "cost": 200000,
                "dps bonus": 10000,
                "count": 0,
                "purchased": False
            }
        }
    
    def load_data(self):
        # sets up a game folder directory path using the current folder containing THIS file
        # give the Game class a map property which uses the Map class to parse the level1.txt file
        # loads image file from images folder

        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')

        self.clicker_painting_img = pg.image.load(path.join(self.img_folder, 'mona_lisa.png')).convert_alpha()
        self.clicker_painting_img = pg.transform.scale(self.clicker_painting_img, (288, 372))

        self.bg_img = pg.image.load(path.join(self.img_folder, 'paint_drying_clicker_bg.png')).convert()
        self.bg_img = pg.transform.scale(self.bg_img, (CLICKER_W, CLICKER_H))

        self.upgrades_bg_img = pg.image.load(path.join(self.img_folder, 'paint_drying_clicker_upgrades_bg.png')).convert()
        self.upgrades_bg_img = pg.transform.scale(self.upgrades_bg_img, (CLICKER_W, CLICKER_H))

        self.og_clicker_painting_img = self.clicker_painting_img.copy()
    
    def new(self):
        # the sprite Groups allow us to update and draw sprites in grouped batches
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_floating_text = pg.sprite.Group()
        
        # placing painting
        self.clicker_painting_rect = self.clicker_painting_img.get_rect()
        self.clicker_painting_rect.center = (CLICKER_W // 4, CLICKER_H // 2)
        
        self.scale_timer = 0
        self.is_scaling = False # whether or not the painting is expanded (for click effect)
        self.scale_duration = 60 # how long the painting is expanded (ms)
    
    def run(self):
        while self.playing:
            # game clock
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
            if event.type == pg.QUIT: # closing the game loop
                self.playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos() # gets location of mouse when clicked
                if self.current_screen == "game":
                    if self.clicker_painting_rect.collidepoint(mouse_pos): # if painting is clicked
                        self.click_painting()

                    # prestige button logic
                    ascension_rect = self.get_ascension_rect()
                    if ascension_rect.collidepoint(mouse_pos):
                        self.buy_ascension()

                    # permanent upgrades button logic
                    upgrade_upgrades_rect = self.get_upgrade_upgrades_rect()
                    if upgrade_upgrades_rect.collidepoint(mouse_pos):
                        self.current_screen = "upgrade upgrades"
                    for key in self.upgrades.keys():
                        upgrade_rect = self.get_upgrade_rect(key)
                        if upgrade_rect.collidepoint(mouse_pos):
                            self.buy_upgrade(key)

                # for the permanent upgrades screen
                elif self.current_screen == "upgrade upgrades":
                    back_rect = self.get_back_button_rect()
                    if back_rect.collidepoint(mouse_pos):
                        self.current_screen = "game"

                    # displays only the permanent upgrades unlocked based on prestige (2 more per level)
                    keys = list(self.permanent_upgrades.keys())
                    if self.ascension_count >= 1:
                        for i, key in enumerate(keys):
                            perm_rect = self.get_permanent_upgrade_rect(i)
                            if perm_rect.collidepoint(mouse_pos):
                                self.buy_permanent_upgrade(key)
    
    def click_painting(self): # logic for giving dryness when the painting is clicked
        dps_bonus = 0
        if self.permanent_upgrades["Thermotropism"]["purchased"]: # 1% of dps added to each click
            dps_bonus = self.dryness_per_second * 0.01

        self.dryness += self.dryness_per_click + dps_bonus

        # expanding the painting when clicked
        self.is_scaling = True
        self.scale_timer = pg.time.get_ticks()
        
        # adding dryness numbers when painting is clicked
        FloatingText(self, f"+{self.dryness_per_click + dps_bonus:,.2f}", 30, YELLOW, self.clicker_painting_rect.centerx, self.clicker_painting_rect.top)

    def buy_upgrade(self, key):
        upgrade = self.upgrades[key]
        is_dps_upgrade = "dps bonus" in upgrade
        
        if self.dryness >= upgrade["cost"]:
            self.dryness -= upgrade["cost"]
            
            if is_dps_upgrade: # if dps upgrade, count goes up b/c you can buy multiple
                upgrade["count"] += 1
                
                # increases cost by 5% of previous to the nearest whole number
                new_cost = upgrade["cost"] * (1 + 0.05 * upgrade["count"])
                upgrade["cost"] = round(new_cost)
                
            elif not upgrade["purchased"]: # for dpc upgrades, buyable only once
                self.dryness_per_click = upgrade["dpc"]
                upgrade["purchased"] = True
    
    def get_ascension_rect(self): # getting button placement for prestige button
        BUTTON_W = 180
        BUTTON_H = 50
        X = CLICKER_W // 2 - BUTTON_W // 2
        Y = CLICKER_H * 0.85
        return pg.Rect(X, Y, BUTTON_W, BUTTON_H)
    
    def get_upgrade_upgrades_rect(self): # permanent upgrades button placement
        BUTTON_W = 200
        BUTTON_H = 50
        X = CLICKER_W // 2 - BUTTON_W // 2
        Y = CLICKER_H * 0.85 - 60
        return pg.Rect(X, Y, BUTTON_W, BUTTON_H)
    
    def get_back_button_rect(self): # back button for permanent upgrades screen to bring back to main screen (game)
        BUTTON_W = 100
        BUTTON_H = 40
        X = CLICKER_W - BUTTON_W - 20
        Y = CLICKER_H - BUTTON_H - 20
        return pg.Rect(X, Y, BUTTON_W, BUTTON_H)

    def get_permanent_upgrade_rect(self, index): # for every permanent upgrade button (columns of 4)
        UPGRADE_W = 300
        UPGRADE_H = 100
        PADDING_X = 75
        PADDING_Y = 20
        COL_H = 4

        row = index % COL_H
        col = index // COL_H

        X = 50 + col * (UPGRADE_W + PADDING_X)
        Y = 150 + row * (UPGRADE_H + PADDING_Y)
        return pg.Rect(X, Y, UPGRADE_W, UPGRADE_H)

    def reset_game(self): # after ascending, resets everything except for the permanent upgrades
        self.dryness = 0
        self.dryness_per_click = 1
        self.dryness_per_second = 0.0
        self.autoclick_timer = 0.0
        for upgrade in self.upgrades.values():
            upgrade["purchased"] = False
            upgrade["cost"] = upgrade["base cost"]
            if "count" in upgrade:
                upgrade["count"] = 0
    
    def buy_ascension(self):
        if self.dryness >= self.ascension_cost:
            self.ascension_count += 1
            self.ascension_cost *= 10
            self.current_screen = "game"
            self.reset_game()
    
    def buy_permanent_upgrade(self, key):
        upgrade = self.permanent_upgrades[key]
        if self.ascension_count >= 1 and not upgrade["purchased"]:
            if self.dryness >= upgrade["cost"]:
                self.dryness -= upgrade["cost"]
                upgrade["purchased"] = True
        
    def update(self):
        self.all_sprites.update() # updating all sprites

        base_dps = 0 # initial dps before any upgrades

        light_bulb_dps = 0
        
        # multipliers for permanent upgrades
        fan_multiplier = 1.0
        blanket_dps_mod = 1.0
        heater_fan_bonus_multiplier = 1.0 
        campfire_multiplier = 1.0
        heat_lamp_multiplier = 1.0

        if self.permanent_upgrades["Superfans"]["purchased"]: # fan dps increased to 10
            fan_multiplier = 2.0
            
        if self.permanent_upgrades["Heavy Blankets"]["purchased"]: # blanket dps increased to 0.5
            blanket_dps_mod = 5.0 
        
        if self.permanent_upgrades["Warmer Lamps"]["purchased"]: # lamp  dps multiplied by half of the no. of light bulbs
            light_bulb_count = self.upgrades["fan"].get("count", 0)
            if light_bulb_count >= 4:
                heat_lamp_multiplier = light_bulb_count // 2

        fan_count = self.upgrades["fan"].get("count", 0)
        if self.permanent_upgrades["Fan Heaters"]["purchased"]: # increases heater dps by 1% for every 5 fans
            heater_fan_bonus_multiplier += (fan_count // 5) * 0.01
        
        if self.permanent_upgrades["Bonfire"]["purchased"]: # campfire dps increased to 5,000
            campfire_multiplier = 2.0

        for upgrade in self.upgrades.values(): # adding the normal upgrade dpss
            if "dps bonus" in upgrade:
                count = upgrade.get("count", 0) # dps multiplied by count
                bonus = upgrade["dps bonus"] # how much is added to the base dps (0)
                
                dps_contribution = bonus * count
                
                if upgrade["name"] == "Light Bulb":
                    light_bulb_dps += dps_contribution
                elif upgrade["name"] == "Fan": 
                    base_dps += dps_contribution * fan_multiplier
                elif upgrade["name"] == "Blanket":
                    base_dps += dps_contribution * blanket_dps_mod
                elif upgrade["name"] == "Heat Lamp":
                    base_dps += dps_contribution * heat_lamp_multiplier
                elif upgrade["name"] == "Mini Heater" or upgrade["name"] == "Portable Heater":
                    base_dps += dps_contribution * heater_fan_bonus_multiplier
                elif upgrade["name"] == "Bonfire":
                    base_dps += dps_contribution * campfire_multiplier
                else:
                    base_dps += dps_contribution

        if self.permanent_upgrades["Incandescence"]["purchased"]: # light bulb dps increased to 2
            light_bulb_dps *= 2 
            
        total_dps = base_dps + light_bulb_dps
        if self.permanent_upgrades["Better Dryers"]["purchased"]: # increases dps by 1% of itself
            total_dps *= 1.01
        self.dryness_per_second = total_dps

        # adding total dps to the total dryness
        self.dryness += total_dps * self.dt
        
        # autoclicker logic
        if self.permanent_upgrades["Autoclicker"]["purchased"]:
            autoclick_data = self.permanent_upgrades["Autoclicker"]
            cooldown = autoclick_data["cooldown"] # how long between clicks
            # logic for cooldown reduction (-0.5s per 2 lava buckets, capped at -4.9s)
            lbucket_count = self.upgrades["lava bucket"].get("count", 0)
            if self.permanent_upgrades["Lava Chicken"]["purchased"]:
                if lbucket_count <= 19:
                    cooldown -= 0.5 * (lbucket_count // 2)
                elif lbucket_count > 19 and lbucket_count < 22: # special case for -0.2s
                    cooldown = 0.3
                elif lbucket_count >= 22: # special case for -0.2s
                    cooldown = 0.1
            self.autoclick_timer += self.dt
            
            if self.autoclick_timer >= cooldown:
                if self.permanent_upgrades["Thermotropism"]["purchased"]: # thermotropism applies to autoclicker
                    click_value = self.dryness_per_click + (self.dryness_per_second * 0.01)
                    self.dryness += click_value
                else: # thermotropism not purchased yet
                    click_value = self.dryness_per_click
                    self.dryness += click_value
                self.autoclick_timer = 0.0
                
                # autoclicker text for how much gained per autoclick
                FloatingText(self, f"Autoclick +{click_value:,.2f}", 30, CYAN, 
                             self.clicker_painting_rect.centerx + random.randint(-50, 50), 
                             self.clicker_painting_rect.centery + random.randint(-50, 50))
                
        if self.is_scaling:
            elapsed = pg.time.get_ticks() - self.scale_timer
            
            if elapsed < self.scale_duration: # expanding the image for 0.6s
                scale_factor = 1.1 
                new_width = int(self.og_clicker_painting_img.get_width() * scale_factor)
                new_height = int(self.og_clicker_painting_img.get_height() * scale_factor)
                self.clicker_painting_img = pg.transform.scale(self.og_clicker_painting_img, (new_width, new_height))
                
                center = self.clicker_painting_rect.center
                self.clicker_painting_rect = self.clicker_painting_img.get_rect()
                self.clicker_painting_rect.center = center
            else: # bringing the painting back to og size
                self.clicker_painting_img = self.og_clicker_painting_img.copy()
                center = self.clicker_painting_rect.center
                self.clicker_painting_rect = self.clicker_painting_img.get_rect()
                self.clicker_painting_rect.center = center
                self.is_scaling = False
    
    def draw_text(self, surface, text, size, color, x, y): # to make drawing text easier
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
    
    def get_upgrade_rect(self, key): # placement for all upgrade buttons (2 per row)
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
    
    def draw_upgrade_area(self): # drawing upgrade buttons
        for key, upgrade_data in self.upgrades.items():
            rect = self.get_upgrade_rect(key)
            is_dps_upgrade = "dps bonus" in upgrade_data
            color = GREY
            if not upgrade_data["purchased"]:
                # visual indicator for if buyable
                if self.dryness >= upgrade_data["cost"]: # can afford to buy the upgrade
                    color = GREEN
                elif not is_dps_upgrade and upgrade_data["purchased"]: # already bought and can't buy more
                    color = GREY
                else: # to expensive
                    color = RED

            pg.draw.rect(self.screen, color, rect, border_radius = 10)

            name_text = upgrade_data["name"] # name of the upgrade
            
            if is_dps_upgrade: # how many bought already
                name_text = f"{upgrade_data['name']} (x{upgrade_data['count']})"
                
            self.draw_text(self.screen, name_text, 24, WHITE, rect.centerx, rect.top + 10)

            if is_dps_upgrade: # how much dps does one add
                effect_text = f"+{upgrade_data['dps bonus']:,} /s" # adding ':,' adds commas every 3 digits to make the no. more easy to read
            else: # if dpc upgrade, updates description update to 'purchased' upon purchase
                dpc_value = upgrade_data.get("dpc", 0)
                if upgrade_data["purchased"]:
                    effect_text = "PURCHASED"
                else:
                    effect_text = f"{dpc_value} DPC"
            
            # placing info on the buttons
            self.draw_text(self.screen, effect_text, 18, WHITE, rect.centerx, rect.top + 35)
            self.draw_text(self.screen, effect_text, 18, WHITE, rect.centerx, rect.top + 35)

            if is_dps_upgrade or not upgrade_data["purchased"]: # cost display
                self.draw_text(self.screen, f"Cost: {upgrade_data['cost']:,}", 18, WHITE, rect.centerx, rect.top + 55)

    def draw_ascension_button(self):
        rect = self.get_ascension_rect()
        can_ascend = self.dryness >= self.ascension_cost
        color = GREEN if can_ascend else DARK_GREY # color updates based on whether or not you can afford
        pg.draw.rect(self.screen, color, rect, border_radius=5)
        
        text = f"Ascend ({self.ascension_count})"
        cost_text = f"Cost: {self.ascension_cost:,}" 
        
        self.draw_text(self.screen, text, 20, WHITE, rect.centerx, rect.top + 5)
        self.draw_text(self.screen, cost_text, 16, YELLOW, rect.centerx, rect.top + 25)
        
    def draw_permanent_upgrades(self):
        keys = list(self.permanent_upgrades.keys())
        
        # how many upgradees are shown (2x the ascension level)
        upgrades_to_show = self.ascension_count * 2
        keys = keys[:upgrades_to_show]

        for i, key in enumerate(keys): # drawing all the permanent upgrades
            upgrade_data = self.permanent_upgrades[key]
            rect = self.get_permanent_upgrade_rect(i)
            can_afford = self.dryness >= upgrade_data.get("cost", 0)
            
            if upgrade_data["purchased"]:
                color = GREY 
                text_status = "PURCHASED"
            elif self.ascension_count == 0:
                color = DARK_GREY 
                text_status = "Ascend once to Buy"
            elif can_afford: 
                color = GREEN
                text_status = f"Cost: {upgrade_data['cost']:,}" 
            else:
                color = RED
                text_status = f"Cost: {upgrade_data['cost']:,}" 
            
            pg.draw.rect(self.screen, color, rect, border_radius=5)

            self.draw_text(self.screen, key, 24, WHITE, rect.centerx, rect.top + 10)
            
            # descriptions b/c more complicated upgrades
            upgrade_description = ""
            if key == "Thermotropism":
                upgrade_description = "Clicking also adds 1% of your DPS"
            elif key == "Incandescence":
                upgrade_description = "Light bulb's dps x2"
            elif key == "Autoclicker":
                upgrade_description = f"Autoclicks every 5 seconds"
            elif key == "Superfans":
                upgrade_description = "Fan's dps x2"
            elif key == "Heavy Blankets":
                upgrade_description = "Blanket's dps x5"
            elif key == "Fan Heaters":
                upgrade_description = "Heaters' dps increases by 1% every 5 fans"
            elif key == "Bonfire":
                upgrade_description = "Campfire's dps x2"
            elif key == "Lava Chicken":
                upgrade_description = "-0.5 Autoclicker cooldown every 2 lava buckets"
            elif key == "Warmer Lamps":
                upgrade_description = "Heat Lamp's dps x half the no. of light bulbs"
            elif key == "Better Dryers":
                upgrade_description = "1% of DPS added to itself"
            
            self.draw_text(self.screen,  upgrade_description, 16, WHITE, rect.centerx, rect.top + 40)
            self.draw_text(self.screen, text_status, 18, YELLOW, rect.centerx, rect.top + 70)

    def draw_upgrade_upgrades_screen(self): # creates the permanent upgrades screen
        self.screen.blit(self.upgrades_bg_img, (0, 0))

        self.draw_text(self.screen, "Upgrade Upgrades", 48, WHITE, CLICKER_W // 2, 50)
        
        rect = self.get_back_button_rect()
        pg.draw.rect(self.screen, RED, rect, border_radius=5)
        self.draw_text(self.screen, "Back", 24, WHITE, rect.centerx, rect.centery - 15)
        
        if self.ascension_count == 0: # doesn't draw any upgrades in prestige is 0
            self.draw_text(self.screen, "Nothing to see here. Try ascending for upgrades to your upgrades.", 30, WHITE, CLICKER_W // 2, CLICKER_H // 2)
        else: # draws upgrades with prestige >= 1
            self.draw_permanent_upgrades()
    
    def draw(self): # creating the main game screen
        if self.current_screen == "game":
            self.screen.blit(self.bg_img, (0, 0))
            self.screen.blit(self.clicker_painting_img, self.clicker_painting_rect)
            
            # dryness amount label (dpc label | dps label)
            dryness_text = f"Dryness: {int(self.dryness):,} (DPC: {self.dryness_per_click:,} | DPS: {self.dryness_per_second:,.2f})" # :.2f limits to 2 decimal points
            self.draw_text(self.screen, dryness_text, 36, WHITE, CLICKER_W // 2, 20)
            
            self.draw_upgrade_area()
            self.draw_ascension_button()

            rect = self.get_upgrade_upgrades_rect()
            pg.draw.rect(self.screen, BLUE, rect, border_radius=5)
            self.draw_text(self.screen, "Upgrade Upgrades", 24, WHITE, rect.centerx, rect.centery - 15)
            
            # drawing the dpc numbers
            self.all_floating_text.draw(self.screen) 
        
        # drawing permanent upgrades screen
        elif self.current_screen == "upgrade upgrades":
            self.draw_upgrade_upgrades_screen()

        pg.display.flip()

# running the game
if __name__ == "__main__":
    # creating an instance or instanciating the game class
    g = Game()
    g.new()
    g.run()