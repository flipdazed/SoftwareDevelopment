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
        
        self.active = []
        
        # revert to initial state
        for attr, val in self.init.iteritems():
            setattr(self, attr, val)
        
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
            count += 1
            self.logger.debug('iteration #{}: Moving {} from deck to active'.format(count, card.name))
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
                
                self.hand == self.hand
                if(len(self.hand)>0):  # Are there cards in the hand
                    # transfer all cards from hand to active
                    # add values in hand to current totals
                    self.play_all_cards()
                
                # Display User hand
                self.print_hand()
                
                # Display User active cards
                self.print_active_cards()
                
                # Display PC state
                self.display_values()
            
            if iuser_action.isdigit():   # Play a specific card
                if( int(iuser_action) < len(self.hand)):
                    self.play_a_card(card_number=iuser_action)
                
                # Display User hand
                self.print_hand()
                
                # Display User active cards
                self.print_active_cards()
                
                # Display PC state
                self.display_values()
            
            if (iuser_action == 'B'):    # Buy cards
                
                # Check player has self.money available
                while self.money > 0: # no warning of no self.money
                    
                    # Display central.central cards state
                    central.print_active_cards(index=True)
                    
                    # User chooses a card to purchase
                    print "Choose a card to buy [0-n], S for supplement, E to end buying"
                    ibuy_input = raw_input("Choose option: ").upper()
                    
                    # Evaluate choice
                    if ibuy_input == 'S': # Buy a supplement
                        if len(central.supplements) > 0: # If supplements exist
                            
                            # Buy if player has enough self.money
                            # Move to player's discard pile
                            if self.money >= central.supplements[0].cost:
                                self.money = self.money - central.supplements[0].cost
                                self.discard.append(central.supplements.pop())
                                print "Supplement Bought"
                            else:
                                print "insufficient money to buy"
                        else:
                            print "no supplements left"
                    
                    elif ibuy_input == 'E': # User ends shopping spree
                        break
                    elif ibuy_input.isdigit(): # Buy a card
                        if int(ibuy_input) < len(central.active): # If card exists
                             # Buy if User has enough self.money
                             # Move directly to discard pile
                             if self.money >= central.active[int(ibuy_input)].cost:
                                self.money = self.money - central.active[int(ibuy_input)].cost
                                self.discard.append(central.active.pop(int(ibuy_input)))
                                
                                # Refill active from central.central deck
                                # if there are cards in central.central
                                if( len(central.deck) > 0):
                                    card = central.deck.pop()
                                    central.active.append(card)
                                else:
                                    # If no cards in central.central deck,
                                    # reduce activesize by 1
                                    central.hand_size -= 1
                                print "Card bought"
                             else:
                                print "insufficient money to buy"
                        else:
                             print "enter a valid index number"
                    else:
                        print "Enter a valid option"
            
            if iuser_action == 'A':      # Attack
                computer.health -= self.attack
                self.attack = 0
            
            if iuser_action == 'E':      # Ends turn
                
                # If User has cards in the hand add to discard pile
                self.discard_hand()
                
                # If there cards in User active deck
                # then move all cards from active to discard
                self.discard_active_cards()
                
                # Move cards from User deck to User's hand
                self.deck_to_hand()
                break
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
            cb = True
            templist = []
            print "Starting Money %s and cb %s " % (self.money, cb)
            # Loop while cb, conditions:
            # len(templist) > 0 and money != 0
            while cb:
                # The temporary list of purchased
                # cards in the buying process
                templist = [] # This will be a list of tuples
                
                # Select Supplements if cost < self.money
                if len(central.supplements) > 0:                  # If there are any supplements
                    if central.supplements[0].cost <= self.money:      # If PC has enough money
                        # Add to temporary purchases
                        templist.append(("S", central.supplements[0]))
                
                # Select cards where cost of card_i < money
                for intindex in xrange(0, central.hand_size):  # Loop all cards
                    if central.active[intindex].cost <= self.money:   # if PC has enough money
                        # Add to temporary purchases
                        templist.append((intindex, central.active[intindex]))
                
                if len(templist) >0: # If more than one card was added to templist
                    
                    highestIndex = 0 # Index of most desirable card purchase
                    
                    # Loop through the temp list by index
                    # Identifies the highest value item in the list
                    # Prioritises on attack (self.aggressive) or self.money (greedy)
                    # if equal values
                    for intindex in xrange(0,len(templist)):
                        
                        # Primary comparison: Get most expensive card
                        if templist[intindex][1].cost > templist[highestIndex][1].cost:
                            highestIndex = intindex
                        
                        # Secondary comparison: AI chosen strategy
                        if templist[intindex][1].cost == templist[highestIndex][1].cost:
                            if self.aggressive:  # Aggresive strategy
                                # Set highestIndex to this card if highest attack
                                if templist[intindex][1].get_attack() >templist[highestIndex][1].get_attack():
                                    highestIndex = intindex
                            
                            else:           # Greedy strategy
                                # Set highestIndex to this card if highest money
                                if templist[intindex][1].get_attack() >templist[highestIndex][1].get_money():
                                    highestIndex = intindex
                    
                    
                    # Contains two parts of information:
                    # 1. If integer then it is a card from the active deck
                    # 2. If non-integer then it is a supplement
                    # 
                    # If 1. then the integer may take a value
                    # between 0 and up to (not including) the size
                    # if the active deck
                    source = templist[highestIndex][0]
                    
                    # This is a card from the active deck
                    if source in xrange(0,central.hand_size):
                        
                        # If PC has money to purchase:
                        # comparison has alrady been made
                        if self.money >= central.active[int(source)].cost:
                            
                            # Add card to PC discard pile
                            self.money = self.money - central.active[int(source)].cost
                            card = central.active.pop(int(source))
                            print "Card bought %s" % card
                            self.discard.append(card)
                            
                            # Refill active from central.central deck
                            # if there are cards in central.central
                            if( len(central.deck) > 0):
                                card = central.deck.pop()
                                central.active.append(card)
                            else:
                                # If no cards in central.central deck,
                                # reduce activesize by 1
                                central.hand_size -= 1
                        else:
                            print "Error Occurred"
                    
                    else: # This is a supplement as it is not in the range [0,5]
                        # If PC has money to purchase:
                        # comparison has alrady been made
                        if self.money >= central.supplements[0].cost:
                            self.money = self.money - central.supplements[0].cost
                            card = central.supplements.pop()
                            self.discard.append(card)
                            print "Supplement Bought %s" % card
                        else:
                            print "Error Occurred"
                    
                    # ^Loop: Buy another card
                else:           # Exit loop if PC couldn't buy any cards
                    cb = False
                if self.money == 0:  # Exit loop if no money
                    # This is a subcomparison that of the above
                    # This will just exit the loop 1 cycle earlier
                    cb = False
        else:           # Don't buy if no money
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
    def save_exit(self):
        """UnFriendly exit"""
        print "\n\nSad to see you leave so quickly. Please return soon! :)" 
        sys.exit() # Terminate
        pass