import random
import copy

def Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    


def Deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Deck.suits for rank in Deck.ranks]
        self.deckSize = len(self.cards)
        random.shuffle(self.cards)

    def takeOut(self,numCards):
        if numCards > self.deckSize:
            return None
        randomNumbers = []
        for _ in numCards:
            index = random.randrange(self.deckSize)
            while index in randomNumbers:
                index = random.randrange(self.deckSize)
            randomNumbers.append(index)
        returnCards = [copy.deepcopy(self.cards[index]) for index in randomNumbers]
        for index in randomNumbers:
            del self.cards[index]
        return tuple(returnCards)
    
    def reset(self):
        self.cards = [Card(suit, rank) for suit in Deck.suits for rank in Deck.ranks]
        random.shuffle(self.cards)
    


