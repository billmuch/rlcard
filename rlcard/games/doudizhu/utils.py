''' Doudizhu utils
'''

import os
import json
from collections import OrderedDict
import numpy as np
import threading
import collections
from itertools import combinations
from bisect import bisect_left

import rlcard

# Read required docs
ROOT_PATH = rlcard.__path__[0]

# a map of action to abstract action
with open(os.path.join(ROOT_PATH, 'games/doudizhu/jsondata/specific_map.json'), 'r') as file:
    SPECIFIC_MAP = json.load(file, object_pairs_hook=OrderedDict)

# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'games/doudizhu/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())

# a map of card to its type. Also return both dict and list to accelerate
with open(os.path.join(ROOT_PATH, 'games/doudizhu/jsondata/card_type.json'), 'r') as file:
    data = json.load(file, object_pairs_hook=OrderedDict)
    CARD_TYPE = (data, list(data), set(data))

# a map of type to its cards
with open(os.path.join(ROOT_PATH, 'games/doudizhu/jsondata/type_card.json'), 'r') as file:
    TYPE_CARD = json.load(file, object_pairs_hook=OrderedDict)

# rank list of solo character of cards
CARD_RANK_STR = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K',
                 'A', '2', 'B', 'R']
CARD_RANK_STR_INDEX = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, 
            '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 
            'K': 10, 'A': 11, '2': 12, 'B': 13, 'R': 14}
# rank list
CARD_RANK = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K',
             'A', '2', 'BJ', 'RJ']


def doudizhu_sort_str(card_1, card_2):
    ''' Compare the rank of two cards of str representation

    Args:
        card_1 (str): str representation of solo card
        card_2 (str): str representation of solo card

    Returns:
        int: 1(card_1 > card_2) / 0(card_1 = card2) / -1(card_1 < card_2)
    '''
    key_1 = CARD_RANK_STR.index(card_1)
    key_2 = CARD_RANK_STR.index(card_2)
    if key_1 > key_2:
        return 1
    if key_1 < key_2:
        return -1
    return 0


def doudizhu_sort_card(card_1, card_2):
    ''' Compare the rank of two cards of Card object

    Args:
        card_1 (object): object of Card
        card_2 (object): object of card
    '''
    key = []
    for card in [card_1, card_2]:
        if card.rank == '':
            key.append(CARD_RANK.index(card.suit))
        else:
            key.append(CARD_RANK.index(card.rank))
    if key[0] > key[1]:
        return 1
    if key[0] < key[1]:
        return -1
    return 0


def get_landlord_score(current_hand):
    ''' Roughly judge the quality of the hand, and provide a score as basis to
    bid landlord.

    Args:
        current_hand (str): string of cards. Eg: '56888TTQKKKAA222R'

    Returns:
        int: score
    '''
    score_map = {'A': 1, '2': 2, 'B': 3, 'R': 4}
    score = 0
    # rocket
    if current_hand[-2:] == 'BR':
        score += 8
        current_hand = current_hand[:-2]
    length = len(current_hand)
    i = 0
    while i < length:
        # bomb
        if i <= (length - 4) and current_hand[i] == current_hand[i+3]:
            score += 6
            i += 4
            continue
        # 2, Black Joker, Red Joker
        if current_hand[i] in score_map:
            score += score_map[current_hand[i]]
        i += 1
    return score


def get_optimal_action(probs, legal_actions):
    ''' Determine the optimal action from legal actions
    according to the probabilities of abstract actions.

    Args:
        probs (list): list of probabilities of abstract actions
        legal_actions (list): list of legal actions

    Returns:
        str: optimal legal action
    '''
    abstract_actions = [SPECIFIC_MAP[action] for action in legal_actions]
    action_probs = []
    for actions in abstract_actions:
        max_prob = -1
        for action in actions:
            prob = probs[ACTION_SPACE[action]]
            if prob > max_prob:
                max_prob = prob
        action_probs.append(max_prob)
    optimal_prob = max(action_probs)
    optimal_actions = [legal_actions[index] for index,
                       prob in enumerate(action_probs) if prob == optimal_prob]
    if len(optimal_actions) > 1:
        return np.random.choice(optimal_actions)
    return optimal_actions[0]


