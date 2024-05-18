#This file was created by: Dexter Kunimura
#This code was inspired Zelda and informed by Chris Bradfield
#from (this place) import (everything)
from settings import *
import pygame as pg
from healthbar import *
from os import path
# from random import choice

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
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
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.player_img
        # self.spritesheet = Spritesheet(path.join(img_folder, 'theBell.png'))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.level2spawn = 0
        self.speed = 300
        self.hitpoints = 100
        self.weapon_drawn = False
        self.weapon = None
        self.weapon_dir = (0,0)
        self.dir = vec(0,0)
        self.weapon_type = ""
        self.weapon = Weapon(self.game, self.weapon_type, self.rect.x, self.rect.y, 16, 16, (0,0))
        self.swinging = False
        self.weapon_offset_x = 20 
        self.weapon_offset_y = 0


    #making the movement controls for the player
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        
        if keys[pg.K_e]:
            if not self.swinging:
                self.swinging = True
                if self.weapon:
                    self.weapon.swing()

    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            # Create the weapon at the player's position plus the offset
            self.weapon = Weapon(self.game, self.weapon_type, self.rect.x + self.weapon_offset_x, self.rect.y + self.weapon_offset_y, 16, 16, self.dir)
            
    #lays down rules for what happens when you hit a wall (hit a wall=cannot move in that direction)
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

    #determines what will happen when you hit special things
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1

            if str(hits[0].__class__.__name__) == "slap_juice":
                print(hits[0].__class__.__name__)
                self.speed += 150
                self.hitpoints += 50
                #changing the player expression back to normal if you stepped on the trap
                self.image = self.game.player_img
                self.rect = self.image.get_rect()

            if str(hits[0].__class__.__name__) == "trap":
                print(hits[0].__class__.__name__)
                self.speed -= 150
                self.hitpoints -= 50
                #changing the player to a pained expression upon stepping on the trap
                self.image = self.game.trapped_img
                #update the player's rect to the new image
                self.rect = self.image.get_rect()

            if str(hits[0].__class__.__name__) == "chug_jug":
                # double the size of the player's image
                self.image = pg.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
                # update the player's rect to match the new size
                self.rect = self.image.get_rect()

            if str(hits[0].__class__.__name__) == "mob":
                self.hitpoints -= 1
                hits[0].health -= 1

            if str(hits[0].__class__.__name__) == "Level2hallway":
                self.level2spawn += 1

    #making the list for things that get killed (disappear) upon collision
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.get_mouse()
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coin, True)
        self.collide_with_group(self.game.slap_juice, True)
        self.collide_with_group(self.game.chug_jug, True)
        self.collide_with_group(self.game.trap, True)
        self.collide_with_group(self.game.Level2hallway, True)
        if not self.weapon_drawn:
            if self.weapon:
                self.weapon.kill()
                self.weapon = None

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

class Level2hallway(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Level2hallway
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BGCOLOR)
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
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.basic_sword_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.rect.width = w
        self.rect.height = h
        self.pos = vec(x,y)
        self.dir = dir
        self.typ = typ
        self.original_x = x  # Store original x position
        self.original_y = y  # Store original y position
        self.swinging_duration = 0.2  # Duration of swing animation in seconds
        self.swinging_timer = 0  # Timer for swing animation
        print("I created a sword")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "mob":
                print("you hurt a mob!")
                hits[0].hitpoints -= 10
            # if str(hits[0].__class__.__name__) == "Mob2":
            #     print("you hurt a mob!")
            #     hits[0].hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Wall":
                print("you hit a wall")

    def swing(self):
        self.swinging = True
        self.angle = 45 if self.direction == vec(1, 0) else -45 if self.direction == vec(-1, 0) else 0

    def swinging_animation_finished(self):
        # This function should return True if the swinging animation is finished
        # Placeholder logic for animation duration or other criteria
        return True

    def return_to_original_position(self):
        self.angle = 0
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        if self.swinging:
            self.rotate_weapon()

    def rotate_weapon(self):
        # Store the current center of the weapon
        old_center = self.rect.center
        # Rotate the weapon image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        # Update the rect with the new image dimensions
        self.rect = self.image.get_rect()
        # Restore the rect's center to the old center
        self.rect.center = old_center
                
    def track(self, obj):
        self.vx = obj.vx
        self.vy = obj.vy
        # self.rect.width = obj.rect.x+self.dir[0]*32+5
        # self.rect.width = obj.rect.y*self.dir[1]*32+5
    def update(self):
        if not self.game.player.weapon_drawn:  # Check if weapon should be drawn
            self.kill()  # Kill the weapon if not drawn
            return
        self.track(self.game.player)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_group(self.game.mob, False)
        self.collide_with_group(self.game.walls, True)
        # hits = pg.sprite.spritecollide(self, self.game.mobs, False)
        # if hits:
        #     hits[0].hitpoints -= 1

#brainless mob for when i have to take pictures of it
# class mob(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.mob
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image = game.mob_img
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE

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
        self.hitpoints = 100
        self.x = x
        self.y = y
        #making the movement and speed of the mob (how fast it moves, its collision, etc.)
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
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