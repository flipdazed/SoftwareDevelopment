#!/usr/bin/env python
# encoding: utf-8

from logs import *
logger = logging.getLogger(__name__)

from common import *
from game_art import Art

class __CentralLoggers(object):
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
class ___UserLoggers(object):
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
    def logger_new_desired(self):
        """ Displays the new most desired card by the computer
        when iterating through its wishlist
        Only used in Computer.turn()"""
        self.logger.debug("New desired card index: {}".format(self.potential_card_index))
        pass
# separates classes in my editor
@wrap_all(log_me)
class Central(CommonActions,__CentralLoggers):
    """The Central Deck Class"""
    def __init__(self, parent, hand_size, deck_settings, name, supplements):
        """initial settings for the central cards"""
        self.parent = parent
        
        self.art = Art() # create art for game
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        get_logger(self)
        self.player_logger = self.logger.game
        
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
    
    def print_supplements(self, index=False, logger=None):
        """Display supplements"""
        title = self.art.make_title("Supplements")
        supplement = str(self.supplements[0])
        
        # make the title of the supplements
        if logger:
            logger(title)
        else:
            self.player_logger(title)
        
        # print the supplements
        if len(self.supplements) == 0:
            self.logger.game(self.art.index_buffer+ \
            "Nothing interesting to see here...")
        else:
            num_str = "[S] " if index else self.art.index_buffer
            self.logger.game(num_str + "{}".format(supplement))
        
        # prints the underline
        self.player_logger(self.art.underline)
        pass
    def display_all_active(self):
        """displays both active cards and the supplements"""
        self.logger.game("")
        self.print_active_cards(title="Central Buyable Cards")
        self.print_supplements()
        pass
