# name:         wordle.py
# author:       Ding Jérémy
# date:         08.10.2024
#
# description:  See read me for rules
#
import random
import pygame
from pygame import gfxdraw


class Wordle:
    """
    Worlde game class

    Attributs:
    file_name:  path of the txt file containing all words
    screen:     screen object used to display the game
    """

    C_SCREEN_DIMENSIONS = (600, 600)
    C_GRID_DIMENSIONS = (5, 6)

    C_BACKGROUND_COLOR = (10, 10, 10)
    C_LINE_COLOR = (50, 50, 50)
    C_LETTER_FONT_COLOR = (255, 255, 255)

    # Defines the offset in regards to the rectangle position, useful to
    # shift the letter position
    C_LETTER_FONT_OFFSET = (15, 8)
    C_LETTER_SQR_SIZE = (60, 60)

    C_LETTER_CORRECT_COLOR = (0, 255, 0)
    C_LETTER_NEARLY_COLOR = (0, 0, 255)

    # defines the dimensions of the letters display
    # it defines the surface on which the entire array
    # of letters is displayed

    C_LETTER_DISPLAY_WIDTH = C_GRID_DIMENSIONS[0] * (C_LETTER_SQR_SIZE[0] + 2)
    C_LETTER_DISPLAY_HEIGHT = C_GRID_DIMENSIONS[1] * (C_LETTER_SQR_SIZE[1] + 2)

    # Defines its dimensions
    C_LETTER_DISPLAY_X = C_SCREEN_DIMENSIONS[0] / 2 - C_LETTER_DISPLAY_WIDTH / 2
    C_LETTER_DISPLAY_Y = 50

    def __init__(self, file_name, screen):
        # Txt file that contains all words
        self.file_name = file_name
        self.file = None

        # Defines the word list
        self.words = []
        # Word to be guessed
        self.correct_word = None

        self.screen = screen
        self.pygame = pygame

        # Defines the grid of letter_cases
        self.grid = []
        # Defines the game font
        self.letter_font = pygame.font.SysFont(
            "Neue Helvetica 75 Bold", Wordle.C_LETTER_SQR_SIZE[0]
        )

    def read_file(self):
        """Read file a save the word list"""
        self.words = self.file.readlines()

    def open_file(self):
        """Opens the file, return true or false"""
        self.file = open(self.file_name)

        if self.file is None:
            return False
        return True

    def generate_grid(self):
        """Generate all objects related to the grid"""
        size_x = Wordle.C_GRID_DIMENSIONS[0]
        size_y = Wordle.C_GRID_DIMENSIONS[1]
        # Calculate spacings
        spc_x = Wordle.C_LETTER_DISPLAY_WIDTH / size_x
        spc_y = Wordle.C_LETTER_DISPLAY_HEIGHT / size_y

        # Get offsets
        off_x = Wordle.C_LETTER_DISPLAY_X
        off_y = Wordle.C_LETTER_DISPLAY_Y

        for i in range(size_y):
            for j in range(size_x):
                self.grid.append(
                    Letter_case([off_x + spc_x * j, off_y + spc_y * i], self)
                )

    def init_game(self):
        """Initialize the game, opens text file, creates objects etc"""
        # Tries opening the file
        if self.open_file() is False:
            print("Impossible to load file: " + self.file_name)
            return False

        # Reads the words file
        self.read_file()

        # Generate a grid
        self.generate_grid()

        # Pick a random word
        self.correct_word = random.choice(self.words)

        return True

    def show(self):
        """Displays the game to the screen"""
        # Background
        self.screen.fill(Wordle.C_BACKGROUND_COLOR)

        # Letters
        for letter in self.grid:
            letter.show()


class Letter_case:
    """
    Defines a letter emplacement.

    Attributs:
    position: [int, int] Position of the square
    wordle:[Wordle] Wordle game object
    """

    def __init__(self, position, wordle):
        self.dimensions = Wordle.C_LETTER_SQR_SIZE
        self.color = Wordle.C_BACKGROUND_COLOR

        self.position = position

        # Save useful drawing attributs
        self.screen = wordle.screen
        self.wordle = wordle

        self.letter = random.choice("ABCDEFGHIJKLMNOPQRSTUV")

    def show(self):
        """Shows the square"""
        # Defines the rectangle object
        rectangle = pygame.rect.Rect(
            self.position[0],
            self.position[1],
            Wordle.C_LETTER_SQR_SIZE[0],
            Wordle.C_LETTER_SQR_SIZE[1],
        )
        # Draws inner rectangle
        pygame.draw.rect(self.screen, self.color, rectangle)
        # Draws edges
        pygame.draw.rect(self.screen, Wordle.C_LINE_COLOR, rectangle, 3)
        # Writes letter
        pos_x = self.position[0] + Wordle.C_LETTER_FONT_OFFSET[0]
        pos_y = self.position[1] + Wordle.C_LETTER_FONT_OFFSET[1]

        txt = self.wordle.letter_font.render(
            self.letter, True, Wordle.C_LETTER_FONT_COLOR
        )
        self.screen.blit(txt, (pos_x, pos_y))
