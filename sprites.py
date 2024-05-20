#This file was created by: Dexter Kunimura
#This code was inspired Zelda and informed by Chris Bradfield
#from (this place) import (everything)
from settings import *
import pygame as pg
from healthbar import *
from os import path
from random import choice
# from random import choice

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
SWING_DURATION_IN_MS = 500
SPRITESHEET = "theBell.png"



vec =pg.math.Vector2

dir = path.dirname(__file__)
img_dir = path.join(dir, 'images')

def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

#making the player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 100
        self.weapon_drawn = False
        self.weapon_type = ""
        self.weapon = None
        self.swinging = False
        self.weapon_offset_x = 20 
        self.weapon_offset_y = 0
        self.dir = vec(1, 0)
        self.status = ""

        def set_status(self, status):
            self.status = status
            if self.weapon:
                self.weapon.update_image()

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            self.dir = vec(-1, 0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.dir = vec(1, 0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
            self.dir = vec(0, -1)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.dir = vec(0, 1)
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

        if keys[pg.K_q]:
            if not self.weapon_drawn:
                self.weapon_drawn = True
                self.weapon = Weapon(self.game, self.weapon_type, self.rect.x + self.weapon_offset_x, self.rect.y + self.weapon_offset_y, 16, 16, self.dir)

        if keys[pg.K_e]:
            if not self.swinging and self.weapon_drawn and self.weapon:
                self.swinging = True
                self.weapon.swing()
        
        if self.weapon:
            self.weapon.dir = self.dir

    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            self.weapon = Weapon(self.game, self.weapon_type, self.rect.x + self.weapon_offset_x, self.rect.y + self.weapon_offset_y, 16, 16, self.dir)
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1

            if str(hits[0].__class__.__name__) == "swordfusion":
                fusion = choice(SWORD_FUSIONS)
                if fusion == "Bloodthirsty":
                    self.status = "Bloodthirsty"
                    print("Bloodthirsty")
                if fusion == "Mighty":
                    self.status = "Mighty"
                    print("Mighty")
                if fusion == "Vorpal":
                    self.status = "Vorpal"
                    print("Vorpal")
                if fusion == "Toxic":
                    self.status = "Toxic"
                    print("Toxic")
                if fusion == "Burning":
                    self.status = "Burning"
                    print("Burning")
                if fusion == "Chilled":
                    self.status = "Chilled"
                    print("Chilled")


            if str(hits[0].__class__.__name__) == "slap_juice":
                print(hits[0].__class__.__name__)
                self.speed += 150
                self.hitpoints += 50
                self.image = self.game.player_img
                self.rect = self.image.get_rect()

            if str(hits[0].__class__.__name__) == "trap":
                print(hits[0].__class__.__name__)
                self.speed -= 150
                self.hitpoints -= 50
                self.image = self.game.trapped_img
                self.rect = self.image.get_rect()

            if str(hits[0].__class__.__name__) == "chug_jug":
                self.image = pg.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
                self.rect = self.image.get_rect()
                self.hitpoints = 200

            if str(hits[0].__class__.__name__) == "mob":
                self.hitpoints -= 40

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coin, True)
        self.collide_with_group(self.game.slap_juice, True)
        self.collide_with_group(self.game.chug_jug, True)
        self.collide_with_group(self.game.trap, True)
        self.collide_with_group(self.game.mob, True)
        self.collide_with_group(self.game.swordfusion, True)
        self.collide_with_group(self.game.Level2hallway, True)

        if self.weapon:
            if self.weapon_drawn:
                self.weapon.update()
            # Check for collision with mobs when swinging the weapon
            if self.swinging:
                self.weapon.collide_with_mobs()

        if self.swinging and self.weapon:
            if self.weapon.swinging_animation_finished():
                self.weapon.return_to_original_position()
                self.swinging = False



#designing the size and looks of the wall        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.image = game.wall_img
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#designing the size and looks of the coin class
class coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coin
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#designing the size and looks of the power up class
class slap_juice(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.slap_juice
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.slap_juice_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#designing the size and looks of the mushroom class
class chug_jug(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.chug_jug
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.chug_jug_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#designing the size and looks of the trap
class trap(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.trap
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.trap_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Weapon(pg.sprite.Sprite):
    def __init__(self, game, typ, x, y, w, h, dir):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.image = game.basic_sword_img
        self.update_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.pos = vec(x, y)
        self.dir = dir  # Store the direction of the player
        self.typ = typ
        self.original_image = self.image.copy()
        self.original_pos = vec(x, y)
        self.angle = 0  # Angle for swinging animation
        self.swinging = False
        self.swing_start_time = 0

    def update_image(self):
        if self.game.player.status == "Bloodthirsty":
            self.image = self.game.bloodthirsty_saw_img
            # self.rect = self.image.get_rect()
            
        elif self.game.player.status == "Mighty":
            self.image = self.game.mighty_axe_img
            # self.rect = self.image.get_rect()

        elif self.game.player.status == "Toxic":
            self.image = self.game.toxic_blade_img
            # self.rect = self.image.get_rect()

        elif self.game.player.status == "Vorpal":
            self.image = self.game.vorpal_blade_img
            # self.rect = self.image.get_rect()
        else:
            self.image = self.game.basic_sword_img
        self.original_image = self.image.copy()


    def swing(self):
        self.swinging = True
        self.swing_start_time = pg.time.get_ticks()  # Store the start time of the swing animation
        self.angle = 0

    def swinging_animation_finished(self):
        if pg.time.get_ticks() - self.swing_start_time > SWING_DURATION_IN_MS:
            self.swinging = False
            return True
        return False
    
    def return_to_original_position(self):
        self.angle = 0
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.original_pos
    
    def update(self):
        self.update_image()
        if self.swinging:
            self.rotate_weapon()
            elapsed_time = pg.time.get_ticks() - self.swing_start_time
            if elapsed_time > SWING_DURATION_IN_MS:
                self.swinging = False
                self.return_to_original_position()
                self.collide_with_mobs()
          
        else:
            # Adjust the position of the weapon based on the direction of the player
            if self.dir.x == 1:  # Player moved right
                self.rect.topleft = self.game.player.rect.topright
            elif self.dir.x == -1:  # Player moved left
                self.rect.topright = self.game.player.rect.topleft
            elif self.dir.y == 1:  # Player moved down
                self.rect.topright = self.game.player.rect.bottomright
            elif self.dir.y == -1:  # Player moved up
                self.rect.bottomleft = self.game.player.rect.topleft
        
            if self.dir.y == -1:  # Player moved up
                self.image = pg.transform.rotate(self.original_image, 90)
            elif self.dir.x == -1:  # Player moved left
                self.image = pg.transform.rotate(self.original_image, 180)
            elif self.dir.y == 1:  # Player moved down
                self.image = pg.transform.rotate(self.original_image, 270)
            elif self.dir.x == 1:  # Player moved up
                self.image = self.original_image.copy()

    def rotate_weapon(self):
        old_center = self.rect.center
        self.angle += 10
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def collide_with_mobs(self):
        hits = pg.sprite.spritecollide(self, self.game.mob, False)
        for hit in hits:
                hit.hitpoints -= 5
                if self.game.player.status == "Bloodthirsty":
                    self.game.player.hitpoints += 0.1  # Gain 2 health points per hit
                # Ensure the player's health does not exceed the maximum health limit, e.g., 100
                    self.game.player.hitpoints = min(self.game.player.hitpoints, 100)

                if self.game.player.status == "Mighty":
                    hit.stun(3000)
            


class swordfusion(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.swordfusion
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.sword_fusion_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#creating the rules for the mob class
class mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image = game.mob_img
        self.hitpoints = MOB_HITPOINTS
        self.x = x
        self.y = y
        #making the movement and speed of the mob (how fast it moves, its collision, etc.)
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 0
        self.stunned = False
        self.stun_end_time = 0

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y

    def update(self):
        if self.stunned and pg.time.get_ticks() < self.stun_end_time:
            return  # If stunned, do nothing
        else:
            self.stunned = False

        pass
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        if self.hitpoints < 0:
            self.kill()
        if self.hitpoints < 1000:
            print("ambatudieee")

    def stun(self, duration):
        self.stunned = True
        self.stun_end_time = pg.time.get_ticks() + duration

#making the pathfinding and pursuing of the player for the mob
def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
def update(self):
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.walls, 'y')