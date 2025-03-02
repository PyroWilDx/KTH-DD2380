#!/usr/bin/env python3

import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

inf_value = 42424242
max_time = 0.090


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def heuristic(state):
    score_0 = state.player_scores[0]
    caught_fish_0 = state.player_caught[0]
    if caught_fish_0 != -1:
        score_0 += state.fish_scores[caught_fish_0]

    score_1 = state.player_scores[1]
    caught_fish_1 = state.player_caught[1]
    if caught_fish_1 != -1:
        score_1 += state.fish_scores[caught_fish_1]

    hook_position_0 = state.hook_positions[0]
    hook_position_1 = state.hook_positions[1]
    for fish_index, fish_position in state.fish_positions.items():
        fish_value = state.fish_scores[fish_index]
        dxdy_0 = distance(hook_position_0, fish_position)
        dxdy_1 = distance(hook_position_1, fish_position)
        score_0 += fish_value / (dxdy_0 + 1)
        score_1 += fish_value / (dxdy_1 + 1)

        if dxdy_0 < dxdy_1:
            score_0 += fish_value / (dxdy_1 + 1)
        elif dxdy_1 < dxdy_0:
            score_1 += fish_value / (dxdy_0 + 1)

    return score_0 - score_1


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()
            node = Node(message=msg, player=0)
            best_move = self.search_best_next_move_it(node)

            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move_it(self, node):
        start_time = time.time()

        i = 2
        while True:
            curr_start_time = time.time()
            best_move = self.search_best_next_move(node, i)
            curr_time = time.time()
            if curr_time - start_time + 5 * (curr_time - curr_start_time) > max_time:
                return best_move
            i += 1

    def search_best_next_move(self, node, i):
        childs = node.compute_and_get_children()
        childs = sorted(childs, key=lambda v: heuristic(v.state), reverse=True)

        best_move = None
        score_max = -inf_value
        for child in childs:
            score = self.search_best_next_move_rec(child, -inf_value, inf_value, i - 1)
            if score > score_max:
                best_move = child.move
                score_max = score

        return ACTION_TO_STR[best_move]

    def search_best_next_move_rec(self, node, a, b, i):
        if i == 0:
            return heuristic(node.state)

        childs = node.compute_and_get_children()
        if len(childs) == 0:
            return heuristic(node.state)

        if node.state.player == 0:
            childs = sorted(childs, key=lambda v: heuristic(v.state), reverse=True)
            score_max = -inf_value
            for child in childs:
                score = self.search_best_next_move_rec(child, a, b, i - 1)
                if score > score_max:
                    score_max = score

                a = max(a, score)
                if a >= b:
                    break
            return score_max

        childs = sorted(childs, key=lambda v: heuristic(v.state))
        score_min = inf_value
        for child in childs:
            score = self.search_best_next_move_rec(child, a, b, i - 1)
            if score < score_min:
                score_min = score

            b = min(b, score)
            if a >= b:
                break
        return score_min
