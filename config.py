# This class contains and builds the decks used in the game
from logs import *
import itertools, random
import collections
logger = logging.getLogger(__name__)

logger.debug("imported configurations")


defaults = {
    "central":{
        "name":'Central', #"Central",
        "hand_size":5,
        "deck_settings":[ # Central deck paramss
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
        ,"supplements": 
            [{"count":10 ,"params":{"name":'Levy', "attack":1, "money":2, "cost":2}}]
        }
    ,"user":{
        "name":'Lord Vadar',  #"Player One",
        "health":30,
        "hand_size":5,
        "deck_settings":[ # User's deck
            {"count":8 ,"params":{"name":'Serf', "attack":0, "money":1, "cost":0}},
            {"count":2 ,"params":{"name":'Squire', "attack":1, "money":0, "cost":0}}
            ]
        }
    ,"computer":{
        "name": 'Computer', #"Computer Player",
        "health":30,
        "hand_size":5,
        "deck_settings":[ # computer deck
            {"count":8 ,"params":{"name":'Serf', "attack":0, "money":1, "cost":0}},
            {"count":2 ,"params":{"name":'Squire', "attack":1, "money":0, "cost":0}}
            ]
        }
    }