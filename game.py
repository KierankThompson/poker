from card import Card,Deck
from table import Table
from lookup import *
from player import Player, AI


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
    


def main():
    table = Table()
    deck = Deck()
    human = Player(1000)
    ai = AI(1000)
    turn = 1
    while True:
        #Blind
        if turn % 2:
            human.bet(5)
        else:
            ai.bet(5)
        table.addPot(5)

        human.getHand(deck)
        ai.getHand(deck)
        break





    
    

if __name__ == "__main__":
    main()