# This is a python testing file
from engine import *
import itertools, random
import collections
import logging
loglevel=logging.DEBUG

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
        self.logger.setLevel(loglevel)
        self.logger.info('Logger started.')
        
        # create classes of users and central deck
        self.central = Central()
        self.user = User()
        self.computer = Computer()
        
        # runs all tests
        tests = [
            "newgame_settings",
            "replay_settings"]
        
        self.run_tests(tests)
        pass
    
    def run_tests(self, tests, display=True):
        """Runs all functions"""
        
        # loop through all functions
        # and get results - store in a dictionary
        # prints out if display=True
        for func_name in tests:
            self.logger.info("Running Test: {}".format(func_name))
            res = getattr(self, func_name)()
            
            if res: 
                self.logger.error("Test Failed: {}".format(func_name)) 
            else:
                self.logger.info("Test Passed: {}".format(func_name))
        
        pass
    
    def newgame_settings(self):
        """Tests that new game settings match the original game settings"""
        
        self.computer.newgame()
        self.user.newgame()
        self.central.newgame()
        
        test_attrs = {
            'computer':self.computer.__dict__,
            'user':self.user.__dict__,
            'central':self.central.__dict__}
        
        
        # loop through all variables
        original_settings = self.__original_newgame_settings()
        error = self.__loop_compare(original_settings, test_attrs)
        return error
    
    def replay_settings(self):
        """Tests that replay game settings match the original game settings"""
        
        # create parameters for tests
        self.computer.replay()
        self.user.replay()
        self.central.replay()
        
        test_attrs = {
            'computer':self.computer.__dict__,
            'user':self.user.__dict__,
            'central':self.central.__dict__}
        
        # loop through all variables
        original_settings = self.__original_replay_settings()
        error = self.__loop_compare(original_settings, test_attrs)
        return error
    
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
                print "Couldn't find attr: {}".format(item_name)
                error=True
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
        
        a = [i.__dict__ if isinstance(i,Card) else i \
            for i in flatten(a)]
        
        b = [i.__dict__ if isinstance(i,Card) else i \
            for i in flatten(b)]
        
        # must sort the variables to ensure correct comparision
        a = sorted(a)
        b = sorted(b)
        
        # are both items the same
        same = (b == a)
        return same
    def __original_newgame_settings(self):
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
        return items

    def __original_replay_settings(self):
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
        return items
    
    def __redundant__importing(self):
        """tests that the class is imported as expected"""
        
        # Attempt to obtain a Card object
        test = Card('Archer', (3, 0), 2)
        
        assert type(test).__name__ == 'Card'    # test class importing
        
        # get configuration
        config = GetConfig()
        # set global variables from config iterable
        for item_name,item in config.initial:
            globals()[item_name] = item
        
        # test value
        playeronedeck_test = [
            8 * [Card('Serf', (0, 1), 0)],
            2 * [Card('Squire', (1, 0), 0)]
            ]
        
        # check imported values are the same as expected
        assert playeronedeck[0][0].__dict__ == playeronedeck_test[0][0].__dict__
        
        # will only return if all assertions succeed
        return True
        

if __name__ == '__main__':
    test = Settings()