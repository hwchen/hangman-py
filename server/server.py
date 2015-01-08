#! /usr/bin/env python3

# Server file for hangman game


from flask import Flask, jsonify, request, make_response
import random
import sys
import string

# This section is for flask setup, routes.

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(game.to_json())

@app.route('/guess', methods = ['PUT'])
def put_guess():
    #server-side error checks: 
    guess_json = request.get_json(force=True)
    game.guess(int(guess_json['spot']),guess_json['letter'])
    game.state()
    return jsonify(game.to_json())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    

# This section for game logic.

class Game(object):

    def __init__(self):
        self.words = []
        self.target = ""
        self.wrong = 0
        self.current = ""
        self.result = "continue"

    def to_json(self):
        return {'target'  : self.target,
                'wrong'   : self.wrong,
                'current' : self.current,
                'result'  : self.result
               }

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
    #Can't be scaled this way.
    #How to scale? Don't want to grab one thread, just make
    #asynchronous. For web side. On back-end, multiple games may
    #run at once.
    game = Game()
    game.load_words("words.txt")
    game.init_target()
    app.run(debug=True)
