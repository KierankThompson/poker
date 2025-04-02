from card import Deck

class Player():
    def __init__(self,startingMoney):
        self.money = startingMoney
        self.hand = []

    def bet(self,betSize):
        self.money -= betSize

    def winPot(self,potSize):
        self.money += potSize
    
    def getHand(self,deck):
        self.hand = deck.takeout(2)

    
    
    def reset(self):
        self.hand = []

