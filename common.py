#!/usr/bin/env python
# encoding: utf-8

# contains the common actions
import random

from logs import *

class Card(object):
    """Creates the card objects used in game"""
    def __init__(self, name, attack, money, cost, name_padding=15, num_padding=2):
        self.name = name
        self.cost = cost
        self.attack = attack
        self.money = money
        
        self.name_padding = name_padding
        self.num_padding = num_padding
        
        self.padded_vals = (
            str(self.cost).ljust(self.num_padding),
            self.name.ljust(self.name_padding),
            str(self.attack).ljust(self.num_padding),
            str(self.money).ljust(self.num_padding),
        )
        
    def __str__(self):
        """outputs string of the card details when called as print Card()"""
        s_out = "Cost: {0} ~ {1} ~ Stats ... Attack: {2}, Money: {3}".format(
            *self.padded_vals)
        return s_out
    
    def get_attack(self):
        return self.attack
    
    def get_money(self):
        return self.money

@wrap_all(log_me)
class CommonActions(object):
    """Contains the common actions
    used by all game classes
    """
    def __init__(self):
        # self.art = Art()
        pass
    
    def deck_to_hand(self):
        """
        Move cards from central.central deck 
        to active central.central deck
        
        Container is the dictionary within the
        class that need to be called with the
        getattr()
        """
        # For each index in player hand
        # Refills player hand from player deck.
        # If deck is empty, discard pile is shuffled
        # and becomes deck
        for i in xrange(0, self.hand_size):
            
            # Shuffle deck computer.pC['hand_size times
            # if length of deck = 0
            # Will only be done once
            if (len(self.deck) == 0):
                self.logger.debug("Deck length is zero!")
                random.shuffle(self.discard)   # Shuffle discard pile
                self.logger.debug("shuffled deck")
                self.deck = self.discard  # Make deck the discard
                self.discard = []              # empty the discard pile
                self.logger.debug("Moved discard pile to deck. Discard pile set to empty.")
            card = self.deck.pop()
            self.hand.append(card)
            self.logger.debug("Iteration #{}: Drawn {} from deck and added to hand".format(i,card.name))
        pass
    
    def print_active_cards(self, title=None, index=False):
        """Display cards in active"""
        
        if title is None: title = "Your Played Cards"
        
        # switch depending on player type
        self.logger.debug("Actor is: {}".format(type(self).__name__))
        
        title = self.art.make_title(title)
        self.player_logger(title)
        
        self._print_cards(self.active, index=index)
        self.player_logger(self.art.underline)
        pass
        
    def deck_creator(self, deck_list):
        """Creates the deck from a list of dictionaries
    
        _Input_
        list of dicts. 
            dict contents: 
            "card" : dict containing all **kwargs for Card()
            "count" : number of cards with these settings to create
    
        _Output_
        list of Card() types
    
        Expected input example:
        [{"count":1, "card":{"name":'Archer', "attack":3, "money":0, "cost":2}},
        {"count":2, "card":{"name":'Baker', "attack":0, "money":0, "cost":2}}]
    
        Expected Output example:
        [Card('Archer', 3,0,2), Card('Baker', 0,0,2), Card('Baker', 0,0,2)]
        """
        deck = [] # get deck ready
        for card in deck_list:
            for _ in xrange(card["count"]):
                # passes the dictionary as a keyword arg (**kwarg)
                deck.append(Card(
                    name_padding=self.parent.max_card_name_len,
                    num_padding=2,
                    **card["params"]
                    ))
            self.logger.debug("Created {}x{}".format(card["count"], card["params"]["name"]))
        return deck
    
    def _print_cards(self, cards, index=False):
        """Prints out the cards provided"""
        # max card name length
        
        if len(cards) == 0:
            self.logger.game(self.art.index_buffer+ \
            "Nothing interesting to see here...")
        else:
            for i, card in enumerate(cards):
                num_str = "[{}] ".format(i) if index else self.art.index_buffer
                self.logger.game(num_str + "{}".format(card))
        pass
    
