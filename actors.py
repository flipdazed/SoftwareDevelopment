#!/usr/bin/env python
# encoding: utf-8

from logs import *
logger = logging.getLogger(__name__)

from common import *

class CommonCentralLoggers(object):
    """dumping ground for messy loggers
    from central"""
    def __init__(self):
        pass
    def logger_attr_set(self,attr,val):
        """Logs attribute and value cutting off at 10char
        used in Central().newgame()"""
        # logging
        str_val = str(val) # for logging
        if len(str_val) > 9:
            str_val=str_val[:10]
            self.logger.debug("Setting attribute {} to {} ... (shortened to 10 char)".format(attr, str_val))
        else:
            str_val
        pass
class CommonUserLoggers(object):
    """dumping ground for messy loggers
    from User and Computer"""
    def __init__(self):
        pass
    def logger_affords_card(self, num, name, cost, can_afford=True,wishlist=True):
        """ Displays if the actor can afford the card
        This is used both in User().turn() and Computer.turn()"""
        wishlist = " Added to wish list" if wishlist else ""
        afford = "can afford" if can_afford else "can not afford"
        self.logger.debug("{5} {4} {0}x{1} at cost:{2}.{3}".format(num, name, cost, wishlist, can_afford, self.name))
        pass
    def logger_buy_card(self,card, self_money, change_in_money):
        """ Displays the actor buying the card
        This is used both in User().turn() and Computer.turn()"""
        self.logger.debug("{3} bought 1x{0}, money:{1}+{2}".format(card.name, self_money, change_in_money,self.name))
        pass
    def logger_compare_cards(self, val_name, is_isnt, pot_val, des_val):
        """ Displays the comparison made by the Computer
         when picking cards for its wishlist
        Only used in Computer.turn()"""
        self.logger.debug("Potential card ({2}:{0}) {3} higher {2} than desired card ({2}:{1})".format(
            pot_val,des_val,val_name,is_isnt))
        pass
    def logger_new_desired(self, card_index):
        """ Displays the new most desired card by the computer
        when iterating through its wishlist
        Only used in Computer.turn()"""
        self.logger.debug("New desired card index: {}".format(card_index))
        pass
# separates classes in my editor
@wrap_all(log_me)
class Central(CommonActions,CommonCentralLoggers):
    """The Central Deck Class"""
    def __init__(self, parent, hand_size, deck_settings, name, supplements):
        """initial settings for the central cards"""
        self.parent = parent
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Central")
        self.logger.debug("Central Created.")
        
        self.hand_size = hand_size
        self.name = name
        self.deck_settings = deck_settings
        self.supplement_settings = supplements
        
        # create newgame paramters
        self.newgame()
        
    
    def newgame(self):
        """Initiates a new game by refreshing saved config parameters"""
            
        self.active = []
        
        # revert to initial state stored in self.init
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
            
            # this produces a log to the screen
            self.logger_attr_set(attr, val)
        
        # create new decks
        self.deck = self.deck_creator(self.deck_settings)
        self.supplements = self.deck_creator(self.supplement_settings)
        
        # shuffle decks
        random.shuffle(self.deck)
        
        pass
    
    def deck_to_active(self):
        """ moves cards from one item to another"""
        for i in xrange(0, self.hand_size):
            card = self.deck.pop()
            self.active.append(card)
            self.logger.debug('iteration #{}: Moving {} from deck to active'.format(i, card.name))
        pass
    
    def print_supplements(self):
        """Display supplements"""
        self.logger.game("Supplements")
        if len(self.supplements) > 0:
            self.logger.game(self.supplements[0])
        pass
    def display_all_active(self):
        """displays both active cards and the supplements"""
        self.print_active_cards()
        self.print_supplements()
        pass
