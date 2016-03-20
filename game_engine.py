#!/usr/bin/env python
# encoding: utf-8

# This file contains the initial config data
import sys
import inspect

from logs import *
from actors import *

# separates classes in my editor
@wrap_all(log_me)
class Gameplay(object):
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
        
        def log_death(self, player):
            self.logger.debug("{} has died with health {}".format(player.name, player.health))
            pass
        def log_health_comp(self, heathier, healthless, equal=False):
            equal_health = "equal" if equal else "greater"
            self.logger.debug("{} (health:{}) has "" health than {} (health:{})".format(
                heathier.name, heathier.health,healthless.name, healthless.health),equal_health)
            pass
        
        # end_game = False flags the end of a game
        if self.user.health <= 0:   # User has died
            log_death(self, self.user)
            end_game = True
            self.logger.game("{} wins".format(self.user.name))
        
        elif self.computer.health <= 0: # PC has died
            log_death(self, self.computer)
            end_game = True
            self.logger.game("{} wins".format(self.computer.name))
            
        elif self.central.hand_size == 0: # Game ends if size of active deck is zero
            self.logger.debug("Central Hand is zero (hand size:{})".format(self.central.hand_size))
            self.logger.game("")
            self.logger.game("No more cards available...".format(self.user.name))
            
            if self.user.health > self.computer.health:
                self.logger.game("{} Wins on Health".format(self.user.name))
                log_health_comp(self, self.user, self.computer)
            elif self.computer.health > self.user.health:
                self.logger.game("{} Wins on Health".format(self.computer.name))
                log_health_comp(self, self.user, self.computer)
            else: # No clear winner
                log_health_comp(self, self.user, self.computer, equal=True)
                self.logger.game("It is a Draw!")
            end_game = False
        else:
            self.logger.debug("Player are both healthy: ({} health:{}, {} health:{})".format(
                self.user.name, self.user.health,self.computer.name, self.computer.health))
            self.logger.debug("Central Hand size is not zero (hand size:{})".format(self.central.hand_size))
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