@wrap_all(log_me)
class CommonUserActions(object):
    """Contains actions for user and computer"""
    def __init__(self):
        pass
    def newgame(self):
        
        # revert to initial state
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
        
        self.active = []
        self.hand = []
        self.discard = []
        
        self.deck = self.deck_creator(self.deck_settings)
        
        pass
    def end_turn(self):
        """Ends the turn of the user"""
        self.logger.debug("Ending Turn: {}".format(self.name))
        # If player has cards in the hand add to discard pile
        self.discard_hand()
        
        # If there cards in active deck
        # then move all cards from active to discard
        self.discard_active_cards()
        
        # Move cards from deck to hand
        self.deck_to_hand()
        pass
    def play_all_cards(self):
        """transfer all cards from hand to active
            add values in hand to current totals
        
            should only be used by User and Computer
        """
        
        for i in xrange(0, len(self.hand)):
            card = self.hand.pop()
            self.active.append(card)
            self.logger.debug("Iteration #{}: Drawn {} from deck and added to active deck".format(i,card.name))
            self.__add_values_to_total(card)
        pass
    
    def play_a_card(self, card_number):
        """plays a specific card...
        
        Transfer card to active
        add values in hand to current totals
        """
        i=0
        card_number = int(card_number)
        # Transfer card to active
        # add values in hand to current totals
        card = self.hand.pop(card_number)
        self.active.append(card)
        self.logger.debug("Iteration #{}: Drawn {} from deck and added to active deck".format(i,card.name))
                
        self.__add_values_to_total(card)
        pass
    def __add_values_to_total(self, card):
        """Adds money and attack to total"""
        
        money_i = card.get_money()
        attack_i = card.get_attack()
        self.logger.debug("Money:{}+{}    Attack:{}+{}".format(self.money, money_i, self.attack, attack_i))
        self.money += money_i
        self.attack += attack_i
        pass
    def discard_hand(self):
        """If there are cards in the hand add to discard pile"""
        if (len(self.hand) > 0 ):
            # Iterate through all cards in player hand
            for i in xrange(0, len(self.hand)):
                card = self.hand.pop()
                self.logger.debug("Iteration #{}: Moving {} from hand and added to discard pile".format(i, card.name))
                self.discard.append(card)
        else:
            self.logger.debug("Hand length is zero. No cards to discard.")
        pass
    
    def discard_active_cards(self):
        """If there cards in PC active deck
        then move all cards from active to discard"""
        if (len(self.active) > 0 ):
            for i in xrange(0, len(self.active)):
                card = self.active.pop()
                self.logger.debug("Iteration #{}: Moving {} from hand and added to discard pile".format(i, card.name))
                self.discard.append(card)
        else:
            self.logger.debug("Active Deck length is zero. No cards to discard.")
        pass
    def display_values(self, attack=None, money=None):
        """ Display player values"""
        
        # allows forced values
        if attack is None: attack = self.attack
        if money is None:  money  = self.money
        
        padded_name = self.name.ljust(self.parent.max_player_name_len)
        out_str = "{}     Values :: ".format(padded_name)
        out_str += "  Attack: {}  Money: {}".format(
            attack, money)
        
        self.player_logger("")
        self.player_logger(out_str)
        self.player_logger("")
        pass
    def show_health(self):
        """Shows players' health"""
        # creates an attribute based on the class
        
        padded_name = self.name.ljust(self.parent.max_player_name_len)
        out_str = "{}     Health : ".format(padded_name)
        out_str += "{}".format(self.health)
        self.player_logger(out_str)
        
        pass
        
    def attack_player(self, other_player):
        """ Attack another player
        other_player expected input is a class
        that corresponds to another sibling player
        an example of this from self = game.User() would be:
            self.attack(self.parent.computer)
        which would attack the computer form the player
        """
        
        self.logger.debug("{0} Attacking {1} with strength {2}".format(self.name, other_player.name, self.attack))
        self.logger.debug("{0} Health before attack: {1}".format(other_player.name, other_player.health))
        other_player.health -= self.attack
        self.attack = 0
        self.logger.debug("{0} Attack: {1}".format(self.name, self.attack))
        pass
    def reset_vals(self):
        """resets money and attack"""
        self.logger.debug("Money and Attack set to 0 for {}".format(self.name))
        self.money = 0
        self.attack = 0
        pass