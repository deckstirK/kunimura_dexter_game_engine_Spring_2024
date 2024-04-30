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
        self.load_data()

                # TRANSPLANT THIS
    
    # making the sprites for the objects in the game
    def load_data(self):
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
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
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
    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
             s.kill()
        # reset criteria for changing level
        self.player.level2spawn = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
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

    def update(self):
            self.all_sprites.update()
            if self.player.level2spawn > 0:
                self.change_level(LEVEL2)

#INSTANTIATING!!!! (creating an instance of the game)
g = Game()
#use game method run to run the game
#g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_start_screen()