# separates classes in my editor
@wrap_all(log_me)
class User(CommonActions, CommonUserActions, ___UserLoggers):
    """The User Class"""
    def __init__(self, parent, hand_size, deck_settings, name, health):
        """initial settings for the User"""
        self.parent = parent
        self.art = Art() # create art for game
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        get_logger(self)
        self.player_logger = self.logger.user
        
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        
        # create newgame paramters
        self.newgame()
    
    def print_hand(self):
        """displays the indexed user hand"""
        
        # Display User hand
        self.player_logger("")
        self.player_logger(self.art.make_title("Your Hand"))
        self._print_cards(self.hand, index=True)
        self.player_logger(self.art.underline)
        
        pass
    def turn(self):
        """Contains the User Actions UI"""
        # iterators to count self.money
        # and attack in players' hands
        self.reset_vals() # resetes money / attack
        
        # a first message is shown as an example
        self.clear_delayed_messages()
        self.add_delayed_message("Play cards to build Money and Attack.",self.logger.game)
        self.add_delayed_message("Both Attack and Money will return to 0 at the end of your turn.", self.logger.game)
        
        # User's Turn
        while not self.parent.end():
            
            self.parent.clear_term()
            
            # Display health state
            self.parent.display_health_status()
            
            # display active deck and supplements
            self.parent.central.display_all_active()
            self.logger.game("")
            self.show_updated_user_state()
            
            self.print_delayed_messages()
            
            # In-game actions UI
            self.player_logger("")
            self.player_logger(self.art.choose_action)
            self.player_logger(self.art.card_options)
            self.player_logger(self.art.game_options)
            self.player_logger(self.art.underline)
            
            # get user input
            iuser_action = raw_input().upper()
            self.logger.debug("User Input: {}".format(iuser_action))
            
            if iuser_action == 'P':         # Play all cards
                self.logger.debug("Play all cards action selected (input: {}) ...".format(iuser_action))
                
                if(len(self.hand)>0):  # Are there cards in the hand
                    self.logger.debug("There are cards ({}) in the Users hand".format(len(self.hand)))
                    # transfer all cards from hand to active
                    # add values in hand to current totals
                    self.play_all_cards()
                else: # there are no cards in the user's hand
                    self.add_delayed_message(
                        "There are no cards currently in your hand to play!", self.logger.game)
                    self.logger.debug("There are cards ({}) in the Users hand".format(len(self.hand)))
                    
            elif iuser_action.isdigit():    # Play a specific card
                
                self.logger.debug("Play a single card action selected (input: {}) ...".format(iuser_action))
                
                # check the card number is valid
                if int(iuser_action) in xrange(0, len(self.hand)):
                    self.logger.debug("{} is a valid card number.".format(int(iuser_action)))
                    self.play_a_card(card_number=iuser_action)
                elif len(self.hand) == 0:
                    self.logger.game("There are no cards currently in your hand to play!")
                else:
                    self.logger.game("'{}' is not a valid option. Please try again.".format(iuser_action))
                
                self.__show_updated_user_state()
                
            elif (iuser_action == 'B'):     # Buy cards
                self.logger.debug("Buy Cards action selected (input: {}) ...".format(iuser_action))
                self.card_shop() # go to the shop to buy cards
                
            elif iuser_action == 'A':       # Attack
                self.logger.debug("Attack action selected (input: {}) ...".format(iuser_action))
                self.attack_player(self.parent.computer)
            
            elif iuser_action == 'E':       # Ends turn
                self.logger.debug("End Turn action selected (input: {}) ...".format(iuser_action))
                break
            elif iuser_action == 'Q':       # Quit Game
                self.logger.debug("User wants to quite the game")
                self.parent.hostile_exit()
            else:
                self.logger.debug(
                "No action matched to input (input: {}) ...".format(iuser_action))
                self.add_delayed_message(
                    "'{}' is not a valid option. Please try again.".format(iuser_action),
                    self.logger.game)
        
        # ends turn and prints debug message
        self.end_turn()
        pass
    def card_shop(self):
        """contains the shop for buying cards"""
        
        # clear any stored messages
        self.clear_delayed_messages(in_shop=True)
        
        # Check player has self.money available
        while self.money > 0: # no warning of no self.money
            self.parent.clear_term() # clear the screen
            # welcome to the shop
            self.logger.game(self.art.shop)
            self.logger.game(self.art.underline)
            self.logger.game("Cards bought here are added to your discard pile.")
            self.logger.game("You will have a random chance to pick them at each new turn.")
            self.logger.game("")
            
            self.logger.debug("Starting new purchase loop with money: {}".format(self.money))
            
            # Display central.central cards state
            self.parent.central.print_active_cards("Central Buyable Cards", index=True)
            self.parent.central.print_supplements(index=True)
            self.logger.game("")
            
            self.player_logger("Current money: {}".format(self.money))
            
            # display delayed messages
            self.print_delayed_messages(in_shop=True)
            
            # User chooses a card to purchase
            self.player_logger("")
            self.player_logger(self.art.choose_action)
            self.player_logger(self.art.shop_options)
            self.player_logger(self.art.underline)
            ibuy_input = raw_input().upper()
            
            self.logger.debug("User Input: {}".format(ibuy_input))
            
            if ibuy_input.isdigit() or ibuy_input == 'S': # users attempts to purcahse a card
                self.purchase_cards(ibuy_input)
            
            elif ibuy_input == 'E':         # User ends shopping spree
                self.logger.debug("End buying action selected (input: {}) ...".format(ibuy_input))
                break
            
            elif ibuy_input == 'Q':       # Quit Game
                self.logger.debug("User wants to quit the game")
                self.parent.hostile_exit()
            else:                           # cycle the shopping loop
                self.logger.debug("No action matched to input (input: {}) ...".format(ibuy_input))
                self.add_delayed_message(
                    "'{}' is not a valid option. Please try again.".format(ibuy_input),
                    self.logger.game, in_shop=True)
        
        self.logger.debug("Exiting the card shop")
        self.exit_card_shop()
        pass
    def purchase_cards(self, ibuy_input):
        """User purchases cards"""
        # Evaluate choice
        if ibuy_input == 'S': # Buy a supplement
            self.logger.debug("Buy supplement action selected (input: {}) ...".format(ibuy_input))
            self.buy_supplement() # buys a supplement subject to conditions - see function
        
        elif ibuy_input.isdigit(): # Buy a card
            self.logger.debug("Buy card {0} action selected (input: {0}) ...".format(ibuy_input))
            
            if int(ibuy_input) in xrange(0,len(self.parent.central.active)): # If card exists
                self.logger.debug("{} is a valid card number.".format(int(ibuy_input)))
                self.buy_card_by_index(ibuy_input)
            else:
                self.logger.debug("{} is not valid card number for card for range:0-{}".format(int(ibuy_input),len(self.parent.central.active)))
                self.add_delayed_message("Enter a valid index number", self.logger.game, in_shop=True)
        pass
    def buy_card_by_index(self, ibuy_input):
        """buys a particular card by index
        it is assumed that an evaluation has already been made to assess
        that the index is valid
        """
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
           
           self.add_delayed_message("Card bought", in_shop=True)
        else:
           self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False,wishlist=False)
           self.add_delayed_message(
               "Insufficient money to buy. Current money: {}".format(self.money),
               in_shop=True)
        pass
    def buy_supplement(self):
        """buys a supplement from the parent.central"""
        
        if len(self.parent.central.supplements) > 0: # If supplements exist
            self.logger.debug("Supplements Detected by {}".format(self.name))
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
                self.add_delayed_message("Supplement Bought.", in_shop=True)
            else:
                self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False,wishlist=False)
                self.add_delayed_message(
                    "Insufficient money to buy. Current money: {}".format(self.money),
                    in_shop=True)
        else:
            self.logger.debug("No Supplements available")
            self.add_delayed_message("No Supplements Left!", self.logger.game, in_shop=True)
        pass
    def show_updated_user_state(self):
        """Shows the updated / current user state"""
        self.print_active_cards()   # Display User active cards
        self.print_hand()           # Display User hand
        self.display_values()       # Display PC state
        pass
    
    def clear_delayed_messages(self, in_shop=False):
        """clears ready for turn"""
        
        if in_shop:
            self.delayed_shop_messages = []
        else:
            self.delayed_messages = []
        pass
    
    def add_delayed_message(self, msg, logger=None, in_shop=False):
        """add a delayed message"""
        if logger is None: logger = self.player_logger
        
        msg_dict = {"msg":msg, "logger":logger}
        if in_shop:
            self.delayed_shop_messages.append(msg_dict)
        else:
            self.delayed_messages.append(msg_dict)
        pass
    
    def print_delayed_messages(self, in_shop=False):
        """prints all the delayed messages"""
        if in_shop:
            iterator = self.delayed_shop_messages
        else:
            iterator = self.delayed_messages
        
        while iterator:
            item = iterator.pop()
            msg = item["msg"]
            logger = item["logger"]
            logger(msg) # use logger from dict to output message
        pass
    def exit_card_shop(self):
        """UI for exiting the card shop"""
        
        # user is ungracefully booted from shop
        if self.money == 0:
            self.parent.clear_term() # clear the screen
            # welcome to the shop
            self.logger.game(self.art.shop)
            self.logger.game(self.art.underline)
            self.logger.game("Cards bought here are added to your discard pile")
            self.logger.game("")
        
            self.print_delayed_messages(in_shop=True)
            self.logger.game("Unfortunately you have no remaining money...")
            self.logger.game("You are being kicked out of the shop.")
            self.parent.wait_for_user()
        else: # else user has a nice quick exit
            pass
        self.add_delayed_message("You return from the Shop.", self.logger.game)
        pass
