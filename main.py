# name:         main.py
# author:       Ding Jérémy
# date:         08.10.2024
#
# description:  See read me for rules
#

from wordle import Wordle
import pygame, sys

# Main game loop
running = True

# Initialize pygame
pygame.init()

# Set up the window dimensions
window_width = 640
window_height = 480
window_size = (window_width, window_height)

# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("WORDLE")

# Define a background color (RGB)
background_color = (50, 150, 255)  # Light blue

# Create wordle
wordle = Wordle("word_list.txt", screen)

# Tries opening the file
if wordle.open_file() is False:
    print("Impossible to load file: " + wordle.file_name)
    running = False

# Read words
wordle.read_file()


# File opened normally
while running:
    # Handle events (e.g., window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with the color
    screen.fill(background_color)

    # Update the display
    pygame.display.flip()

# Clean up and quit pygame
wordle.file.close()
pygame.quit()
sys.exit()
