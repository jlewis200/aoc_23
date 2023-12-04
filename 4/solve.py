#!/usr/bin/env python3

import re


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_cards(lines):
    cards = {}
    for line in lines:
        card_metadata, card_data = line.split(":")
        card_number = int(re.search(r"\d+", card_metadata).group())
        cards[card_number] = parse_card_data(card_data)
    return cards


def parse_card_data(card_data):
    winning, draws = card_data.split("|")
    winning = set(re.findall(r"\d+", winning))
    draws = set(re.findall(r"\d+", draws))
    return winning, draws


def get_matches(cards):
    return [len(winning & draws) for winning, draws in cards.values()]


def get_values(matches):
    return [0 if match == 0 else 2 ** (match - 1) for match in matches]


def get_card_counts(matches):
    components = [1] * len(matches)
    for idx, (match, component) in enumerate(zip(matches, components)):
        for jdx in range(idx + 1, idx + 1 + match):
            components[jdx] += component
    return components


def main(filename="input.txt"):
    cards = parse_cards(read_file(filename))
    matches = get_matches(cards)
    print(f"part 1:  {sum(get_values(matches))}")
    print(f"part 2:  {sum(get_card_counts(matches))}")


if __name__ == "__main__":
    main()
