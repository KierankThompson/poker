from card import Card, Deck


class Table():
    def __init__(self):
        self.cards = []
        self.pot = 0
    
    def addPot(self,bet):
        self.pot += bet
    
    def flop(self,deck):
        cards = deck.takeout(3)
        for card in cards:
            self.cards.append(card)
    
    def turn(self,deck):
        card = deck.takeout(1)
        self.cards.append(card)
    
    def river(self,deck):
        self.turn(deck)

    def reset(self):
        self.cards = []
        self.pot = 0