def cards2str(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of Card objects

    Returns:
        string: string representation of cards
    '''
    response = ''
    for card in cards:
        if card.rank == '':
            response += card.suit[0]
        else:
            response += card.rank
    return response

_local_objs = threading.local()
_local_objs.cached_candidate_cards = None
def contains_cards(candidate, target):
    ''' Check if cards of candidate contains cards of target.

    Args:
        candidate (string): A string representing the cards of candidate
        target (string): A string representing the number of cards of target

    Returns:
        boolean
    '''
    # In normal cases, most continuous calls of this function 
    #   will test different targets against the same candidate.
    # So the cached counts of each card in candidate can speed up 
    #   the comparison for following tests if candidate keeps the same.
    if not _local_objs.cached_candidate_cards or _local_objs.cached_candidate_cards != candidate:
        _local_objs.cached_candidate_cards = candidate
        cards_dict = collections.defaultdict(int)
        for card in candidate:
            cards_dict[card] += 1
        _local_objs.cached_candidate_cards_dict = cards_dict
    cards_dict = _local_objs.cached_candidate_cards_dict
    if (target == ''):
        return True
    curr_card = target[0]
    curr_count = 1
    for card in target[1:]:
        if (card != curr_card):
            if (cards_dict[curr_card] < curr_count):
                return False
            curr_card = card
            curr_count = 1
        else:
            curr_count += 1
    if (cards_dict[curr_card] < curr_count):
        return False
    return True

def encode_cards(plane, cards):
    ''' Encode cards and represerve it into plane.

    Args:
        cards (list or str): list or str of cards, every entry is a
    character of solo representation of card
    '''
    if not cards:
        return None
    layer = 1
    if len(cards) == 1:
        rank = CARD_RANK_STR.index(cards[0])
        plane[layer][rank] = 1
        plane[0][rank] = 0
    else:
        for index, card in enumerate(cards):
            if index == 0:
                continue
            if card == cards[index-1]:
                layer += 1
            else:
                rank = CARD_RANK_STR.index(cards[index-1])
                plane[layer][rank] = 1
                layer = 1
                plane[0][rank] = 0
        rank = CARD_RANK_STR.index(cards[-1])
        plane[layer][rank] = 1
        plane[0][rank] = 0

class DoudizhuRule(object):
    ''' Rule based playable cards generator '''

    def __init__(self, hand_cards):
        self.hand_cards = hand_cards
        self.cards_dict = collections.defaultdict(int)
        for card in hand_cards:
            self.cards_dict[card] += 1
        self.cards_count = np.array([self.cards_dict[k] for k in CARD_RANK_STR])
        self.non_zero_index = None
        self.more_than_1_index = None
        self.more_than_2_index = None
        self.more_than_3_index = None
        self.solo_chain_indexs = None
        self.pair_chain_indexs = None
        self.trio_chain_indexs = None        

    def chain_indexes(self, indexes_list):
        ''' Find chains for solos, pairs and trios by using indexes_list

        Args:
            indexes_list: the indexes of cards those have the same count, the count could be 1, 2, or 3.

        Returns: 
            list of tuples: [(start_index1, length1), (start_index1, length1), ...]

        '''
        chains = []
        prev_index = -100
        count = 0
        start = None
        for i in indexes_list:
            if (i[0] >= 12): #no chains for '2BR'
                break
            if (i[0] == prev_index + 1):
                count += 1
            else:
                if (count > 1):
                    chains.append((start, count))
                count = 1
                start = i[0]
            prev_index = i[0]
        if (count > 1):
            chains.append((start, count))
        return chains

    def solo_attachments(self, chain_start, chain_length, size):
        ''' Find solo attachments for trio_chain_solo_x and four_two_solo

        Args:
            chain_start: the index of start card of the trio_chain or trio or four
            chain_length: the size of the sequence of the chain, 1 for trio_solo or four_two_solo
            size: count of solos for the attachments

        Returns: 
            list of tuples: [attachment1, attachment2, ...]
                            Each attachment has two elemnts, 
                            the first one contains indexes of attached cards smaller than the index of chain_start,
                            the first one contains indexes of attached cards larger than the index of chain_start
        '''
        attachments = set()
        candidates = []
        prev_card = None
        same_card_count = 0
        for card in self.hand_cards:
            #dont count those cards in the chain
            if (CARD_RANK_STR_INDEX[card] >= chain_start and CARD_RANK_STR_INDEX[card] < chain_start + chain_length):
                continue
            if (card == prev_card):
                #attachments can not have bomb
                if (same_card_count == 3):
                    continue
                #attachments can not have 3 same cards consecutive with the trio (except 3 cards of '222')
                elif (same_card_count == 2 and (CARD_RANK_STR_INDEX[card] == chain_start - 1 or CARD_RANK_STR_INDEX[card] == chain_start + chain_length) and card != '2'):
                    continue
                else:
                    same_card_count += 1
            else:
                prev_card = card
                same_card_count = 1
            candidates.append(CARD_RANK_STR_INDEX[card])
        for attachment in combinations(candidates, size):
            if (attachment[-1] == 14 and attachment[-2] == 13):
                continue
            i = bisect_left(attachment, chain_start)
            attachments.add((attachment[:i], attachment[i:]))
        return list(attachments)

    def pair_attachments(self, chain_start, chain_length, size):
        ''' Find pair attachments for trio_chain_pair_x and four_two_pair

        Args:
            chain_start: the index of start card of the trio_chain or trio or four
            chain_length: the size of the sequence of the chain, 1 for trio_pair or four_two_pair
            size: count of pairs for the attachments

        Returns: 
            list of tuples: [attachment1, attachment2, ...]
                            Each attachment has two elemnts, 
                            the first one contains indexes of attached cards smaller than the index of chain_start,
                            the first one contains indexes of attached cards larger than the index of chain_start
        '''
        attachments = set()
        candidates = []
        for i in range(len(self.cards_count)):
            if (i >= chain_start and i < chain_start + chain_length):
                continue
            if (self.cards_count[i] == 2 or self.cards_count[i] == 3):
                candidates.append(i)
            elif (self.cards_count[i] == 4):
                candidates.append(i)
        for attachment in combinations(candidates, size):
            if (attachment[-1] == 14 and attachment[-2] == 13):
                continue
            i = bisect_left(attachment, chain_start)
            attachments.add((attachment[:i], attachment[i:]))
        return list(attachments)

    def get_non_zero_index(self):
        if (self.non_zero_index is None):
            self.non_zero_indexe = np.argwhere(self.cards_count > 0)
        return self.non_zero_indexe

    def get_more_than_1_index(self):
        if (self.more_than_1_index is None):
            self.more_than_1_index = np.argwhere(self.cards_count > 1)
        return self.more_than_1_index

    def get_more_than_2_index(self):
        if (self.more_than_2_index is None):
            self.more_than_2_index = np.argwhere(self.cards_count > 2)
        return self.more_than_2_index

    def get_more_than_3_index(self):
        if (self.more_than_3_index is None):
            self.more_than_3_index = np.argwhere(self.cards_count > 3)
        return self.more_than_3_index

    def get_solo_chain_indexes(self):
        if (self.solo_chain_indexs is None):
            self.solo_chain_indexs = self.chain_indexes(self.get_non_zero_index())
        return self.solo_chain_indexs

    def get_pair_chain_indexes(self):
        if (self.pair_chain_indexs is None):
            self.pair_chain_indexs = self.chain_indexes(self.get_more_than_1_index())
        return self.pair_chain_indexs

    def get_trio_chain_indexes(self):
        if (self.trio_chain_indexs is None):
            self.trio_chain_indexs = self.chain_indexes(self.get_more_than_2_index())
        return self.trio_chain_indexs

    def get_solo(self):
        return set([CARD_RANK_STR[i[0]] for i in self.get_non_zero_index()])

    def get_pair(self):
        return set([CARD_RANK_STR[i[0]] * 2 for i in self.get_more_than_1_index()])

    def get_bomb(self):
        return set([CARD_RANK_STR[i[0]] * 4 for i in self.get_more_than_3_index()])

    def get_four_two_solo(self):
        playable_cards = set()
        for i in self.get_more_than_3_index():
            for left, right in self.solo_attachments(i[0], 1, 2):
                pre_attached = ''
                for j in left:
                    pre_attached += CARD_RANK_STR[j]
                post_attached = ''
                for j in right:
                    post_attached += CARD_RANK_STR[j]
                playable_cards.add(pre_attached + CARD_RANK_STR[i[0]] * 4 + post_attached)
        return playable_cards

    def get_four_two_pair(self):
        playable_cards = set()
        for i in self.get_more_than_3_index():
            for left, right in self.pair_attachments(i[0], 1, 2):
                pre_attached = ''
                for j in left:
                    pre_attached += CARD_RANK_STR[j] * 2
                post_attached = ''
                for j in right:
                    post_attached += CARD_RANK_STR[j] * 2
                playable_cards.add(pre_attached + CARD_RANK_STR[i[0]] * 4 + post_attached)
        return playable_cards

    def get_solo_chain_n(self, n):
        if (n < 5 or n > 12):
            return set()
        playable_cards = set()
        for (start_index, length) in self.get_solo_chain_indexes():
            s, l = start_index, length
            while(l >= n):
                cards = ''
                for i in range(n):
                    cards += CARD_RANK_STR[s + i]
                playable_cards.add(cards)
                l -= 1
                s += 1
        return playable_cards

    def get_pair_chain_n(self, n):
        if (n < 3 or n > 10):
            return set()
        playable_cards = set()
        for (start_index, length) in self.get_pair_chain_indexes():
            s, l = start_index, length
            while(l >= n):
                cards = ''
                for i in range(n):
                    cards += CARD_RANK_STR[s + i] * 2
                playable_cards.add(cards)
                l -= 1
                s += 1
        return playable_cards

    def get_trio(self):
        return set([CARD_RANK_STR[i[0]] * 3 for i in self.get_more_than_2_index()])

    def get_trio_solo(self):
        playable_cards = set()
        for i in self.get_more_than_2_index():
            for j in self.get_non_zero_index():
                if (j < i):
                    playable_cards.add(CARD_RANK_STR[j[0]] + CARD_RANK_STR[i[0]] * 3)
                elif (j > i):
                    playable_cards.add(CARD_RANK_STR[i[0]] * 3 + CARD_RANK_STR[j[0]])
        return playable_cards

    def get_trio_pair(self):
        playable_cards = set()
        for i in self.get_more_than_2_index():
            for j in self.get_more_than_1_index():
                if (j < i):
                    playable_cards.add(CARD_RANK_STR[j[0]] * 2 + CARD_RANK_STR[i[0]] * 3)
                elif (j > i):
                    playable_cards.add(CARD_RANK_STR[i[0]] * 3 + CARD_RANK_STR[j[0]] * 2)
        return playable_cards

    def get_trio_chain_n(self, n):
        if (n < 2 or n > 6):
            return set()
        playable_cards = set()
        for (start_index, length) in self.get_trio_chain_indexes():
            s, l = start_index, length
            while(l >= n):
                cards = ''
                for i in range(n):
                    cards += CARD_RANK_STR[s + i] * 3
                playable_cards.add(cards)
                l -= 1
                s += 1
        return playable_cards

    def get_trio_solo_chain_n(self, n):
        if (n < 2 or n > 5):
            return set()
        playable_cards = set()
        for (start_index, length) in self.get_trio_chain_indexes():
            s, l = start_index, length
            while(l >= n):
                cards = ''
                for i in range(n):
                    cards += CARD_RANK_STR[s + i] * 3
                for left, right in self.solo_attachments(s, n, n):
                        pre_attached = ''
                        for j in left:
                            pre_attached += CARD_RANK_STR[j]
                        post_attached = ''
                        for j in right:
                            post_attached += CARD_RANK_STR[j]
                        playable_cards.add(pre_attached + cards + post_attached)
                playable_cards.add(cards)
                l -= 1
                s += 1
        return playable_cards

    def get_trio_pair_chain_n(self, n):
        if (n < 2 or n > 4):
            return set()
        playable_cards = set()
        for (start_index, length) in self.get_trio_chain_indexes():
            s, l = start_index, length
            while(l >= n):
                cards = ''
                for i in range(n):
                    cards += CARD_RANK_STR[s + i] * 3
                for left, right in self.pair_attachments(s, n, n):
                        pre_attached = ''
                        for j in left:
                            pre_attached += CARD_RANK_STR[j] * 2
                        post_attached = ''
                        for j in right:
                            post_attached += CARD_RANK_STR[j] * 2
                        playable_cards.add(pre_attached + cards + post_attached)
                playable_cards.add(cards)
                l -= 1
                s += 1
        return playable_cards
        
    def get_rocket(self):
        if (self.cards_count[13] and self.cards_count[14]):
            return set([CARD_RANK_STR[13] + CARD_RANK_STR[14]])
        else:
            return set()

    def playable_cards(self, card_type = None):
        ''' Get playable cards from self.hand_cards for card_type.

        Args:
            card_type: which type of playable cards to generate. None for all types of playable cards. 

        Returns:
            set: set of string of playable cards
        '''
        # for all types
        if (not card_type):
            playable_cards = set()
            playable_cards.update(self.get_solo())
            playable_cards.update(self.get_pair())
            playable_cards.update(self.get_trio())
            playable_cards.update(self.get_trio_solo())
            playable_cards.update(self.get_trio_pair())
            playable_cards.update(self.get_four_two_solo())
            playable_cards.update(self.get_four_two_pair())
            playable_cards.update(self.get_bomb())
            playable_cards.update(self.get_rocket())
            #solo_chain_5 -- #solo_chain_12     
            for (start_index, length) in self.get_solo_chain_indexes():
                s, l = start_index, length
                while(l >= 5):
                    cards = ''
                    curr_index = s - 1
                    curr_length = 0
                    while (curr_length < l and curr_length < 12):
                        curr_index += 1
                        curr_length += 1
                        cards += CARD_RANK_STR[curr_index]
                        if (curr_length >= 5):
                            playable_cards.add(cards)
                    l -= 1
                    s += 1
            #pair_chain_3 -- #pair_chain_10
            for (start_index, length) in self.get_pair_chain_indexes():
                s, l = start_index, length
                while(l >= 3):
                    cards = ''
                    curr_index = s - 1
                    curr_length = 0
                    while (curr_length < l and curr_length < 10):
                        curr_index += 1
                        curr_length += 1
                        cards += CARD_RANK_STR[curr_index] * 2
                        if (curr_length >= 3):
                            playable_cards.add(cards)
                    l -= 1
                    s += 1
            #trio_chain_2 -- trio_chain_6; trio_solo_chain_2 -- trio_solo_chain_5; trio_pair_chain_2 -- trio_pair_chain_4
            for (start_index, length) in self.get_trio_chain_indexes():
                s, l = start_index, length
                while(l >= 2):
                    cards = ''
                    curr_index = s - 1
                    curr_length = 0
                    while (curr_length < l and curr_length < 6):
                        curr_index += 1
                        curr_length += 1
                        cards += CARD_RANK_STR[curr_index] * 3

                        #trio_chain_2 to trio_chain_6
                        if (curr_length >= 2 and curr_length <= 6):
                            playable_cards.add(cards)
                        
                        #trio_solo_chain_2 to trio_solo_chain_5
                        if (curr_length >= 2 and curr_length <= 5):
                            for left, right in self.solo_attachments(s, curr_length, curr_length):
                                pre_attached = ''
                                for j in left:
                                    pre_attached += CARD_RANK_STR[j]
                                post_attached = ''
                                for j in right:
                                    post_attached += CARD_RANK_STR[j]
                                playable_cards.add(pre_attached + cards + post_attached)
                        
                        #trio_pair_chain2 -- trio_pair_chain_4
                        if (curr_length >= 2 and curr_length <= 4):
                            for left, right in self.pair_attachments(s, curr_length, curr_length):
                                pre_attached = ''
                                for j in left:
                                    pre_attached += CARD_RANK_STR[j] * 2
                                post_attached = ''
                                for j in right:
                                    post_attached += CARD_RANK_STR[j] * 2
                                playable_cards.add(pre_attached + cards + post_attached)
                    l -= 1
                    s += 1
            return playable_cards
        elif (card_type == 'solo'):
            return self.get_solo()
        elif (card_type[:11] == 'solo_chain_'):
            n = int(card_type[-1])
            if (n < 5):
                n = int(card_type[-2:])
            return self.get_solo_chain_n(n)
        elif (card_type == 'pair'):
            return self.get_pair()
        elif (card_type[:11] == 'pair_chain_'):
            n = int(card_type[-1])
            if (n < 3):
                n = int(card_type[-2:])
            return self.get_pair_chain_n(n)
        elif (card_type == 'trio'):
            return self.get_trio()
        elif (card_type[:11] == 'trio_chain_'):
            n = int(card_type[-1])
            return self.get_trio_chain_n(n)
        elif (card_type == 'trio_solo'):
            return self.get_trio_solo()
        elif (card_type[:16] == 'trio_solo_chain_'):
            n = int(card_type[-1])
            return self.get_trio_solo_chain_n(n)
        elif (card_type == 'trio_pair'):
            return self.get_trio_pair()
        elif (card_type[:16] == 'trio_pair_chain_'):
            n = int(card_type[-1])
            return self.get_trio_pair_chain_n(n)
        elif (card_type == 'four_two_solo'):
            return self.get_four_two_solo()
        elif (card_type == 'four_two_pair'):
            return self.get_four_two_pair()
        elif (card_type == 'bomb'):
            return self.get_bomb()
        elif (card_type == 'rocket'):
            return self.get_rocket()
        else:
            return set()

def get_gt_cards(player, greater_player):
    ''' Provide player's cards which are greater than the ones played by
    previous player in one round

    Args:
        player (DoudizhuPlayer object): the player waiting to play cards
        greater_player (DoudizhuPlayer object): the player who played current biggest cards.

    Returns:
        list: list of string of greater cards

    Note:
        1. return value contains 'pass'
    '''
    # add 'pass' to legal actions
    gt_cards = ['pass']
    current_hand = cards2str(player.current_hand)
    target_cards = greater_player.played_cards
    target_types = CARD_TYPE[0][target_cards]
    type_dict = {}
    for card_type, weight in target_types:
        if card_type not in type_dict:
            type_dict[card_type] = weight
    if 'rocket' in type_dict:
        return gt_cards
    type_dict['rocket'] = -1
    if 'bomb' not in type_dict:
        type_dict['bomb'] = -1
    for card_type, weight in type_dict.items():
        w = int(weight)
        for candidate in DoudizhuRule(current_hand).playable_cards(card_type):
            if (int(CARD_TYPE[0][candidate][0][1]) > w):
                gt_cards.append(candidate)
        # candidate = TYPE_CARD[card_type]
        # for can_weight, cards_list in candidate.items():
        #     if int(can_weight) > int(weight):
        #         for cards in cards_list:
        #             # TODO: improve efficiency
        #             if cards not in gt_cards and contains_cards(current_hand, cards):
        #                 # if self.contains_cards(current_hand, cards):
        #                 gt_cards.append(cards)
    return gt_cards


# Test json order
#if __name__ == '__main__':
#    for action, index in ACTION_SPACE.items():
#        if action != ACTION_LIST[index]:
#            print('order error')