# separates classes in my editor
@wrap_all(log_me)
class User(CommonActions, CommonUserActions, CommonUserLoggers):
    """The User Class"""
    def __init__(self, parent, hand_size, deck_settings, name, health):
        """initial settings for the User"""
        self.parent = parent
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        get_logger(self)
        
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        
        # create newgame paramters
        self.newgame()
    
    def print_hand(self):
        """displays the indexed user hand"""
        
        # Display User hand
        self.logger.game("")
        self.logger.game("Your Hand")
        self._print_cards(self.hand, index=True)
        
        pass
    def turn(self):
        """Contains the User Actions UI"""
        # iterators to count self.money
        # and attack in players' hands
        self.money = 0
        self.attack = 0
        
        while True: # User's Turn
            
            # Display health state
            self.logger.game("")
            self.show_health()
            self.parent.computer.show_health()
            
            # Display User hand
            self.print_hand()
            
            # In-game actions UI
            self.logger.game("")
            self.logger.game("Choose Action: (P = Play All Cards, [0-n] = Play Card by Index, B = Buy Card, A = Attack, E = End Turn)")
            iuser_action = raw_input().upper()
            self.logger.debug("User Input: {}".format(iuser_action))
            
            if iuser_action == 'P':      # Play all cards
                self.logger.debug("Play all cards action selected (input: {}) ...".format(iuser_action))
                
                if(len(self.hand)>0):  # Are there cards in the hand
                    self.logger.debug("There are cards ({}) in the Users hand".format(len(self.hand)))
                    # transfer all cards from hand to active
                    # add values in hand to current totals
                    self.play_all_cards()
                
                # Display User hand
                self.print_hand()
                
                # Display User active cards
                self.print_active_cards()
                
                # Display PC state
                self.display_values()
            
            elif iuser_action.isdigit():   # Play a specific card
                self.logger.debug("Play a single card action selected (input: {}) ...".format(iuser_action))
                
                if int(iuser_action) in xrange(0, len(self.hand)):
                    self.logger.debug("{} is a valid card number.".format(int(iuser_action)))
                    self.play_a_card(card_number=iuser_action)
                
                # Display User hand
                self.print_hand()
                
                # Display User active cards
                self.print_active_cards()
                
                # Display PC state
                self.display_values()
            
            elif (iuser_action == 'B'):    # Buy cards
                self.logger.debug("Buy Cards action selected (input: {}) ...".format(iuser_action))
                
                # Check player has self.money available
                while self.money > 0: # no warning of no self.money
                    self.logger.debug("Starting new purchase loop with money: {}".format(self.money))
                    
                    # Display central.central cards state
                    self.parent.central.print_active_cards(index=True)
                    
                    # User chooses a card to purchase
                    self.logger.game("")
                    self.logger.game("Choose a card to buy [0-n], S for supplement, E to end buying")
                    self.logger.game("Choose option: ")
                    ibuy_input = raw_input().upper()
                    self.logger.debug("User Input: {}".format(ibuy_input))
                    
                    # Evaluate choice
                    if ibuy_input == 'S': # Buy a supplement
                        self.logger.debug("Buy supplement action selected (input: {}) ...".format(ibuy_input))
                        if len(self.parent.central.supplements) > 0: # If supplements exist
                            self.logger.debug("Supplements Detected by Computer")
                            purchase_card = self.parent.central.supplements[0]
                            
                            # Buy if player has enough self.money
                            # Move to player's discard pile
                            if self.money >= purchase_card.cost:
                                self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=True,wishlist=False)
                                
                                card = self.parent.central.supplements.pop()
                                self.discard.append(card)
                                
                                new_money = - card.cost
                                self.logger_buy_card(card, self.money, new_money)
                                self.money += new_money
                                self.logger.game("Supplement Bought")
                            else:
                                self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False,wishlist=False)
                                self.logger.game("Insufficient money to buy")
                        else:
                            self.logger.debug("No Supplements available")
                            self.logger.game("No Supplements left")
                    
                    elif ibuy_input.isdigit(): # Buy a card
                        self.logger.debug("Buy card {0} action selected (input: {0}) ...".format(ibuy_input))
                        
                        if int(ibuy_input) in xrange(0,len(self.parent.central.active)): # If card exists
                             self.logger.debug("{} is a valid card number.".format(int(ibuy_input)))
                             
                             # Buy if User has enough self.money
                             # Move directly to discard pile
                             purchase_card = self.parent.central.active[int(ibuy_input)]
                             if self.money >= purchase_card.cost:
                                self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=True,wishlist=False)
                                
                                card = self.parent.central.active.pop(int(ibuy_input))
                                self.discard.append(card)
                                
                                new_money = - card.cost
                                self.logger_buy_card(card, self.money, new_money)
                                self.money += new_money
                                
                                # Refill active from self.parent.central.central deck
                                # if there are cards in self.parent.central.central
                                self.logger.debug("Attempting to refill card central active deck from central deck...")
                                if len(self.parent.central.deck) > 0:
                                    self.logger.debug("{} cards in central deck".format(len(self.parent.central.deck)))
                                    card = self.parent.central.deck.pop()
                                    self.parent.central.active.append(card)
                                    self.logger.debug("Moved 1x{} from {} to {}".format(card.name, "central deck", "central active deck"))
                                else:
                                    # If no cards in self.parent.central.central deck,
                                    # reduce activesize by 1
                                    self.logger.debug("No cards in central deck to refill central active deck.")
                                    self.logger.debug("central hand_size:{}-1".format(self.parent.central.hand_size))
                                    self.parent.central.hand_size -= 1
                                
                                self.logger.game("Card bought")
                             else:
                                self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False,wishlist=False)
                                self.logger.game("Insufficient money to buy")
                        else:
                            self.logger.debug("{} is not valid card number for card for range:0-{}".format(int(ibuy_input),len(self.parent.central.active)))
                            self.logger.game("Enter a valid index number")
                    elif ibuy_input == 'E': # User ends shopping spree
                        self.logger.debug("End buying action selected (input: {}) ...".format(ibuy_input))
                        break
                    else:
                        self.logger.debug("No action matched to input (input: {}) ...".format(ibuy_input))
                        self.logger.game("Enter a valid option")
            
            elif iuser_action == 'A':      # Attack
                self.logger.debug("Attack action selected (input: {}) ...".format(iuser_action))
                
                self.logger.debug("{} Health before attack: {}".format(self.parent.computer.name, self.parent.computer.health))
                self.parent.computer.health -= self.attack
                self.attack = 0
                self.logger.debug("{} Attack: {}".format(self.name, self.attack))
            
            elif iuser_action == 'E':      # Ends turn
                self.logger.debug("End Turn action selected (input: {}) ...".format(iuser_action))
                break
            else:
                self.logger.debug("No action matched to input (input: {}) ...".format(iuser_action))
            
        self.end_turn()
        pass
