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
    print("Your hand: ", hand, "\nYour total: ", total)
    
    
def dealer_print(hand, total): 
    """
    Prints dealer's current hand and total
    """
    print("Dealer hand: ", hand, "\nDealer total: ", total)
    
    
def dealer_turn(your_hand, dealer_hand, total, dtotal, deck, turn=True): 
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
        if total > 21: # Evaluating a player's hand to see if they have an ace
            check_ace(your_hand)
            total = hand_total(your_hand)
            player_print(your_hand, total)
            continue
            
        dtotal = hand_total(dealer_hand)
        dealer_print(dealer_hand, dtotal)

        while dtotal <= 16: # Dealing cards to the dealer if they have less than or equal to 16
            deal_card(dealer_hand, deck)
            dtotal = hand_total(dealer_hand)
            dealer_print(dealer_hand, dtotal)

        if dtotal == 21: # Checking if the dealer wins
            print("Game Over. House wins.")
            loss += 1
            break

        elif dtotal > 21: # Checking if the dealer busts
            if check_ace(dealer_hand):
                continue
            else:
                print("Dealer busts! You win!")
                wins += 1
                break

        elif 17 <= dtotal <= 21: # Comparing dealer hand to player hand
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
    return [wins, loss, draw]


def play_again():
    """
    Loops the game
    """
    while True: # Asking the player to play again or not
        ans = input("Play again? \n").lower()
        if ans == 'yes' or ans == 'y':
            return True
        elif ans == 'no' or ans == 'n':
            return False
        else:
            print("Yes or no? ")
            continue
            
def blackjack(deck):
    """
    Playing Blackjack
    """
    your_hand   = deal_card([], deck, 2)
    dealer_hand = deal_card([], deck, 2)

    print("Your hand: ", your_hand)
    print("Dealer hand: ", dealer_hand[0])
    
    # Tallying wins, losses, and draws
    wins = 0
    draw = 0
    loss = 0
    
    # Looping through the moves
    while len(deck) > 1:
        print('Remaining cards: ', len(deck), '\n')
        
        # Checking if the player has a natural blackjack
        if hand_total(your_hand) == 21 and hand_total(dealer_hand) < 21:
            dealer_print(dealer_hand, hand_total(dealer_hand))
            print("Congratulations! Blackjack!")
            wins += 1
            break
        
        # Checking if the player and the dealer tie if they both have natural blackjacks
        elif hand_total(your_hand) == 21 and hand_total(dealer_hand) == 21:
            dealer_print(dealer_hand, hand_total(dealer_hand))
            print("It's a draw. Bet is returned.")
            draw += 1
            break
            
        # Allowing the player to make a move
        move = input("Hit or stay? ").lower()
        
        if move == "hit":
            deal_card(your_hand, deck)
            total = hand_total(your_hand)
            if  total > 21:              # Checking if the player busts
                if check_ace(your_hand): # Checking for an ace in the player hand
                    total = hand_total(your_hand)
                    player_print(your_hand, total)
                    continue
                else:                    # Otherwise they bust
                    player_print(your_hand, total)
                    print("Dealer wins. You lose.")
                    loss += 1
                    break
            elif total < 21:             # Going back to asking the player for a move
                player_print(your_hand, total)
                continue
            elif total == 21:            # Checking if the player succeeded in achieving blackjack
                player_print(your_hand, total)
                print("Blackjack! You win!")
                wins += 1
                break
        elif move == "stay":
            total  = hand_total(your_hand)
            dtotal = hand_total(dealer_hand)
            
            # Running the function for the dealer's turn
            result = dealer_turn(your_hand, dealer_hand, total, dtotal, deck)
            
            # The results of the dealer's turn
            wins += result[0]
            loss += result[1]
            draw += result[2]
            break
                
        else:
            # Continuing the loop if input was different from 'hit' or 'stay'
            print('Please type hit or stay')
            continue
            
    # Returning the results of the game        
    return [wins, loss, draw]

def play_blackjack():
    """
    Looping the game until no cards left
    """
    deck = create_deck()
    
    play = True
    wins = 0
    rounds_played = 0
    
    while play:
        
        # Running blackjack
        game = blackjack(deck)
        
        # Recording the results: wins, loss, draw
        wins += game[0]
        rounds_played += sum(game)
        
        print("Wins: ", result, '/', rounds_played)
        
        # Determining if there are enough cards left
        if len(deck) < 6:
            print("Not enough cards left. Game over.")
            break
        play = play_again()
        
play_blackjack()