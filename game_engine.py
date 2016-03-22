#!/usr/bin/env python
# encoding: utf-8

# This file contains the initial config data
import sys
import os
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
        
        self.art = Art() # create art for game
        # logging
        get_logger(self)
        self.clear_term()
        
        
        pass
    def clear_term(self):
        """clears terminal"""
        os.system('clear')
        pass
    
    def configure(self, defaults):
        """configure the game settings
        Relies on the defaults settings being in an expected format
        
        minimal example below of expected input:
        
        defaults = {
            "central":{
                "name":'Central', #"Central",
                "hand_size":5,
                "deck_settings":[ # Central deck paramss
                    {"count":4 ,"params":{"name":'Archer', "attack":3, "money":0, "cost":2}},
                    ]
                ,"supplements": 
                    [{"count":10 ,"params":{"name":'Levy', "attack":1, "money":2, "cost":2}}]
                }
            ,"user":{
                "name":'Lord Vadar',  #"Player One",
                "health":30,
                "hand_size":5,
                "deck_settings":[ # User's deck
                    {"count":8 ,"params":{"name":'Serf', "attack":0, "money":1, "cost":0}},
                    ]
                }
            ,"computer":{
                "name": 'Computer', #"Computer Player",
                "health":30,
                "hand_size":5,
                "deck_settings":[ # computer deck
                    {"count":8 ,"params":{"name":'Serf', "attack":0, "money":1, "cost":0}},
                    ]
                }
            }
        """
        
        # this is used to align all the text nicely
        self.card_names = [card["params"]["name"] \
            for _,val in defaults.iteritems() for card in val['deck_settings']]
        
        # exit if no cards
        if not self.card_names:
            error_msg = "Unfortunately no cards could be found in config.py!"
            self.hostile_exit(msg=error_msg)
        
        self.max_card_name_len = max([len(name) for name in self.card_names])
        self.max_player_name_len = max([len(val["name"]) \
            for _ ,val in defaults.iteritems()])
        self.user = self.User(**defaults['user'])
        self.computer = self.Computer(**defaults['computer'])
        self.central = self.Central(**defaults['central'])
        
        # players to iterate
        self.actors = ["user", "computer"]
        pass
    
    def play(self):
        """the main game loop continues while
        self.continue_game is True"""
        
        self.continue_game = True
        
        while self.continue_game:
            logger.debug("Starting New Round")
            self.continue_game = self.next_round()
        
        pass
    def next_round(self):
        """Iterate for each round of the game
        
        Returns a variable determining if the game should continue
        This relies on a list defines in __init__()
        that contains the user and computer definitions
        """
        # User goes first followed by PC
        for actor in self.actors: # iterate the players
            # Check for end of game
            logger.debug("Checking End Game Conditions...")
            if self.end(): # True if end game conditions are met
            
                # Asking user if they want to replay
                logger.debug("Starting Replay...")
                self.continue_game = self.replay()
                if not self.continue_game: break
            else:
            
                #### Start User Turn ####
                player = getattr(self, actor) # well pleased with this
                logger.debug("Start {} Turn...".format(player.name))
                player.turn()
                logger.debug("End {} Turn.".format(player.name))
                #### End User Turn ####
                
        return self.continue_game
    def end(self, display=True):
        """Checks for end game conditions
        The flag "display" lets the end()
        be purely used as a function with no
        in game output
        """
        end_game = False
        
        # end_game = False flags the end of a game
        if self.user.health <= 0:   # User has died
            if display: self.logger_win_by_death(
                winner=self.computer, loser=self.user)
            end_game = True
            
        elif self.computer.health <= 0: # PC has died
            if display: self.logger_win_by_death(
                winner=self.user, loser=self.computer)
            end_game = True
            
        elif self.central.hand_size == 0: # Game ends if size of active deck is zero
            if display: self.logger_out_of_cards()
            if self.user.health > self.computer.health:
                if display: self.logger_win_on_health(
                    winner=self.user, loser=self.computer)
            
            elif self.computer.health > self.user.health:
                if display: self.logger_win_on_health(
                    winner=self.computer, loser=self.user)
            
            else: # No clear winner
                if display: self.logger_win_on_health(winner=self.computer,
                    loser=self.user, equal=True)
            # don't end game if none of the above is true
            end_game = False
        else:
            if display: self.logger_continue_game()
        return end_game
    def replay(self):
        """Asks User if they want to replay"""
        
        self.logger.game("Do you want to play another game?")
        iplay_game = raw_input().upper()
        self.continue_game = (iplay_game=='Y')
        
        # Initiate new game sequence
        if self.continue_game:
            
            # Starting the game
            self.logger.game("Do you want an aggressive (A) opponent or a greedy (G) opponent")
            iopponent_type = raw_input().upper()
            aggressive = (iopponent_type=='A')
            
            self.setup_game()
            
        return self.continue_game
    def new(self, welcome_msg=""):
        """starts the new game sequence
        expects welcome message as string"""
        default_msg = "Welcome to my wonderful game. I hope you are as excited as I am to play!"
        
        if not self.art.check_terminal_width():
            self.logger.game("For best results resize the terminal window to:")
            self.logger.game(" >= 78 columns and >= 90 rows")
            self.logger.game("Press any key to continue or 'Q' to quit.")
            if raw_input().upper() == 'Q':
                self.hostile_exit(safemode=True)
        
        if not welcome_msg:
            welcome_msg = default_msg
        self.logger.game(self.art.welcome)
        self.logger.game(welcome_msg)
        
        self.logger.game(self.art.underline)
        self.logger.game("Do you want to play? 'Y' to continue, else exit")
        iplay_game = raw_input().upper()
        
        continue_game = (iplay_game=='Y')
        if not continue_game: 
            self.exit()
        
        self.logger.game("Do you want an aggressive (A) opponent or a greedy (G) opponent")
        iopponent_type = raw_input().upper()
        
        self.computer.aggressive = (iopponent_type=='A') # store opponent type
        self.logger.debug("Computer mode set to {}".format("Aggressive" if self.computer.aggressive else "Greedy"))
        
        self.setup_game()
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
        self.central.display_all_active()
        self.wait_for_user()
        pass
    def exit(self, exit_msg=""):
        """Friendly exit expects exit message as string"""
        default_msg = "Hope to see you again soon. Goodbye! (:"
        if not exit_msg:
            exit_msg = default_msg
        
        self.clear_term()
        self.logger.game(self.art.goodbye)
        self.logger.game("")
        self.logger.game(exit_msg)
        self.logger.game("")
        self.logger.game("")
        sys.exit() # Terminate
        pass
    def hostile_exit(self, msg=None,safemode=False):
        """UnFriendly exit"""
        
        if safemode: # we don't know the size of temrinal
            goodbye = self.art.goodbye_mini
        else:
            goodbye = self.art.goodbye
        
        if msg is None: msg = "Sad to see you leave so quickly..."
        
        self.clear_term()
        self.logger.game(goodbye)
        self.logger.game("")
        self.logger.game(msg)
        self.logger.game("Please return soon! :)")
        self.logger.game("")
        sys.exit() # Terminate
        pass
    def display_health_status(self):
        """Displays the health of both players"""
        # Display health state
        self.logger.game("")
        self.logger.game(self.art.make_title(" Health Bar ", center=False))
        self.user.show_health()
        self.computer.show_health()
        self.logger.game(self.art.underline)
        pass
    def wait_for_user(self):
        """Ask use to proceed"""
        self.user.player_logger("")
        self.user.player_logger(self.art.choose_action)
        self.user.player_logger(self.art.continue_game)
        self.user.player_logger(self.art.underline)
        if raw_input().upper() == 'Q': 
            self.logger.debug("User wants to quite the game")
            self.hostile_exit()
        pass