# separates classes in my editor
@wrap_all(log_me)
class Computer(CommonActions, CommonUserActions, ___UserLoggers):
    """The Computer Player Class"""
    def __init__(self, parent, hand_size, deck_settings, name, health):
        """initial settings for the computer player"""
        self.parent = parent
        self.art = Art() # create art for game
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
        self.player_logger = self.logger.computer
        
        # create newgame paramters
        self.newgame()
    def turn(self):
        """contains the computer turn routines"""
        # Iterators to count money
        # and attack in User's hands
        self.parent.clear_term()
        self.reset_vals() # reset money and attack to zero
        
        # transfer all cards from hand to active
        # add values in hand to current totals
        self.play_all_cards()
        
        self.logger.debug("Storing computer values ready for attack")
        stored_attack = self.attack
        stored_money  = self.money
        
        # PC starts by attacking User
        self.attack_player(self.parent.user)
        
        # Display health state
        self.parent.display_health_status()
        
        # Display PC state
        self.logger.debug("Displaying stored computer values from before attack")
        self.display_values(stored_attack, stored_money)
        
        # Display PC state
        name_pad = self.parent.max_player_name_len
        self.player_logger(\
        "{}     Attacking!".format(self.name.ljust(name_pad)))
        self.parent.user.player_logger(\
        "{}     Suffered a beating of -{} Health".format(
                self.parent.user.name.ljust(name_pad),stored_attack))
        
        self.logger.debug("Displaying stored computer values from AFTER attack")
        self.display_values()
        
        computer_buys_title = self.art.make_title("{} Buying".format(self.name))
        self.player_logger(computer_buys_title)
        self.purchase_cards()
        self.player_logger(self.art.underline)
        self.player_logger("")
        
        self.end_turn()
        self.player_logger("{} turn ending".format(self.name))
        self.parent.wait_for_user()
        pass
    
    def purchase_cards(self):
        """This routine contains the actions required for the computer
        to make card purchases"""
        
        can_afford_cards = True
        if can_afford_cards and self.money > 0:   # Commence buying if PC has money 
            self.logger.debug("Starting new purchase loop with money: {}".format(self.money))
            self.player_logger("")
            self.player_logger("{} is browsing... Money: {}".format(
            self.name ,self.money))
            # Loop while cb, conditions:
            # len(self.wish_list) > 0 and money != 0
            # The temporary list of purchased
            # cards in the buying process
            self.wish_list = self.get_wish_list()
            
            if len(self.wish_list) > 0: # If more than one card was added to self.wish_list
                
                self.logger.debug("Wish list is not empty ({} cards)".format(len(self.wish_list)))
                self.desired_card_index = 0 # Index of most desirable card purchase
                
                # Loop through the temp list by index
                # Identifies the highest value item in the list
                # Prioritises on attack (self.aggressive) or self.money (greedy)
                # if equal values
                self.logger.debug("Finding the most desirable purchase...")
                self.desired = self.most_desirable_card_in_wishlist()
                
                # Contains two parts of information:
                # 1. If integer then it is a card from the active deck
                # 2. If non-integer then it is a supplement
                # 
                # If 1. then the integer may take a value
                # between 0 and up to (not including) the size
                # if the active deck
                card_index = self.desired[0]
                self.logger.debug("{0} attempts to purchase {1} (Index: {2})".format(self.name, *self.desired))
                self.buy_card_by_index(card_index)
                
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
            self.player_logger("No Money to buy anything")
        pass
    
    def buy_card_by_index(self, source):
        """Attempts to buy a card given a source
        
        Expected format of source = integer or 'S'"""
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
                
                self.logger.game("Card bought... {}".format(card))
                
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
                self.player_logger("Supplement Bought {}".format(card))
                
                new_money = - card.cost
                self.logger_buy_card(card, self.money, new_money)
                self.money += new_money
            else:
                self.logger_affords_card(1, purchase_card.name, purchase_card.cost, can_afford=False)
                self.logger.critical("Error Occurred")
        pass
    def get_wish_list(self):
        """Gets the list of cards that the computer wishes to try and buy"""
        self.wish_list = [] # This will be a list of tuples
        self.logger.debug("Temp purchase list (wish list) initiated")
        
        self.__add_affordable_supplements_to_wishlist()
        self.__add_affordable_cards_to_wishlist()
        
        return self.wish_list
    
    def most_desirable_card_in_wishlist(self):
        """This routine expects that self.wish_list exists in the format
            of [( val, Card() )]
            where val = integer or "S"
            It returns a single list element corresponding to the most desired card
            """
        desired = self.wish_list[self.desired_card_index]
        for self.potential_card_index in xrange(0,len(self.wish_list)):
            
            potential = self.wish_list[self.potential_card_index]
            self.logger.debug("Current most desired card: {}".format(desired[1].name))
            self.logger.debug("Comparing against potential card: {}".format(potential[1].name))
            
            self.card_selector_AI(desired, potential)
            desired = self.wish_list[self.desired_card_index]
        return desired
    
    def card_selector_AI(self, desired, potential):
        """The computer AI that decides which card it likes the most to buy
        between two cards provided
        
        This function relies on two key global variables:
            self.desired_card_index
            self.potential_card_index
        
        Expected format of desired, potential:
            ( val, Card() )
            where val = integer or "S"
        """
        
        # Primary comparison: Get most expensive card
        self.logger.debug("Primary comparison (Cost) ...")
        self.__primary_card_selector_AI(desired, potential)
        
        if potential[1].cost == desired[1].cost:
            # Secondary comparison: AI chosen strategy
            self.__secondary_card_selector_AI(desired, potential)
        else:
            self.logger.debug("Secondary comparison (Strategy Dependent) not undertaken.")
        pass 
    def __primary_card_selector_AI(self, desired, potential):
        """This is the first method that the computer uses to decide on a card purchase
    
        This function relies on two key global variables:
            self.desired_card_index
            self.potential_card_index
        
        Expected format of desired, potential:
            ( val, Card() )
            where val = integer or "S"
        """
        if potential[1].cost > desired[1].cost:
            self.desired_card_index = self.potential_card_index
    
            self.logger_compare_cards("cost", "is", potential[1].cost, desired[1].cost)
            self.logger_new_desired() # Log the action
        else:
            self.logger_compare_cards("cost", "is not", potential[1].cost, desired[1].cost)
        pass
    def __secondary_card_selector_AI(self, desired, potential):
        """This is the first method that the computer uses to decide on a card purchase
        
        This function uses the self.aggressive variable to decide how to proceeed
        
        This function relies on two key global variables:
            self.desired_card_index
            self.potential_card_index
        
        Expected format of desired, potential:
            ( val, Card() )
            where val = integer or "S"
        """
        self.logger.debug("Secondary comparison (Strategy Dependent)...")
        
        if self.aggressive:  # Aggresive strategy
            self.logger.debug("Using Aggressive strategy")
            self.__secondary_ai_aggressive_comparison(potential, desired)
        else:           # Greedy strategy
            self.logger.debug("Using Non-Aggressive strategy")
            self.__secondary_ai_nonaggressive_comparison(potential, desired)
            
        pass
    def __secondary_ai_nonaggressive_comparison(self, potential, desired):
        """This routine is used if the computer is set to aggressive
        
        This function relies on two key global variables:
            self.desired_card_index
            self.potential_card_index
        
        Expected format of desired, potential:
            ( val, Card() )
            where val = integer or "S"
        """
        # Set self.desired_card_index to this card if highest money
        if potential[1].get_attack() > desired[1].get_money():
            self.desired_card_index = self.potential_card_index
            
            self.logger_compare_cards("money", "is", potential[1].money, desired[1].money)
            self.logger_new_desired() # Log the action
        else:
            self.logger_compare_cards("money", "is not", potential[1].money, desired[1].money)
            
        pass
    def __secondary_ai_aggressive_comparison(self, potential, desired):
        """This routine is used if the computer is set to aggressive
        
        This function relies on two key global variables:
            self.desired_card_index
            self.potential_card_index
        
        Expected format of desired, potential:
            ( val, Card() )
            where val = integer or "S"
        """
        # Set self.desired_card_index to this card if highest attack
        if potential[1].get_attack() > desired[1].get_attack():
            self.desired_card_index = self.potential_card_index
            
            self.logger_compare_cards("attack", "is", potential[1].attack, desired[1].attack)
            self.logger_new_desired() # Log the action
        else:
            self.logger_compare_cards("attack", "is not", potential[1].attack, desired[1].attack)
        pass
    def __add_affordable_cards_to_wishlist(self):
        """adds the affordable cards the the wish_list
        expects that self.wish_list exists as a list
        """
        # Select cards where cost of card_i < money
        for self.potential_card_index in xrange(0, self.parent.central.hand_size):  # Loop all cards
        
            self.logger_new_desired() # Log the action
            card = self.parent.central.active[self.potential_card_index]
        
            if card.cost <= self.money:   # if PC has enough money
                # Add to temporary purchases
                self.wish_list.append((self.potential_card_index, card))
                self.logger_affords_card(1, card.name, card.cost)  # logger action
            else:
                self.logger_affords_card(1, card.name, card.cost, can_afford=False)  # logger action
        pass
    def __add_affordable_supplements_to_wishlist(self):
        """adds the affordable cards the the wish_list
        expects that self.wish_list exists as a list
        """
        # Select Supplements if cost < self.money
        if len(self.parent.central.supplements) > 0: # If there are any supplements
            self.logger.debug("Supplements Detected by {}".format(self.name))  # logger action
            
            card = self.parent.central.supplements[0]
            if card.cost <= self.money:      # If PC has enough money
                # Add to temporary purchases
                self.wish_list.append(("S", card))
                self.logger_affords_card(1, card.name, card.cost)  # logger action
            else:
                self.logger_affords_card(1, card.name, card.cost, can_afford=False)  # logger action
        else:
            self.logger.debug("No Supplements available")
        pass