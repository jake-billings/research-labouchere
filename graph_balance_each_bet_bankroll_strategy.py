# Copyright (c) 2017 [Jake Billings]
# See LICENSE for more information

import random

from labouchere import gamble
from export_csv import export_array_as_csv

from graph_balance_each_bet import gamble


# Return a random boolean in order to simulate a coin flip.
# This is approximately 50% odds.
# The odds are not 50% on online betting sites. They typically take a "house advantage," so the odds are actually
# similar to 49.95%.
def flip_coin():
    return bool(random.getrandbits(1))


# Store the player's balance/betting history over multiple rounds of bankroll/Zimmerman strategy
def run_bankroll_strategy(sequence=[1,2,3], rounds=1000, max_balance=6000, initial_balance=4000):
    data = [['bet', 'won', 'balance', 'sequence', 'event', 'extracted profit']]

    # Calculate the initial bet that Labouchere will make
    initial_bet = sequence[0]
    if len(sequence) > 1:
        initial_bet += sequence[-1]

    # Store the current balance in a variable
    balance = initial_balance

    # Store the "extracted profit" or "money scraped off the top"
    extracted_profit = 0

    # Prepare to store statistics for how many times Labouchere wins and loses.
    wins = 0
    losses = 0
    draws = 0

    # Run the number of rounds stored in the variable rounds
    for i in range(1, rounds):
        # Stop playing if you're out of money.
        if balance<initial_bet:
            # print "You're broke."
            break

        # Run one full round of Labouchere
        num_bets, resulting_balance, history = gamble(sequence=[1, 2, 3], balance=balance)
        history[-1].append(extracted_profit)
        data += history

        # Store if Labouchere made a profit, or "won"
        if resulting_balance > initial_balance:
            wins += 1
        elif resulting_balance < initial_balance:
            losses += 1
        else:
            draws += 1

        # Store the new balance from Labouchere
        balance = resulting_balance

        # Scrape off the top in accordance with the bankroll strategy
        unwanted_money = balance-max_balance
        if unwanted_money > 0:
            balance -= unwanted_money
            extracted_profit += unwanted_money

    # Print statistics
    print "Ran with initial sequence", sequence
    print "Initial balance $"+str(initial_balance)
    print "Rounds %s, Wins %s, Losses %s, Draws %s, Balance $%s, Loss $%s" % (wins+losses+draws, wins, losses, draws, balance, initial_balance-balance)
    print "Extracted Profit: $%s, Profit and Balance: $%s, Total Gain: %s" % (extracted_profit, balance+extracted_profit, (balance+extracted_profit)-initial_balance)

    return data

if __name__ == "__main__":
    print run_bankroll_strategy()
    export_array_as_csv(run_bankroll_strategy(), name='balance_after_each_bet_bankroll.csv')
