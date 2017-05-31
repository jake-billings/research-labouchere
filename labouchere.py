import random


def flip_coin():
    return bool(random.getrandbits(1))


def gamble(sequence, balance):
    won = flip_coin()

    if len(sequence)<1:
        print "Aborting because the sequence is empty"
        return balance

    if len(sequence) is 1:
        bet = sequence[0]
    else:
        bet = sequence[0] + sequence[-1]

    if bet > balance:
        print "Aborting because you're broke", balance
        return balance

    print "Betting " + str(bet) + " with a balance of " + str(balance) + " due to sequence " + str(sequence)

    if won:
        print "won"
        return gamble(sequence[1:-1], balance+bet)
    else:
        print "lost"
        return gamble(sequence+[bet], balance-bet)