# This is the main game file
import sys
import random
from logs import *
import game_engine
from config import defaults

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    
    # logging
    logger.debug("Starting Game...")
    
    # instanciate the game settings
    user = game_engine.User(**defaults['user'])
    computer = game_engine.Computer(**defaults['computer'])
    engine = game_engine.Central(**defaults['engine'])
    
    # Move cards from engine.central deck 
    # to active engine.central deck
    engine.deck_to_active()
    
    # Move cards from User deck to User's hand
    user.deck_to_hand()
    
    # Move cards from PC deck to PC's hand
    computer.deck_to_hand()
    
    # Display engine.central cards state
    engine.print_active_cards()
    engine.print_supplements()
    
    # Starting the game
    iplay_game = raw_input("Do you want to play a game?").upper()
    continue_game = (iplay_game=='Y')
    iopponent_type = raw_input("Do you want an aggressive (A) opponent or an greedy (G) opponent").upper()
    aggressive = (iopponent_type=='A')
    
    # Each loop is a new round in the game
    # User goes first followed by PC
    while continue_game:
        # logging
        logger.debug("Starting New Round.")
        
        # logging
        logger.debug("Start User Turn...")
        
        # iterators to count user.money
        # and attack in players' hands
        user.money = 0
        user.attack = 0
        
        while True: # User's Turn
            
            # Display health state
            print "" # Temporary until UI Fix
            user.show_health()
            computer.show_health()
            
            # Display User hand
            user.print_hand()
            
            # In-game actions UI
            print "\nChoose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)"
            iuser_action = raw_input("Enter Action: ").upper()
            if iuser_action == 'P':      # Play all cards
                
                if(len(user.pO['hand'])>0):  # Are there cards in the hand
                    # transfer all cards from hand to active
                    # add values in hand to current totals
                    user.play_all_cards()
                
                # Display User hand
                user.print_hand()
                
                # Display User active cards
                user.print_active_cards()
                
                # Display PC state
                user.display_values()
                
            if iuser_action.isdigit():   # Play a specific card
                if( int(iuser_action) < len(user.pO['hand'])):
                    user.play_a_card(card_number=iuser_action)
                
                # Display User hand
                user.print_hand()
                
                # Display User active cards
                user.print_active_cards()
                
                # Display PC state
                user.display_values()
            
            if (iuser_action == 'B'):    # Buy cards
                
                # Check player has user.money available
                while user.money > 0: # no warning of no user.money
                    
                    # Display engine.central cards state
                    engine.print_active_cards()
                    
                    # User chooses a card to purchase
                    print "Choose a card to buy [0-n], S for supplement, E to end buying"
                    ibuy_input = raw_input("Choose option: ").upper()
                    
                    # Evaluate choice
                    if ibuy_input == 'S': # Buy a supplement
                        if len(engine.central['supplement']) > 0: # If supplements exist
                            
                            # Buy if player has enough user.money
                            # Move to player's discard pile
                            if user.money >= engine.central['supplement'][0].cost:
                                user.money = user.money - engine.central['supplement'][0].cost
                                user.pO['discard'].append(engine.central['supplement'].pop())
                                print "Supplement Bought"
                            else:
                                print "insufficient money to buy"
                        else:
                            print "no supplements left"
                    
                    elif ibuy_input == 'E': # User ends shopping spree
                        break
                    elif ibuy_input.isdigit(): # Buy a card
                        if int(ibuy_input) < len(engine.central['active']): # If card exists
                             # Buy if User has enough user.money
                             # Move directly to discard pile
                             if user.money >= engine.central['active'][int(ibuy_input)].cost:
                                user.money = user.money - engine.central['active'][int(ibuy_input)].cost
                                user.pO['discard'].append(engine.central['active'].pop(int(ibuy_input)))
                                
                                # Refill active from engine.central deck
                                # if there are cards in engine.central
                                if( len(engine.central['deck']) > 0):
                                    card = engine.central['deck'].pop()
                                    engine.central['active'].append(card)
                                else:
                                    # If no cards in engine.central deck,
                                    # reduce activesize by 1
                                    engine.central['activesize'] -= 1
                                print "Card bought"
                             else:
                                print "insufficient money to buy"
                        else:
                             print "enter a valid index number"
                    else:
                        print "Enter a valid option"
            
            
            if iuser_action == 'A':      # Attack
                computer.pC['health'] -= user.attack
                user.attack = 0
            
            if iuser_action == 'E':      # Ends turn
                
                # If User has cards in the hand add to discard pile
                user.discard_hand()
                
                # If there cards in User active deck
                # then move all cards from active to discard
                user.discard_active_cards()
                
                # Move cards from User deck to User's hand
                user.deck_to_hand()
                break
        
        #### End User Turn ####
        
        # logging
        logger.debug("End User Turn.")
        
        # Display engine.central cards state
        engine.print_active_cards()
        
        # Display supplements
        engine.print_supplements()
        
        # Display health state
        print ""
        user.show_health()
        computer.show_health()
        
        
        #### Start PC Turn ####
        # logging
        logger.debug("Starting Computer Turn...")
        
        # Iterators to count money
        # and attack in User's hands
        computer.money = 0
        computer.attack = 0
        
        # transfer all cards from hand to active
        # add values in hand to current totals
        computer.play_all_cards()
        
        # Display PC state
        computer.display_values()
        
        # PC starts by attacking User
        print " Computer attacking with strength %s" % computer.attack
        user.pO['health'] -= computer.attack
        computer.attack = 0
        
        # Display health state
        print ""
        user.show_health()
        computer.show_health()
        
        # Display PC state
        computer.display_values()
        
        print "Computer buying"
        # This loop should never run more than once
        # due to the conditions in the inner cb loop
        if computer.money > 0:   # Commence buying if PC has money 
            cb = True
            templist = []
            print "Starting Money %s and cb %s " % (computer.money, cb)
            # Loop while cb, conditions:
            # len(templist) > 0 and money != 0
            while cb:
                # The temporary list of purchased
                # cards in the buying process
                templist = [] # This will be a list of tuples
                
                # Select Supplements if cost < computer.money
                if len(engine.central['supplement']) > 0:                  # If there are any supplements
                    if engine.central['supplement'][0].cost <= computer.money:      # If PC has enough money
                        # Add to temporary purchases
                        templist.append(("S", engine.central['supplement'][0]))
                
                # Select cards where cost of card_i < money
                for intindex in xrange(0, engine.central['activesize']):  # Loop all cards
                    if engine.central['active'][intindex].cost <= computer.money:   # if PC has enough money
                        # Add to temporary purchases
                        templist.append((intindex, engine.central['active'][intindex]))
                
                if len(templist) >0: # If more than one card was added to templist
                    
                    highestIndex = 0 # Index of most desirable card purchase
                    
                    # Loop through the temp list by index
                    # Identifies the highest value item in the list
                    # Prioritises on attack (aggressive) or computer.money (greedy)
                    # if equal values
                    for intindex in xrange(0,len(templist)):
                        
                        # Primary comparison: Get most expensive card
                        if templist[intindex][1].cost > templist[highestIndex][1].cost:
                            highestIndex = intindex
                        
                        # Secondary comparison: AI chosen strategy
                        if templist[intindex][1].cost == templist[highestIndex][1].cost:
                            if aggressive:  # Aggresive strategy
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
                    if source in xrange(0,engine.central['activesize']):
                        
                        # If PC has money to purchase:
                        # comparison has alrady been made
                        if computer.money >= engine.central['active'][int(source)].cost:
                            
                            # Add card to PC discard pile
                            computer.money = computer.money - engine.central['active'][int(source)].cost
                            card = engine.central['active'].pop(int(source))
                            print "Card bought %s" % card
                            computer.pC['discard'].append(card)
                            
                            # Refill active from engine.central deck
                            # if there are cards in engine.central
                            if( len(engine.central['deck']) > 0):
                                card = engine.central['deck'].pop()
                                engine.central['active'].append(card)
                            else:
                                # If no cards in engine.central deck,
                                # reduce activesize by 1
                                engine.central['activesize'] -= 1
                        else:
                            print "Error Occurred"
                    
                    else: # This is a supplement as it is not in the range [0,5]
                        # If PC has money to purchase:
                        # comparison has alrady been made
                        if computer.money >= engine.central['supplement'][0].cost:
                            computer.money = computer.money - engine.central['supplement'][0].cost
                            card = engine.central['supplement'].pop()
                            computer.pC['discard'].append(card)
                            print "Supplement Bought %s" % card
                        else:
                            print "Error Occurred"
                    
                    # ^Loop: Buy another card
                else:           # Exit loop if PC couldn't buy any cards
                    cb = False
                if computer.money == 0:  # Exit loop if no money
                    # This is a subcomparison that of the above
                    # This will just exit the loop 1 cycle earlier
                    cb = False
        else:           # Don't buy if no money
            print "No Money to buy anything"
        
        # If player has cards in the hand add to discard pile
        computer.discard_hand()
        
        # If there cards in PC active deck
        # then move all cards from active to discard
        # currently this will alwayds be true as PC
        # plays all by default.
        computer.discard_active_cards()
        
        # Move cards from PC deck to PC hand
        computer.deck_to_hand()
        
        print "Computer turn ending"
        
        # logging
        logger.debug("End Computer Turn...")
        #### End PC Turn ####
        
        # Display engine.central cards state
        engine.print_active_cards()
        
        # Display supplements
        engine.print_supplements()
        
        # Display health state
        print ""
        user.show_health()
        computer.show_health()
        
        
        # Check for end of game
        # logging
        logger.debug("Checking End Game Conditions...")
        # continue_game = False flags the end of a game
        if user.pO['health'] <= 0:   # User has died
            continue_game = False
            print "Computer wins"
        elif computer.pC['health'] <= 0: # PC has died
            continue_game = False
            print 'Player One Wins'
        
        # Game ends if size of active deck is zero
        elif engine.central['activesize'] == 0:
            print "No more cards available"
            if user.pO['health'] > computer.pC['health']:
                print "Player One Wins on Health"
            elif computer.pC['health'] > user.pO['health']:
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
            continue_game = False # End game flag set
        
        # New game interface
        if not continue_game:
            iplay_game = raw_input("\nDo you want to play another game?").upper()
            continue_game = (iplay_game=='Y')
            
            logger.debug("Starting Replay...")
            # Initiate new game sequence
            if continue_game:
                
                # Starting the game
                iopponent_type = raw_input("Do you want an aggressive (A) opponent or an greedy (G) opponent").upper()
                aggressive = (iopponent_type=='A')
                
                # call the replay game settings
                user.newgame()
                computer.newgame()
                engine.newgame()
                
                # Move cards from engine.central deck 
                # to active engine.central deck
                engine.deck_to_active()
                
                # Move cards from User deck to User's hand
                user.deck_to_hand()
                
                # Move cards from PC deck to PC's hand
                computer.deck_to_hand()
                
                # Display engine.central cards state
                engine.print_active_cards()
                engine.print_supplements()
    
    sys.exit() # Terminate