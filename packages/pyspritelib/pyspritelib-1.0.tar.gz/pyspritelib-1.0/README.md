# pyspritelib

`pyspritelib` is a simple Python package that provides a utility class for handling spritesheets in Pygame.

## Installation

```bash
pip install pyspritelib

# Usage

```python
import pygame
from pyspritelib import spritesheet

# Initialize Pygame
pygame.init()

# Load your spritesheet image
spritesheet_image = pygame.image.load('path_to_your_spritesheet.png').convert_alpha()

# Create a SpriteSheet object
sprite_sheet = spritesheet(spritesheet_image)

# Get a specific frame from the spritesheet
frame = sprite_sheet.get_image(frame=0, width=32, height=32, scale=2, colour=(0, 0, 0))


# frame: index of the sprite to use in the sheet (0 for the first frame)
# width: width of each individual sprite
# height: height of each individual sprite
# scale: scaling factor for the image (1 for original size)
# colour: background color for transparency


#EXAMPLE:
import pygame
from pyspritelib import spritesheet

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple SpriteSheet Example")

# Load your spritesheet image
spritesheet_image = pygame.image.load('image.png').convert_alpha()

# Create a SpriteSheet object
sprite_sheet = spritesheet(spritesheet_image)

# Get a specific sprite from the spritesheet
frame1 = sprite_sheet.get_image(frame=0, width=64, height=64, scale=2, colour=(255, 255, 255))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Draw the sprite
    screen.blit(frame1, (100, 100))

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
