import logging
from logging import getLogger
from typing import List
import copy
import time

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s line:%(lineno)s [%(levelname)s]: %(message)s")
logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)

PLAYER_NUMBER = 2
MAX_CARD = 8


def main():
    logger.info("Start main")

    start = time.time()
    results = start_game()
    elapsed_time = time.time() - start

    logger.debug("Elapsed Time :{0}".format(elapsed_time) + "[sec]")

    trials = len(results)
    first_win = sum(result.win_player == 0 for result in results)
    logger.debug("Trials: " + str(trials) + ", First Win: " + str(first_win) + ", Second Win: " + str(trials - first_win))
    # logger.debug(list_to_str(results))


def start_game() -> list:
    players = [[i + 1 for i in range(0, MAX_CARD)] for j in range(0, PLAYER_NUMBER)]

    results = game_next(players, [], 0, 0)

    return results


def game_next(players: List[List[int]], layout: List[int], order: int, turn: int) -> List[object]:
    # まだカードを持っているプレイヤーの数が1以下
    end_game = [len(players[i]) == 0 for i in range(0, len(players))].count(True) >= 1
    if end_game:
        # logger.debug("End Game")
        return [GameResult(players.index([]))]

    can_pass = len(layout) != 0 and True not in list(
        map(lambda player: len(player) != 0 and max(player) > layout[0] and players.index(player) != prev_order(order, len(players)),
            players))
    if can_pass:
        # logger.debug("Pass")
        return game_next(players, [], next_order(order, len(players)), turn)

    results = []
    for card in players[order]:
        can_play_card = len(layout) == 0 or card > layout[0]
        if can_play_card:
            # logger.debug("Turn: " + str(turn) + ", Card: " + str(card) + ", Layout: " + str([card for card in layout]) + ", Order: " + str(order) + ", Players: " + str([player for player in players]))
            # logger.debug("Play Card: " + str(card))
            played_players = copy.deepcopy(players)
            played_players[order].remove(card)
            results += game_next(played_players, [card], next_order(order, len(players)), turn + 1)

    # logger.debug("return: " + list_to_str(results))
    return results


def prev_order(order, count):
    prev = order - 1
    if prev < 0:
        prev = count - 1
    return prev


def next_order(order, count):
    next = order + 1
    if next >= count:
        next = 0
    return next


def list_to_str(list: list):
    return str([str(item) for item in list])


class GameResult(object):

    def __init__(self, win_player):
        self.win_player = win_player

    def __str__(self):
        return "Win: " + str(self.win_player)


if __name__ == '__main__':
    main()
