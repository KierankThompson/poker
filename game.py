from card import Card,Deck
from table import Table
from train import *
from player import Player, AI
import curses
import time


valuetoRank = {
    1: "High Card",
    2: "One Pair",
    3: "Two Pair",
    4: "Three of a Kind",
    5: "Straight",
    6: "Flush",
    7: "Full House",
    8: "Four of a Kind",
    9: "Straight Flush",
}


def pokerGame(stdscr):
    player = Player()
    opponent = AI()
    min_bet_size = 2
    
    turn = 0
    table = Table()
    deck = Deck()
    players = [player, opponent]
    while player.money > 0 and opponent.money > 0:
        cur_bet_size = 2
        stdscr.clear()
        if turn % 2 == 0:
            player.bet(min_bet_size)
            table.addPot(min_bet_size)
        else:
            opponent.bet(min_bet_size)
            table.addPot(min_bet_size)
        player.getHand(deck)
        opponent.getHand(deck)
        historyString = f"{evalpreFlop(opponent.hand)}"
        folded = False
        all_in = False
        ai_move = None
        for stage in ["Preflop", "Flop", "Turn", "River"]:
            if stage == "Flop":
                table.flop(deck)
                historyString =  historyString[0] + str(best_hand_value(opponent.hand + table.cards,5)) + historyString[1:]
            elif stage == "Turn":
                table.turn(deck)
                historyString =  historyString[0] + str(best_hand_value(opponent.hand + table.cards,6)) + historyString[1:]
            elif stage == "River":
                table.river(deck)
                historyString =  historyString[0] + str(best_hand_value(opponent.hand + table.cards,7)) + historyString[1:]
            if stage == "Preflop":  
                first, second = (1, 0) if turn % 2 == 0 else (0, 1)
            else:  
                first, second = (0, 1) if turn % 2 == 0 else (1, 0)
            
            while True:
                for i in [first, second]:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"Stage: {stage}")
                    stdscr.addstr(1, 0, f"Turn: {turn}")
                    stdscr.addstr(2, 0, f"Pot: {table.pot}")
                    stdscr.addstr(3, 0, f"Board: {' '.join(str(c) for c in table.cards)}")
                    stdscr.addstr(4, 0, f"Your hand: {player.hand[0]} {player.hand[1]}")
                    stdscr.addstr(5, 0, f"Your stack: {player.money}")
                    stdscr.addstr(6, 0, f"AI stack: {opponent.money}")
                    stdscr.addstr(7, 0, f"AI move: {ai_move}")
                    if all_in:
                         stdscr.addstr(8, 0, "(f)old, or (c)all?: ")
                    else:
                         stdscr.addstr(8, 0, "(f)old, (b)et, or (c)all?: ")
                    current_player = players[i]
                    if isinstance(current_player, AI):
                        ai_move = current_player.decide_action(historyString)
                        time.sleep(1)
                        historyString += ai_move[0]
                        if ai_move == "fold":
                            player.winPot(table)
                            folded = True
                            break
                        else:
                            if all_in:
                                ai_move == "call"
                            if ai_move == "bet":
                                bet_amount = min(cur_bet_size + min_bet_size, opponent.money)
                                opponent.bet(bet_amount)
                                table.addPot(bet_amount)
                                cur_bet_size = bet_amount
                                if opponent.money == 0:
                                    all_in == True
                            if ai_move == "call":
                                bet_amount = min(cur_bet_size, opponent.money)    
                                opponent.bet(bet_amount)
                                table.addPot(bet_amount)
                                cur_bet_size = 0
                        if historyString[-2:] == 'bb' and ai_move[0] == 'b':
                            continue
                        historyString += ai_move[0]
                    else:
                        key = ''
                        curses.echo()
                        if all_in:
                            while True:
                                key = stdscr.getkey()
                                if key in ['f', 'c']:
                                    break
                        else:
                            while True:
                                key = stdscr.getkey()
                                if key in ['f', 'b', 'c']:
                                    break
                        curses.noecho()
                        if key == "f":
                            opponent.winPot(table)
                            folded = True
                            break
                        if key == "b":
                            bet_amount = min(cur_bet_size + min_bet_size, opponent.money)
                            player.bet(bet_amount)
                            table.addPot(bet_amount)
                            cur_bet_size = bet_amount
                            if player.money == 0:
                                all_in == True
                        if key == "c":
                            bet_amount = min(cur_bet_size, opponent.money)     
                            player.bet(bet_amount)
                            table.addPot(bet_amount)
                            cur_bet_size = 0
                        if historyString[-2:] == 'bb' and key == 'b':
                            continue
                        historyString += key
                if cur_bet_size == 0 or folded or all_in:
                    break
            if folded or all_in:
                break
        if len(table.cards) != 5:
                table.cards += deck.takeOut(5-len(table.cards))
        stdscr.clear()
        stdscr.addstr(0, 0, f"Stage: Showdown")
        stdscr.addstr(1, 0, f"Turn: {turn}")
        stdscr.addstr(2, 0, f"Pot: {table.pot}")
        stdscr.addstr(3, 0, f"Board: {' '.join(str(c) for c in table.cards)}")
        stdscr.addstr(4, 0, f"Your hand: {player.hand[0]} {player.hand[1]}")
        stdscr.addstr(5, 0, f"Your stack: {player.money}")
        stdscr.addstr(6, 0, f"AI stack: {opponent.money}")
        stdscr.addstr(7, 0, f"AI move: {ai_move}")
        if not folded:
            ai_hand = f"{opponent.hand[0]} {opponent.hand[1]}"
            p_score = evalFinal(player.hand + table.cards)
            ai_score = evalFinal(opponent.hand + table.cards)
            if p_score > ai_score:
                result = f"You win with {valuetoRank[best_hand_value(player.hand + table.cards,7)]}"
                player.winPot(table)
            elif p_score < ai_score:
                result = f"AI wins with {valuetoRank[best_hand_value(opponent.hand + table.cards,7)]}"
                opponent.winPot(table)
            else:
                result = "Tie. Pot split."
                player.money += table.pot // 2
                opponent.money += table.pot // 2
            stdscr.addstr(6, 0, f"AI hand: {ai_hand}")
            stdscr.addstr(7, 0, result)
        else:
            stdscr.addstr(6, 0, "One player folded. Pot awarded.")
        stdscr.refresh()
        player.reset()
        opponent.reset()
        table.reset()
        deck.reset()
        turn += 1
        time.sleep(3)

    stdscr.clear()
    if player.money > 0:
        stdscr.addstr(0, 0, f"Game Over. You won!")
    else:
        stdscr.addstr(0, 0, f"Game Over. You lost...")
    stdscr.refresh()
    time.sleep(5)
    

        
def main(stdscr):
    curses.curs_set(0)  
    stdscr.clear()
    pokerGame(stdscr)
        
if __name__ == "__main__":
    curses.wrapper(main)