# name:         wordle.py
# author:       Ding Jérémy
# date:         08.10.2024
#
# description:  See read me for rules
#


class Wordle:
    """
    Worlde game class

    Attributs:
    file_name:  path of the txt file containing all words
    screen:     screen object used to display the game
    """

    def __init__(self, file_name, screen=None):
        # Txt file that contains all words
        self.file_name = file_name
        self.file = None

        # Defines the word list
        self.words = []

    def read_file(self):
        """Read file a save the word list"""
        self.words.append(self.file.readlines())

    def open_file(self):
        """Opens the file, return true or false"""
        self.file = open(self.file_name)

        if self.file is None:
            return False
        return True

    def show(self):
        """Displays the game to the screen"""
