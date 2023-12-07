import time

CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


def get_participants(lines) -> list:
    participants = [None] * len(lines)
    for index in range(len(lines)):
        cards, bid = lines[index].split(" ")
        participants[index] = Hand(cards, int(bid))
    return participants

def get_value_of_card(card):
    return CARDS.index(card) + 1

class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.type = self.get_type()

    def get_type(self):
        occurrence = {item: self.cards.count(item) for item in self.cards}
        max_occurrences = max(occurrence.values())

        if max_occurrences == 5:
            return 7
        elif max_occurrences == 4:
            return 6
        elif max_occurrences == 3:
            if 2 in occurrence.values():
                return 5
            else:
                return 4
        elif max_occurrences == 2:
            # two pairs
            if len(occurrence.values()) == 3:
                return 3
            # only one pair
            else:
                return 2
        else:
            return 1

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        index = 0
        while self.cards[index] == other.cards[index]:
            index += 1
        return get_value_of_card(self.cards[index]) < get_value_of_card(other.cards[index])


start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

participants = get_participants(lines)
participants = sorted(participants)

total = 0
for index in range(len(participants)):
    total += (index + 1) * participants[index].bid

print(f"Total-winnings = {total}")

end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
