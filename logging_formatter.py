#!/usr/bin/env python
# encoding: utf-8
import logging
import sys

### Create new Logging level for game messages ###
# set up custom logging level or game output
GAME = 25
logging.addLevelName(GAME, "GAME")
logging.GAME = GAME
def game(self, message, *args, **kwargs):
    # Yes, logger takes its '*args' as 'args'
    if self.isEnabledFor(GAME):
        self._log(GAME, message, args, **kwargs)
logging.Logger.game = game
### End creation of new logging level ####

# Custom formatter for logging
# http://stackoverflow.com/a/8349076/4013571
class MyFormatter(logging.Formatter):
    """Class to create custom formats"""
    err_fmt  = "ERROR: %(module)s: %(lineno)d: %(msg)s"
    dbg_fmt  = "DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "INFO: %(module)s: %(msg)s"
    game_fmt = "GAME: %(msg)s"
    
    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)

    
    def format(self, record):
        
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt
        
        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = MyFormatter.dbg_fmt
        elif record.levelno == logging.INFO:
            self._fmt = MyFormatter.info_fmt
        elif record.levelno == logging.GAME: # This is for the game messages
            self._fmt = MyFormatter.game_fmt
        elif record.levelno >= logging.ERROR:
            self._fmt = MyFormatter.err_fmt
        
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)
        
        # Restore the original format configured by the user
        self._fmt = format_orig
        
        return result

fmt = MyFormatter()
hdlr = logging.StreamHandler(sys.stdout)

hdlr.setFormatter(fmt)
logging.root.addHandler(hdlr)