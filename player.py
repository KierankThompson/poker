from card import Deck
from table import Table
import random
import pickle
from train import *


class Player():
    def __init__(self,startingMoney=10):
        self.money = startingMoney
        self.hand = []

    def bet(self,betSize):
        self.money -= betSize

    def winPot(self,table):
        self.money += table.pot
        table.pot = 0
    
    def getHand(self,deck):
        self.hand = deck.takeOut(2)

    def reset(self):
        self.hand = []


ACTIONS = ["fold", "call", "bet"]
class AI(Player):
    
    def __init__(self,startingMoney=10, strategy_file="strategy_file.pkl"):
        super().__init__(startingMoney)
        with open(strategy_file, "rb") as f:
            self.strategy = pickle.load(f)
    def decide_action(self, historyString):
        info_key = historyString
        if info_key in self.strategy:
            strategy = self.strategy[info_key].get_average_strategy()
        else:
            strategy = [1/3, 1/3, 1/3]  

        action = random.choices(ACTIONS, weights=strategy)[0]
        return action

    
            
        
        
        
        





