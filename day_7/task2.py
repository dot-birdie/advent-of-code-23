import time


def get_participants(lines) -> list:
    participants = [None] * len(lines)
    for index in range(len(lines)):
        cards, bid = lines[index].split(" ")
        participants[index] = JokerHand(cards, int(bid))
    return participants


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.type = self.get_type()
        self.CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def get_value_of_card(self, card):
        return self.CARDS.index(card) + 1

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
        return self.get_value_of_card(self.cards[index]) < self.get_value_of_card(other.cards[index])


class JokerHand(Hand):

    def __init__(self, cards, bid):
        self.JOKER_CARD = "J"
        super().__init__(cards, bid)
        self.CARDS = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def get_type(self):
        occurrence = {item: self.cards.count(item) for item in self.cards}
        number_jokers = 0
        if self.JOKER_CARD in occurrence:
            number_jokers = occurrence[self.JOKER_CARD]
            occurrence.pop(self.JOKER_CARD)
        else:
            return super().get_type()

        if len(occurrence.values()) == 0:
            # all cards are jokers
            return 7

        max_occurrences = max(occurrence.values())
        if max_occurrences + number_jokers == 5:
            return 7
        elif max_occurrences + number_jokers == 4:
            return 6
        elif max_occurrences + number_jokers == 3:
            if number_jokers == 1:
                if len(occurrence) == 2:
                    # one joker card was removed
                    # no occurrence can be 3, therefore here 2,2 only possibility -> full house
                    return 5
                else:
                    return 4
            else:
                # only possibility here are 2 jokers, with more jokers the type was already found
                # with two jokers no full house possible -> two time occance to four of a kind
                return 4
        else:
            # case two pairs can not happen -> tripple is better type
            # case high card does not happen because at least one joker, else super method would have been executed
            return 2


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
