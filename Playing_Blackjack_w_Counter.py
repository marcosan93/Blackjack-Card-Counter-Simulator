import random

def check_ace(hand): 
    """
    Checks if there's an ace in the hand in case total went over 21
    """
    if 'A' in hand:
        hand[hand.index('A')] = 'A.'
        return True
    else:
        return False
    

def hand_total(hand): 
    """
    Calculates sum total values from a list of strings using a dictionary
    """
    d_val = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
             '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11, 'A.': 1}
    return sum(d_val[i] for i in hand)


def deal_card(hand, deck, num_of_cards=1): 
    """
    Deals a card, defaulted to one card
    """
    for _ in range(num_of_cards):
        hand.append(deck.pop())
    return hand


def create_deck(num_of_decks=1): 
    """
    Creates a standard playing card deck, defaulted to one deck
    """
    deck = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']*4*num_of_decks
    random.shuffle(deck)
    return deck


def player_print(hand, total): 
    """
    Prints player's current hand and total
    """
    print("\nYour hand: ", hand, "\nYour total: ", total)
    
    
def dealer_print(hand, total): 
    """
    Prints dealer's current hand and total
    """
    print("\nDealer hand: ", hand, "\nDealer total: ", total)
    

def play_again():
    """
    Loops the game
    """
    while True: 
        # Asking the player to play again or not
        ans = input("Play again? \n").lower()
        if ans == 'yes' or ans == 'y':
            print("\n------------ Another Round of Blackjack -------------")
            return True
        elif ans == 'no' or ans == 'n':
            return False
        else:
            print("Yes or no? ")
            continue
            
def dealer_turn(your_hand, dealer_hand, total, dtotal, r_count, true_cnt, deck, turn=True): 
    """
    Activates the dealer's turn if player's move was 'stay'
    """
    # Tallying wins, losses, and draws
    wins = 0
    draw = 0
    loss = 0
    
    # Looping through the moves
    while turn:
        total  = hand_total(your_hand)
        if total > 21: 
            
            # Evaluating a player's hand to see if they have an ace
            check_ace(your_hand)
            total = hand_total(your_hand)
            player_print(your_hand, total)
            continue
            
        dtotal = hand_total(dealer_hand)
        dealer_print(dealer_hand, dtotal)

        while dtotal <= 16: 
            
            # Dealing cards to the dealer if they have less than or equal to 16
            deal_card(dealer_hand, deck)
            dtotal = hand_total(dealer_hand)
            dealer_print(dealer_hand, dtotal)
            
            # Counter
            r_count += card_counter(dealer_hand[-1:])
            true_cnt = true_counter(deck, r_count)
            print_count(true_cnt, r_count)
            
        # Checking if the dealer wins
        if dtotal == 21: 
            print("Game Over. House wins.")
            loss += 1
            break
        
        # Checking if the dealer busts
        elif dtotal > 21: 
            if check_ace(dealer_hand):
                continue
            else:
                print("Dealer busts! You win!")
                wins += 1
                break
                
        # Comparing dealer hand to player hand
        elif 17 <= dtotal <= 21: 
            if dtotal > total:
                print("Game Over. House wins")
                loss += 1
                break
            elif dtotal < total:
                print("Congratulations! You win!")
                wins += 1
                break
            elif dtotal == total:
                print("Draw. No lost bet.")
                draw += 1
                break
            else:
                print("House busts. You win!")
                wins += 1
                break
    return [wins, loss, draw, r_count, true_cnt]

import pandas as pd

def card_counter(hand, strategy='Hi-Lo'):
    """
    Counting cards based on strategy selected
    Returns sum of the values
    """
    
    df = pd.read_pickle('Card_Counting_Values')

    return sum([df.loc[strategy][i].item() for i in hand])

def true_counter(deck, r_count):
    """
    Calculates and returns the true count rounded down
    """
    try:
        return r_count//(len(deck)//52)
    except:
        
        # Compensating for when there is less than 52 cards or 1 deck left
        return r_count


def print_count(true_cnt, r_count):
    """
    Prints out current counts
    """
    print('\nRunning Count: --->', r_count, '\nTrue Count: ', true_cnt)
    
