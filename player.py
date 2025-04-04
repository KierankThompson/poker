from card import Deck
from table import Table
import random
import numpy as np


class Player():
    def __init__(self,startingMoney=1000):
        self.money = startingMoney
        self.hand = []

    def bet(self,betSize):
        self.money -= betSize

    def winPot(self,table):
        self.money += table.potsize
        table.potsize = 0
    
    def getHand(self,deck):
        self.hand = deck.takeOut(2)

    
    
    def reset(self):
        self.hand = []

class AI(Player):
    
    def __init__(self,startingMoney=1000):
        super().__init__(startingMoney)

    def evalPreFlop(self, isBlind = True, curBet = 0):
        if not self.hand:
            return 0
        maxScore = 41 ** 2
        score = maxScore
        if (self.hand[0].bit & self.hand[1].bit & 0xf000):
            score = maxScore
        else:
            score = (self.hand[0].bit & 0xff) * (self.hand[1].bit & 0xff)
        if isBlind:
            ratio = 1 - (score/maxScore-0.3)
            rand = random.randrange(1)
            if ratio > rand:
                return 5 + min(self.money,int(self.money * np.random.normal(0.1)))
            else:
                return 5
        else:
            ratio = score/maxScore - 0.1
            
        
        
        
        





