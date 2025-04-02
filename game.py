from card import Card,Deck
from table import Table


def evalHand(cards):
    if len(cards) != 5:
        raise Exception("Hand Must Have 5 Cards")
    return cards[0].bit & cards[1].bit & cards[2].bit & cards[3].bit & cards[4].bit & 0xF000
    


def main():
    d = Deck()
    cards = []
    result = 0
    while result == 0:
        cards = d.takeOut(5)
        d.reset()
        result = evalHand(cards)
    print(result)
    print(cards)
    
    

if __name__ == "__main__":
    main()