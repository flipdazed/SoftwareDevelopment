# ___Change Log (from previous)___
# Comments and readability added where necessary as part of debug

import sys
import random
from config import *
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    
    # logging
    logger.debug("Starting Game...")
    
    # instanciate the game settings
    user = User()
    computer = Computer()
    engine = Central()
    
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
        
        # iterators to count money
        # and attack in players' hands
        money = 0
        attack = 0
        
        while True: # User's Turn
            
            # Display health state
            print ""
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
                    for x in xrange(0, len(user.pO['hand'])):
                        card = user.pO['hand'].pop()
                        user.pO['active'].append(card)
                        money = money + card.get_money()
                        attack = attack + card.get_attack()
                
                # Display User hand
                user.print_hand()
                
                # Display User active cards
                user.print_active_cards()
                
                # Display User values
                print "\nYour Values"
                print "Money %s, Attack %s" % (money, attack)
                
            if iuser_action.isdigit():   # Play a specific card
                if( int(iuser_action) < len(user.pO['hand'])):
                    
                    # Transfer card to active
                    # add values in hand to current totals
                    card = user.pO['hand'].pop(int(iuser_action))
                    user.pO['active'].append(card)
                    money = money + card.get_money()
                    attack = attack + card.get_attack()
                    
                
                # Display User hand
                user.print_hand()
                
                # Display User active cards
                user.print_active_cards()
                
                # Display User values
                print "\nYour Values"
                print "Money %s, Attack %s" % (money, attack)
            
            if (iuser_action == 'B'):    # Buy cards
                
                # Check player has money available
                while money > 0: # no warning of no money
                    
                    # Display engine.central cards state
                    engine.print_active_cards()
                    
                    # User chooses a card to purchase
                    print "Choose a card to buy [0-n], S for supplement, E to end buying"
                    ibuy_input = raw_input("Choose option: ").upper()
                    
                    # Evaluate choice
                    if ibuy_input == 'S': # Buy a supplement
                        if len(engine.central['supplement']) > 0: # If supplements exist
                            
                            # Buy if player has enough money
                            # Move to player's discard pile
                            if money >= engine.central['supplement'][0].cost:
                                money = money - engine.central['supplement'][0].cost
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
                             # Buy if User has enough money
                             # Move directly to discard pile
                             if money >= engine.central['active'][int(ibuy_input)].cost:
                                money = money - engine.central['active'][int(ibuy_input)].cost
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
                computer.pC['health'] -= attack
                attack = 0
            if iuser_action == 'E':      # Ends turn
                
                # If User has cards in the hand add to discard pile
                if (len(user.pO['hand']) >0 ):
                    for x in xrange(0, len(user.pO['hand'])):
                        user.pO['discard'].append(user.pO['hand'].pop())
                
                # If there cards in User active deck
                # then move all cards from active to discard
                if (len(user.pO['active']) >0 ):
                    for x in xrange(0, len(user.pO['active'])):
                        user.pO['discard'].append(user.pO['active'].pop())
                
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
        money = 0
        attack = 0
        
        # Sum up money and attack in PC hand
        for x in xrange(0, len(computer.pC['hand'])):
            card = computer.pC['hand'].pop()
            computer.pC['active'].append(card)
            money = money + card.get_money()
            attack = attack + card.get_attack()
        
        # Display PC state
        print " Computer player values attack %s, money %s" % (attack, money)
        
        # PC starts by attacking User
        print " Computer attacking with strength %s" % attack
        user.pO['health'] -= attack
        attack = 0
        
        # Display health state
        print ""
        user.show_health()
        computer.show_health()
        
        # Display PC state
        print "Computer player values attack %s, money %s" % (attack, money)
        
        print "Computer buying"
        # This loop should never run more than once
        # due to the conditions in the inner cb loop
        if money > 0:   # Commence buying if PC has money 
            cb = True
            templist = []
            print "Starting Money %s and cb %s " % (money, cb)
            # Loop while cb, conditions:
            # len(templist) > 0 and money != 0
            while cb:
                # The temporary list of purchased
                # cards in the buying process
                templist = [] # This will be a list of tuples
                
                # Select Supplements if cost < money
                if len(engine.central['supplement']) > 0:                  # If there are any supplements
                    if engine.central['supplement'][0].cost <= money:      # If PC has enough money
                        # Add to temporary purchases
                        templist.append(("S", engine.central['supplement'][0]))
                
                # Select cards where cost of card_i < money
                for intindex in xrange(0, engine.central['activesize']):  # Loop all cards
                    if engine.central['active'][intindex].cost <= money:   # if PC has enough money
                        # Add to temporary purchases
                        templist.append((intindex, engine.central['active'][intindex]))
                
                if len(templist) >0: # If more than one card was added to templist
                    
                    highestIndex = 0 # Index of most desirable card purchase
                    
                    # Loop through the temp list by index
                    # Identifies the highest value item in the list
                    # Prioritises on attack (aggressive) or money (greedy)
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
                        if money >= engine.central['active'][int(source)].cost:
                            
                            # Add card to PC discard pile
                            money = money - engine.central['active'][int(source)].cost
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
                        if money >= engine.central['supplement'][0].cost:
                            money = money - engine.central['supplement'][0].cost
                            card = engine.central['supplement'].pop()
                            computer.pC['discard'].append(card)
                            print "Supplement Bought %s" % card
                        else:
                            print "Error Occurred"
                    
                    # ^Loop: Buy another card
                else:           # Exit loop if PC couldn't buy any cards
                    cb = False
                if money == 0:  # Exit loop if no money
                    # This is a subcomparison that of the above
                    # This will just exit the loop 1 cycle earlier
                    cb = False
        else:           # Don't buy if no money
            print "No Money to buy anything"
        
        # If PC has cards in the hand add to discard pile
        if (len(computer.pC['hand']) > 0 ):
            # Iterate through all cards in PC hand
            for x in xrange(0, len(computer.pC['hand'])):
                computer.pC['discard'].append(computer.pC['hand'].pop())
        
        # If there cards in PC active deck
        # then move all cards from active to discard
        # currently this will alwayds be true as PC
        # plays all by default.
        if (len(computer.pC['active']) > 0 ):
            for x in xrange(0, len(computer.pC['active'])):
                computer.pC['discard'].append(computer.pC['active'].pop())
        
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
            
            # Initiate new game sequence
            if continue_game:
                
                # Starting the game
                iopponent_type = raw_input("Do you want an aggressive (A) opponent or an greedy (G) opponent").upper()
                aggressive = (iopponent_type=='A')
                
                # call the replay game settings
                user.replay()
                computer.replay()
                engine.replay()
                
                # Move cards from engine.central deck 
                # to active engine.central deck
                count = 0
                while count < engine.central['activesize']:
                    card = engine.central['deck'].pop()
                    engine.central['active'].append(card)
                    count = count + 1
                
                # Move cards from User deck to User's hand
                user.deck_to_hand()
                
                # Move cards from PC deck to PC's hand
                computer.deck_to_hand()
                
                # Display engine.central cards state
                engine.print_active_cards_hand()
                engine.print_supplements()
    
    sys.exit() # Terminate