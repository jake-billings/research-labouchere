# Copyright (c) 2017 [Jake Billings]
# See LICENSE for more information

import time
from labouchere import gamble


# This sequence prints the results of running the bankroll strategy to the console.
#
# The bankroll strategy, also known as the Zimmerman Strategy, takes the aggregate of multiple rounds of Labouchere
# betting. Supposedly by making bets much smaller than one's bankroll, one can maximize the probability of winning
# because it is very unlikely that Labouchere will result in the loss of the entire bankroll all at once.
#
# After reach round of Labouchere, if a balance is above a certain threshold, all money above that threshold is removed
# from the bankroll as profit, and it is never used for gambling again.
#
# sequence The initial sequence to use in every round of Labouchere
# rounds The number of rounds of Labouchere to run
# max_balance The threshold above which profits are extracted from the bankroll (balance)
# initial_balance The initial size of bankroll (balance) to use
def run_bankroll_strategy(sequence=[0.00001,0.00002,0.00003], rounds=5, max_balance=0.6, initial_balance=0.5):
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
        bets, resulting_balance = gamble(sequence, balance)

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

    return (balance+extracted_profit)-initial_balance


# Utility function to export the results of multiple runs of the bankroll strategy to a CSV file
def calculate_and_export_aggregate():
    data = []

    count = 14000
    start = time.time()
    for i in range(1,count):
        result = run_bankroll_strategy()
        data.append(result)
        print result
    end = time.time()
    print "Done in %s seconds; Avg. %s seconds/sim" % ((end-start),(end-start)/count)

    with open('export_2.csv', 'w') as wfile:
        for cell in data:
            wfile.write(str(cell)+'\n')

if __name__ == "__main__":
    run_bankroll_strategy()
