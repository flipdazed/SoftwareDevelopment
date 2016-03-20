# This file contains the initial config data
import sys
import inspect

from logs import *
from common import *
logger = logging.getLogger(__name__)

# separates classes in my editor
@wrap_all(log_me)
class Central(CommonActions):
    """The Central Deck Class"""
    
    def __init__(self, hand_size, deck_settings, name, supplements):
        """initial settings for the central cards"""
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Central")
        self.logger.debug("Central Created.")
        
        # my name
        self.whoami = 'central'
        
        self.hand_size = hand_size
        self.name = name
        self.deck_settings = deck_settings
        self.supplement_settings = supplements
        
        # create newgame paramters
        self.newgame()
        
    
    def newgame(self):
        """Initiates a new game by refreshing saved config parameters"""
        
        def log_attr_set(self,attr,val):
            """Logs attribute and value cutting off at 10char"""
            # logging
            str_val = str(val) # for logging
            if len(str_val) > 9:
                str_val=str_val[:10]
                self.logger.debug("Setting attribute {} to {} ... (shortened to 10 char)".format(attr, str_val))
            else:
                str_val
            pass
            
        self.active = []
        
        # revert to initial state
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
            log_attr_set(self, attr, val)
        
        self.deck = self.deck_creator(self.deck_settings)
        self.supplements = self.deck_creator(self.supplement_settings)
        
        random.shuffle(self.deck)
        
        pass
    
    def deck_to_active(self):
        """ moves cards from one item to another"""
        count = 0
        
        while count < self.hand_size:
            card = self.deck.pop()
            self.active.append(card)
            self.logger.debug('iteration #{}: Moving {} from deck to active'.format(count, card.name))
            count += 1
        pass
    
    def print_supplements(self):
        """Display supplements"""
        print "Supplement"
        if len(self.supplements) > 0:
            print self.supplements[0]
        pass
    def display_all_active(self):
        """displays both active cards and the supplements"""
        self.print_active_cards()
        self.print_supplements()
        pass
