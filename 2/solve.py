#!/usr/bin/env python3

import re


def read_file(filename="input.txt"):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse_games(lines):
    games = {}
    for line in lines:
        game_metadata, game_data = line.split(":")
        game_number = int(re.search(r"\d+", game_metadata)[0])
        games[game_number] = get_sub_games(game_data)
    return games


def get_sub_games(game_data):
    sub_games = []
    for sub_game in game_data.split(";"):
        sub_games.append(
            {
                "red": get_cube_count(sub_game, "red"),
                "green": get_cube_count(sub_game, "green"),
                "blue": get_cube_count(sub_game, "blue"),
            }
        )
    return sub_games


def get_cube_count(sub_game, color):
    count = re.search(fr"\d+(?= {color})", sub_game)
    return 0 if count is None else int(count[0])


def get_valid_games(games, thresholds):
    valid_games = []
    for game, sub_games in games.items():
        valid = True
        for sub_game in sub_games:
            valid &= sub_game["red"] <= thresholds["red"]
            valid &= sub_game["green"] <= thresholds["green"]
            valid &= sub_game["blue"] <= thresholds["blue"]
        if valid:
            valid_games.append(game)
    return valid_games


def get_min_powers(games):
    min_powers = []
    for sub_games in games.values():
        red, green, blue = 0, 0, 0
        for sub_game in sub_games:
            red = max(red, sub_game["red"])
            green = max(green, sub_game["green"])
            blue = max(blue, sub_game["blue"])
        min_powers.append(red * green * blue)
    return min_powers


def main():
    games = parse_games(read_file())
    valid_games = get_valid_games(games, {"red": 12, "green": 13, "blue": 14})
    min_powers = get_min_powers(games)
    print(f"part 1:  {sum(valid_games)}")
    print(f"part 2:  {sum(min_powers)}")


if __name__ == "__main__":
    main()
