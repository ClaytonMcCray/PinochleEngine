from random import randint, shuffle

# TODO ########################################################
# (1) Need to be able to play cards that have already been melded
# (2) See TODO in find_best_meld
# (3) Add option to swap dix for trump (also double check official rules about that)
# (4) See TODO in CLIPinochle2.py
#################################################################


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
    pinochle = []  # assigned value at the opening of each game in open_game
    meld_score_values = [40, 20, 20, 20, 150, 100, 80, 60, 40, 10]
    melds = [royal_marriage, marriage_one, marriage_two, marriage_three, 
            flush, aces, kings, queens, jacks, dix]
    ############################################################
    trick_winner = ''
    dealer = 'player'  # opening value to be edited by game
    lead = 'computer'  # opening value to be edited by game

#################################################################


# a Deck in this case is just a special stack that gets dealt from the last index upwards
# not to be confused with a deque
class Deck:
    def __init__(shuffle=True):
        self.raw_deck = ['AS', '10S', 'KS', 'QS', 'JS', '9S', 'AC', '10C', 
                        'KC', 'QC', 'JC', '9C', 'AD', '10D', 'KD', 'QD', 'JD',
                        '9D', 'AH', '10H', 'KH', 'QH', 'JH', '9H', 'AS', 
                        '10S', 'KS', 'QS', 'JS', '9S', 'AC', '10C', 'KC',
                        'QC', 'JC', '9C', 'AD', '10D', 'KD', 'QD', 'JD', 
                        '9D', 'AH', '10H', 'KH', 'QH', 'JH', '9H']
        self.deck = None
        self.shuffle() if shuffle else self.set_deck(self.raw_deck)
        self.dix = None  # this will be empty until the user calls set_dix()


    def set_deck(self, deck):
        self.deck = [card for card in deck]
        
    
    # technically someone is probably cheating if they change this value, but I'm not the boss
    def set_dix(self, card=self.peek())  # hmmm card=self.peek() might be invalid sytax
        self.dix = card

    
    def get_dix(self):
        return self.dix


    def shuffle(self):
        self.deck = [card for card in self.raw_deck]  # deep copy
        shuffle(self.deck)

    def peek(self, idx=-1):
        return self.deck[idx]


    def deal_card(self):
        return self.deck.pop()



class Player:
    def __init__(self, opening_hand, trump, score):
        self.hand = []
        self.set_hand(opening_hand)
        self.trump = trump
        self.organize_hand()
        self.score = score
        self.won_cards = []
        self.melds = []

    def get_score(self):
        return self.score

    def set_melds(self, attempt):
        ind_meld = []  # tmp to hold tokens from attempt after removed from self.hand
        # make sure that the attempted cards were actually in the players hand; 
        # if so, add to ind_meld, pop from hand
        for i in attempt:
            for j in self.hand:
                if i == j:
                    ind_meld.append(j)
                    self.hand.remove(j)
        score, success = get_meld_score(ind_meld, self.trump)
        if success:
            self.score += score
            self.melds.append(ind_meld)
            return True
        else:
            for i in ind_meld:  # put un-melded cards back in the players hand
                self.hand.append(i)
            self.organize_hand()
            return False

    def set_hand(self, cards):  # cards is a []
        self.hand = cards

    def get_hand(self):
        return self.hand

    def organize_hand(self):
        # these first few lines filter out the trump suit so it can go first
        suits = ['spades', 'hearts', 'clubs', 'diamonds']
        trump_suit = get_suit(self.trump)
        suits.remove(trump_suit)
        sorted_hand = []
        tmp_sorted = []
        # manually set the trumps
        for i in self.hand:
            if get_suit(i) == trump_suit:
                tmp_sorted.append(get_rank(self.trump, i))
        tmp_sorted.sort()
        for card in tmp_sorted:
            sorted_hand.append(card)
        tmp_sorted = []
        for i in suits:  # now the rest of the cards will get sorted behind the trump
            for j in self.hand:
                if get_suit(j) == i:
                    tmp_sorted.append(get_rank(self.trump, j))
            tmp_sorted.sort()
            for card in tmp_sorted:
                sorted_hand.append(card)
            tmp_sorted = []
        token_sorted_hand = []
        for rank in sorted_hand:
            token_sorted_hand.append(get_card_from_rank(self.trump, rank))
        self.set_hand(token_sorted_hand)

    def update_hand(self, played_card, new_card):
        # checks the hand and the melds for the played card
        found_card = False
        if played_card in self.hand:
            self.hand.remove(played_card)
            found_card = True
        else:
            for i in self.melds:
                if played_card in i:
                    i.remove(played_card)
                    found_card = True
        if found_card:
            self.hand.append(new_card)
            self.organize_hand()
        else:
            raise IndexError('Card Not Found!')

    def hand_contains(self, cards):
        tmp = False
        for i in cards:
            if i in self.hand:
                tmp = True
        return tmp

    def set_won_cards(self, cards):
        for i in cards:
            self.won_cards.append(i)

    def get_playable_cards(self, one_d_list=False):  # unlike Computer, Player defaults to a 1D list
        cards = []
        if one_d_list:
            for i in self.hand:
                cards.append(i)
            for j in self.melds:
                for q in j:
                    cards.append(q)
        else:
            cards = [self.hand, self.melds]
        return cards


