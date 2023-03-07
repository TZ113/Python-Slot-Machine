# This is my attempt at python-slot-machine from techwithtim

import random
import sys

MAX_LINES = 3

MIN_BET = 1
MAX_BET = 50

ROWS = 3
COLS = 3

symbols_count = {"A": 2, "B": 4, "C": 6, "D": 8}

symbols_value = {"A": 5, "B": 4, "C": 3, "D": 2}


def get_deposit():
    """Prompts the user for depositing an amount, and checks whether it's a valid input, and then returns that amount."""
    while True:
        balance = input("How much you want to deposit? $")
        if balance.isdigit() and (balance := int(balance)) > 0:
            break
        else:
            print("Please enter a valid amount.")

    return balance


def get_number_of_lines():
    """Prompts the user for how many lines he wants to bet on , and returns the number of lines"""
    while True:
        lines = input(f"How many lines you want to bet on between 1-{MAX_LINES}? ")
        if lines.isdigit() and 1 <= (lines := int(lines)) <= MAX_LINES:
            break
        else:
            print("Please enter a valid number.")

    return lines


def get_bet(balance, lines):
    """Prompts the user for entering a bet amount for each of the lines he chose, checks whether if it's a valid amount and returns it."""
    while True:
        bet_amount = input(
            f"You have ${balance} left. Minimum bet is ${MIN_BET} and maximum is ${MAX_BET}. How much you want to bet per line you chose? $"
        )
        if (
            bet_amount.isdigit()
            and MIN_BET <= int(bet_amount) <= MAX_BET
            and (total_bet := int(bet_amount) * lines) <= balance
        ):
            break
        elif bet_amount.isdigit() and MIN_BET <= int(bet_amount) <= MAX_BET:
            print("You don't have sufficient balance for that bet.")
        else:
            print("Please enter a valid amount.")

    return total_bet


def spin(rows, cols, symbols):
    """This function implements the spinning of a slot-machine, it produces a list of symbols and then randomly inserts from them into columns, and all these columns are returned as lists inside a list"""
    all_symbols = []
    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)
    all_cols = []
    for _ in range(cols):
        col = []
        current_symbols = all_symbols.copy()
        for _ in range(rows):
            symbol = random.choice(current_symbols)
            col.append(symbol)
            current_symbols.remove(symbol)
        all_cols.append(col)

    return all_cols


def print_lines(columns):
    """Prints the columns or reels in a way that can be read by the user as the result of spinning"""
    for i in range(len(columns[0])):
        for j, column in enumerate(columns):
            if j == len(columns) - 1:
                print(column[i])
            else:
                print(column[i], end=" | ")


def check_winnings(columns, bet, values, lines):
    """Checks whether the user has won anything, then returns the winnings and a list containing the line numbers he's won"""
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbols = []
        for column in columns:
            symbols.append(column[line])
        if all([symbols[i] == symbols[0] for i in range(len(symbols))]):
            winning_lines.append(line + 1)
            winnings += bet / lines * values[symbols[0]]

    return int(winnings), winning_lines


def game():
    """This function simulates the game by calling all the other functions in appropriate manner, it doesn't return anything."""
    balance = get_deposit()
    while True:
        if balance <= 0:
            sys.exit("You have ran out of balance, go home!")
        res = input(
            f"Your current balance is ${balance}. Press Enter if you want to play, or q to quit. "
        )
        if res == "q":
            sys.exit("Goodbye!")
        elif res == "":
            lines = get_number_of_lines()
            bet = get_bet(balance, lines)
            balance -= bet
            while True:
                if lines == 1:
                    ans = input(
                        f"You are betting ${bet} on line 1. Press Enter to continue.."
                    )
                else:
                    all_lines = [line for line in range(1, lines + 1)]
                    print(f"You're betting ${int(bet/lines)} on each of lines", end=" ")
                    print(*all_lines, sep=", ", end=" ")
                    ans = input(f"totaling ${bet}. Press Enter to continue..")
                if ans == "":
                    break
            slots = spin(ROWS, COLS, symbols_count)
            print_lines(slots)
            winnings, winning_lines = check_winnings(slots, bet, symbols_value, lines)
            balance += winnings
            if len(winning_lines) == 0:
                lines = [i for i in range(1, lines + 1)]
                print(f"You've lost ${bet} on lines ", end="")
                print(*lines, sep=", ", end=".\n")
            elif len(winning_lines) == 1:
                print(f"You've won ${winnings} on line {winning_lines[0]}")
            else:
                print(f"You've won ${winnings} on lines ", end="")
                print(*winning_lines, sep=", ", end=".\n")
        else:
            print("Invalid key.")


if __name__ == "__main__":
    game()
