#!/usr/bin/env python
# encoding: utf-8

# This is the main game file
from logs import *

import game_engine
from config import defaults

def main(game):
    """Main loop to allow error handling"""
    
    game.new()  # Starting the game
    game.play() # plays the game
    game.exit() # a friendly farewell
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