#! /usr/bin/env python3

# Server for hangman game

from flask import Flask, jsonify, request, make_response
import random
import sys
import string

# This section is for flask routes.

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/game_state')
def game_state():
    return jsonify(session.to_json())

@app.route('/game_state', methods = ['PUT'])
def put_guess():
    """basic game loop. refactored it into Session.iterate()"""
    guess_json = request.get_json(force=True)
    session.iterate(guess_json['spot'],guess_json['letter'])
    return jsonify(session.to_json())

@app.route('/new_game')
def new_game():
    """route for starting a new game"""
    session.new_game()
    session.current_game.load_words("words.txt")
    session.current_game.init_target()
    return jsonify(session.to_json())

@app.route('/cheat')
def cheat():
    return jsonify(session.current_game.to_json())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# DB section
    

# This section for game logic.

class Session(object):

    def __init__(self):
        self.sessionID = 1 
        self.sessionWins = 0
        self.sessionLosses = 0
        self.current_game = Game()

    def to_json(self):
        return {'sessionID': self.sessionID,
                'sessionWins': self.sessionWins,
                'sessionLosses': self.sessionLosses,
                'current' : self.current_game.current,
                'wrong' : self.current_game.wrong,
                'message' : self.current_game.message,
                'result' : self.current_game.result
               }

    def new_game(self):
        self.current_game = Game()

    def update_statistics(self):
        """checks if game is a win or loss, then changes stats
           (considered implementing stats change from Game object,
           but seems bad to mutate from below)"""
        if self.current_game.result == "win":
            self.sessionWins += 1
            self.current_game.message = "You won!"
        elif self.current_game.result == "lose":
            self.sessionLosses += 1
            self.current_game.message = "You lost!"
            

    def iterate(self, spot, letter):
        self.current_game.guess(spot,letter)
        self.current_game.update_state()
        self.update_statistics()

class Game(object):

    def __init__(self):
        """Initialize Attributes"""
        self.words = []
        self.target = ""
        self.wrong = 0
        self.current = ""
        self.result = "continue"
        self.message = "Welcome to Hangman! Good Luck!"

    def to_json(self):
        """attributes to JSON format, except for self.words"""
        return {'target'  : self.target,
                'wrong'   : self.wrong,
                'current' : self.current,
                'result'  : self.result,
                'message' : self.message
               }

    def load_words(self, file_path):
        """Reads file into a list
           loads into self.words attribute"""
        word_list = []
        f = open(file_path)
        for line in f:
            word = line.strip()
            word_list.append(word)
        self.words = word_list

    def init_target(self):
        """sets self.word to target, choosing randomly from self.words
           sets self.current as hidden representation of target"""
        self.target = random.choice(self.words)
        self.current = '*' * len(self.target)

    def guess(self, spot, letter):
        """checks for: out of bounds, is letter, is number. Then if guess is correct
            no return, only sets Game attributes .message, .current"""

        # check if spot is a number, breaks out of function if not a number
        if not spot.isdigit():
            self.message = "Your guess of spot {0} is not a number".format(spot)
            return

        # converts spot to integer if function above doesn't break out.
        spot_int = int(spot)

        # checking spot index bounds
        if spot_int > len(self.target)-1:
            self.message = "Spot {0} is outside the length of the target word".format(spot)

        # check if it's alpha
        elif not letter.isalpha():
            self.message = "Your guess of {0} is not a letter".format(letter)

        #check if guess is correct
        elif self.target[spot_int] == letter.lower():
            print("yes")
            if spot_int == len(self.target) -1:
                self.current = self.current[:spot_int] + letter
            else:
                self.current = self.current[:spot_int] + letter + self.current[spot_int + 1:]
            self.message = "Good guess!"
        else: 
            print("no")
            self.wrong += 1
            self.message = "Sorry, incorrect guess."

    def update_state(self):
        if self.current == self.target:
            self.result = "win"
        elif self.wrong == 10:
            self.result = "lose"

if __name__ == '__main__':
    session = Session()
    session.current_game.load_words("words.txt")
    session.current_game.init_target()
    app.run(debug=True)

