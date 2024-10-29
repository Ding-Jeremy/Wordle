# name:         main.py
# author:       Ding Jérémy
# date:         08.10.2024
#
# description:  See read me for rules
#

import os, sys
from . import Wordle

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# Main game loop
running = True

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.display.set_icon(pygame.image.load("assets/thumbnail.png"))
# Set up the window dimensions
window_width = Wordle.C_SCREEN_DIMENSIONS[0]
window_height = Wordle.C_SCREEN_DIMENSIONS[1]
window_size = (window_width, window_height)

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("WORDLE")

# Create wordle
wordle = Wordle("wordle/words/word_list.txt", screen)

# Init worlde game
wordle.init_game()

while running:
    # Handle events (e.g., window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If a key is pressed
        if event.type == pygame.KEYDOWN:
            # Close the game if ESC is pressed
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                wordle.back_space()
            elif event.key == pygame.K_RETURN:
                wordle.check_word()

            # play corresponding key if alphabetic
            elif pygame.key.name(event.key).isalpha():
                wordle.play(pygame.key.name(event.key).capitalize())
    wordle.show()

    # Update the display
    pygame.display.flip()

# Clean up and quit pygame
wordle.file.close()
pygame.quit()
sys.exit()
