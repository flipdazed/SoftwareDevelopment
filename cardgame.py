#!/usr/bin/env python
# encoding: utf-8

# This is the main game file
from logs import *

import game_engine
from config import defaults

###### Options #######
level = logging.GAME
# logging.DEBUG
# logging.INFO
# logging.GAME
######################
logging.root.setLevel(level)

def main(game):
    """Main loop to allow error handling"""
    
    # Starting the game with a friendly message
    game.new("Welcome to my wonderful game. I hope you are as excited as I am to play!")
    
    game.play() # plays the game
    
    # a friendly farewell
    game.exit("Hope to see you again soon. Goodbye! (:")
    pass

if __name__ == '__main__':
    # logging
    logger.debug("Starting Game Engine...")
    game = game_engine.Gameplay()
    
    # instanciate the game settings
    # see function docs for more info on
    # expected values
    game.configure(defaults)
    
    try: # try to play
        main(game)
    except KeyboardInterrupt:
        # for when players rage quit
        game.hostile_exit()
    pass