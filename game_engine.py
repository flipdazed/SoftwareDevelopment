# This file contains the initial config data
from logs import *
import itertools, random
import inspect
from functools import wraps
logger = logging.getLogger(__name__)

# http://stackoverflow.com/a/6307868/4013571
def wrap_all(decorator):
    """wraps all function with the wrapper provided as an argument"""
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

def log_me(func):
    """Adds a logging facility to all functions it wraps"""
    @wraps(func)
    def tmp(*args, **kwargs):
        func_name = func.__name__
        if func_name != '__init__':
            args[0].logger.debug('...running {}'.format(func_name))
        return func(*args, **kwargs)
    return tmp

class Card(object):
    """Creates the card objects used in game"""
    
    def __init__(self, name, attack, money, cost):
        self.name = name
        self.cost = cost
        self.attack = attack
        self.money = money
    
    def __str__(self):
        return 'Name %s costing %s with attack %s and money %s' \
            % (self.name, self.cost, self.attack, self.money)
    
    def get_attack(self):
        return self.attack
    
    def get_money(self):
        return self.money

@wrap_all(log_me)
class CommonActions(object):
    def __init__(self):
        pass
    
    def deck_to_hand(self):
        """
        Move cards from engine.central deck 
        to active engine.central deck
        
        Container is the dictionary within the
        class that need to be called with the
        getattr()
        """
        
        player = getattr(self, self.whoami)
        
        # For each index in player hand
        # Refills player hand from player deck.
        # If deck is empty, discard pile is shuffled
        # and becomes deck
        for x in xrange(0, player['handsize']):
            
            # Shuffle deck computer.pC['handsize'] times
            # if length of deck = 0
            # Will only be done once
            if (len(player['deck']) == 0):
                random.shuffle(player['discard'])   # Shuffle discard pile
                player['deck'] = player['discard']  # Make deck the discard
                player['discard'] = []              # empty the discard pile
            card = player['deck'].pop()
            player['hand'].append(card)
        pass
    
    def print_active_cards(self):
        """Display cards in active"""
        
        player = getattr(self, self.whoami)
        if_user = "Your " if self.whoami == 'pO' else ""
        
        print if_user + "Available Cards"
        for card in player['active']:
            print card
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
                deck.append(Card(**card["params"]))
        return deck

@wrap_all(log_me)
class CommonUserActions(object):
    def __init__(self):
        pass
    def play_all_cards(self):
        """transfer all cards from hand to active
            add values in hand to current totals
        
            should only be used by User and Computer
        """
        player = getattr(self, self.whoami)
        for x in xrange(0, len(player['hand'])):
            card = player['hand'].pop()
            player['active'].append(card)
            self.money = self.money + card.get_money()
            self.attack = self.attack + card.get_attack()
        pass
    
    def play_a_card(self, card_number):
        """plays a specific card...
        
        Transfer card to active
        add values in hand to current totals
        """
        player = getattr(self, self.whoami)
        
        card_number = int(card_number)
        # Transfer card to active
        # add values in hand to current totals
        card = player['hand'].pop(card_number)
        player['active'].append(card)
        self.money = self.money + card.get_money()
        self.attack = self.attack + card.get_attack()
        pass
    
    def discard_hand(self):
        """If there are cards in the hand add to discard pile"""
        
        player = getattr(self, self.whoami)
        
        if (len(player['hand']) > 0 ):
            # Iterate through all cards in player hand
            for x in xrange(0, len(player['hand'])):
                player['discard'].append(player['hand'].pop())
        pass
    
    def discard_active_cards(self):
        """If there cards in PC active deck
        then move all cards from active to discard"""
        
        player = getattr(self, self.whoami)
        
        if (len(player['active']) > 0 ):
            for x in xrange(0, len(player['active'])):
                player['discard'].append(player['active'].pop())
        pass
    def display_values(self):
        """ Display player values"""
        
        player = getattr(self, self.whoami)
        print " {} values attack {}, money {}".format(
            player['name'],self.attack, self.money)
        pass
    def show_health(self):
        """Shows players' health"""
        # creates an attribute based on the class
        player = getattr(self, self.whoami)
        print "{} Health {}".format(player['name'],player['health'])
        pass 
# separates classes in my editor
@wrap_all(log_me)
class Central(CommonActions):
    """The Central Deck Class"""
    
    def __init__(self, hand_size, deck_settings, name, supplements):
        """initial settings for the central cards"""
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Central")
        self.logger.debug("Central Created.")
        
        # my name
        self.whoami = 'central'
        
        self.hand_size = hand_size
        self.name = name
        self.deck_settings = deck_settings
        self.supplement_settings = supplements
        
        # create newgame paramters
        self.newgame()
        
    
    def newgame(self):
        
        self.active = []
        
        # revert to initial state
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
        
        self.deck = self.deck_creator(self.deck_settings)
        self.supplements = self.deck_creator(self.supplement_settings)
        
        random.shuffle(self.deck)
        
        self.central = { # Central deck settings
                'name': self.name,
                'active': self.active,
                'activesize': self.hand_size,
                'supplement': self.supplements,
                'deck': self.deck}
        
        pass
    
    def deck_to_active(self):
        """ moves cards from one item to another"""
        count = 0
        while count < self.central['activesize']:
            card = self.central['deck'].pop()
            self.central['active'].append(card)
            count += 1
        pass
    
    def print_supplements(self):
        """Display supplements"""
        print "Supplement"
        if len(self.central['supplement']) > 0:
            print self.central['supplement'][0]
        pass
    
# separates classes in my editor
@wrap_all(log_me)
class User(CommonActions, CommonUserActions):
    """The User Class"""
    
    def __init__(self, hand_size, deck_settings, name, health):
        """initial settings for the User"""
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        self.logger = logging.getLogger(__name__ + ".User")
        self.logger.debug("User Created.")
        
        # my name
        self.whoami = 'pO'
        
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        
        # create newgame paramters
        self.newgame()
    
    def newgame(self):
        
        # revert to initial state
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
        
        self.active = []
        self.hand = []
        self.discard = []
        
        self.deck = self.deck_creator(self.deck_settings)
        
        # Initial settings
        self.pO = { # User settings
            'name': self.name,
            'health': self.health,
            'deck': self.deck,
            'hand': self.hand,
            'active': self.active,
            'handsize': self.hand_size,
            'discard': self.discard}
        pass
    
    def print_hand(self):
        """displays the indexed user hand"""
        
        # Display User hand
        print "\nYour Hand"
        index = 0
        for card in self.pO['hand']:
            print "[%s] %s" % (index, card)
            index = index + 1
        pass
# separates classes in my editor
@wrap_all(log_me)
class Computer(CommonActions, CommonUserActions):
    """The Computer Player Class"""
    
    def __init__(self, hand_size, deck_settings, name, health):
        """initial settings for the computer player"""
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # intialise params
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Computer")
        self.logger.debug("Computer Created.")
        
        # my name
        self.whoami = 'pC'
        
        # create newgame paramters
        self.newgame()
        
    
    def newgame(self):
        
        # revert to initial state
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
        
        self.active = []
        self.hand = []
        self.discard = []
        
        self.deck = self.deck_creator(self.deck_settings)
        
        # Initial settings
        self.pC = { # User settings
            'name': self.name,
            'health': self.health,
            'deck': self.deck,
            'hand': self.hand,
            'active': self.active,
            'handsize': self.hand_size,
            'discard': self.discard}
        pass