class Computer:
    def __init__(self, hand, trump, score):
        self.score = score
        self.hand = []
        self.set_hand(hand)
        self.trump = trump
        self.played_cards = []
        self.won_cards = []
        self.melds = []

    def get_score(self):
        return self.score

    def get_playable_cards(self, one_d_list=True):  # unlike Player, Computer defaults to a 1D list
        cards = []
        if one_d_list:
            for i in self.hand:
                cards.append(i)
            for j in self.melds:
                for q in j:
                    cards.append(q)
        else:
            cards = [self.hand, self.melds]
        return cards

    def set_hand(self, cards):  # cards is a []
        self.hand = cards

    def set_won_cards(self, cards):
        for i in cards:
            self.won_cards.append(i)

    def update_hand(self, played_card, new_card):
        # this checks melds and the hand for the played card
        if played_card in self.hand:
            self.hand.remove(played_card)
        else:
            for i in self.melds:
                if played_card in i:
                    i.remove(played_card)
        self.hand.append(new_card)

    def update_played_cards(self, player, computer):
        self.played_cards.append(player)
        self.played_cards.append(computer)

    def get_hand(self):
        return self.hand

    # for lead: if false, -> player is lead; else -> computer
    def computer_plays(self, lead, opponent_card=''):
        ranked_hand = []
        for i in self.get_playable_cards():
            ranked_hand.append(get_rank(self.trump, i))
        ranked_hand.sort()  # ranked hand contains melds if they exist
        if not hand_contains_melds(self.hand, self.trump):  # unedited as of the addition of get_playable_cards
            if not lead:                                        # because if it doesn't contain melds,
                if ranked_hand[0] < get_rank(self.trump, opponent_card):  # then self.hand == ranked_hand (in tokens)
                    return get_card_from_rank(self.trump, ranked_hand[0])
                else:
                    if get_card_from_rank(self.trump, ranked_hand[-1]) != '9D':
                        return get_card_from_rank(self.trump, ranked_hand[-1])
                    else:
                        return get_card_from_rank(self.trump, ranked_hand[-2])
            else:  # if the computer leads with no melds, play the strongest card it has
                return get_card_from_rank(self.trump, ranked_hand[0])
        else:                       # all of this should still work because non-melded cards aren't considered
            meld_score, high_meld, non_playable = find_best_meld(self.hand, self.trump)
            # the nested for loop below removes all the cards that match a meld from the hand
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

    def set_melds(self):
        if hand_contains_melds(self.hand, self.trump):  # hand_contains_melds should return boolean
            _, tmp_meld, __ = find_best_meld(self.hand, self.trump)
            self.melds.append(tmp_meld)
            # remove melded cards from hand
            for i in tmp_meld:
                self.hand.remove(i)
            score, ____ = get_meld_score(tmp_meld, self.trump)
            self.score += score
            return True
        else:
            return False

    def get_melds(self):
        return self.melds


def shuffle(deck):


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
    trump = deck[-1]  # TODO shouldn't this be deck[0]?
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

    trump_suit = get_suit(trump)
    if trump_suit == 'diamonds':
        for i in range(len(d_trump)):
            if d_trump[i] == card:
                return i
    elif trump_suit == 'clubs':
        for i in range(len(c_trump)):
            if c_trump[i] == card:
                return i
    elif trump_suit == 'hearts':
        for i in range(len(h_trump)):
            if h_trump[i] == card:
                return i
    elif trump_suit == 'spades':
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

    trump_suit = get_suit(trump)
    if trump_suit == 'diamonds':
        return d_trump[rank]
    elif trump_suit == 'clubs':
        return c_trump[rank]
    elif trump_suit == 'hearts':
        return h_trump[rank]
    elif trump_suit == 'spades':
        return s_trump[rank]


