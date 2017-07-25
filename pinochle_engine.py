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
        self.played_cards = []

    def set_hand(self, cards):  # cards is a []
        self.hand = cards

    def update_hand(self, played_card, new_card):
        self.hand.append(new_card)
        self.hand.remove(played_card)

    def update_played_cards(self, player, computer):
        self.played_cards.append(player)
        self.played_cards(computer)


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


def hand_contains_melds(hand, trump):
    ranked_hand = []
    has_melds = False
    for i in hand:
        ranked_hand.append(get_rank(trump, i))
    royal_marriage = [2, 3]
    marriage_one = [12, 15]
    marriage_two = [13, 16]
    marriage_three = [14, 17]
    flush = [0, 1, 2, 3, 4]
    aces = [0, 6, 7, 8]
    kings = [2, 12, 13, 14]
    queens = [3, 15, 16, 17]
    jacks = [4, 18, 19, 20]
    dix = [5]
    melds = [royal_marriage, marriage_one, marriage_two, marriage_three, flush, aces, kings, queens, jacks, dix]
    # if all of the ranks for a meld exist in the sub list, it will return True
    for i in melds:
        for ranks in i:
            if ranks in ranked_hand:
                has_melds = True
            else:
                has_melds = False
                break
        if has_melds:
            break
    # the pinochle meld is independent of rank, so it is done here with letters
    if 'QS' in hand and 'JD' in hand:
        has_melds = True
    return has_melds


# for lead: if false, -> player is lead; else -> computer
def computer_plays(lead, hand, opponent_card, trump):
    if not hand_contains_melds(hand):
        ranked_hand = []
        for i in hand:
            ranked_hand.append(get_rank(trump, i))
        ranked_hand.sort()
        if not lead:
            if ranked_hand[0] > get_rank(trump, opponent_card):
                return get_card_from_rank(trump, ranked_hand[0])
            else:
                if get_card_from_rank(trump, ranked_hand[-1]) != '9D':
                    return get_card_from_rank(trump, ranked_hand[-1])
                else:
                    return get_card_from_rank(trump, ranked_hand[-2])
