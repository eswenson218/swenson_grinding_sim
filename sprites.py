# Created by Emmanuel Swenson

# The sprites module contains all the sprites
# Sprites include: player, mob - moving object

# Sources
'''
Mr. Cozort's code (https://github.com/ccozort/cozort__tower_of_the_apprentice)
scaling and rotating images in pygame - https://www.youtube.com/watch?v=Xzmpl5tnJnc
'''

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *  # contains Cooldown and other useful tools
import random
import math
from os import path

vec = pg.math.Vector2

pg.mixer.init()
game_folder = path.dirname(__file__)
sound_folder = path.join(game_folder, 'sounds')
painting_dmg = pg.mixer.Sound(path.join(sound_folder, 'wood break.mp3'))
painting_dmg.set_volume(0.1)

# makes Player a sprite
class Player(Sprite): # Sprite is a superclasss inherited by the Player class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_folder, "Drill_On.png"))
        self.image = self.game.player_img
        self.load_images()
        self.image = pg.Surface((64, 64))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # player uses position and velocity vectors for smooth movement
        self.pos = vec(x, y) * TILESIZE[0]
        self.vel = vec(0, 0)
        self.speed = PLAYER_SPEED
        self.health = HEALTH
        self.coins = 0
        self.cd = Cooldown(1000)
        self.direction = 'up'
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.current_frame = 0

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 64, 64),
            self.spritesheet.get_image(0, 0, 64, 64),
            self.spritesheet.get_image(0, 0, 64, 64),
            self.spritesheet.get_image(0, 0, 64, 64),
            self.spritesheet.get_image(64, 0, 64, 64),
            self.spritesheet.get_image(64, 0, 64, 64),
            self.spritesheet.get_image(64, 0, 64, 64),
            self.spritesheet.get_image(64, 0, 64, 64),
            self.spritesheet.get_image(0, 64, 64, 64),
            self.spritesheet.get_image(0, 64, 64, 64),
            self.spritesheet.get_image(0, 64, 64, 64),
            self.spritesheet.get_image(0, 64, 64, 64),
            self.spritesheet.get_image(64, 64, 64, 64),
            self.spritesheet.get_image(64, 64, 64, 64),
            self.spritesheet.get_image(64, 64, 64, 64),
            self.spritesheet.get_image(64, 64, 64, 64)]
        
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        # self.walk_frames_r # telling what animation to cycle through based on which way its facing
        # self.walk_frames_l
        # pg.transform.flip # how to flip an image

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update >= 0:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vel.y = -self.speed
            self.direction = 'up'
        if keys[pg.K_a]:
            self.vel.x = -self.speed
            self.direction = 'left'
        if keys[pg.K_s]:
            self.vel.y = self.speed
            self.direction = 'down'
        if keys[pg.K_d]:
            self.vel.x = self.speed
            self.direction = 'right'
        if keys[pg.K_SPACE]:
            self.spritesheet = Spritesheet(path.join(self.game.img_folder, "Drill_On.png"))
        elif not keys[pg.K_SPACE]:
            self.image = self.game.player_img


        # accounting for diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    # detects wall collisions along each axis
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    if hits[0].state == "moveable":
                        hits[0].pos.x += self.vel.x
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                        
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    # handles collisions with mobs or coins
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1

    def update(self):
        # gets input and applies velocity to position
        self.get_keys()
        self.animate()
        self.pos += self.vel

        # update rect for collision handling
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        # check collisions with mobs and coins
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coins, True)

