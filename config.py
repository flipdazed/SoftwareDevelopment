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
    
class GetConfig(object):
    """Stores configuration paramters"""
    def __init__(self):
        """
        Creates a static attribute to create
        global variables.
        """
        pass
    
    def initial(self):
        """
        Creates an dict.iteritem() of all initial game 
        parameters.
        
        Warning: This will return every item instanced in
        this function as it uses the local() method
        
        for item_name,item in self.initial:
            globals()[item_name] = item
        """
        
        # Initial settings
        pO = { # User settings
            'name': 'player one',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}

        pC = { # PC settings
            'name': 'player computer',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}

        central = { # Central deck settings
            'name': 'central',
            'active': None,
            'activesize': 5,
            'supplement': None,
            'deck': None}

        sdc = [ # Central deck cards
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
                2 * [Card('Assassin', (5, 0), 4)]
            ]

        # User's deck
        playeronedeck = [
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]
            ]

        # Flatten User deck into one list
        pod = list(itertools.chain.from_iterable(playeronedeck))

        # Initiate User deck dictionary
        pO['deck'] = pod
        pO['hand'] = []
        pO['discard'] = []
        pO['active'] = []

        # Create User deck (list of lists)
        playertwodeck = [
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]
            ]

        # Flattens PC deck to one list
        ptd = list(itertools.chain.from_iterable(playertwodeck))

        # Initiate PC deck dictionary
        pC['deck'] = ptd
        pC['hand'] = []
        pC['discard'] = []
        pC['active'] = []

        # Creating supplements
        supplement = 10 * [Card('Levy', (1, 2), 2)]

        # Flatten central deck to one list
        deck = list(itertools.chain.from_iterable(sdc))
        random.shuffle(deck)

        # Create central deck dictionary
        central['deck'] = deck
        central['supplement'] = supplement
        central['active'] = []
        
        items = locals()
        return items.iteritems()
    
    def newgame(self):
        """
        Creates an dict.iteritem() of all initial game 
        parameters.
        
        Warning: This will return every item instanced in
        this function as it uses the local() method
        
        for item_name,item in self.initial:
            globals()[item_name] = item
        """
        pO = { # User settings
            'name': 'player one',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}
        
        pC = {# PC settings
            'name': 'player computer',
            'health': 30,
            'deck': None,
            'hand': None,
            'active': None,
            'handsize': 5,
            'discard': None}
        
        central = { # Central deck settings
            'name': 'central',
            'active': None,
            'activesize': 5,
            'supplement': None,
            'deck': None}
        
         # Changes are made in this list
        sdc = [ # Central deck cards
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
            2 * [Card('Assassin', (5, 0), 4)]
        ]
        
        # Changes are made in this list
        # User's deck
        playeronedeck = [8 * [Card('Serf', (0, 1), 0)],
                         2 * [Card('Squire', (1, 0), 0)]
                    ]
        
        # Flatten list to one list
        pod = list(itertools.chain.from_iterable(playeronedeck))
        
        # Initiate new dictionary
        pO['deck'] = pod
        pO['hand'] = []
        pO['discard'] = []
        pO['active'] = []
        
        # Changes are made in this list
        # Create PC deck (list of lists)
        playertwodeck = [
                    8 * [Card('Serf', (0, 1), 0)],
                    2 * [Card('Squire', (1, 0), 0)]
        ]
        
        # Flatten list of lists
        ptd = list(itertools.chain.from_iterable(playertwodeck))
        
        # Initiate PC deck dictionary
        pC['deck'] = ptd
        pC['hand'] = []
        pC['discard'] = []
        pC['active'] = []
        
        # Creating supplements 
        supplement = 10 * [Card('Levy', (1, 2), 2)]
        
        # Flatten central deck to one list
        deck = list(itertools.chain.from_iterable(sdc))
        random.shuffle(deck)
        
        # Initiate PC deck dictionary
        central['deck'] = deck
        central['supplement'] = supplement
        central['active'] = []
        
        items = locals()
        return items.iteritems()