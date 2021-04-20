from abc import ABC, abstractmethod
from random import sample


class Player(ABC):
    def __init__(self, possible_moves: list):
        self.points = 0
        self.possible_moves = possible_moves  # TODO: na ogół pusta lista tu bedzie, zastanowić się czy nie zrobic None bez parametru

    def add_points(self, n_points_to_add):
        self.points += n_points_to_add

    def set_possible_moves(self, possible_moves: list):
        self.possible_moves = possible_moves

    @abstractmethod
    def make_move(self, mancala_game, player_now):
        pass


class RandomPlayer(Player):
    def make_move(self, mancala_game, player_now):
        try:
            random_hole = sample(self.possible_moves, 1)[0]
        except:
            raise Exception('error when random_sample')
        print(f'RandomPlayer {player_now} move: {random_hole}')
        player_next = mancala_game.move(player_now, random_hole)
        return player_next


class HumanPlayer(Player):
    def make_move(self, mancala_game, player_now):
        go = True
        while go:
            cmd_move = input(f'Player {player_now} move: ').split()
            try:
                player_next = mancala_game.move(player_now, int(cmd_move[0]))
                go = False
            except:
                print(f'Wrong move: {cmd_move[0]}')

        return player_next



