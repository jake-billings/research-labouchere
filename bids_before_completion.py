# Copyright (c) 2017 [Jake Billings]
# See LICENSE for more information

from labouchere import gamble
from export_csv import export_dict_as_csv

from time import time
from math import floor

# Analyzes the number of bets made before a round of labouchere ends
# returns a histogram where the number of rounds resulting in each number of bets is counted
def bids_before_completion_histogram(sequence=[1,2,3], balance=4000, rounds=100, update_frequency=2):
    # Store results in a dict
    results = {}

    # Initialize variables for performance benchmarking
    start = time()
    last_update = 0

    for i in range(1,rounds):
        # Run a simulation and add results to a historgram
        bets, resulting_balance = gamble(sequence, balance)
        results[bets] = results.get(bets, 0) + 1

        # Update a user on the progress of the simulation
        t = time()
        if t - last_update > update_frequency:
            print "Completed %s/%s rounds in %s seconds" % (i,rounds,floor(t-start))
            last_update=t

    # Print a benchmark for how long the simulation took
    end = time()
    print "Done in %s seconds; Avg. %s seconds/round" % ((end-start),(end-start)/rounds)

    return results

if __name__ == "__main__":
    export_dict_as_csv(bids_before_completion_histogram(rounds=10000),name='bids_before_completion.csv')