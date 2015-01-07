#! /usr/bin/env python3

# hangman game

import sys
import string
import random

class Game(object):

    def __init__(self):
        self.words = []
        self.target = ""
        self.wrong = 0
        self.current = ""
        self.result = "continue"

    def load_words(self, file_path):
        """Reads file into a List
           Returns a list of words """
        word_list = []
        f = open(file_path)
        for line in f:
            word = line.strip()
            word_list.append(word)
        self.words = word_list

    def init_target(self):
        """check if words loaded?"""

        self.target = random.choice(self.words)
        self.current = '*' * len(self.target)
        

    def guess(self, spot, letter):
    # check if it was already guessed
    # check if guess is out of bounds
    # check if it's letter and number
    # -- do these at the client first?
        if self.target[spot] == letter:
            print("yes")
            if spot == len(self.target) -1:
                self.current = self.current[:spot] + letter
            else:
                self.current = self.current[:spot] + letter + self.current[spot + 1:]
        else: 
            print("no")
            self.wrong += 1

    def state(self):
        if self.current == self.target:
            self.result = "win"
        elif self.wrong == 10:
            self.result = "lose"

if __name__ == '__main__':
    game = Game()
    game.load_words("words.txt")
    game.init_target()
    print (game.target)
    print (game.current)
    #Don't forget to add error checking
    while game.result == "continue":
        spot_in = int(input("Guess spot: "))
        letter_in = input("Guess letter: ")
        game.guess(spot_in, letter_in)
        print(game.current)
        print("# wrong: %d" % game.wrong)
        game.state() #I don't like that game.result is hidden
        print("game result is: %s" % (game.result))
    if game.result == "win":
        print("you win!")
    else: print("you lose!")

    # Game completely works. Now: error checking and add html server.
