#!/usr/bin/env python
# encoding: utf-8

# This is the main game file
from logs import *

import game_engine
from config import defaults

def main(game):
    """Main loop to allow error handling"""
    
    # instanciate the game settings
    user = game_engine.User(**defaults['user'])
    computer = game_engine.Computer(**defaults['computer'])
    central = game_engine.Central(**defaults['central'])
    
    # Move cards from central.central deck 
    # to active central.central deck
    central.deck_to_active()
    
    # Move cards from User deck to User's hand
    user.deck_to_hand()
    
    # Move cards from PC deck to PC's hand
    computer.deck_to_hand()
    
    # Display central.central cards state
    central.print_active_cards()
    central.print_supplements()
    
    # Starting the game
    logger.game("Do you want to play a game?")
    iplay_game = raw_input().upper()
    continue_game = (iplay_game=='Y')
    
    if not continue_game: game.exit()
     
    logger.game("Do you want an Aggressive (A) opponent or an Greedy (G) opponent")
    iopponent_type = raw_input().upper()
    computer.aggressive = (iopponent_type=='A')
    logger.debug("Computer mode set to {}".format("Aggressive" if computer.aggressive else "Greedy"))
    
    # Each loop is a new round in the game
    # User goes first followed by PC
    while continue_game:
        logger.debug("Starting New Round.")
        
        #### Start User Turn ####
        logger.debug("Start User Turn...")
        user.turn(central, computer)
        logger.debug("End User Turn.")
        #### End User Turn ####
        
        # display active deck and supplements
        central.display_all_active()
        
        # Display health state
        print
        user.show_health()
        computer.show_health()
        
        #### Start PC Turn ####
        logger.debug("Starting Computer Turn...")
        computer.turn(central, user)
        logger.debug("End Computer Turn...")
        #### End PC Turn ####
        
        # display active deck and supplements
        central.display_all_active()
        
        # Display health state
        print
        user.show_health()
        computer.show_health()
        
        # Check for end of game
        logger.debug("Checking End Game Conditions...")
        if game.end(user, computer, central):
            
            # Asking user if they want to replay
            logger.debug("Starting Replay...")
            continue_game = game.replay(user, computer, central)
    game.exit()
    pass

if __name__ == '__main__':
    # logging
    logger.debug("Starting Game...")
    game = game_engine.Gameplay()
    
    try:
        main(game)
    except KeyboardInterrupt:
        game.hostile_exit()
    pass