# separates classes in my editor
@wrap_all(log_me)
class User(CommonActions, CommonUserActions):
    """The User Class"""
    
    def __init__(self, hand_size, deck_settings, name, health):
        """initial settings for the User"""
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # logging
        self.logger = logging.getLogger(__name__ + ".User")
        self.logger.debug("User Created.")
        
        # my name
        self.whoami = 'pO'
        
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        
        # create newgame paramters
        self.newgame()
    
    def print_hand(self):
        """displays the indexed user hand"""
        
        # Display User hand
        print "\nYour Hand"
        self._print_cards(self.hand, index=True)
        pass
    def turn(self, central, computer):
        """Contains the User Actions UI"""
        # iterators to count self.money
        # and attack in players' hands
        self.money = 0
        self.attack = 0
        
        while True: # User's Turn
            
            # Display health state
            print "" # Temporary until UI Fix
            self.show_health()
            computer.show_health()
            
            # Display User hand
            self.print_hand()
            
            # In-game actions UI
            print "\nChoose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)"
            iuser_action = raw_input("Enter Action: ").upper()
            self.logger.debug("User Input: {}".format(iuser_action))
            
            if iuser_action == 'P':      # Play all cards
                self.logger.debug("Play all cards action selected (input: {}) ...".format(iuser_action))
                self.hand == self.hand
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
                
                def log_affords_card(self, num, name, cost, can_afford=True,wishlist=True):
                    wishlist = " Added to wish list" if wishlist else ""
                    afford = "can afford" if can_afford else "can not afford"
                    self.logger.debug("{5} {4} {0}x{1} at cost:{2}.{3}".format(num,name, cost, wishlist, can_afford, self.name))
                    pass
                
                def log_buy_card(self,card, self_money, change_in_money):
                    self.logger.debug("{3} bought 1x{0}, money:{1}+{2}".format(card.name, self_money, change_in_money,self.name))
                    pass
                
                # Check player has self.money available
                while self.money > 0: # no warning of no self.money
                    self.logger.debug("Starting new purchase loop with money: {}".format(self.money))
                    
                    # Display central.central cards state
                    central.print_active_cards(index=True)
                    
                    # User chooses a card to purchase
                    print "Choose a card to buy [0-n], S for supplement, E to end buying"
                    ibuy_input = raw_input("Choose option: ").upper()
                    self.logger.debug("User Input: {}".format(ibuy_input))
                    
                    # Evaluate choice
                    if ibuy_input == 'S': # Buy a supplement
                        self.logger.debug("Buy supplement action selected (input: {}) ...".format(ibuy_input))
                        if len(central.supplements) > 0: # If supplements exist
                            self.logger.debug("Supplements Detected by Computer")
                            purchase_card = central.supplements[0]
                            
                            # Buy if player has enough self.money
                            # Move to player's discard pile
                            if self.money >= purchase_card.cost:
                                log_affords_card(self, 1, purchase_card.name, purchase_card.cost, can_afford=True,wishlist=False)
                                
                                card = central.supplements.pop()
                                self.discard.append(card)
                                
                                new_money = - card.cost
                                log_buy_card(self, card, self.money, new_money)
                                self.money += new_money
                                print "Supplement Bought"
                            else:
                                log_affords_card(self, 1, purchase_card.name, purchase_card.cost, can_afford=False,wishlist=False)
                                print "Insufficient money to buy"
                        else:
                            self.logger.debug("No Supplements available")
                            print "No Supplements left"
                    
                    elif ibuy_input.isdigit(): # Buy a card
                        self.logger.debug("Buy card {0} action selected (input: {0}) ...".format(ibuy_input))
                        
                        if int(ibuy_input) in xrange(0,len(central.active)): # If card exists
                             self.logger.debug("{} is a valid card number.".format(int(ibuy_input)))
                             
                             # Buy if User has enough self.money
                             # Move directly to discard pile
                             purchase_card = central.active[int(ibuy_input)]
                             if self.money >= purchase_card.cost:
                                log_affords_card(self, 1, purchase_card.name, purchase_card.cost, can_afford=True,wishlist=False)
                                
                                card = central.active.pop(int(ibuy_input))
                                self.discard.append(card)
                                
                                new_money = - card.cost
                                log_buy_card(self, card, self.money, new_money)
                                self.money += new_money
                                
                                # Refill active from central.central deck
                                # if there are cards in central.central
                                self.logger.debug("Attempting to refill card central active deck from central deck...")
                                if len(central.deck) > 0:
                                    self.logger.debug("{} cards in central deck".format(len(central.deck)))
                                    card = central.deck.pop()
                                    central.active.append(card)
                                    self.logger.debug("Moved 1x{} from {} to {}".format(card.name, "central deck", "central active deck"))
                                else:
                                    # If no cards in central.central deck,
                                    # reduce activesize by 1
                                    self.logger.debug("No cards in central deck to refill central active deck.")
                                    self.logger.debug("central hand_size:{}-1".format(central.hand_size))
                                    central.hand_size -= 1
                                
                                print "Card bought"
                             else:
                                log_affords_card(self, 1, purchase_card.name, purchase_card.cost, can_afford=False,wishlist=False)
                                print "insufficient money to buy"
                        else:
                            self.logger.debug("{} is not valid card number for card for range:0-{}".format(int(ibuy_input),len(central.active)))
                            print "enter a valid index number"
                    elif ibuy_input == 'E': # User ends shopping spree
                        self.logger.debug("End buying action selected (input: {}) ...".format(ibuy_input))
                        break
                    else:
                        self.logger.debug("No action matched to input (input: {}) ...".format(ibuy_input))
                        print "Enter a valid option"
            
            elif iuser_action == 'A':      # Attack
                self.logger.debug("Attack action selected (input: {}) ...".format(iuser_action))
                
                self.logger.debug("Computer Health before attack: {}".format(computer.health))
                computer.health -= self.attack
                self.attack = 0
                self.logger.debug("User Attack: {}".format(self.attack))
            
            elif iuser_action == 'E':      # Ends turn
                self.logger.debug("End Turn action selected (input: {}) ...".format(iuser_action))
                # If User has cards in the hand add to discard pile
                self.discard_hand()
                
                # If there cards in User active deck
                # then move all cards from active to discard
                self.discard_active_cards()
                
                # Move cards from User deck to User's hand
                self.deck_to_hand()
                
                break
            else:
                self.logger.debug("No action matched to input (input: {}) ...".format(iuser_action))
        pass
