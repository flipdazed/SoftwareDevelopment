#!/usr/bin/env python
# encoding: utf-8

# This file contains the initial config data
import sys
import inspect

from logs import *
from actors import *

class CommonGamePlayLoggers(object):
    """This is a class where I'm dumping
    loggers that are used more than once
    or are messy in main code"""
    def __init__(self):
        pass
    def logger_win_by_death(self, winner, loser):
        """Used in Gameplay().end()
        usage: Gameplay().end()"""
        self.logger.debug("{} has died with health {}".format(loser.name, loser.health))
        self.logger.game("{} wins".format(winner.name))
        pass
    def logger_win_on_health(self, winner, loser, equal=False):
        """Used in Gameplay().end()
        usage: Gameplay().end()"""
        
        if equal:
            self.logger.game("{} Wins on Health".format(winner.name))
        else:
            self.logger.game("It is a Draw!")
        
        equal_health = "equal" if equal else "greater"
        self.logger.debug("{} (health:{}) has "" health than {} (health:{})".format(
            winner.name, winner.health,loser.name, loser.health),equal_health)
        pass
    def logger_continue_game(self):
        """output logger for continuing the game
        usage: Gameplay().end()"""
        self.logger.debug("Player are both healthy: ({} health:{}, {} health:{})".format(
            self.user.name, self.user.health,self.computer.name, self.computer.health))
        self.logger.debug("Central Hand size is not zero (hand size:{})".format(self.central.hand_size))
        pass
    def logger_out_of_cards(self):
        """Output logger for running out of cards
        usage: Gameplay().end()"""
        self.logger.debug("Central Hand is zero (hand size:{})".format(self.central.hand_size))
        self.logger.game("")
        self.logger.game("No more cards available...".format(self.user.name))
    
# separates classes in my editor
@wrap_all(log_me)
class Gameplay(CommonGamePlayLoggers):
    """Gameplay Class"""
    def __init__(self):
        
        self.User = lambda hand_size, deck_settings, name, health: \
            User(self, hand_size, deck_settings, name, health)
        self.Computer = lambda hand_size, deck_settings, name, health: \
            Computer(self, hand_size, deck_settings, name, health)
        self.Central = lambda hand_size, deck_settings, name, supplements: \
            Central(self, hand_size, deck_settings, name, supplements)
        
        # logging
        get_logger(self)
        
        pass
    
    def end(self):
        """Checks for end game conditions"""
        end_game = False
        
        # end_game = False flags the end of a game
        if self.user.health <= 0:   # User has died
            self.logger_win_by_death(winner=self.user, loser=self.computer)
            end_game = True
            
        elif self.computer.health <= 0: # PC has died
            self.logger_win_by_death(winner=self.computer, loser=self.user)
            end_game = True
            
        elif self.central.hand_size == 0: # Game ends if size of active deck is zero
            self.logger_out_of_cards()
            if self.user.health > self.computer.health:
                self.logger_win_on_health(winner=self.user, loser=self.computer)
            
            elif self.computer.health > self.user.health:
                self.logger_win_on_health(winner=self.computer, loser=self.user)
            
            else: # No clear winner
                self.logger_win_on_health(winner=self.computer,
                    loser=self.user, equal=True)
            # don't end game if none of the above is true
            end_game = False
        else:
            self.logger_continue_game()
        return end_game
    def replay(self):
        """Asks User if they want to replay"""
        
        self.logger.game("Do you want to play another game?")
        iplay_game = raw_input().upper()
        continue_game = (iplay_game=='Y')
        
        # Initiate new game sequence
        if continue_game:
            
            # Starting the game
            self.logger.game("Do you want an aggressive (A) opponent or an greedy (G) opponent")
            iopponent_type = raw_input().upper()
            aggressive = (iopponent_type=='A')
            
            self.setup_game()
            
        return continue_game
    def exit(self):
        """Friendly exit"""
        self.logger.game("")
        self.logger.game("Hope to see you again soon. Goodbye :)") 
        sys.exit() # Terminate
        pass
    def hostile_exit(self):
        """UnFriendly exit"""
        self.logger.game("")
        self.logger.game("")
        self.logger.game("Sad to see you leave so quickly. Please return soon! :)")
        sys.exit() # Terminate
        pass
    def setup_game(self):
        """stores routines to set up a new game"""
        # call the replay game settings
        self.user.newgame()
        self.computer.newgame()
        self.central.newgame()
        
        # Move cards from self.central.central deck 
        # to active self.central.central deck
        self.central.deck_to_active()
        
        # Move cards from User deck to User's hand
        self.user.deck_to_hand()
        
        # Move cards from PC deck to PC's hand
        self.computer.deck_to_hand()
        
        # Display self.central.central cards state
        self.central.print_active_cards()
        self.central.print_supplements()
        pass