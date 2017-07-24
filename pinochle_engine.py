from random import randint

raw_deck = ['AS', '10S', 'KS', 'QS', 'JS', '9S', 'AC', '10C', 'KC', 'QC', 'JC', '9C', 'AD', '10D', 'KD', 'QD', 'JD',
            '9D', 'AH', '10H', 'KH', 'QH', 'JH', '9H', 'AS', '10S', 'KS', 'QS', 'JS', '9S', 'AC', '10C', 'KC',
            'QC', 'JC', '9C', 'AD', '10D', 'KD', 'QD', 'JD', '9D', 'AH', '10H', 'KH', 'QH', 'JH', '9H']

# Global settings will go here ##################################


class Variables:
    trump_is_dix = False  # this will track if dix is trump

#################################################################


class Player:
    def __init__(self, opening_hand, trump):
        self.hand = []
        self.set_hand(opening_hand)
        self.trump = trump
        self.organize_hand()

    def set_hand(self, cards):  # cards is a []
        self.hand = cards

    def organize_hand(self):
        hand_rank = []
        for i in self.hand:
            hand_rank.append(get_rank(self.trump, i))
        hand_rank.sort()
        sorted_hand = []
        for i in hand_rank:
            sorted_hand.append(get_card_from_rank(self.trump, i))
        self.set_hand(sorted_hand)

    def print_hand(self):
        printable = '| '
        for i in self.hand:
            printable += i + ' '
        printable += '|'
        print(printable)

    def update_hand(self, played_card, new_card):
        self.hand.append(new_card)
        self.hand.remove(played_card)
        self.organize_hand()


class Computer:
    def __init__(self, hand, trump):
        self.hand = []
        self.set_hand(hand)
        self.trump = trump

    def set_hand(self, cards):  # cards is a []
        self.hand = cards

    def update_hand(self, played_card, new_card):
        self.hand.append(new_card)
        self.hand.remove(played_card)


def shuffle(deck):

    tmp = deck  # so that deck can be returned
    length_total_deck = len(deck)  # this stops me from hard coding the deck length in. more robust
    deck = []
    while True:
        card = tmp[randint(0, 47)]
        counter = 0  # there are two of each card in a pinochle deck, this is to count how many of a give are there
        for x in deck:
            if x == card:  # if the searched card is already in the deck, it finds out how many
                counter += 1
        if counter < 2:
            deck.append(card)
        if len(deck) == length_total_deck:
            break
    return deck


def deal(deck):
    dealer_hand = []
    opponent_hand = []
    counter = 0
    for _ in range(4):
        for a in range(3):
            opponent_hand.append(deck[counter])
            counter += 1
        for a in range(3):
            dealer_hand.append(deck[counter])
            counter += 1

    stock = deck[counter:]
    trump = deck[-1]
    return opponent_hand, dealer_hand, stock, trump


def get_rank(trump, card):  # smaller ranks mean more powerful cards
    d_trump = ['AD', '10D', 'KD', 'QD', 'JD', '9D', 'AS', 'AH', 'AC', '10S', '10H', '10C', 'KS', 'KH', 'KC', 'QS',
               'QH', 'QC', 'JS', 'JH', 'JC', '9S', '9H', '9C']
    c_trump = ['AC', '10C', 'KC', 'QC', 'JC', '9C', 'AS', 'AH', 'AD', '10S', '10H', '10D', 'KS', 'KH', 'KD', 'QS',
               'QH', 'QD', 'JS', 'JH', 'JD', '9S', '9H', '9D']
    h_trump = ['AH', '10H', 'KH', 'QH', 'JH', '9H', 'AS', 'AC', 'AD', '10S', '10C', '10D', 'KS', 'KC', 'KD', 'QS',
               'QC', 'QD', 'JS', 'JC', 'JD', '9S', '9C', '9D']
    s_trump = ['AS', '10S', 'KS', 'QS', 'JS', '9S', 'AH', 'AC', 'AD', '10H', '10C', '10D', 'KH', 'KC', 'KD', 'QH',
               'QC', 'QD', 'JH', 'JC', 'JD', '9H', '9C', '9D']

    if 'D' in trump:
        for i in range(len(d_trump)):
            if d_trump[i] == card:
                return i
    elif 'C' in trump:
        for i in range(len(c_trump)):
            if c_trump[i] == card:
                return i
    elif 'H' in trump:
        for i in range(len(h_trump)):
            if h_trump[i] == card:
                return i
    elif 'S' in trump:
        for i in range(len(s_trump)):
            if s_trump[i] == card:
                return i


def get_card_from_rank(trump, rank):
    d_trump = ['AD', '10D', 'KD', 'QD', 'JD', '9D', 'AS', 'AH', 'AC', '10S', '10H', '10C', 'KS', 'KH', 'KC', 'QS',
               'QH', 'QC', 'JS', 'JH', 'JC', '9S', '9H', '9C']
    c_trump = ['AC', '10C', 'KC', 'QC', 'JC', '9C', 'AS', 'AH', 'AD', '10S', '10H', '10D', 'KS', 'KH', 'KD', 'QS',
               'QH', 'QD', 'JS', 'JH', 'JD', '9S', '9H', '9D']
    h_trump = ['AH', '10H', 'KH', 'QH', 'JH', '9H', 'AS', 'AC', 'AD', '10S', '10C', '10D', 'KS', 'KC', 'KD', 'QS',
               'QC', 'QD', 'JS', 'JC', 'JD', '9S', '9C', '9D']
    s_trump = ['AS', '10S', 'KS', 'QS', 'JS', '9S', 'AH', 'AC', 'AD', '10H', '10C', '10D', 'KH', 'KC', 'KD', 'QH',
               'QC', 'QD', 'JH', 'JC', 'JD', '9H', '9C', '9D']

    if 'D' in trump:
        return d_trump[rank]
    elif 'C' in trump:
        return c_trump[rank]
    elif 'H' in trump:
        return h_trump[rank]
    elif 'S' in trump:
        return s_trump[rank]


def open_game(game_counter, trump):
    if '9' in trump:
        Variables.trump_is_dix = True

    if game_counter % 2 == 0:
        return False, True  # dealer, lead; True = computer, False = player
    else:
        return True, False  # dealer, lead; True = computer, False = player


def computer_plays(lead, hand, opponent_card, trump):
    return hand[randint(0, len(hand) - 1)]