# separates classes in my editor
@wrap_all(log_me)
class Computer(CommonActions, CommonUserActions):
    """The Computer Player Class"""
    
    def __init__(self, hand_size, deck_settings, name, health):
        """initial settings for the computer player"""
        
        # store initial state
        self.init = {attr:val for attr,val in locals().iteritems() if attr != 'self'}
        
        # intialise params
        self.hand_size = hand_size
        self.name = name
        self.health = health
        self.deck_settings = deck_settings
        self.aggressive = True
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Computer")
        self.logger.debug("Computer Created.")
        
        # my name
        self.whoami = 'pC'
        
        # create newgame paramters
        self.newgame()
    def turn(self, central, user):
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
        self.logger.debug("User Health before attack: {}".format(user.health))
        print "Computer attacking with strength %s" % self.attack
        user.health -= self.attack
        self.attack = 0
        self.logger.debug("Computer Attack: {}".format(self.attack))
        
        # Display health state
        print ""
        user.show_health()
        self.show_health()
        
        # Display PC state
        self.display_values()
        
        print "Computer buying"
        # This loop should never run more than once
        # due to the conditions in the inner cb loop
        if self.money > 0:   # Commence buying if PC has money 
            self.logger.debug("Starting new purchase loop with money: {}".format(self.money))
            cb = True
            print "Starting Money %s and cb %s " % (self.money, cb)
            # Loop while cb, conditions:
            # len(wish_list) > 0 and money != 0
            while cb:
                # The temporary list of purchased
                # cards in the buying process
                wish_list = [] # This will be a list of tuples
                self.logger.debug("Temp purchase list (wish list) initiated")
                
                def log_compare_cards(self, val_name, is_isnt, pot_val, des_val):
                    self.logger.debug("Potential card ({2}:{0}) {3} higher {2} than desired card ({2}:{1})".format(
                        pot_val,des_val,val_name,is_isnt))
                    pass
                
                def log_new_desired(self, card_index):
                    self.logger.debug("New desired card index: {}".format(card_index))
                    pass
                
                def log_affords_card(self, num, name, cost, can_afford=True,wishlist=True):
                    wishlist = " Added to wish list" if wishlist else ""
                    afford = "can afford" if can_afford else "can not afford"
                    self.logger.debug("{5} {4} {0}x{1} at cost:{2}.{3}".format(num,name, cost, wishlist, can_afford, self.name))
                    pass
                
                def log_buy_card(self,card, self_money, change_in_money):
                    self.logger.debug("{3} bought 1x{0}, money:{1}+{2}".format(card.name, self_money, change_in_money,self.name))
                    pass
                
                # Select Supplements if cost < self.money
                if len(central.supplements) > 0:                  # If there are any supplements
                    self.logger.debug("Supplements Detected by Computer")
                    
                    card = central.supplements[0]
                    if card.cost <= self.money:      # If PC has enough money
                        # Add to temporary purchases
                        wish_list.append(("S", card))
                        log_affords_card(self, 1, card.name, card.cost)
                    else:
                        log_affords_card(self, 1, card.name, card.cost, can_afford=False)
                else:
                    self.logger.debug("No Supplements available")
                
                # Select cards where cost of card_i < money
                for intindex in xrange(0, central.hand_size):  # Loop all cards
                    card = central.active[intindex]
                    
                    if card.cost <= self.money:   # if PC has enough money
                        # Add to temporary purchases
                        wish_list.append((intindex, card))
                        log_affords_card(self, 1, card.name, card.cost)
                    else:
                        log_affords_card(self, 1, card.name, card.cost, can_afford=False)
                    
                if len(wish_list) > 0: # If more than one card was added to wish_list
                    
                    self.logger.debug("Wish list is not empty ({} cards)".format(len(wish_list)))
                    highestIndex = 0 # Index of most desirable card purchase
                    
                    # Loop through the temp list by index
                    # Identifies the highest value item in the list
                    # Prioritises on attack (self.aggressive) or self.money (greedy)
                    # if equal values
                    self.logger.debug("Finding the most desirable purchase...")
                    for intindex in xrange(0,len(wish_list)):
                        
                        desired = wish_list[highestIndex]
                        potential = wish_list[intindex]
                        self.logger.debug("Current most desired card: {}".format(desired[1].name))
                        self.logger.debug("Comparing against potential card: {}".format(potential[1].name))
                        
                        # Primary comparison: Get most expensive card
                        if potential[1].cost > desired[1].cost:
                            self.logger.debug("Primary comparison (Cost) ...")
                            highestIndex = intindex
                            
                            log_compare_cards(self, "cost", "is", potential[1].cost, desired[1].cost)
                            log_new_desired(self, highestIndex)
                        else:
                            self.logger.debug("Primary comparison (Cost) not undertaken.")
                        
                        # Secondary comparison: AI chosen strategy
                        if potential[1].cost == desired[1].cost:
                            self.logger.debug("Secondary comparison (Strategy Dependent)...")
                            
                            if self.aggressive:  # Aggresive strategy
                                self.logger.debug("Using Aggressive strategy")
                                # Set highestIndex to this card if highest attack
                                if potential[1].get_attack() > desired[1].get_attack():
                                    highestIndex = intindex
                                    
                                    log_compare_cards(self, "attack", "is", potential[1].attack, desired[1].attack)
                                    log_new_desired(self, highestIndex)
                                else:
                                    log_compare_cards(self, "attack", "is not", potential[1].attack, desired[1].attack)
                            
                            else:           # Greedy strategy
                                self.logger.debug("Using Non-Aggressive strategy")
                                # Set highestIndex to this card if highest money
                                if potential[1].get_attack() > desired[1].get_money():
                                    highestIndex = intindex
                                    
                                    log_compare_cards(self, "money", "is", potential[1].money, desired[1].money)
                                    log_new_desired(self, highestIndex)
                                else:
                                    log_compare_cards(self, "money", "is not", potential[1].money, desired[1].money)
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
                    self.logger.debug("Computer attempts to purchase {} (Index: {})".format(*desired))
                    
                    # This is a card from the active deck
                    if source in xrange(0,central.hand_size):
                        purchase_card = central.active[int(source)]
                        
                        self.logger.debug("Index: {} found in Central Hand ({}, cost:{})".format(
                            source, purchase_card.name, purchase_card.cost))
                        
                        # If PC has money to purchase:
                        # comparison has alrady been made
                        if self.money >= purchase_card.cost:
                            log_affords_card(self, 1, purchase_card.name, purchase_card.cost, wishlist=False)
                            
                            # Add card to PC discard pile
                            card = central.active.pop(int(source))
                            self.discard.append(card)
                            
                            print "Card bought %s" % card
                            
                            new_money = - card.cost
                            log_buy_card(self, card, self.money, new_money)
                            self.money += new_money
                            
                            # Refill active from central.central deck
                            # if there are cards in central.central
                            self.logger.debug("Attempting to refill card central active deck from central deck...")
                            if len(central.deck) > 0:
                                self.logger.debug("{} cards in central deck".format(len(central.deck)))
                                card = central.deck.pop()
                                central.active.append(card)
                                self.logger.debug("Moved 1x{} from {} to {}".format(card.name, "central deck", "central active deck"))
                            else:
                                # If no cards in central.central deck,
                                # reduce activesize by 1
                                self.logger.debug("No cards in central deck to refill central active deck.")
                                self.logger.debug("central hand_size:{}-1".format(central.hand_size))
                                central.hand_size -= 1
                                
                        else:
                            log_affords_card(self, 1, purchase_card.name, purchase_card.cost, can_afford=False)
                            print "Error Occurred"
                    
                    else: # This is a supplement as it is not in the range [0,5]
                        # If PC has money to purchase:
                        # comparison has alrady been made
                        purchase_card = central.supplements[0]
                        
                        if self.money >= purchase_card.cost:
                            log_affords_card(self, 1, purchase_card.name, purchase_card.cost, wishlist=False)
                            
                            card = central.supplements.pop()
                            self.discard.append(card)
                            print "Supplement Bought %s" % card
                            
                            new_money = - card.cost
                            log_buy_card(self, card, self.money, new_money)
                            self.money += new_money
                        else:
                            log_affords_card(self, 1, purchase_card.name, purchase_card.cost, can_afford=False)
                            print "Error Occurred"
                    
                    # ^Loop: Buy another card
                else:           # Exit loop if PC couldn't buy any cards
                    cb = False
                    self.logger.debug("Wish list is empty ({} cards)".format(len(wish_list)))
                    
                if self.money == 0:  # Exit loop if no money
                    # This is a subcomparison that of the above
                    # This will just exit the loop 1 cycle earlier
                    cb = False
                    self.logger.debug("Computer has no money. Exiting wish list loop (money: {})".format(self.money))
        else:           # Don't buy if no money
            self.logger.debug("Computer has no money. Exiting purchase loop with money: {}".format(self.money))
            print "No Money to buy anything"
        
        # If player has cards in the hand add to discard pile
        self.discard_hand()
        
        # If there cards in PC active deck
        # then move all cards from active to discard
        # currently this will alwayds be true as PC
        # plays all by default.
        self.discard_active_cards()
        
        # Move cards from PC deck to PC hand
        self.deck_to_hand()
        
        print "Computer turn ending"
    pass
