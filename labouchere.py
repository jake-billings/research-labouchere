# Copyright (c) 2017 [Jake Billings]
# See LICENSE for more information

import random


# Return a random boolean in order to simulate a coin flip.
# This is approximately 50% odds.
# The odds are not 50% on online betting sites. They typically take a "house advantage," so the odds are actually
# similar to 49.95%.
def flip_coin():
    return bool(random.getrandbits(1))


# Runs a simulation of the Labouchere betting system with a given starting sequence and balance.
# Returns the ending balance after running the system to completion
# This is a recursive function. Each function call is one "round" of betting.
#
# See: https://en.wikipedia.org/wiki/Labouch%C3%A8re_system
def gamble(sequence, balance):
    # If the sequence is empty, the labouchere system says that the round is over.
    # End the recursion. This is essentially a win.
    if len(sequence) < 1:
        # print "Aborting because the sequence is empty"
        # Return 0 and the initial balance because no bet was made
        return 0, balance

    # If the sequence is of length 1, the bet is the number in the sequence. Otherwise, it is the first number
    # added to the last number.
    if len(sequence) is 1:
        bet = sequence[0]
    else:
        bet = sequence[0] + sequence[-1]

    # You can't bet more money than you have (this isn't Wall Street), so
    # betting more than the initial balance ends recursion. This is essentially a loss.
    if bet > balance:
        # print "Aborting because you're broke", balance
        # Return 0 and the initial balance because no bet was made
        return 0, balance

    # If a random boolean is true, we won.
    won = flip_coin()

    # print "Betting " + str(bet) + " with a balance of " + str(balance) + " due to sequence " + str(sequence)

    # Add or subtract from the balance based on the result of the bet and then play the next round.
    # Labouchere states that the first and last numbers of the sequence are removed in the event of a win, and the
    # amount of the bet is added to the end of the sequence in the event of a loss.
    if won:
        # print "won"
        bets, resulting_balance = gamble(sequence[1:-1], balance+bet)
        # Increment the number of bets because we made a one and return the resulting balance
        return bets+1, resulting_balance
    else:
        # print "lost"
        bets, resulting_balance = gamble(sequence+[bet], balance-bet)
        # Increment the number of bets because we made a one and return the resulting balance
        return bets+1, resulting_balance
