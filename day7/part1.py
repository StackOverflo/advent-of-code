'''
--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!)
It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here
to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the
horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island,
making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the
machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree
automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of
similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand
consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card
follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other
card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third
label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each
other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand.
If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each
hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand
with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly,
77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have
the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid
multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the
strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be
multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
Your puzzle answer was 249204891.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

'''

from functools import cmp_to_key

filePath = 'day7\input.txt'

cardMappping = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10
}


def getCardFreq(hand) -> dict:
    cardFreq = {}
    for card in hand:
        cardFreq[card] = cardFreq.get(card, 0) + 1
    return cardFreq


def getHandRank(hand) -> int:
    cardFreq = getCardFreq(hand)

    # 5 of a kind
    if len(cardFreq) == 1:
        return 7
    elif len(cardFreq) == 2:
        # 4 of a kind
        if 4 in cardFreq.values():
            return 6
        # if not 4 of a kind, then full house
        else:
            return 5
    elif len(cardFreq) == 3:
        # 3 of a kind
        if 3 in cardFreq.values():
            return 4
        # if not 3 of a kind, then 2 pair
        else:
            return 3
    # 1 pair
    elif len(cardFreq) == 4:
        return 2
    else:
        return 1


def compareHigherHand(hand1, hand2) -> int:
    h1 = hand1[0]
    h2 = hand2[0]
    hand1Rank = getHandRank(h1)
    hand2Rank = getHandRank(h2)

    if hand1Rank != hand2Rank:
        return 1 if hand1Rank > hand2Rank else -1

    # same hands so check high card
    for i in range(0, 5):
        if h1[i] != h2[i]:
            card1 = cardMappping[h1[i]] if h1[i] in cardMappping else int(h1[i])
            card2 = cardMappping[h2[i]] if h2[i] in cardMappping else int(h2[i])

            return 1 if card1 > card2 else -1

    return 0

def main():
    with open(filePath) as f:
        lines = f.readlines()
        hands = [(hand.split()) for hand in lines]

    sortedHands = sorted(hands, key=cmp_to_key(compareHigherHand))

    ans = sum([int(hand[1]) * (i+1) for i, hand in enumerate(sortedHands)])

    print(f'The total winnings are {ans}')


if __name__ == '__main__':
    main()