# separates classes in my editor
@wrap_all(log_me)
class Computer(CommonActions, CommonUserActions, CommonUserLoggers):
    """The Computer Player Class"""
    def __init__(self, parent, hand_size, deck_settings, name, health):
        """initial settings for the computer player"""
        self.parent = parent
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # intialise params
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        self.aggressive = True
        
        # logging
        get_logger(self)
        
        # create newgame paramters
        self.newgame()
    def turn(self):
        """contains the computer turn routines"""
        # Iterators to count money
        # and attack in User's hands
        self.money = 0
        self.attack = 0
        
        # transfer all cards from hand to active
        # add values in hand to current totals
        self.play_all_cards()
        
        # Display PC state
        self.display_values()
        
        # PC starts by attacking User
        self.logger.debug("{} Health before attack: {}".format(self.parent.user.name, self.parent.user.health))
        self.logger.game("{} attacking with strength {}".format(self.name, self.attack))
        self.parent.user.health -= self.attack
        self.attack = 0
        self.logger.debug("{} Attack: {}".format(self.name, self.attack))
        
        # Display health state
        self.logger.game("")
        self.parent.user.show_health()
        self.show_health()
        
        # Display PC state
        self.display_values()
        
        self.logger.game("{} buying".format(self.name))
        self.purchase_cards()
        
        self.end_turn()
        self.logger.game("{} turn ending".format(self.name))
        pass
    
    def purchase_cards(self):
        """This routine contains the actions required for the computer
        to make card purchases"""
        
        can_afford_cards = True
        if can_afford_cards and self.money > 0:   # Commence buying if PC has money 
            self.logger.debug("Starting new purchase loop with money: {}".format(self.money))
            self.logger.game("{} making buying cards... Money {}".format(self.name ,self.money))
            # Loop while cb, conditions:
            # len(self.wish_list) > 0 and money != 0
            # The temporary list of purchased
            # cards in the buying process
            self.wish_list = [] # This will be a list of tuples
            self.logger.debug("Temp purchase list (wish list) initiated")
            
            # Select Supplements if cost < self.money
            if len(self.parent.central.supplements) > 0:                  # If there are any supplements
                self.logger.debug("Supplements Detected by {}".format(self.name))
                
                card = self.parent.central.supplements[0]
                if card.cost <= self.money:      # If PC has enough money
                    # Add to temporary purchases
                    self.wish_list.append(("S", card))
                    self.logger_affords_card(1, card.name, card.cost)
                else:
                    self.logger_affords_card(1, card.name, card.cost, can_afford=False)
            else:
                self.logger.debug("No Supplements available")
            
            # Select cards where cost of card_i < money
            for card_index in xrange(0, self.parent.central.hand_size):  # Loop all cards
                
                self.logger_new_desired(card_index)
                card = self.parent.central.active[card_index]
                
                if card.cost <= self.money:   # if PC has enough money
                    # Add to temporary purchases
                    self.wish_list.append((card_index, card))
                    self.logger_affords_card(1, card.name, card.cost)
                else:
                    self.logger_affords_card(1, card.name, card.cost, can_afford=False)
                
            if len(self.wish_list) > 0: # If more than one card was added to self.wish_list
                
                self.logger.debug("Wish list is not empty ({} cards)".format(len(self.wish_list)))
                highestIndex = 0 # Index of most desirable card purchase
                
                # Loop through the temp list by index
                # Identifies the highest value item in the list
                # Prioritises on attack (self.aggressive) or self.money (greedy)
                # if equal values
                self.logger.debug("Finding the most desirable purchase...")
                for card_index in xrange(0,len(self.wish_list)):
                    
                    desired = self.wish_list[highestIndex]
                    potential = self.wish_list[card_index]
                    self.logger.debug("Current most desired card: {}".format(desired[1].name))
                    self.logger.debug("Comparing against potential card: {}".format(potential[1].name))
                    
                    # Primary comparison: Get most expensive card
                    if potential[1].cost > desired[1].cost:
                        self.logger.debug("Primary comparison (Cost) ...")
                        highestIndex = card_index
                        
                        self.logger_compare_cards("cost", "is", potential[1].cost, desired[1].cost)
                        self.logger_new_desired(highestIndex)
                    else:
                        self.logger.debug("Primary comparison (Cost) not undertaken.")
                    
                    # Secondary comparison: AI chosen strategy
                    if potential[1].cost == desired[1].cost:
                        self.logger.debug("Secondary comparison (Strategy Dependent)...")
                        
                        if self.aggressive:  # Aggresive strategy
                            self.logger.debug("Using Aggressive strategy")
                            # Set highestIndex to this card if highest attack
                            if potential[1].get_attack() > desired[1].get_attack():
                                highestIndex = card_index
                                
                                self.logger_compare_cards("attack", "is", potential[1].attack, desired[1].attack)
                                self.logger_new_desired(highestIndex)
                            else:
                                self.logger_compare_cards("attack", "is not", potential[1].attack, desired[1].attack)
                        
                        else:           # Greedy strategy
                            self.logger.debug("Using Non-Aggressive strategy")
                            # Set highestIndex to this card if highest money
                            if potential[1].get_attack() > desired[1].get_money():
                                highestIndex = card_index
                                
                                self.logger_compare_cards("money", "is", potential[1].money, desired[1].money)
                                self.logger_new_desired(highestIndex)
                            else:
                                self.logger_compare_cards("money", "is not", potential[1].money, desired[1].money)
                    else:
                        self.logger.debug("Secondary comparison (Strategy Dependent) not undertaken.")
                
                # Contains two parts of information:
                # 1. If integer then it is a card from the active deck
                # 2. If non-integer then it is a supplement
                # 
                # If 1. then the integer may take a value
                # between 0 and up to (not including) the size
                # if the active deck
                source = desired[0]
                self.logger.debug("{0} attempts to purchase {1} (Index: {2})".format(self.name, *desired))
                
                # This is a card from the active deck
                if source in xrange(0,self.parent.central.hand_size):
                    purchase_card = self.parent.central.active[int(source)]
                    
                    self.logger.debug("Index: {} found in Central Hand ({}, cost:{})".format(
                        source, purchase_card.name, purchase_card.cost))
                    
                    # If PC has money to purchase:
                    # comparison has alrady been made
                    if self.money >= purchase_card.cost:
                        self.logger_affords_card(1, purchase_card.name, purchase_card.cost, wishlist=False)
                        
                        # Add card to PC discard pile
                        card = self.parent.central.active.pop(int(source))
                        self.discard.append(card)
                        
                        self.logger.game("Card bought {}".format(card))
                        
                        new_money = - card.cost
                        self.logger_buy_card(card, self.money, new_money)
                        self.money += new_money
                        
                        # Refill active from self.parent.central.central deck
                        # if there are cards in self.parent.central.central
                        self.logger.debug("Attempting to refill card central active deck from central deck...")
                        if len(self.parent.central.deck) > 0:
                            self.logger.debug("{} cards in central deck".format(len(self.parent.central.deck)))
                            card = self.parent.central.deck.pop()
                            self.parent.central.active.append(card)
                            self.logger.debug("Moved 1x{} from {} to {}".format(card.name, "central deck", "central active deck"))
                        else:
                            # If no cards in self.parent.central.central deck,
                            # reduce activesize by 1
                            self.logger.debug("No cards in central deck to refill central active deck.")
                            self.logger.debug("central hand_size:{}-1".format(self.parent.central.hand_size))
                            self.parent.central.hand_size -= 1
                            
                    else:
                        self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False)
                        self.logger.critical("Error Occurred")
                
                else: # This is a supplement as it is not in the range [0,5]
                    # If PC has money to purchase:
                    # comparison has alrady been made
                    purchase_card = self.parent.central.supplements[0]
                    
                    if self.money >= purchase_card.cost:
                        self.logger_affords_card(1, purchase_card.name, purchase_card.cost, wishlist=False)
                        
                        card = self.parent.central.supplements.pop()
                        self.discard.append(card)
                        self.logger.game("Supplement Bought {}".format(card))
                        
                        new_money = - card.cost
                        self.logger_buy_card(card, self.money, new_money)
                        self.money += new_money
                    else:
                        self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False)
                        self.logger.critical("Error Occurred")
                
                # ^Loop: Buy another card
            else:           # Exit loop if PC couldn't buy any cards
                can_afford_cards = False # this could be a break statement but this ismore obvious
                self.logger.debug("Wish list is empty ({} cards)".format(len(self.wish_list)))
                
            if self.money == 0:  # Exit loop if no money
                # This is a subcomparison that of the above
                # This will just exit the loop 1 cycle earlier
                self.logger.debug("{} has no money. Exiting wish list loop (money: {})".format(self.name, self.money))
        else:           # Don't buy if no money
            self.logger.debug("{} has no money. Exiting purchase loop with money: {}".format(self.name, self.money))
            self.logger.game("No Money to buy anything")
        pass