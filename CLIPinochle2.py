import pinochle_engine as pe


# useful functions unrelated to actual gameplay ###############
def print_hand(hand):
    printable = '| '
    for i in hand:
        printable += i + ' '
    printable += '|'
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
match_points_mod = 0
current_score_mod = [0, 0]  # [computer, player]
################################################
try:
    match_points_mod = int(input('How many points do you want to play to?\n'))
except ValueError:
    print('Invalid input! You must enter a positive integer.')
    exit(1)


# the loop about to begin controls the looping of a match
def game_play(match_points, current_scores):
    while current_scores[0] < match_points and current_scores[1] < match_points:
        # OPENING #######################################################
        deck = pe.shuffle(pe.raw_deck)
        if pe.Variables.dealer == 'player':
            comp_hand, player_hand, stock, trump = pe.deal(deck)
            pe.Variables.lead = 'computer'
        elif pe.Variables.dealer == 'computer':
            player_hand, comp_hand, stock, trump = pe.deal(deck)
            pe.Variables.lead = 'player'
        else:
            print('Error with dealer assignment in pinochle_engine!')
            player_hand, comp_hand, stock, trump = 0, 0, 0, 0  # to block pep8 issues with assignment
            exit(1)
        player = pe.Player(player_hand, trump, current_scores[1])
        computer = pe.Computer(comp_hand, trump, current_scores[0])
        # END OPENING ######################################################
        # THE PLAY #########################################################
        while len(stock) > 0:
            # TRICK TAKING #################################################
            print('YOUR hand:')
            player.organize_hand()
            print_hand(player.get_hand())
            if pe.Variables.lead == 'player':
                print('YOU are the lead. Play a card.')
                player_card = input_player_card(player.get_hand())
                comp_card = computer.computer_plays(False, player_card)
                print('YOU played: ' + player_card + '\t\tCOMPUTER played: ' + comp_card)
                if pe.determine_winner(player_card, comp_card, trump):
                    print('YOU have won this trick!')
                    pe.Variables.lead = 'player'
                    # to keep track of the cards a player has won until the end of the hand
                    player.set_won_cards([player_card, comp_card])
                    player.update_hand(player_card, stock.pop(0))
                    computer.update_hand(comp_card, stock.pop(0))
                    pe.Variables.trick_winner = 'player'
                else:
                    print('COMPUTER has won this trick.')
                    pe.Variables.lead = 'computer'
                    # to keep track of the cards a player has won until the end of the hand
                    computer.set_won_cards([player_card, comp_card])
                    computer.update_hand(comp_card, stock.pop(0))
                    player.update_hand(player_card, stock.pop(0))
                    pe.Variables.trick_winner = 'computer'
            else:
                print('COMPUTER is the lead. It plays:')
                comp_card = computer.computer_plays(True)
                print(comp_card)
                print('YOU must play.')
                player_card = input_player_card(player.get_hand())
                if pe.determine_winner(comp_card, player_card, trump):
                    print('COMPUTER has won this trick!')
                    pe.Variables.lead = 'computer'
                    # to keep track of the cards a player has won until the end of the hand
                    computer.set_won_cards([player_card, comp_card])
                    computer.update_hand(comp_card, stock.pop(0))
                    player.update_hand(player_card, stock.pop(0))
                    pe.Variables.trick_winner = 'computer'
                else:
                    print('YOU have won this trick!')
                    pe.Variables.lead = 'player'
                    # to keep track of the cards a player has won until the end of the hand
                    player.set_won_cards([player_card, comp_card])
                    player.update_hand(player_card, stock.pop(0))
                    computer.update_hand(comp_card, stock.pop(0))
                    pe.Variables.trick_winner = 'player'
            # END TRICK TAKING ###########################################
            # TODO in The Play
            # (1) Add winner melds using the pe.Variables.trick_winner to know who won
            # (2) score melds
            # (3) check that won cards are being collected with print statements
            # (4) Note that drawing cards was included in TRICK TAKING





game_play(match_points_mod, current_score_mod)
