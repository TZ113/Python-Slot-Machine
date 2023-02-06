import random
import sys

MAX_LINES = 3

MIN_BET = 1
MAX_BET = 50

ROWS = 3
COLS = 3

symbols_count = {
    'A' : 2,
    'B' : 4,
    'C' : 6,
    'D' : 8 
}

symbols_value = {
    'A' : 5,
    'B' : 4,
    'C' : 3,
    'D' : 2
}


def get_deposit():
    while True:
        balance = input('How much you want to deposit? $')
        if balance.isdigit() and (balance := int(balance)) > 0:
            break
        else:
            print("Please enter a valid amount.")
            
    return balance


def get_number_of_lines():
    while True:
        lines = input(f'How many lines you want to bet on between 1-{MAX_LINES}? ')
        if lines.isdigit() and 1 <= (lines := int(lines)) <= MAX_LINES:
            break
        else:
            print("Please enter a valid number.")
            
    return lines


def get_bet(balance, lines):
    while True:
        bet_amount = input(f'You have ${balance} left. Minimum bet is ${MIN_BET} and maximum is ${MAX_BET}. How much you want to bet per line you chose? $')
        if bet_amount.isdigit() and MIN_BET <= int(bet_amount) <= MAX_BET and (total_bet := int(bet_amount) * lines) <= balance:
            break
        elif bet_amount.isdigit() and MIN_BET <= int(bet_amount) <= MAX_BET:
            print("You don't have sufficient balance for that bet.")
        else:
            print('Please enter a valid amount.')
    
    return total_bet


def spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)
    all_rows = []
    for _ in range(rows):
        row = []
        current_symbols = all_symbols.copy()
        for _ in range(cols):
            symbol = random.choice(current_symbols)
            row.append(symbol)
            current_symbols.remove(symbol)
        all_rows.append(row)
    [print(*row, sep=' | ') for row in all_rows]
    return all_rows


def check_winnings(paylines, bet, values, lines):
    print(lines)
    winnings = 0
    winning_lines = []
    for line in range(lines):
        if all([i == paylines[line][0] for i in paylines[line]]):
            symbol = paylines[line][0]
            winnings += values[symbol] * bet / lines
            winning_lines.append(line + 1)
            
    return int(winnings), winning_lines


if __name__ == "__main__":
    balance = get_deposit()
    while True:
        if balance == 0:
            sys.exit('You have ran out of balance, go home!')
        res = input(f"Your current balance is ${balance}. Press Enter if you want to play, or q to quit. ")
        if res == 'q':
            sys.exit('Goodbye!')
        elif res == '':
            lines = get_number_of_lines()
            bet = get_bet(balance, lines)
            balance -= bet
            while True:
                if lines == 1:
                    ans = input(f"You are betting ${bet} on line 1. Press Enter to continue..")
                else:
                    all_lines = [i for i in range(1, lines + 1)]
                    ans = input(f"You're betting ${int(bet/lines)} on each of lines {all_lines}, totaling ${bet}. Press Enter to continue..")
                if ans == '':
                    break
            paylines = spin(ROWS, COLS, symbols_count)
            winnings, winning_lines = check_winnings(paylines, bet, symbols_value, lines)
            balance += winnings
            if len(winning_lines) == 0:
                lines = [i for i in range(1, lines + 1)]
                print(f"You've lost ${bet} on lines ", end='')
                print(*lines, sep=', ', end='.\n')
            elif len(winning_lines) == 1:
                print(f"You've won ${winnings} on line {winning_lines[0]}")
            else:  
                print(f"You've won ${winnings} on lines ", end='')
                print(*winning_lines, sep=', ', end='.\n')
        else:
            print('Invalid key.')

