# name:         __init__.py
# author:       Ding Jérémy
# date:         08.10.2024
#
# description:  See read me for rules
#
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import random
import pygame
from pygame import gfxdraw
from math import *


class Wordle:
    """
    Worlde game class

    Attributs:
    file_name:  path of the txt file containing all words
    screen:     screen object used to display the game
    """

    C_SCREEN_DIMENSIONS = (650, 650)
    C_GRID_DIMENSIONS = (5, 6)

    # Defines the offset in regards to the rectangle position, useful to
    # shift the letter position
    C_LETTER_FONT_OFFSET = (15, 11)
    C_LETTER_SQR_SIZE = (60, 60)

    # Game colors
    C_BACKGROUND_COLOR = "#121213"
    C_LETTER_CORRECT_COLOR = "#538d4e"
    C_LETTER_NEARLY_COLOR = "#b59f3b"
    C_LETTER_PLAYED_COLOR = "#3a3a3c"
    C_LETTER_UNPLAYED_COLOR = "#818384"
    C_LINE_COLOR = (50, 50, 50)
    C_LETTER_FONT_COLOR = (255, 255, 255)

    # defines the dimensions of the letters display
    # it defines the surface on which the entire array
    # of letters is displayed

    C_LETTER_DISPLAY_WIDTH = C_GRID_DIMENSIONS[0] * (C_LETTER_SQR_SIZE[0] + 4)
    C_LETTER_DISPLAY_HEIGHT = C_GRID_DIMENSIONS[1] * (C_LETTER_SQR_SIZE[1] + 4)

    # Defines its positions
    C_LETTER_DISPLAY_X = C_SCREEN_DIMENSIONS[0] / 2 - C_LETTER_DISPLAY_WIDTH / 2
    C_LETTER_DISPLAY_Y = 50

    # Keyboard constants
    C_KEYBOARD_DISPLAY_WIDTH = 500

    C_KEYBOARD_DISPLAY_X = C_SCREEN_DIMENSIONS[0] / 2 - C_KEYBOARD_DISPLAY_WIDTH / 2
    C_KEYBOARD_DISPLAY_Y = 475

    C_KEYBOARD_CASE_DIMENSIONS = (50, 50)
    # X and Y spacing between boxes
    C_KEYBOARD_CASE_SPACING = (5, 5)
    C_KEYBOARD_LETTER_SIZE = 40
    C_KEYBOARD_LETTER_OFFSET = (10, 5)

    # Animations
    C_ANIM_TYPED_LETTER_RANGE = 3
    C_ANIM_TYPE_LETTER_TICK = 0.02

    # Texts
    C_END_TEXT_SIZE = 30

    def __init__(self, file_name, screen):
        # Txt file that contains all words
        self.file_name = file_name
        self.file = None

        # Defines the word list
        self.words = []
        # Word to be guessed
        self.correct_word = None

        # Cursors that helps keep track of current
        # letter position
        self.cursor_letter = 0
        self.cursor_line = 0
        self.screen = screen
        self.pygame = pygame

        # Defines the grid of letter_cases
        self.grid = []
        # Defines the game font
        self.letter_font = pygame.font.SysFont(
            "Neue Helvetica 75 Bold", Wordle.C_LETTER_SQR_SIZE[0]
        )
        self.kbrd_letter_font = pygame.font.SysFont(
            "Neue Helvetica 75 Bold", Wordle.C_KEYBOARD_LETTER_SIZE
        )

        # Create a virtual keyboard
        self.keyboard = Keyboard_panel(self)

        # Keep track of played letters and their status
        self.played_letters_none = ""
        self.played_letters_placement = ""
        self.played_letters_correct = ""

        # Main flag
        self.playing = True

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

    def play(self, letter):
        """
        Tries playing a letter
        Arguments:
        letter: [char] letter to play
        """
        # Check that not the end of the line
        if self.cursor_letter == Wordle.C_GRID_DIMENSIONS[0]:
            return
        # Check if letter is too big
        if len(letter) != 1:
            return
        # Check it is a valid position
        if self.cursor_line == Wordle.C_GRID_DIMENSIONS[1]:
            self.playing = False
            return

        self.grid[
            self.cursor_line * Wordle.C_GRID_DIMENSIONS[0] + self.cursor_letter
        ].letter = letter
        # Increment cursor
        self.cursor_letter += 1

    def back_space(self):
        """Executes a backspace, remove last entered
        char and moves the cursor back"""
        # Come back one step
        self.cursor_letter -= 1
        if self.cursor_letter < 0:
            self.cursor_letter = 0
            return
        self.get_current_grid_elem().letter = ""

    def check_word(self):
        """Called to check the current line"""
        number_corrects = 0
        # If current line is not full (cursor)
        if self.cursor_letter < Wordle.C_GRID_DIMENSIONS[0]:
            return False

        # Read current word
        typed_word = self.get_current_word()

        # Check if the word exists
        try:
            self.words.index(typed_word)
        except:
            return False

        # Check every letter
        # Cursor start
        c_strt = self.cursor_line * Wordle.C_GRID_DIMENSIONS[0]

        # Get hints
        hints = self.generate_hints(typed_word)

        # Sets hints colors & push letters into the arrays
        for i in range(Wordle.C_GRID_DIMENSIONS[0]):
            value = hints[i]
            if value == "CORRECT":
                self.played_letters_correct += self.grid[c_strt + i].letter
                self.grid[c_strt + i].color = Wordle.C_LETTER_CORRECT_COLOR
            elif value == "PLACEMENT":
                self.played_letters_placement += self.grid[c_strt + i].letter
                self.grid[c_strt + i].color = Wordle.C_LETTER_NEARLY_COLOR
            else:
                self.played_letters_none += self.grid[c_strt + i].letter
                self.grid[c_strt + i].color = Wordle.C_LETTER_PLAYED_COLOR
        # Go to the next line
        self.cursor_line += 1
        self.cursor_letter = 0

    def get_current_word(self):
        """Get the current typed word."""
        word = ""
        # Get the start char position
        start_c = self.cursor_line * Wordle.C_GRID_DIMENSIONS[0]
        # Goes though the grid
        for i in range(start_c, start_c + Wordle.C_GRID_DIMENSIONS[0]):
            word += self.grid[i].letter
        # Add cariage return
        word += "\n"
        return word

    def get_current_grid_elem(self):
        """Get the current grid element from the cursors"""
        return self.grid[
            self.cursor_line * Wordle.C_GRID_DIMENSIONS[0] + self.cursor_letter
        ]
        """Check a letter in the grid. Compares it to the hidden word
        Returns:
        \"CORRECT\": Correct placement and letter
        \"PLACEMENT\": Correct letter wrong placement
        \"NONE\":   Not present in the word
        """
        # Get grid index
        index = cursor_line * Wordle.C_GRID_DIMENSIONS[0] + cursor_letter

        # Get the letter
        letter = self.grid[index].letter

        # Goes through hidden word
        # Check if the letter is correctly placed
        if letter == self.correct_word[cursor_letter]:
            return "CORRECT"
        # Check if letter present
        try:
            self.correct_word.index(letter)
            return "PLACEMENT"
        except:

            return "NONE"

    def generate_hints(self, word_to_check):
        """Returns an array of colors correponding to hints"""
        guess_word = word_to_check
        secret_word = self.correct_word
        width = Wordle.C_GRID_DIMENSIONS[0]

        feedback = ["NONE"] * width  # Initialize all to gray
        # Track indices of secret_word that have been matched for green
        used_indices = []

        # Step 1: First pass to mark 'green' feedback
        for i in range(width):
            if guess_word[i] == secret_word[i]:
                feedback[i] = "CORRECT"
                used_indices.append(i)  # Mark this index as used for a green match

        # Step 2: Second pass to mark 'yellow' feedback
        for i in range(width):
            # Skip greens, we're only checking for yellows now
            if feedback[i] != "CORRECT":
                if guess_word[i] in secret_word:
                    for j in range(width):
                        # Check if the letter exists in secret_word at another position
                        # Ensure we are not placing a yellow for positions already marked green
                        if guess_word[i] == secret_word[j] and j not in used_indices:
                            feedback[i] = "PLACEMENT"
                            used_indices.append(j)
                            break  # Exit loop once we find the first valid yellow match

        return feedback

    def show(self):
        """Displays the game to the screen"""
        # Background
        self.screen.fill(Wordle.C_BACKGROUND_COLOR)

        # Letters
        for letter in self.grid:
            letter.show()

        # Keyboard
        self.keyboard.show()

        # If finished then show end screen
        if not self.playing:
            self.show_end()
            return

    def show_end(self):
        """Shows the end frame, displays the word on screen, blur the background"""
        end_test = pygame.font.SysFont("Neue Helvetica 75 Bold", Wordle.C_END_TEXT_SIZE)
        txt = end_test.render(
            "The word was: " + self.correct_word, True, Wordle.C_LETTER_FONT_COLOR
        )

        # Calculate position for end text
        pos_x = Wordle.C_SCREEN_DIMENSIONS[0] / 2 - 100
        pos_y = Wordle.C_KEYBOARD_DISPLAY_Y - 30
        self.screen.blit(txt, (pos_x, pos_y))

        pass


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
        self.letter = ""

        # Animation related, if a letter is entered, makes the square "vibrate"
        self.animation_counter = 0
        self.last_letter = ""

    def show(self):
        """Shows the square"""
        # Check if animated
        if self.letter != self.last_letter and self.animation_counter < 2 * pi:
            self.animation_counter += Wordle.C_ANIM_TYPE_LETTER_TICK
        else:
            self.animation_counter = 0
            self.last_letter = self.letter

        animation_offset = Wordle.C_ANIM_TYPED_LETTER_RANGE * sin(
            self.animation_counter
        )

        # Defines the rectangle object
        rectangle = pygame.rect.Rect(
            self.position[0] - animation_offset,
            self.position[1] - animation_offset,
            Wordle.C_LETTER_SQR_SIZE[0] + 2 * animation_offset,
            Wordle.C_LETTER_SQR_SIZE[1] + 2 * animation_offset,
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


class Keyboard_panel:
    """
    Defines a panel that represents a keyboard.
    Used to show the user the keys that he has already used

    Attributs:
    wordle:[Wordle] Wordle game object
    """

    def __init__(self, wordle):
        self.screen = wordle.screen
        # List of rows
        self.top_row = "QWERTZUIOP"
        self.middle_row = "ASDFGHJKL"
        self.bottom_row = "YXCVBNM"

        self.rows = []
        self.rows.append(self.top_row)
        self.rows.append(self.middle_row)
        self.rows.append(self.bottom_row)

        self.wordle = wordle

        pass

    def set_letter_state(self, letter, state):
        """
        Set the letter state
        Arguments:
        letter: [A - Z]
        state: "CORRECT", "PLACEMENT", "NONE"
        """

    def show(self):
        """Displays the keyboard"""
        # Draws first row
        # Calculate width and height from each letters
        start_row_y = Wordle.C_KEYBOARD_DISPLAY_Y

        case_width = Wordle.C_KEYBOARD_CASE_DIMENSIONS[0]
        case_height = Wordle.C_KEYBOARD_CASE_DIMENSIONS[1]
        spacing_x = Wordle.C_KEYBOARD_CASE_SPACING[0]
        spacing_y = Wordle.C_KEYBOARD_CASE_SPACING[1]

        # Draws keyboard lines
        for i in range(3):
            for j in range(len(self.rows[i])):
                # Compute all positions and dimensions
                # Compute center position
                center_x = Wordle.C_SCREEN_DIMENSIONS[0] / 2
                # Compute letter row width
                row_width = len(self.rows[i]) * (case_width + spacing_x)
                # Compute starting x
                start_row_x = center_x - row_width / 2

                # Compute dimensions
                x = start_row_x + j * (case_width + spacing_x)
                y = start_row_y + i * (case_height + spacing_y)
                letter = self.rows[i][j]

                # Draws the rectangles
                rect = pygame.rect.Rect(x, y, case_width, case_height)

                # Defines color by letter status
                if letter in self.wordle.played_letters_correct:
                    color = Wordle.C_LETTER_CORRECT_COLOR
                elif letter in self.wordle.played_letters_placement:
                    color = Wordle.C_LETTER_NEARLY_COLOR
                elif letter in self.wordle.played_letters_none:
                    color = Wordle.C_LETTER_PLAYED_COLOR
                else:
                    color = Wordle.C_LETTER_UNPLAYED_COLOR

                # Draws rectangle
                pygame.draw.rect(self.screen, color, rect, border_radius=7)

                # Draws edges
                pygame.draw.rect(
                    self.screen, Wordle.C_LINE_COLOR, rect, 3, border_radius=7
                )

                # Writes letter
                txt = self.wordle.kbrd_letter_font.render(
                    self.rows[i][j], True, Wordle.C_LETTER_FONT_COLOR
                )
                # Draws letter with offset
                self.screen.blit(
                    txt,
                    (
                        x + Wordle.C_KEYBOARD_LETTER_OFFSET[0],
                        y + Wordle.C_KEYBOARD_LETTER_OFFSET[1],
                    ),
                )
