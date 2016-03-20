# This is a python testing file
import config
import game_engine
from game_engine import Card
from logs import *

import itertools, random
import collections

logger = logging.getLogger(__name__)


def flatten(l):
    """This flattens arbitrarily annoying lists / dicts"""
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

class Settings(object):
    """This contains the tests related to the game settings"""
    def __init__(self):
        """run tests"""
        
        # creates a logger for the test file
        self.logger = logging.getLogger(__name__+".Settings")
        self.logger.info('Logger started.')
        
        # create classes of users and central deck
        self.engine = game_engine.Central(**config.defaults['engine'])
        self.user = game_engine.User(**config.defaults['user'])
        self.computer = game_engine.Computer(**config.defaults['computer'])
        
        # runs all tests
        tests = [
            "newgame_settings",
            "deck_creator"
            ]
        
        self.run_tests(tests)
        pass
    
    def run_tests(self, tests, display=True):
        """Runs all functions"""
        
        self.logger.info("Begin Testing Cycle\n")
        # loop through all functions
        # and get results - store in a dictionary
        # prints out if display=True
        for func_name in tests:
            self.logger.info("Running Test: {}".format(func_name))
            func = getattr(self, func_name)
            self.logger.debug(func.__doc__)
            res = func()
            
            if res: 
                self.logger.error("Test Failed: {}".format(func_name)) 
            else:
                self.logger.info("Test Passed: {}".format(func_name))
        
        pass
    
    def deck_creator(self):
        """Tests the deck creator can correctly create Card() classes"""
        
        class __Card(object):
            """Original Card Class"""
            
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
        
        def expected():
            """Taken directly from original game code"""
            sdc = [ # Central deck cards
                    4 * [__Card('Archer', (3, 0), 2)],
                    4 * [__Card('Baker', (0, 3), 2)],
                    3 * [__Card('Swordsman', (4, 0), 3)],
                    2 * [__Card('Knight', (6, 0), 5)],
                    3 * [__Card('Tailor', (0, 4), 3)],
                    3 * [__Card('Crossbowman', (4, 0), 3)],
                    3 * [__Card('Merchant', (0, 5), 4)],
                    4 * [__Card('Thug', (2, 0), 1)],
                    4 * [__Card('Thief', (1, 1), 1)],
                    2 * [__Card('Catapult', (7, 0), 6)],
                    2 * [__Card('Caravan', (1, 5), 5)],
                    2 * [__Card('Assassin', (5, 0), 4)]]
            
            # Flatten central deck to one list
            deck = list(itertools.chain.from_iterable(sdc))
            return deck
        
        
        deck_settings = [ # Central deck paramss
            {"count":4 ,"params":{"name":'Archer', "attack":3, "money":0, "cost":2}},
            {"count":4 ,"params":{"name":'Baker', "attack":0, "money":3, "cost":2}},
            {"count":3 ,"params":{"name":'Swordsman', "attack":4, "money":0, "cost":3}},
            {"count":2 ,"params":{"name":'Knight', "attack":6, "money":0, "cost":5}},
            {"count":3 ,"params":{"name":'Tailor', "attack":0, "money":4, "cost":3}},
            {"count":3 ,"params":{"name":'Crossbowman', "attack":4, "money":0, "cost":3}},
            {"count":3 ,"params":{"name":'Merchant', "attack":0, "money":5, "cost":4}},
            {"count":4 ,"params":{"name":'Thug', "attack":2, "money":0, "cost":1}},
            {"count":4 ,"params":{"name":'Thief', "attack":1, "money":1, "cost":1}},
            {"count":2 ,"params":{"name":'Catapult', "attack":7, "money":0, "cost":6}},
            {"count":2 ,"params":{"name":'Caravan', "attack":1, "money":5, "cost":5}},
            {"count":2 ,"params":{"name":'Assassin', "attack":5, "money":0, "cost":4}}
            ]
        
        # create deck
        test_deck = self.user.deck_creator(deck_settings)
        # create expected output
        expected_deck = expected()
        
        # routine returns true if success so result must be not True
        error = not self.compare_vals(test_deck, expected_deck)
        
        return error
    
    def newgame_settings(self):
        """Tests that new game settings match the original game settings"""
        
        self.computer.newgame()
        self.user.newgame()
        self.engine.newgame()
        
        central = { # Central deck settings
                'name': self.engine.name,
                'active': self.engine.active,
                'activesize': self.engine.hand_size,
                'supplement': self.engine.supplements,
                'deck': self.engine.deck}
        # Initial settings
        pO = { # User settings
            'name': self.user.name,
            'health': self.user.health,
            'deck': self.user.deck,
            'hand': self.user.hand,
            'active': self.user.active,
            'handsize': self.user.hand_size,
            'discard': self.user.discard}
        
        # Initial settings
        pC = { # User settings
            'name': self.computer.name,
            'health': self.computer.health,
            'deck': self.computer.deck,
            'hand': self.computer.hand,
            'active': self.computer.active,
            'handsize': self.computer.hand_size,
            'discard': self.computer.discard}
        
        test_attrs = {
            "computer":{'pC':pC},
            "player":{'pO':pO},
            "Engine":{'central':central}}
        
        # loop through all variables
        original_settings = self.__original_newgame_settings()
        error = self.__loop_compare(original_settings, test_attrs)
        return error

    def compare_vals(self, a, b):
        """Compares values from the game
        
        Input::
        a,b :: Iterables - recursive allowed can contain Card()
        
        Output::
        same :: boolean - True if items seem the same
        
        Creates a list of flattened parameters using 
        the function flattened()
        
        This returns most values but Card() remain.
        Fundamentally, Card() contain the parameters we
        need to check so an isinstance() and __dict__ rip
        open each and every Card()'s attributes
        
        We then compare sorted lists.
        """
        
        same = False
        
        # create unsorted flattened lists for a and b
        
        a = [i.__dict__ if 'class' in str(type(i)) else i for i in flatten(a)]
        b = [i.__dict__ if 'class' in str(type(i)) else i for i in flatten(b)]
        
        # must sort the variables to ensure correct comparision
        a = sorted(a)
        b = sorted(b)
        
        # are both items the same
        same = (b == a)
        return same
    def __loop_compare(self, original_settings, test_attrs):
        """combined functionality for initial settings comparision
        
        Used in:
            self.replay_settings()
            self.newgame_settings()
            
        compares values from the two input lists
        """
        
        error = False
                
        for item_name,item in original_settings.iteritems():
            if item_name == 'self': continue # don't compare self!
            # loop through each class and find the class that contains
            # the variable - check it is correct and verify vairables
            in_class = None
            attr_is_same = False
            for class_name,class_attrs in test_attrs.iteritems():
                
                # see if variable is in class
                if item_name in class_attrs.keys():
                    in_class = class_name
                    
                    if in_class: 
                        attr_is_same = self.compare_vals(class_attrs[item_name], item)
                        
            
            # report error status
            if in_class:
                
                if attr_is_same: 
                    self.logger.debug("Items are same. Found {0} in {1}".format(
                        item_name, in_class, attr_is_same))
                else:
                    error = True
                    self.logger.warning("Items not same. Found {0} in {1}".format(
                        item_name, in_class, attr_is_same))
            else:
                self.logger.warning("Couldn't find attr: {}".format(item_name))
                error=True
        return error
    
    def __original_newgame_settings(self):
        """
        Creates an dict.iteritem() of all initial game 
        parameters.
    
        Warning: This will return every item instanced in
        this function as it uses the local() method
    
        for item_name,item in self.initial:
            globals()[item_name] = item
        """
        
        class __old_Card(object):
            def __init__(self, name, values=(0, 0), cost=1, clan=None):
                self.name = name
                self.cost = cost
                self.values = values
                self.clan = clan
            def __str__(self):
                        return 'Name %s costing %s with attack %s and money %s' % (self.name, self.cost, self.values[0], self.values[1])
            def get_attack(self):
                return self.values[0]
            def get_money(self):
                    return self.values[1]
        
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
                4 * [__old_Card('Archer', (3, 0), 2)],
                4 * [__old_Card('Baker', (0, 3), 2)],
                3 * [__old_Card('Swordsman', (4, 0), 3)],
                2 * [__old_Card('Knight', (6, 0), 5)],
                3 * [__old_Card('Tailor', (0, 4), 3)],
                3 * [__old_Card('Crossbowman', (4, 0), 3)],
                3 * [__old_Card('Merchant', (0, 5), 4)],
                4 * [__old_Card('Thug', (2, 0), 1)],
                4 * [__old_Card('Thief', (1, 1), 1)],
                2 * [__old_Card('Catapult', (7, 0), 6)],
                2 * [__old_Card('Caravan', (1, 5), 5)],
                2 * [__old_Card('Assassin', (5, 0), 4)]
            ]

        # User's deck
        playeronedeck = [
            8 * [__old_Card('Serf', (0, 1), 0)],
            2 * [__old_Card('Squire', (1, 0), 0)]
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
            8 * [__old_Card('Serf', (0, 1), 0)],
            2 * [__old_Card('Squire', (1, 0), 0)]
            ]

        # Flattens PC deck to one list
        ptd = list(itertools.chain.from_iterable(playertwodeck))

        # Initiate PC deck dictionary
        pC['deck'] = ptd
        pC['hand'] = []
        pC['discard'] = []
        pC['active'] = []

        # Creating supplements
        supplement = 10 * [__old_Card('Levy', (1, 2), 2)]

        # Flatten central deck to one list
        deck = list(itertools.chain.from_iterable(sdc))
        random.shuffle(deck)

        # Create central deck dictionary
        central['deck'] = deck
        central['supplement'] = supplement
        central['active'] = []
    
        # items = locals()
        # only want to return pC, pO and central
        items = {"pC":pC,"pO":pO,"central":central}
        return items


if __name__ == '__main__':
    test = Settings()