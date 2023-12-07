#!/usr/bin/env python3

import numpy as np


class Hand:
    card_map = {
        "T": 10,
        "J": -1,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, cards, bid):
        self.original_cards = cards
        self.cards = np.array(self._map_cards(cards))
        self.bid = bid
        self.strength = self._get_best_strength(0)

    @classmethod
    def _map_cards(cls, cards):
        return list(map(cls._map_card, cards))

    @classmethod
    def _map_card(cls, card):
        if card in cls.card_map:
            return cls.card_map[card]
        return int(card)

    def _get_best_strength(self, strength):
        strength = self._get_strength()
        if -1 in self.cards:
            idx = np.where(self.cards == -1)[0][0]
            cards_copy = self.cards.copy()
            for new_card in range(1, 15):
                self.cards[idx] = new_card
                strength = max(strength, self._get_best_strength(strength))
            self.cards = cards_copy
        return strength

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
                if self_card != other_card:
                    return self_card < other_card
        return self.strength < other.strength


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_hands(lines):
    hands = []
    for idx, line in enumerate(lines):
        cards, bid = line.strip().split()
        hands.append(Hand(list(cards), int(bid)))
        print(f"{idx} {hands[-1].original_cards} {hands[-1].strength}")
    return hands


def get_winnings(hands):
    winnings = []
    for multiplier, hand in enumerate(sorted(hands, reverse=False), start=1):
        winnings.append(multiplier * hand.bid)
        print(f"{hand.original_cards} {hand.strength}")
    return winnings


def main(filename="input.txt"):
    hands = parse_hands(read_file(filename))
    winnings = get_winnings(hands)
    print(f"part 1:  {sum(winnings)}")


if __name__ == "__main__":
    main("test.txt")
    main()