def open_game(trump, game_counter=0):
    if '9' in trump:
        Variables.trump_is_dix = True

    # set up the pinochle score
    qs_rank = get_rank(trump, 'QS')
    jd_rank = get_rank(trump, 'JD')
    Variables.pinochle = [qs_rank, jd_rank]
    Variables.melds.append(Variables.pinochle)
    Variables.meld_score_values.append(40)

    if game_counter % 2 == 0:
        return 'player', 'computer'  # dealer, lead; True = computer, False = player
    else:
        return 'computer', 'player'  # dealer, lead; True = computer, False = player


def hand_contains_melds(hand, trump):
    ranked_hand = []
    has_melds = False
    for i in hand:
        ranked_hand.append(get_rank(trump, i))
    # if all of the ranks for a meld exist in the sub list, it will return True
    for i in Variables.melds:
        for ranks in i:
            if ranks in ranked_hand:
                has_melds = True
            else:
                has_melds = False
                break
        if has_melds:
            break
    # the pinochle meld is independent of rank, so it is done here with tokens
    if 'QS' in hand and 'JD' in hand:
        has_melds = True
    return has_melds


# this method really isn't thorougly tested since making a pinochle a ranked meld available in Variables
def find_best_meld(hand, trump):
    ranked_hand = []
    for i in hand:
        ranked_hand.append(get_rank(trump, i))
    point_values = []
    cards = []
    exists = False
    for i in range(len(Variables.melds)):
        for ranks in Variables.melds[i]:
            if ranks in ranked_hand:
                exists = True
            else:
                exists = False
                break
        if exists:
            point_values.append(Variables.meld_score_values[i])
            tmp = []  # holds the card names of the cards in the current meld
            for c in Variables.melds[i]:
                tmp.append(get_card_from_rank(trump, c))
            cards.append(tmp)
    unordered_points = point_values
    point_values.sort()
    try:  # I'm pretty sure that this will throw an error if the hand contains no melds. Hence the try
        highest_score = point_values[-1]
    except IndexError:
        highest_score = 0
    for i in range(len(unordered_points)):
        for q in point_values:
            if unordered_points[i] == q:
                return highest_score, cards[i], cards  # point value of highest meld, highest meld, all melds,


# check the suit of a given card. this will regulate the way it is handled
def get_suit(card):
    if 'S' in card:
        return 'spades'
    elif 'H' in card:
        return 'hearts'
    elif 'D' in card:
        return 'diamonds'
    elif 'C' in card:
        return 'clubs'
    else:
        raise IndexError('Must call on a card object!')


# returns True if lead wins, False if follower wins
def determine_winner(lead_card, follower_card, trump):
    lead_suit = get_suit(lead_card)
    follower_suit = get_suit(follower_card)
    trump_suit = get_suit(trump)
    if get_rank(trump, lead_card) <= get_rank(trump, follower_card):  # the lead played a higher card
        return True
    else:  # the follower played a higher card
        if (lead_suit == follower_suit) or (follower_suit == trump_suit):  # check that leader followed suit or trumped
            return False
        else:
            return True


# this is where one of the players has gone over the match_points score
def is_match_over(match_points, current_scores):
    # check that at least one player is over match points
    if current_scores[0] >= match_points or current_scores[1] >= match_points:
        # check that ONLY one player is over match points
        if current_scores[0] < match_points or current_scores[1] < match_points:
            return True
        else:
            return False


# it is important to remember that this method takes TOKENS not ranked cards
def get_meld_score(meld_tokens, trump):
    rank_ind_meld = []  # tmp to hold ranked version of the meld
    for card in meld_tokens:
        rank_ind_meld.append(get_rank(trump, card))
    # check that the meld is a real meld option
    for i in range(len(Variables.melds)):
        if rank_ind_meld == Variables.melds[i]:
            meld_score_index = i
            success = True
            break
    try:
        return Variables.meld_score_values[meld_score_index], success
    except NameError:
        return 0, False