# separates classes in my editor
@wrap_all(log_me)
class Gameplay(object):
    
    def __init__(self):
        
        # logging
        self.logger = logging.getLogger(__name__ + ".Game")
        self.logger.debug("Game Created.")
        
        # my name
        self.whoami = 'game'
        pass
    def end(self, user, computer, central):
        """Checks for end game conditions"""
        end_game = False
        
        # continue_game = False flags the end of a game
        if user.health <= 0:   # User has died
            end_game = True
            print "Computer wins"
        elif computer.health <= 0: # PC has died
            end_game = True
            print 'Player One Wins'
        
        # Game ends if size of active deck is zero
        elif central.hand_size == 0:
            print "No more cards available"
            if user.health > computer.health:
                print "Player One Wins on Health"
            elif computer.health > user.health:
                print "Computer Wins"
            else: # No clear winner: compare card stengths
                pHT = 0
                computer.pCT = 0
                if pHT > computer.pCT:
                    print "Player One Wins on Card Strength"
                elif computer.pCT > pHT:
                    print "Computer Wins on Card Strength"
                else:
                    print "Draw"
        return end_game
    def replay(self, user, computer, central):
        """Asks User if they want to replay"""
        iplay_game = raw_input("\nDo you want to play another game?").upper()
        continue_game = (iplay_game=='Y')
        
        # Initiate new game sequence
        if continue_game:
            
            # Starting the game
            iopponent_type = raw_input("Do you want an aggressive (A) opponent or an greedy (G) opponent").upper()
            aggressive = (iopponent_type=='A')
            
            # call the replay game settings
            user.newgame()
            computer.newgame()
            central.newgame()
            
            # Move cards from central.central deck 
            # to active central.central deck
            central.deck_to_active()
            
            # Move cards from User deck to User's hand
            user.deck_to_hand()
            
            # Move cards from PC deck to PC's hand
            computer.deck_to_hand()
            
            # Display central.central cards state
            central.print_active_cards()
            central.print_supplements()
        return continue_game
    def exit(self):
        """Friendly exit"""
        print "\nHope to see you again soon. Goodbye :)" 
        sys.exit() # Terminate
        pass
    def hostile_exit(self):
        """UnFriendly exit"""
        print "\n\nSad to see you leave so quickly. Please return soon! :)" 
        sys.exit() # Terminate
        pass