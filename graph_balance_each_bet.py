import random

from labouchere import gamble
from export_csv import export_array_as_csv


# Return a random boolean in order to simulate a coin flip.
# This is approximately 50% odds.
# The odds are not 50% on online betting sites. They typically take a "house advantage," so the odds are actually
# similar to 49.95%.
def flip_coin():
    return bool(random.getrandbits(1))


# Runs labouchere (see labouchere.py) but records the balance after every bet
def gamble(sequence=[1,2,3], balance=4000, history=[]):
    # If the sequence is empty, the labouchere system says that the round is over.
    # End the recursion. This is essentially a win.
    if len(sequence) < 1:
        # print "Aborting because the sequence is empty"
        # Return 0 and the initial balance because no bet was made
        return 0, balance, [[0, 0, balance, sequence, 'won']]

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
        return 0, balance, [[0, 0, balance, sequence, 'broke']]

    # If a random boolean is true, we won.
    won = flip_coin()

    # Add or subtract from the balance based on the result of the bet and then play the next round.
    # Labouchere states that the first and last numbers of the sequence are removed in the event of a win, and the
    # amount of the bet is added to the end of the sequence in the event of a loss.
    if won:
        bets, resulting_balance, history = gamble(sequence[1:-1], balance+bet, history)
        # Increment the number of bets because we made a one and return the resulting balance

        resulting_history = [[bet, won, balance, sequence]]+history
        return bets+1, resulting_balance, resulting_history
    else:
        bets, resulting_balance, history = gamble(sequence+[bet], balance-bet, history)
        resulting_history = [[bet, won, balance, sequence]]+history
        return bets+1, resulting_balance, resulting_history


# Store the player's balance/betting history over multiple rounds
def gamble_multiple_times(rounds=10000, initial_balance=4000):
    data = [['bet', 'won', 'balance', 'sequence', 'event']]
    balance = initial_balance
    for i in range(0, rounds):
        num_bets, balance, history = gamble(sequence=[1, 2, 3], balance=balance)
        data += history
        if balance < 1:
            break
    return data

if __name__ == "__main__":
    export_array_as_csv(gamble_multiple_times(), name='balance_after_each_bet.csv')
