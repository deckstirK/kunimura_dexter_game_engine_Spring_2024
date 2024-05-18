import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Health Bar Above Player")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.health = 100

    def update(self):
        pass

# Health bar function
def draw_health_bar(player_pos, player_health):
    # Calculate the position of the health bar above the player
    health_bar_width = 50
    health_bar_height = 10
    health_bar_x = player_pos[0] - health_bar_width // 2
    health_bar_y = player_pos[1] - 20  # Adjust this value to position the health bar above the player
    health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
    
    # Draw the health bar background
    pygame.draw.rect(screen, WHITE, health_bar_rect)
    
    # Calculate the width of the health bar based on player's health
    health_width = health_bar_width * (player_health / 100)
    health_rect = pygame.Rect(health_bar_x, health_bar_y, health_width, health_bar_height)
    
    # Draw the health bar
    pygame.draw.rect(screen, RED, health_rect)

# Create player object
player = Player()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update player
    player.update()
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw player
    screen.blit(player.image, player.rect)
    
    # Draw health bar above player
    draw_health_bar(player.rect.center, player.health)
    
    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()