# makes Mob a sprite
class Mob(Sprite):
    def __init__(self, game, x, y, type = "animal"):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.type = type
        self.game = game
        mob_type = random.randint(1,3)
        
        # Animation setup
        self.last_update = 0
        self.frame_rate = 100  # Time between frame updates in milliseconds
        
        if mob_type == 1:
            self.static_image = game.pig_img
            raw_spritesheet_img = game.pig_moving_img
            self.animal_type = "pig"
            self.damage = 15
            self.frame_width = 64
            self.frame_height = 64
        elif mob_type == 2:
            self.static_image = game.chicken_img
            raw_spritesheet_img = game.chicken_moving_img
            self.animal_type = "chicken"
            self.damage = 5
            self.frame_width = 32
            self.frame_height = 32
        else:
            self.static_image = game.cow_img
            raw_spritesheet_img = game.cow_moving_img
            self.animal_type = "cow"
            self.damage = 25
            self.frame_width = 96
            self.frame_height = 96
            
        self.animation_frames = []
        spritesheet_width = raw_spritesheet_img.get_width()
        spritesheet_height = raw_spritesheet_img.get_height()
        
        self.frames_x = spritesheet_width // self.frame_width
        self.frames_y = spritesheet_height // self.frame_height
        
        for row in range(self.frames_y):
            for col in range(self.frames_x):
                source_x = col * self.frame_width
                source_y = row * self.frame_height
                frame_surface = pg.Surface((self.frame_width, self.frame_height), pg.SRCALPHA)
                frame_surface.blit(raw_spritesheet_img, (0, 0), 
                                (source_x, source_y, self.frame_width, self.frame_height))
                self.animation_frames.append(frame_surface)
        
        self.current_frame = 0
        self.image = self.animation_frames[0]
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.speed = MOB_SPEED
        self.speedchangex = False
        self.speedchangey = False
        self.startspeed = 1
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x *= random.choice([-1,1])
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                self.vel.y *= random.choice([-1,1])
 
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.original_image = self.animation_frames[self.current_frame]

    def update(self):
        # mob behavior
        if self.type == "chase":
            if self.game.player.pos.x > self.pos.x:
                self.vel.x = 1
            else:
                self.vel.x = -1
            if self.game.player.pos.y > self.pos.y:
                self.vel.y = 1
            else:
                self.vel.y = -1
        elif self.type == "animal":
            target = self.game.all_targets.sprites()[0] if self.game.all_targets else None
            if target:
                direction = vec(target.rect.centerx - self.rect.centerx, 
                             target.rect.centery - self.rect.centery)
                if direction.length() > 0:
                    self.animate()
                    
                    angle = math.degrees(math.atan2(-direction.y, direction.x))
                    self.image = pg.transform.rotate(self.original_image, angle - 90)
                    old_center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
                    self.vel = direction.normalize()
        
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

# makes Coin a sprite
class Coin(Sprite):
    def __init__(self, game, x, y, falling=False):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = game.sun_powerup_img
        self.rect = self.image.get_rect()
        self.falling = falling
        if not falling:
            self.rect.x = x * TILESIZE[0]
            self.rect.y = y * TILESIZE[1]
            self.vel = vec(0, 0)
        else:
            self.rect.x = int(x)
            self.rect.y = int(y)
            self.vel = vec(0, 150)
            self.pos = vec(self.rect.x, self.rect.y)

    def activate(self):
        self.game.time = max(0, self.game.time - 5)
        painting = self.game.all_targets.sprites()[0] if self.game.all_targets else None
        if painting:
            max_hp = getattr(painting, 'max_health', 100)
            painting.health = min(max_hp, painting.health + 5)
        self.kill()

    def update(self):
        if self.falling:
            dt = self.game.dt if hasattr(self.game, 'dt') else (1 / 60)
            self.pos += self.vel * dt
            self.rect.x = int(self.pos.x)
            self.rect.y = int(self.pos.y)
            if self.rect.top > HEIGHT:
                self.kill()
        else:
            pass


# makes Wall a sprite
class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    if hits[0].state == "moveable":
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width      
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.right
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:              
                if self.vel.y > 0:
                    if hits[0].state == "moveable":
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                        
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    def update(self):
        # wall
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Projectile(Sprite):
    def __init__(self, game, x, y, dir):
        self.game = game
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = dir
        self.pos = vec(x,y)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            self.kill()

class Target_Object(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_targets
        Sprite.__init__(self, self.groups)
        self.health = 100
        painting_num = random.randint(1, 4)
        self.painting_type = painting_num
        self.image = getattr(game, f'painting_{painting_num}_img')
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE[0]
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.current_state = 'normal'

    def update_painting_state(self):
        new_state = 'normal'
        if self.health <= 25:
            new_state = 'badly_damaged'
        elif self.health <= 50:
            new_state = 'damaged'

        if new_state != self.current_state:
            self.current_state = new_state
            image_suffix = '' if new_state == 'normal' else f'_{new_state}'
            self.image = getattr(self.game, f'painting_{self.painting_type}{image_suffix}_img')
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if hits:
            painting_dmg.play()
            mob = hits[0]
            self.health -= mob.damage
            if self.health <= 0:
                self.game.playing = False
                self.kill()
            else:
                self.update_painting_state()

class FloatingText(Sprite):
    def __init__(self, game, text, size, color, x, y):
        self._layer = 10
        Sprite.__init__(self, game.all_sprites, game.all_floating_text)
        self.game = game
        self.font = pg.font.match_font('Arial')
        self.size = size
        self.color = color
        
        self.image = self.render_text(text)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - 50)
        
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, -40)
        self.lifetime = 2000
        self.spawn_time = pg.time.get_ticks()

    def render_text(self, text):
        font = pg.font.Font(self.font, self.size)
        return font.render(text, True, self.color)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()