from functools import cmp_to_key

hands = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

hands = open("input.txt", "r").read()

hands_bids = [h.strip().split() for h in hands.splitlines() if h.strip()]

cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

class Hand:
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        
    @property
    def kind(self):
        # Five of a kind
        for card in cards:
            if self.cards.count(card) == 5:
                return 0
        # Four of a kind
        for card in cards:
            if self.cards.count(card) == 4:
                return 1
        # Full house
        for card in cards:
            if self.cards.count(card) == 3:
                for other_card in cards:
                    if self.cards.count(other_card) == 2 and card != other_card:
                        return 2
        # Three of a kind
        for card in cards:
            if self.cards.count(card) == 3:
                return 3
        # Two pairs
        for card in cards:
            if self.cards.count(card) == 2:
                for other_card in cards:
                    if self.cards.count(other_card) == 2 and card != other_card:
                        return 4
        # One pair
        for card in cards:
            if self.cards.count(card) == 2:
                return 5
        return 6
    
    def compare(self, other: "Hand"):
        if self.kind > other.kind:
            return 1
        elif self.kind < other.kind:
            return -1
        else:
            for (card, other_card) in zip(self.cards, other.cards):
                if cards.index(card) > cards.index(other_card):
                    return 1
                elif cards.index(card) < cards.index(other_card):
                    return -1
            return 0

handes = [Hand(h[0], int(h[1])) for h in hands_bids]
handes.sort(key=cmp_to_key(lambda a, b: a.compare(b)), reverse=True)

# for i, h in enumerate(handes):
#     print(i, h.cards, h.bid, (i+1)*h.bid)

print("result:", sum([(i+1)*h.bid for i, h in enumerate(handes)]))
