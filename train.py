from card import Card,Deck
from table import Table
from lookup import *
from player import Player, AI
import copy
import pickle


def find_fast(x):
    x += 0xe91aaa35
    x ^= x >> 16
    x += x << 8
    x &= 0xffffffff
    x ^= x >> 4
    b = (x >> 8) & 0x1ff
    a = (x + (x << 2)) >> 19
    r = (a ^ hash_adjust[b]) & 0x1fff
    return hash_values[r]


def evalHand(cards):
    if len(cards) != 5:
        raise Exception("Hand Must Have 5 Cards")
    q = (cards[0].bit | cards[1].bit | cards[2].bit | cards[3].bit | cards[4].bit) >> 16
    s = 0
    if (cards[0].bit & cards[1].bit & cards[2].bit & cards[3].bit & cards[4].bit & 0xf000):
        return flushes[q]
    if ((s := unique5[q])):
        return s
    q = (cards[0].bit & 0xff) * (cards[1].bit & 0xff) * (cards[2].bit & 0xff) * (cards[3].bit & 0xff) * (cards[4].bit & 0xff)
    return find_fast(q)


def evalpreFlop(cards):
    sameSuit = {6144: 1, 5120: 1, 3072: 1, 4608: 1, 2560: 1, 4352: 1, 1536: 1, 2304: 1, 1280: 1, 768: 1, 4224: 1,
                2176: 2, 384: 2, 4160: 2, 1152: 2, 640: 2, 4104: 2, 4128: 2, 2112: 2, 320: 2, 4097: 2, 192: 2,
                576: 3, 1088: 3, 2080: 3, 96: 3, 2064: 3, 160: 3, 2056: 3, 48: 3, 288: 3, 2052: 3, 2050: 3, 2049: 3,
                1056: 4, 80: 4, 24: 4, 544: 4, 12: 4, 1040: 4, 40: 4, 144: 4, 1032: 4, 12: 4, 1028: 4, 1026: 4, 272: 4, 1025: 4, 10: 4, 72: 4, 528: 4,
                520: 5, 6: 5, 36: 5, 516: 5, 514: 5, 136: 5, 513: 5, 18: 5, 9: 5, 264: 5, 68: 5, 260: 5, 258: 5, 5: 5, 257: 5,
                34: 6, 3: 6, 132: 6, 130: 6, 17: 6, 129: 6, 66: 6, 33: 6}
    offSuit = {4096: 1, 2048: 1, 1024: 1, 512: 1, 256: 1, 5120: 1, 128: 1, 5120: 1, 3072: 1,
               64: 2, 4608: 2, 32: 2, 2560: 2,
               4352: 3, 2304: 3, 8: 3, 768: 3, 1280: 3, 4: 3, 2: 3, 1: 3,
               384: 4, 4224: 4, 640: 4,
               2176: 5, 1152: 5, 4160: 5, 192: 5, 320: 5,
               4104: 6, 4128: 6, 4100: 6, 576: 6, 4098: 6, 2112: 6, 4112: 6, 96: 6, 1088: 6, 4097: 6, 160: 6,
               48: 7, 2080: 7, 24: 7, 288: 7, 2064: 7, 80: 7, 12: 7, 2056: 7, 544: 7, 40: 7, 1056: 7, 2052: 7, 2050: 7, 144: 7, 2049: 7, 20: 7, 1040: 7, 10: 7, 72: 7, 272: 7,
               1032: 8, 6: 8, 1028: 8, 1026: 8, 36: 8, 1025: 8, 528: 8, 18: 8, 520: 8, 136: 8, 9: 8, 516: 8, 514: 8, 5: 8, 513: 8, 68: 8, 264: 8, 260: 8, 3: 8,
               34: 9, 257: 9, 17: 9, 132: 9, 130: 9, 129: 9, 66: 9, 65: 9, 33: 9}
    if len(cards) != 2:
       raise Exception("Hand Must Have 2 Cards")
    q = (cards[0].bit | cards[1].bit) >> 16
    if (cards[0].bit & cards[1].bit & 0xf000):
        return sameSuit.get(q,9)
    return offSuit.get(q,9)
        



def handRank(value):
    if (value > 6185):
        return "High Card"   
    if (value > 3325): 
        return "One Pair"       
    if (value > 2467): 
        return "Two Pair"       
    if (value > 1609): 
        return "Three of a Kind"  
    if (value > 1599): 
        return "Straight"      
    if (value > 322): 
        return "Flush"         
    if (value > 166):
        return "Full House"       
    if (value > 10):   
        return "Four of a Kind"  
    return "Straight Flush"  

def evaluateFlop(value):
    rank = handRank(value)
    rank_to_value = {
        "High Card": 1,
        "One Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
    }
    return rank_to_value.get(rank, 10)

def evalFinal(cards):
    best = float('-inf')
    p = perm7
    for idxs in p:
        combo = [cards[i] for i in idxs]
        val = evalHand(combo)
        if val > best:
            best = val
    return best

