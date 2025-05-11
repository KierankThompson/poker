import pickle
from train import *

def main():
    with open("strategy_file.pkl", "rb") as f:
            strategy = pickle.load(f)
            for i in strategy:
                if len(i) == 4:
                    print(i,strategy[i].get_average_strategy())
                    

if __name__ == "__main__":
      main()

