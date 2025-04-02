import random
import copy

class Card():
    rankBitMap = {"Two":16, "Three":17, "Four":18, "Five":19, "Six":20, "Seven":21, "Eight":22, "Nine":23, "Ten":24, "Jack":25, "Queen":26, "King":27, "Ace":28}
    suitBitMap = {"Hearts": 12, "Diamonds": 13, "Clubs": 14, "Spades": 15}
    rankMap = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,"Jack": 11, "Queen": 12, "King": 13, "Ace": 14}
    primeMap = {"Two": 2, "Three": 3, "Four": 5, "Five": 7, "Six": 11, "Seven": 13, "Eight": 17, "Nine": 19, "Ten": 23, "Jack": 29, "Queen": 31, "King": 37, "Ace": 41}

    def __init__(self,rank,suit):
        self.suit = suit
        self.rank = rank
        self.bit = Card.primeMap[rank]
        self.bit |= (Card.rankMap[rank] << 8)
        self.bit |= (1 << Card.suitBitMap[suit])
        self.bit |= (1 << Card.rankBitMap[rank])
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    


class Deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits]
        self.deckSize = len(self.cards)
        random.shuffle(self.cards)

    def takeOut(self,numCards):
        if numCards > self.deckSize:
            raise IndexError("Not Enough Cards in Deck")
        randomNumbers = []
        for _ in range(numCards):
            index = random.randrange(self.deckSize)
            while index in randomNumbers:
                index = random.randrange(self.deckSize)
            randomNumbers.append(index)
        returnCards = [copy.deepcopy(self.cards[index]) for index in randomNumbers]
        for index in sorted(randomNumbers,reverse=True):
            del self.cards[index]
        self.deckSize -= len(randomNumbers)
        return returnCards
    
    def reset(self):
        self.cards = [Card(rank, suit) for suit in Deck.suits for rank in Deck.ranks]
        self.deckSize = len(self.cards)
        random.shuffle(self.cards)
    