def best_hand_value(cards, perms):
        best = float('-inf')
        p = [[0, 1, 2, 3, 4]]
        if perms == 6:
            p = perm6
        elif perms == 7:
            p = perm7
        for idxs in p:
            combo = [cards[i] for i in idxs]
            val = evalHand(combo)
            if val > best:
                best = val
        return evaluateFlop(best)


NUM_ACTIONS = 3
ACTIONS = ["fold", "call", "bet"]
info_sets = {}
startIterations = 0

class InfoSet:
    def __init__(self, key):
        self.key = key
        self.regret_sum = [0.0 for _ in ACTIONS]  
        self.strategy_sum = [0.0 for _ in ACTIONS]  

    def get_strategy(self, realization_weight):
        strategy = [max(r, 0) for r in self.regret_sum]
        normalizing_sum = sum(strategy)
        if normalizing_sum > 0:
            strategy = [r / normalizing_sum for r in strategy]
        else:
            strategy = [1.0 / len(ACTIONS)] * len(ACTIONS)  

        
        self.strategy_sum = [s + realization_weight * p for s, p in zip(self.strategy_sum, strategy)]
        return strategy

    def get_average_strategy(self):
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            return [s / normalizing_sum for s in self.strategy_sum]
        else:
            return [1.0 / len(ACTIONS)] * len(ACTIONS)
        
class History:
    def __init__(self):
        self.total_pot_size = 0
        self.history_str = ""
        self.min_bet_size = 2
        self.game_stage = 2
        self.curr_round_plays = 0



def cfr(history, community_cards, all_community_cards, hands, p0, p1):
    plays = len(history.history_str)
    player = plays % 2
    opponent = 1 - player
    if plays >= 1:
        if history.history_str[-1] == "f":  
            return history.total_pot_size
        elif history.game_stage == 6:
            hand = hands[player] + community_cards
            opponent_hand = hands[opponent] + community_cards
            score = float('-inf')
            for idxs in perm7:
                combo = [hand[i] for i in idxs]
                val = evalHand(combo)
                score = max(score,val)
            opponent_score = float('-inf')
            for idxs in perm7:
                combo = [hand[i] for i in idxs]
                val = evalHand(combo)
                score = max(opponent_score,val)

            if score == opponent_score:  
                return history.total_pot_size / 2
            elif score < opponent_score:
                return history.total_pot_size
            else:
                return -history.total_pot_size
    if community_cards == None:
        info_key = f"{evalpreFlop(hands[player])}{history.history_str}"
    else:
        combinedHand = hands[player] + community_cards
        info_key = (f"{evalpreFlop(hands[player])}{best_hand_value(combinedHand, len(combinedHand))}{history.history_str}")
    infoset = info_sets.setdefault(info_key, InfoSet(info_key))
    strategy = infoset.get_strategy(p0 if player == 0 else p1)
    util = [0.0] * len(ACTIONS)
    nodeUtil = 0.0
    for a, action in enumerate(ACTIONS):
        nextHistory = copy.deepcopy(history)
        new_community_cards = copy.deepcopy(community_cards)

        nextHistory.curr_round_plays += 1
        nextHistory.history_str += action[0]
        if action == "call":
            nextHistory.total_pot_size += nextHistory.min_bet_size
            if (nextHistory.curr_round_plays > 1):  
                nextHistory.game_stage += 1
                nextHistory.curr_round_plays = 0
                nextHistory.min_bet_size = 0  
                if nextHistory.game_stage == 3:  
                    new_community_cards = all_community_cards[:3]
                elif nextHistory.game_stage == 4:  
                    new_community_cards += [all_community_cards[3]]
                elif nextHistory.game_stage == 5:  
                    new_community_cards += [all_community_cards[4]]
        elif action == "bet":
            if (len(nextHistory.history_str) > 3) and nextHistory.history_str[-3:] == "bbb":
                continue
            nextHistory.min_bet_size = 2
            nextHistory.total_pot_size += nextHistory.min_bet_size
        util[a] = (
            -cfr(nextHistory, new_community_cards, all_community_cards, hands, p0 * strategy[a], p1)
            if player == 0
            else -cfr(nextHistory, new_community_cards, all_community_cards, hands, p0, p1 * strategy[a])
        )
        nodeUtil += strategy[a] * util[a]
    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        infoset.regret_sum[a] += (p1 if player == 0 else p0) * regret
    return nodeUtil
            
averageUtils = []                    
        

def save_strategy(info_sets, filename):
    with open(filename, "wb") as f:
        pickle.dump(info_sets, f)

def train(iterations, save=True):
    deck = Deck()
    util = 0
    average_utils = []

    for i in range(startIterations, iterations):
        deck.reset()
        player = Player()
        opponent = Player()
        player.getHand(deck)
        opponent.getHand(deck)

        all_community_cards = deck.takeOut(5)

        private_cards = [player.hand, opponent.hand]
        community_cards = None
        history = History()

        
        util += cfr(history, community_cards, all_community_cards, private_cards, 1, 1)

        

        if save and i % 100 == 0 and i > 0:
            save_strategy(info_sets, f"strategy_checkpoint_{i}.pkl")


def main():
    iterations = 100000  
    train(iterations, save=True)


if __name__ == "__main__":
    main()
    
        
            
        
        