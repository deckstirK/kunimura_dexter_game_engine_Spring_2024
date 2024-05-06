#This file was created by: Dexter Kunimura

'''
add sprites
add more power ups (THE MUSHROOM!!!!!!!)
add a hallway


Beta Goals
add a shop with a unique look (maybe)
consistent levels (pick up a coin, return the room, coin gone)
SOUNDS!
'''
#import libraries and modules
import pygame as pg
from random import randint
from settings import *
from sprites import *
import sys
from os import path
import pickle
# from maps import *

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"
#define game class
class Game:
    #create init functions
    def __init__(self):
        #initialize pygame
        pg.init()
        #sets the size and name of the game window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        #get pygame clock and start running
        self.clock = pg.time.Clock()
        self.level_states = self.load_game('savegame.pickle') or {}
        self.load_data(LEVEL1)
                       
    def save_game(self, filename):
            with open(filename, 'wb') as f:
                pickle.dump(self.level_states, f)
    
    def load_game(self, filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def load_level(self, level):
        # Load the level data
        self.load_data(level)

    # Check if level state exists, otherwise initialize it
        if level not in self.level_states:
            self.level_states[level] = {}

    # Load coins state for the level
        coins_state = self.level_states[level].get('coins', {})
    
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'c':  # Check if it's a coin tile
                    coin_id = f"{row}_{col}"  # Generate a unique ID for the coin
                    coin_spawned = coins_state.get(coin_id, False)  # Check if the coin was collected
                    if not coin_spawned:
                        coin(self, col, row)  # Spawn the coin if not collected
    
    def leave_level(self, level):
        self.save_game('savegame.pickle')
    
    # making the sprites for the objects in the game
    def load_data(self, lvl):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, "smile.png")).convert_alpha()
        self.trapped_img = pg.image.load(path.join(self.img_folder, "anguish.png")).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, "stoic.png")).convert_alpha()
        self.coin_img = pg.image.load(path.join(self.img_folder, "medallion.png")).convert_alpha()
        self.slap_juice_img = pg.image.load(path.join(self.img_folder, "slapjuice.png")).convert_alpha()
        self.chug_jug_img = pg.image.load(path.join(self.img_folder, "chugjug.png")).convert_alpha()
        self.wall_img = pg.image.load(path.join(self.img_folder, "bricks.png")).convert_alpha()
        self.trap_img = pg.image.load(path.join(self.img_folder, "ouchie.png")).convert_alpha()
        self.map_data = []
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                self.map_data.append(list(line.strip()))

    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coin = pg.sprite.Group()
        self.mob = pg.sprite.Group()
        self.slap_juice = pg.sprite.Group()
        self.chug_jug = pg.sprite.Group()
        self.trap = pg.sprite.Group()
        self.Level2hallway = pg.sprite.Group()
        self.load_level(LEVEL1)  # Load the first level when starting a new game
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)

   
        #determining placement features for map making
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'c':
                    print("a coin at", row, col)
                    coin(self, col, row)
                if tile == 's':
                    print ("a slapjuice at", row, col)
                    slap_juice(self, col, row)
                if tile == 'm':
                    print("a mob at", row, col)
                    mob(self, col, row)
                if tile == 'j':
                    print("a chug jug at", row, col)
                    chug_jug(self, col, row)
                if tile == 't':
                    print("a trap at", row, col)
                    trap(self, col, row)
                if tile == '2':
                    print("a Level2hallway at", row, col)
                    Level2hallway(self, col, row)

    #compiling together all the aforementioned items and preparing them for when you activate the game
    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            if self.player.leave_level():
                self.leave_level(self.current_level)
    def quit(self):
         pg.quit()
         sys.exit()

    #making the method for drawing the grid
    def draw_grid(self):
     for x in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY (x,0), (x, HEIGHT))
     for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))


    #making the background
    def draw(self):
         self.screen.fill(BGCOLOR)
        #  self.draw_grid()
         self.all_sprites.draw(self.screen)
         pg.display.flip()

    #saying what will happen if certain things are done by the player that are outside of the game 
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYUP:
            

                if event.key == pg.K_p:
                    if not self.paused:
                        self.paused = True
                    else:
                        self.paused = False

    #supposed make the start screen (i didnt make a draw text feature)

    # def start_screen(self):
    #     running = True
    #     while running:
    #         self.screen.fill(WHITE)
    #         self.draw_text("Simple Game", font, BLACK, WIDTH // 2, HEIGHT // 4)
    #         self.draw_text("Press SPACE to Start", font, BLACK, WIDTH // 2, HEIGHT // 2)
    #         self.draw_text("Press ESC to Quit", font, BLACK, WIDTH // 2, HEIGHT * 3 // 4)
    #         pg.display.update()

    #         for event in pg.event.get():
    #             if event.type == pg.QUIT:
    #                 self.quit()
    #             if event.type == pg.KEYDOWN:
    #                 if event.key == pg.K_SPACE:
    #                     running = False
    #                 if event.key == pg.K_ESCAPE:
    #                     self.quit()

    # def draw_text(self, text, font, color, x, y):
    #     text_surface = font.render(text, True, color)
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (x, y)
    #     self.screen.blit(text_surface, text_rect)
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             running = False
    #             pg.quit()
    #             sys.exit()
    #         if event.type == pg.KEYDOWN:
    #             if event.key == pg.K_SPACE:
    #                 # Start the game
    #                 return
    #             if event.key == pg.K_ESCAPE:
    #                 running = False
    #                 pg.quit()
    #                 sys.exit()
    '''
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    '''

    #idk what this is for
    def wait_for_key(self):
        waiting = True
        while waiting: 
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting == False
                    self.quit()
                if event.type == g.KEYUP:
                    waiting == False

    #making a level change feature
    def change_level(self, lvl, enter_side):
        # Load new level here...
        if enter_side == 'right':
            self.player.rect.x = 0
        else:  # enter_side == 'left'
            self.player.rect.x = WIDTH - TILESIZE
        self.player.rect.y = self.find_spawn_row(self.map_data) * TILESIZE
     # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
            self.map_data.append(line)
        # Set player's position based on the side they entered from
        if enter_side == 'right':
            self.player.rect.x = 0
        else:  # enter_side == 'left'
            self.player.rect.x = WIDTH - TILESIZE
        self.player.rect.y = self.find_spawn_row(self.map_data) * TILESIZE
        
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.traps = pg.sprite.Group()
        self.chug_jug = pg.sprite.Group()
        self.slap_juice = pg.sprite.Group()
        self.load_data(lvl)

        #if self.player is None:
        self.new()

        for row, tiles in enumerate(self.map_data):
            print(row)
        for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'c':
                    print("a coin at", row, col)
                    coin(self, col, row)
                if tile == 's':
                    slap_juice(self, col, row)
                if tile == 'm':
                    print("a mob at", row, col)
                    mob(self, col, row)
                if tile == 'j':
                    print("a chug_jug at", row, col)
                    chug_jug(self, col, row)
                if tile == 't':
                    print("a trap at", row, col)
                    trap(self, col, row)
                if tile == '2':
                    print("a Level2hallway at", row, col)
                    Level2hallway(self, col, row)

    def collect_coin(self, level, coin):
        if level in self.level_states and coin.id in self.level_states[level]:
            del self.level_states[level][coin.id]

    def update(self):
        self.all_sprites.update()
        player_col = self.player.rect.x // TILESIZE
        player_row = self.player.rect.y // TILESIZE
        if (0 <= player_row < len(self.map_data)) and (0 <= player_col < len(self.map_data[0])):
            if self.map_data[player_row][player_col] == '2':
                self.change_level(LEVEL2, 'right' if self.player.vx > 0 else 'left')
            if self.map_data[player_row][player_col] == '3':
                self.change_level(LEVEL1, 'right' if self.player.vx > 0 else 'left')

    def find_spawn_row(self, level):
        for row, tiles in enumerate(level):
            if '3' in tiles:
                return row
        return 0  # Default spawn row if no '3' tile is found
    
#INSTANTIATING!!!! (creating an instance of the game)
g = Game()
#use game method run to run the game
#g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_start_screen()