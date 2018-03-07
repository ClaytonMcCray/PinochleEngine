from random import randint

raw_deck = ['AS', '10S', 'KS', 'QS', 'JS', '9S', 'AC', '10C', 'KC', 'QC', 'JC', '9C', 'AD', '10D', 'KD', 'QD', 'JD',
            '9D', 'AH', '10H', 'KH', 'QH', 'JH', '9H', 'AS', '10S', 'KS', 'QS', 'JS', '9S', 'AC', '10C', 'KC',
            'QC', 'JC', '9C', 'AD', '10D', 'KD', 'QD', 'JD', '9D', 'AH', '10H', 'KH', 'QH', 'JH', '9H']

# Global settings will go here ##################################


class Variables:
    trump_is_dix = False  # this will track if dix is trump
    stock = []
    # melds ####################################################
    # Note that the pinochle meld is not included because it is independent
    # of trump (and therefore rank values)
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
    meld_score_values = [40, 20, 20, 20, 150, 100, 80, 60, 40, 10]
    ############################################################
    trick_winner = False

#################################################################


class Player:
    def __init__(self, opening_hand, trump):
        self.hand = []
        self.set_hand(opening_hand)
        self.trump = trump
        self.organize_hand()

    def set_hand(self, cards):  # cards is a []
        self.hand = cards

    def get_hand(self):
        return self.hand

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

    def hand_contains(self, cards):
        tmp = False
        for i in cards:
            if i in self.hand:
                tmp = True
        return tmp


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
        self.played_cards.append(computer)

    def get_hand(self):
        return self.hand

    # for lead: if false, -> player is lead; else -> computer
    def computer_plays(self, lead, opponent_card):
        ranked_hand = []
        for i in self.hand:
            ranked_hand.append(get_rank(self.trump, i))
        ranked_hand.sort()
        if not hand_contains_melds(self.hand, self.trump):
            if not lead:
                if ranked_hand[0] < get_rank(self.trump, opponent_card):
                    return get_card_from_rank(self.trump, ranked_hand[0])
                else:
                    if get_card_from_rank(self.trump, ranked_hand[-1]) != '9D':
                        return get_card_from_rank(self.trump, ranked_hand[-1])
                    else:
                        return get_card_from_rank(self.trump, ranked_hand[-2])
            else:  # if the computer leads with no melds, play the strongest card it has
                return get_card_from_rank(self.trump, ranked_hand[0])
        else:
            meld_score, high_meld, non_playable, pinochle = find_best_meld(self.hand, self.trump)
            # the nested for loop below removes all the cards that match a meld from the hand
            if pinochle:  # removes a pinochle if it's in the hand
                ranked_hand.remove(get_rank(self.trump, 'QS'))
                ranked_hand.remove(get_rank(self.trump, 'JD'))
            for meld in non_playable:
                for card in meld:
                    try:  # this is because if a card exists in multiple melds, it might have already been removed
                        ranked_hand.remove(get_rank(self.trump, card))
                    except ValueError:
                        pass
            if not lead:
                if ranked_hand[0] < get_rank(self.trump, opponent_card):
                    return get_card_from_rank(self.trump, ranked_hand[0])
                else:
                    if get_card_from_rank(self.trump, ranked_hand[-1]) != '9D':
                        return get_card_from_rank(self.trump, ranked_hand[-1])
                    else:
                        return get_card_from_rank(self.trump, ranked_hand[-2])
            else:  # play strongest hand not part of existing meld
                return get_card_from_rank(self.trump, ranked_hand[0])


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
    melds = [Variables.royal_marriage, Variables.marriage_one, Variables.marriage_two,
             Variables.marriage_three, Variables.flush, Variables.aces, Variables.kings, Variables.queens,
             Variables.jacks, Variables.dix]
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


def find_best_meld(hand, trump):
    ranked_hand = []
    for i in hand:
        ranked_hand.append(get_rank(trump, i))
    pinochle = False
    melds = [Variables.royal_marriage, Variables.marriage_one, Variables.marriage_two,
             Variables.marriage_three, Variables.flush, Variables.aces, Variables.kings, Variables.queens,
             Variables.jacks, Variables.dix]
    point_values = []
    cards = []
    exists = False
    if 'QS' in hand and 'JD' in hand:
        pinochle = True
    for i in range(len(melds)):
        for ranks in melds[i]:
            if ranks in ranked_hand:
                exists = True
            else:
                exists = False
                break
        if exists:
            point_values.append(Variables.meld_score_values[i])
            tmp = []  # holds the card names of the cards in the current meld
            for c in melds[i]:
                tmp.append(get_card_from_rank(trump, c))
            cards.append(tmp)
    unordered_points = point_values
    point_values.sort()
    highest_score = point_values[-1]
    for i in range(len(unordered_points)):
        for q in point_values:
            if unordered_points[i] == q:
                return highest_score, cards[i], cards, pinochle  # point value of highest meld, highest meld, all melds,
            # pinochle


# check the suit of a given card. this will regulate the way it is handled
def get_suit(card):
    if 'S' in card:
        return 'spades'
    elif 'H' in card:
        return 'hearts'
    elif 'D' in card:
        return 'diamonds'
    else:
        raise IndexError('Must call on a card object!')


# returns True if lead wins, False if follower wins
def determine_winner(lead, follower, trump):
    lead_suit = get_suit(lead)
    follower_suit = get_suit(follower)
    trump_suit = get_suit(trump)
    if get_rank(lead, trump) <= get_rank(follower, trump):  # the lead played a higher card
        return True
    else:  # the follower played a higher card
        if (lead_suit == follower_suit) or (follower_suit == trump_suit):  # check that leader followed suit or trumped
            return False
        else:
            return True


