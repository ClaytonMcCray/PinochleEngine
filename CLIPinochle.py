import pinochle_engine as pe


def input_player_card(hand):
    while True:
        card = input()
        if card in hand:
            break
        else:
            print('YOU do not hold that card!')
    return card


def game_play(lead_player, comp_hand, p_hand, trump):
    if not lead_player:
        player_card = input_player_card(p_hand)
        computer_card = computer.computer_plays(lead_player, player_card)
        print('YOU played: ' + player_card + '\tCOMPUTER played: ' + computer_card)
        if pe.get_rank(trump_card, player_card) <= pe.get_rank(trump_card, computer_card):
            print('YOU won this trick!')
            winner = False
        else:
            print('COMPUTER won this trick!')
            winner = True
    else:
        computer_card = computer.computer_plays(lead_player, 'comp_is_lead')
        print('COMPUTER played: ' + computer_card)
        player_card = input_player_card(p_hand)
        if pe.get_rank(trump_card, computer_card) <= pe.get_rank(trump_card, player_card):
            print('COMPUTER won this trick!')
            winner = True
        else:
            print('YOU won this trick!')
            winner = False
    return player_card, computer_card, winner  # winner is the winner of the trick, True = computer

game_count = 0  # this will determine whose turn it is to deal
while True:  # this loop will eventually control the entire match
    computer_hand, player_hand, pe.Variables.stock, trump_card = pe.deal(pe.shuffle(pe.raw_deck))
    dealer, lead = pe.open_game(game_count, trump_card)  # dealer = False -> player, else: -> computer
    if not dealer:  # i.e. player is the dealer
        print('YOU are the dealer!')
    else:
        print('The COMPUTER deals!')
    print('Trumps: ' + trump_card)
    player = pe.Player(player_hand, trump_card)
    computer = pe.Computer(computer_hand, trump_card)
    while len(pe.Variables.stock) > 0:  # this loop controls the individual game
        player.print_hand()
        p_card, c_card, first_draw = game_play(lead, computer.hand, player.hand, trump_card)
        if not first_draw:
            player.update_hand(p_card, pe.Variables.stock.pop(0))
            computer.update_hand(c_card, pe.Variables.stock.pop(0))
        else:
            computer.update_hand(c_card, pe.Variables.stock.pop(0))
            player.update_hand(p_card, pe.Variables.stock.pop(0))


    break

