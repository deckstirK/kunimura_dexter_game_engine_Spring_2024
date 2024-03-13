#This file was created by: Dexter Kunimura

'''
add sprites
add more power ups (THE MUSHROOM!!!!!!!)
make moving mob
'''
#import libraries and modules
import pygame as pg
from random import randint
from settings import *
from sprites import *
import sys
from os import path
from images import *

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
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, "smile.png")).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
   # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coin = pg.sprite.Group()
        self.mob = pg.sprite.Group()
        self.power_up = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
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
                if tile == 'u':
                    power_up(self, col, row)
                if tile == 'm':
                    print("a mob at", row, col)
                    mob(self, col, row)

    def update(self):
        self.all_sprites.update()
                    
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

    def draw_grid(self):
     for x in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
     for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))

    def draw(self):
         self.screen.fill(BGCOLOR)
         self.draw_grid()
         self.all_sprites.draw(self.screen)
         pg.display.flip()
     
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
    #         if event.type == pg.KEYDOWN:
    #             if event.key == pg.K_LEFT:
    #                 self.player.move(dx=-1)
    #             if event.key == pg.K_RIGHT:
    #                 self.player.move(dx=1)
    #             if event.key == pg.K_DOWN:
    #                 self.player.move(dy=1)
    #             if event.key == pg.K_UP:
    #                 self.player.move(dy=-1)
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen", 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()
        self.wait_for_key()
        
        pass 

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
                    # self.running = False

#INSTANTIATING!!!! (creating an instance of the game)
g = Game()
#use game method run to run the game
#g.show_start_screen()
while True:
    g.new()
    g.run()
    #g.show_go_screen()