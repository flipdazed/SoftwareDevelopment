# This file contains the initial config data
import itertools, random
from functools import wraps
import logging
loglevel=logging.INFO

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
    
    def __init__(self, name, values=(0, 0), cost=1):
        self.name = name
        self.cost = cost
        self.attack, self.money = values
        
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
    
    def __init__(self):
        """initial settings for the central cards"""
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Central")
        self.logger.setLevel(loglevel)
        self.logger.debug("Central Created.")
        
        # my name
        self.whoami = 'central'
        
        # create newgame paramters
        self.newgame()
        pass
    
    
    def newgame(self):
        self.central = { # Central deck settings
                'name': 'central',
                'active': None,
                'activesize': 5,
                'supplement': None,
                'deck': None}
    
        self.sdc = [ # Central deck cards
                4 * [Card('Archer', (3, 0), 2)],
                4 * [Card('Baker', (0, 3), 2)],
                3 * [Card('Swordsman', (4, 0), 3)],
                2 * [Card('Knight', (6, 0), 5)],
                3 * [Card('Tailor', (0, 4), 3)],
                3 * [Card('Crossbowman', (4, 0), 3)],
                3 * [Card('Merchant', (0, 5), 4)],
                4 * [Card('Thug', (2, 0), 1)],
                4 * [Card('Thief', (1, 1), 1)],
                2 * [Card('Catapult', (7, 0), 6)],
                2 * [Card('Caravan', (1, 5), 5)],
                2 * [Card('Assassin', (5, 0), 4)]]
        
        # Creating supplements
        self.supplement = 10 * [Card('Levy', (1, 2), 2)]
        
        # Flatten central deck to one list
        self.deck = list(itertools.chain.from_iterable(self.sdc))
        random.shuffle(self.deck)
        
        # Create central deck dictionary
        self.central['deck'] = self.deck
        self.central['supplement'] = self.supplement
        self.central['active'] = []
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
    
    def __init__(self):
        """initial settings for the User"""
        
        # logging
        self.logger = logging.getLogger(__name__ + ".User")
        self.logger.setLevel(loglevel)
        self.logger.debug("User Created.")
        
        # my name
        self.whoami = 'pO'
        
        # create newgame paramters
        self.newgame()
        pass
    
    
    def newgame(self):
        """initial default settings for the user"""
        
        # Initial settings
        self.pO = { # User settings
            'name': 'player one',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}
        
        self.playeronedeck = [ # User's deck
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]
            ]
        
        # Flatten User deck into one list
        self.pod = list(itertools.chain.from_iterable(self.playeronedeck))
        
        # Initiate User deck dictionary
        self.pO['deck'] = self.pod
        self.pO['hand'] = []
        self.pO['discard'] = []
        self.pO['active'] = []
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
    
    def __init__(self):
        """initial settings for the computer player"""
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Computer")
        self.logger.setLevel(loglevel)
        self.logger.debug("Computer Created.")
        
        # my name
        self.whoami = 'pC'
        
        # create newgame paramters
        self.newgame()
        
    
    def newgame(self):
        self.pC = { # PC settings
            'name': 'player computer',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}
        
        # Create User deck (list of lists)
        self.playertwodeck = [
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]]
            
        # Flattens PC deck to one list
        self.ptd = list(itertools.chain.from_iterable(self.playertwodeck))
        
        # Initiate PC deck dictionary
        self.pC['deck'] = self.ptd
        self.pC['hand'] = []
        self.pC['discard'] = []
        self.pC['active'] = []
        pass