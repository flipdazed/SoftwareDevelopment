# This is a python testing file
from config import *
import itertools, random

class Settings(object):
    def __init__(self):
        """run tests"""
        self.runAll()
        pass
    
    def runAll(self, display=True):
        """Runs all functions"""
        self.all_tests = ["importing"]
        
        # loop through all functions
        # and get results - store in a dictionary
        # prints out if display=True
        for func_name in self.all_tests:
            res = getattr(self, func_name)()
            if display: print "Test: {} - {}".format(func_name, res)
        
        pass
    
    def importing(self):
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