def blackjack(deck, r_count, true_cnt):
    """
    Playing Blackjack
    """
    your_hand   = deal_card([], deck, 2)
    dealer_hand = deal_card([], deck, 2)

    print("Your hand: ", your_hand)
    print("Dealer hand: ", dealer_hand[:1])
    
    # Tallying wins, losses, and draws
    wins = 0
    draw = 0
    loss = 0
    
    # Card Counting
    r_count  += card_counter(your_hand) + card_counter(dealer_hand[:1])
    true_cnt  = true_counter(deck, r_count)
    print_count(true_cnt, r_count) 
    
    # Looping through the moves
    while len(deck) > 1:
        print('Remaining cards: ', len(deck), '\n')
        
        # Checking if the player has a natural blackjack
        if hand_total(your_hand) == 21 and hand_total(dealer_hand) < 21:
            dealer_print(dealer_hand, hand_total(dealer_hand))
            
            # Counter
            r_count += card_counter(dealer_hand[-1:])
            true_cnt = true_counter(deck, r_count)
            print_count(true_cnt, r_count)
            
            print("Congratulations! Blackjack!")
            wins += 1
            break
        
        # Checking if the player and the dealer tie if they both have natural blackjacks
        elif hand_total(your_hand) == 21 and hand_total(dealer_hand) == 21:
            dealer_print(dealer_hand, hand_total(dealer_hand))
            
            # Counter
            r_count += card_counter(dealer_hand[-1:])
            true_cnt = true_counter(deck, r_count)
            print_count(true_cnt, r_count)
            
            print("It's a draw. Bet is returned.")
            draw += 1
            break
            
        # Allowing the player to make a move
        move = input("Hit or stay? ").lower()
        
        if move == "hit" or move == "h":
            deal_card(your_hand, deck)
            total = hand_total(your_hand)
            
            # Counter
            r_count += card_counter(your_hand[-1:])
            true_cnt = true_counter(deck, r_count)
            print_count(true_cnt, r_count)
            
            # Checking if the player busts
            if  total > 21:              
                
                # Checking for an ace in the player hand
                if check_ace(your_hand): 
                    total = hand_total(your_hand)
                    player_print(your_hand, total)
                    continue
                    
                # Otherwise they bust
                else:                    
                    player_print(your_hand, total)
                    print("Dealer wins. You lose.")
                    loss += 1
                    break
            
            elif total < 21:             
                player_print(your_hand, total)
                
                # Going back to asking the player for a move
                continue
                
            # Checking if the player succeeded in achieving blackjack
            elif total == 21:            
                player_print(your_hand, total)
                print("Blackjack! You win!")
                wins += 1
                break
        elif move == "stay" or move == "s":
            total  = hand_total(your_hand)
            dtotal = hand_total(dealer_hand)
            
            # Counter
            r_count += card_counter(dealer_hand[-1:])
            true_cnt = true_counter(deck, r_count)
            
            # Running the function for the dealer's turn
            result = dealer_turn(your_hand, dealer_hand, total, dtotal, r_count, true_cnt, deck)
            
            # The results of the dealer's turn
            wins += result[0]
            loss += result[1]
            draw += result[2]
            
            # Counter 
            r_count  = result[3]
            true_cnt = result[4]
            print_count(true_cnt, r_count)
            break
                
        else:
            # Continuing the loop if input was different from 'hit' or 'stay'
            print('Please type hit or stay')
            continue
            
    # Returning the results of the game        
    return [wins, loss, draw, r_count, true_cnt]

def play_blackjack():
    """
    Looping the game until no cards left
    """
    deck = create_deck(6)
    
    play = True
    wins = 0
    rounds_played = 0
    r_count = 0
    true_cnt = 0
    
    while play:
        
        # Running blackjack
        game = blackjack(deck, r_count, true_cnt)
        
        # Recording the results: wins, loss, draw
        wins += game[0]
        rounds_played += sum(game[:3])
        
        r_count = game[3]
        true_cnt = game[4]
        
        print("Wins: ", wins, '/', rounds_played)
        
        # Determining if there are enough cards left
        if len(deck) < 12:
            print("Not enough cards left. Game over.")
            break
        play = play_again()
        
play_blackjack()