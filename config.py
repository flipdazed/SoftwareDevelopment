# This file contains the initial config data
import itertools, random

class Card(object):
    """Creates the card objects used in game"""
    def __init__(self, name, values=(0, 0), cost=1):
        self.name = name
        self.cost = cost
        self.values = values
    
    def __str__(self):
        return 'Name %s costing %s with attack %s and money %s' \
            % (self.name, self.cost, self.values[0], self.values[1])
    
    def get_attack(self):
        return self.values[0]
    
    def get_money(self):
        return self.values[1]
    
# separates classes in my editor
class Central(object):
    """The Central Deck Class"""
    def __init__(self):
        """initial settings for the central cards"""
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
    
    def replay(self):
        """creates parameters for newgame"""
        
        self.central = { # Central deck settings
            'name': 'central',
            'active': None,
            'activesize': 5,
            'supplement': None,
            'deck': None}
            
        # Changes are made in this list
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
            2 * [Card('Catapault', (7, 0), 6)],
            2 * [Card('Caravan', (1, 5), 5)],
            2 * [Card('Assassin', (5, 0), 4)]]
        
        # Creating supplements 
        self.supplement = 10 * [Card('Levy', (1, 2), 2)]
        
        # Flatten central deck to one list
        self.deck = list(itertools.chain.from_iterable(self.sdc))
        random.shuffle(self.deck)
        
        # Initiate PC deck dictionary
        self.central['deck'] = self.deck
        self.central['supplement'] = self.supplement
        self.central['active'] = []
        pass

# separates classes in my editor
class User(object):
    """The User Class"""
    def __init__(self):
        """initial settings for the User"""
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
    
    def replay(self):
        """creates parameters for newgame"""
        self.pO = { # User settings
            'name': 'player one',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}
        
        # Changes are made in this list
        # User's deck
        self.playeronedeck = [
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]]
        
        # Flatten list to one list
        self.pod = list(itertools.chain.from_iterable(self.playeronedeck))
        
        # Initiate new dictionary
        self.pO['deck'] = self.pod
        self.pO['hand'] = []
        self.pO['discard'] = []
        self.pO['active'] = []

# separates classes in my editor
class Computer(object):
    """The Computer Player Class"""
    def __init__(self):
        """initial settings for the computer player"""
        
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
    
    def replay(self):
        """creates parameters for newgame"""
        
        self.pC = {# PC settings
            'name': 'player computer',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}
        
        # Changes are made in this list
        # Create PC deck (list of lists)
        self.playertwodeck = [
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]]
        
        # Flatten list of lists
        self.ptd = list(itertools.chain.from_iterable(self.playertwodeck))
        
        # Initiate PC deck dictionary
        self.pC['deck'] = self.ptd
        self.pC['hand'] = []
        self.pC['discard'] = []
        self.pC['active'] = []