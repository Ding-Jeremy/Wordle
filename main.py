# name:         main.py
# author:       Ding Jérémy
# date:         08.10.2024
#
# description:  See read me for rules
#

from wordle import Wordle
import pygame, sys
from pygame import gfxdraw

# Main game loop
running = True

# Initialize pygame
pygame.init()
pygame.font.init()

# Set up the window dimensions
window_width = Wordle.C_SCREEN_DIMENSIONS[0]
window_height = Wordle.C_SCREEN_DIMENSIONS[1]
window_size = (window_width, window_height)

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("WORDLE")

# Create wordle
wordle = Wordle("word_list.txt", screen)

wordle.init_game()


while running:
    # Handle events (e.g., window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    wordle.show()

    # Update the display
    pygame.display.flip()

# Clean up and quit pygame
wordle.file.close()
pygame.quit()
sys.exit()
