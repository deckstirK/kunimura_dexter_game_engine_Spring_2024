import pygame
from pygame.locals import *

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Level Transition Example")

# Define the player
player_rect = pygame.Rect(50, 50, 30, 30)

# Define the gap in the wall
gap_rect = pygame.Rect(400, 200, 100, 200)

# Main game loop
running = True
level = 1

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_rect.move_ip(-5, 0)
    if keys[K_RIGHT]:
        player_rect.move_ip(5, 0)
    if keys[K_UP]:
        player_rect.move_ip(0, -5)
    if keys[K_DOWN]:
        player_rect.move_ip(0, 5)

    # Check for collision with gap
    if player_rect.colliderect(gap_rect):
        # Transition to the next level
        level += 1
        gap_rect.y += 300  # Move the gap to a new position
        player_rect.x = 50  # Reset player position
        player_rect.y = 50

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, player_rect)
    pygame.draw.rect(screen, BLACK, gap_rect)
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
