from labouchere import gamble
from export_csv import export_array_as_csv

from time import time
from math import floor


# Analyzes the number of bets won
# returns a histogram where the number of rounds resulting in each number of bets is counted
def wins_to_bankroll(sequence=[1, 2, 3], min_bankroll=0, max_bankroll=40000, step=1, rounds_per_bankroll=1000,
                     update_frequency=2):
    # Store results in a dict
    results = [['balance', 'wins', 'losses', 'draws']]

    # Initialize variables for performance benchmarking
    start = time()
    last_update = 0

    # Calculate the total number of simulations that will be run in order to give the user
    # updates. This process can take a few minutes to complete, so updates are nice.
    total_rounds = (max_bankroll - min_bankroll) / step * rounds_per_bankroll

    # Iterate over each balance we intend to run simulations for
    for balance in range(min_bankroll, max_bankroll, step):
        wins = 0
        losses = 0
        draws = 0

        # Run rounds_per_bankroll number of simulations with balance
        for i in range(0, rounds_per_bankroll):
            bets, resulting_balance = gamble(sequence, balance)

            if resulting_balance > balance:
                wins += 1
            elif balance > resulting_balance:
                losses += 1
            else:
                draws += 1

            # Update a user on the progress of the simulation
            t = time()
            if t - last_update > update_frequency:
                print "Completed %s/%s rounds in %s seconds" % (
                    balance / step * rounds_per_bankroll, total_rounds, floor(t - start))
                last_update = t

        # Append a row for later export to CSV (or other processing)
        results.append([balance, wins, losses, draws])

    # Print a benchmark for how long the simulation took
    end = time()
    print "Done in %s seconds; Avg. %s seconds/round" % ((end - start), (end - start) / total_rounds)

    return results


# Analyzes the number of bets won
# returns a histogram where the number of rounds resulting in each number of bets is counted
# Downsamples proportionally to the log of the bankroll
def wins_to_bankroll_downsampled(
        sequence=[1, 2, 3],
        min_bankroll=0,
        max_bankroll=400000,
        rounds_per_bankroll=10000,
        update_frequency=2,
        downsample_constant=10):
    # Store results in a dict
    results = [['balance', 'wins', 'losses', 'draws']]

    # Initialize variables for performance benchmarking
    start = time()
    last_update = 0

    total_rounds = (max_bankroll - min_bankroll) / 1 * rounds_per_bankroll

    step = 1
    balance = min_bankroll

    while balance < max_bankroll:
        wins = 0
        losses = 0
        draws = 0

        for i in range(0, rounds_per_bankroll):
            bets, resulting_balance = gamble(sequence, balance)

            if resulting_balance > balance:
                wins += 1
            elif balance > resulting_balance:
                losses += 1
            else:
                draws += 1

            # Update a user on the progress of the simulation
            t = time()
            if t - last_update > update_frequency:
                print "Completed %s/<%s rounds in %s seconds. Step size: %s" % (
                balance / step * rounds_per_bankroll, total_rounds, floor(t - start), step)
                last_update = t

        results.append([balance, wins, losses, draws])

        balance += step
        step = floor(balance / downsample_constant)

        if step < 1:
            step = 1

    # Print a benchmark for how long the simulation took
    end = time()
    print "Done in %s seconds; Avg. %s seconds/round" % ((end - start), (end - start) / total_rounds)

    return results


if __name__ == "__main__":
    export_array_as_csv(wins_to_bankroll_downsampled(), name='wins_to_bankroll.csv')
