#!/usr/bin/env python3

import numpy as np


class Hand:
    card_map = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, cards, bid):
        self.cards = np.array(self._map_cards(cards))
        self.bid = bid
        self.strength = self._get_strength()

    @classmethod
    def _map_cards(cls, cards):
        return list(map(cls._map_card, cards))

    @classmethod
    def _map_card(cls, card):
        if card in cls.card_map:
            return cls.card_map[card]
        return int(card)

    def _get_strength(self):
        self.unique, self.counts = np.unique(self.cards, return_counts=True)
        strength = 0
        if self._five_of_a_kind():
            strength = 6
        elif self._four_of_a_kind():
            strength = 5
        elif self._full_house():
            strength = 4
        elif self._three_of_a_kind():
            strength = 3
        elif self._two_pair():
            strength = 2
        elif self._one_pair():
            strength = 1
        return strength

    def _five_of_a_kind(self):
        return 5 in self.counts

    def _four_of_a_kind(self):
        return 4 in self.counts

    def _full_house(self):
        return self._three_of_a_kind() and self._one_pair()

    def _three_of_a_kind(self):
        return 3 in self.counts

    def _two_pair(self):
        _, count_counts = np.unique(self.counts, return_counts=True)
        return 2 in self.counts and 2 in count_counts

    def _one_pair(self):
        return 2 in self.counts

    def __lt__(self, other):
        if self.strength == other.strength:
            for self_card, other_card in zip(self.cards, other.cards):
                if self_card == other_card:
                    continue
                return self_card < other_card
        return self.strength < other.strength


class HandVariant(Hand):
    card_map = {
        "T": 10,
        "J": -1,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, cards, bid):
        super().__init__(cards, bid)
        self.strength = self._get_best_strength(0)

    def _get_best_strength(self, strength):
        strength = self._get_strength()
        if -1 in self.cards:
            strength = self._enumerate_alternates(strength)
        return strength

    def _enumerate_alternates(self, strength):
        idx = np.where(self.cards == -1)[0][0]
        cards_copy = self.cards.copy()
        for new_card in range(1, 15):
            self.cards[idx] = new_card
            strength = max(strength, self._get_best_strength(strength))
        self.cards = cards_copy
        return strength


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_hands(lines, hand_type):
    hands = []
    for line in lines:
        cards, bid = line.strip().split()
        hands.append(hand_type(list(cards), int(bid)))
    return hands


def get_winnings(hands):
    winnings = []
    for multiplier, hand in enumerate(sorted(hands, reverse=False), start=1):
        winnings.append(multiplier * hand.bid)
    return winnings


def main(filename="input.txt"):
    lines = read_file(filename)
    print(f"part 1:  {sum(get_winnings(parse_hands(lines, Hand)))}")
    print(f"part 2:  {sum(get_winnings(parse_hands(lines, HandVariant)))}")


if __name__ == "__main__":
    main("test.txt")
    main()
