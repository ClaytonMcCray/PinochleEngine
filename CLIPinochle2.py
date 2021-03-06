#!./venv/bin/python3

import pinochle_engine as pe


# useful functions unrelated to actual gameplay ###############
def print_hand(hand):
    printable = '\t| '
    for i in hand[0]:
        printable += i + ' '
    printable += '|'
    # Add melds to the right
    printable += '\t'
    for i in hand[1]:
        printable += '|| '
        for j in i:
            printable += j + ' '
    printable += '||'
    print(printable)


def input_player_card(hand):
    played = False
    while not played:
        card = input()
        if card not in hand:
            print('YOU must play a card in your hand.')
        else:
            return card

#################################################################


# The MATCH
# MATCH variables ##############################
match_points_mod = 0  # why does this say "_mod"?
current_score_mod = {'computer' : 0, 'player' : 0}  # why does this have a trailing mod?
game_counter = 0
################################################
try:
    match_points_mod = int(input('How many points do you want to play to?\n'))
except ValueError:
    print('Invalid input! You must enter a positive integer.')
    exit(1)


# the loop about to begin controls the looping of a match
def game_play(match_points, current_scores):
    while current_scores['computer'] < match_points and current_scores['player'] < match_points:
        # OPENING #######################################################
        trick_counter = 0  # for tracking which trick is going on
        deck = pe.Deck()
        if pe.Variables.dealer == 'player':
            comp_hand, player_hand = pe.deal(deck)
            pe.Variables.lead = 'computer'
        elif pe.Variables.dealer == 'computer':
            player_hand, comp_hand = pe.deal(deck)
            pe.Variables.lead = 'player'
        else:
            print('Error with dealer assignment in pinochle_engine!')
            player_hand, comp_hand = None, None  # to block pep8 issues with assignment
            exit(1)
        pe.open_game(deck.get_trump())
        player = pe.Player(player_hand, deck.get_trump(), current_scores['player'])
        computer = pe.Computer(comp_hand, deck.get_trump(), current_scores['computer'])
        # END OPENING ######################################################
        # THE PLAY #########################################################
        while len(deck) > 0:
            trick_counter += 1
            print('(' + str(trick_counter) + ')')
            # TRICK TAKING #################################################
            print('\tTrump is: ' + deck.get_trump())
            print('\tYOUR cards:')
            player.organize_hand()
            print_hand(player.get_playable_cards())
            if pe.Variables.lead == 'player':
                print('\tYOU are the lead. Play a card.')
                player_card = input_player_card(player.get_playable_cards(True))
                comp_card = computer.computer_plays(False, player_card)
                print('\tYOU played: ' + player_card + '\t\tCOMPUTER played: ' + comp_card)
                if pe.determine_winner(player_card, comp_card, deck.get_trump()):
                    print('\tYOU have won this trick!')
                    pe.Variables.lead = 'player'
                    # to keep track of the cards a player has won until the end of the hand
                    player.set_won_cards([player_card, comp_card])
                    player.update_hand(player_card, deck.deal_card())
                    computer.update_hand(comp_card, deck.deal_card())
                    pe.Variables.trick_winner = 'player'
                else:
                    print('\tCOMPUTER has won this trick.')
                    pe.Variables.lead = 'computer'
                    # to keep track of the cards a player has won until the end of the hand
                    computer.set_won_cards([player_card, comp_card])
                    computer.update_hand(comp_card, deck.deal_card())
                    player.update_hand(player_card, deck.deal_card())
                    pe.Variables.trick_winner = 'computer'
            else:
                print('\tCOMPUTER is the lead. It plays:')
                comp_card = computer.computer_plays(True)
                print(comp_card)
                print('\tYOU must play.')
                player_card = input_player_card(player.get_playable_cards(True))
                print('\tYOU played: ' + player_card + '\t\tCOMPUTER played: ' + comp_card)
                if pe.determine_winner(comp_card, player_card, deck.get_trump()):
                    print('\tCOMPUTER has won this trick!')
                    pe.Variables.lead = 'computer'
                    # to keep track of the cards a player has won until the end of the hand
                    computer.set_won_cards([player_card, comp_card])
                    computer.update_hand(comp_card, deck.deal_card())
                    player.update_hand(player_card, deck.deal_card())
                    pe.Variables.trick_winner = 'computer'
                else:
                    print('\tYOU have won this trick!')
                    pe.Variables.lead = 'player'
                    # to keep track of the cards a player has won until the end of the hand
                    player.set_won_cards([player_card, comp_card])
                    player.update_hand(player_card, deck.deal_card())
                    computer.update_hand(comp_card, deck.deal_card())
                    pe.Variables.trick_winner = 'player'
            # END TRICK TAKING ###########################################
            # TODO in The Play
            # (3) check that won cards are being collected with print statements
            # (5) Test the new player.set_melds(). Also the computer.set_melds().
            # (6) Fix annoying bars around computer.set_melds() printout from above
            # BEGIN MELDING ##############################################
            if pe.Variables.trick_winner == 'player':
                print_hand(player.get_playable_cards())
                while True:
                    attempt_meld = input('\tWhat do YOU want to meld? Type "none" to skip.\n')
                    if attempt_meld == "none":
                        break
                    else:
                        attempt_meld = attempt_meld.split()
                    if player.set_melds(attempt_meld):
                        print('\tOkay! YOUR new hand:')
                        print_hand(player.get_playable_cards())
                        break
                    else:
                        print('\tOops, that didn\'t work. Try a different meld.')
            else:
                print('\tThe COMPUTER will now meld.')
                if computer.set_melds():
                    print_hand([[], computer.get_melds()])
                else:
                    print('\tThe COMPUTER has not melded!')
            print('\tHere are the scores:')
            print('\tYOU: ' + str(player.get_score()) + '\t\tCOMPUTER: ' + str(computer.get_score()))
        break



game_play(match_points_mod, current_score_mod)

