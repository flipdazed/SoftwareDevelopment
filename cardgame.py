#!/usr/bin/env python
# encoding: utf-8

# This is the main game file
from logs import *

import game_engine
from config import defaults

def main(game):
    """Main loop to allow error handling"""
    
    # Move cards from game.central.central deck 
    # to active game.central.central deck
    game.central.deck_to_active()
    
    # Move cards from User deck to User's hand
    game.user.deck_to_hand()
    
    # Move cards from PC deck to PC's hand
    game.computer.deck_to_hand()
    
    # Display game.central.central cards state
    game.central.print_active_cards()
    game.central.print_supplements()
    
    # Starting the game
    logger.game("Do you want to play a game?")
    iplay_game = raw_input().upper()
    continue_game = (iplay_game=='Y')
    
    if not continue_game: game.exit()
     
    logger.game("Do you want an Aggressive (A) opponent or an Greedy (G) opponent")
    iopponent_type = raw_input().upper()
    game.computer.aggressive = (iopponent_type=='A')
    logger.debug("Computer mode set to {}".format("Aggressive" if game.computer.aggressive else "Greedy"))
    
    # Each loop is a new round in the game
    # User goes first followed by PC
    while continue_game:
        logger.debug("Starting New Round.")
        
        #### Start User Turn ####
        logger.debug("Start User Turn...")
        game.user.turn()
        logger.debug("End User Turn.")
        #### End User Turn ####
        
        # display active deck and supplements
        game.central.display_all_active()
        
        # Display health state
        print
        game.user.show_health()
        game.computer.show_health()
        
        #### Start PC Turn ####
        logger.debug("Starting Computer Turn...")
        game.computer.turn()
        logger.debug("End Computer Turn...")
        #### End PC Turn ####
        
        # display active deck and supplements
        game.central.display_all_active()
        
        # Display health state
        print
        game.user.show_health()
        game.computer.show_health()
        
        # Check for end of game
        logger.debug("Checking End Game Conditions...")
        if game.end():
            
            # Asking user if they want to replay
            logger.debug("Starting Replay...")
            continue_game = game.replay()
    game.exit()
    pass

if __name__ == '__main__':
    # logging
    logger.debug("Starting Game...")
    game = game_engine.Gameplay()
    
    # instanciate the game settings
    game.user = game.User(**defaults['user'])
    game.computer = game.Computer(**defaults['computer'])
    game.central = game.Central(**defaults['central'])
    
    try:
        main(game)
    except KeyboardInterrupt:
        game.hostile_exit()
    pass