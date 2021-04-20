import argparse
import sys
from player import *


class MancalaGame:
    def __init__(self, fst_player: Player, snd_player: Player, n_holes: int, n_stones: int, show_after_move: bool):
        self.players = [fst_player, snd_player]
        self.fst_holes = [n_stones] * n_holes
        self.snd_holes = [n_stones] * n_holes
        self.holes = [self.fst_holes, self.snd_holes]

        # self.fst_player = fst_player
        # self.snd_player = snd_player

        self.show_after_move = show_after_move
        self.counter = 0
        fst_player.set_possible_moves(list(range(0, n_holes)))
        snd_player.set_possible_moves(list(range(0, n_holes)))

    def print_actual_board(self, counter):
        print(f'{counter}')
        # print('------------------------------------------')
        # print('| H2 |  5  |  4  |  3  |  2  |  1  |  0  |')
        print('------------------------------------------')
        print(
            f'| {self.players[1].points} |  {self.snd_holes[5]}  |  {self.snd_holes[4]}  |  {self.snd_holes[3]}  |  '
            f'{self.snd_holes[2]}  |  {self.snd_holes[1]}  |  {self.snd_holes[0]}  |')
        print('-----------------------------------------------')
        print(
            f'     |  {self.fst_holes[0]}  |  {self.fst_holes[1]}  |  {self.fst_holes[2]}  |  {self.fst_holes[3]}  |  '
            f'{self.fst_holes[4]}  |  {self.fst_holes[5]}  |  {self.players[0].points} |')
        print('     ------------------------------------------')
        # print('     |  0  |  1  |  2  |  3  |  4  |  5  |  H1 |')
        # print('     ------------------------------------------')
        suma = 0
        for hole in self.fst_holes:
            suma += hole
        for hole in self.snd_holes:
            suma += hole
        suma += self.players[0].points + self.players[1].points
        print(f'sum = {suma}')

    def play(self, player_now):
        player_next = 1 - player_now
        if len(self.players[0].possible_moves) > 0 or len(self.players[1].possible_moves) > 0:
            # move player and choose next player
            # command = input(f'Player {player_now} move: ').split()
            # try:
            #     player_next = self.move(player_now, int(command[0]))
            # except:
            #     print("Wrong move: ", command[0])
            player_next = self.players[player_now].make_move(self, player_now)

            # update possible moves
            self.players[player_now].possible_moves.clear()
            self.players[1 - player_now].possible_moves.clear()
            for hole_idx in range(len(self.holes[player_now])):
                if self.holes[player_now][hole_idx] != 0:
                    self.players[player_now].possible_moves.append(hole_idx)

            for hole_idx in range(len(self.holes[1 - player_now])):
                if self.holes[1 - player_now][hole_idx] != 0:
                    self.players[1 - player_now].possible_moves.append(hole_idx)

            # no more stones?
            # self.players[0].possible_moves = []  # for test
            if len(self.players[0 + player_now].possible_moves) == 0:
                for hole in self.holes[1 - player_now]:
                    self.players[1 - player_now].points += hole
                for hole_idx in range(len(self.holes[1 - player_now])):
                    self.holes[1 - player_now][hole_idx] = 0

            self.players[1 - player_now].possible_moves.clear()
            for hole_idx in range(len(self.holes[1 - player_now])):
                if self.holes[1 - player_now][hole_idx] != 0:
                    self.players[1 - player_now].possible_moves.append(hole_idx)

            if len(self.players[1 - player_now].possible_moves) == 0:
                for hole in self.holes[0 + player_now]:
                    self.players[0 + player_now].points += hole
                for hole_idx in range(len(self.holes[0 + player_now])):
                    self.holes[0 + player_now][hole_idx] = 0

            self.players[player_now].possible_moves.clear()
            for hole_idx in range(len(self.holes[player_now])):
                if self.holes[player_now][hole_idx] != 0:
                    self.players[player_now].possible_moves.append(hole_idx)

        if len(self.players[0].possible_moves) == 0 and len(self.players[1].possible_moves) == 0:
            self.counter += 1
            self.print_actual_board(f'game over in {self.counter} steps')

        else:
            if len(self.players[0].possible_moves) == 0 and len(self.players[1].possible_moves) == 0:
                self.counter += 1
                self.print_actual_board(f'game over in {self.counter} steps')
            else:
                self.counter += 1
                if self.show_after_move:
                    self.print_actual_board(f'counter: {self.counter}')
                self.play(player_next)

    def move(self, player: int, hole: int):
        assert (player == 0 or player == 1)
        if player == 0:
            assert (self.fst_holes[hole] > 0)
        elif player == 1:
            assert (self.snd_holes[hole] > 0)

        next_player = 1 - player

        assert (hole < len(self.holes[0 + player]))
        n_stones = self.holes[0 + player][hole]
        i_hole = hole + 1
        self.holes[0 + player][hole] = 0
        # while n_stones > 0:
        while True:
            while i_hole < len(self.holes[0 + player]):
                if i_hole != hole:
                    n_stones -= 1
                    if n_stones == 0:
                        if self.holes[0 + player][i_hole] == 0:
                            n_stones_opposite = self.holes[1 - player][len(self.holes[1 - player]) - 1 - i_hole]
                            if n_stones_opposite != 0:
                                self.holes[1 - player][len(self.holes[1 - player]) - 1 - i_hole] = 0
                                self.players[player].points += 1 + n_stones_opposite
                            else:
                                self.holes[0 + player][i_hole] += 1
                            i_hole = -99
                        else:
                            self.holes[0 + player][i_hole] += 1
                            i_hole += 1
                        break
                    else:
                        self.holes[0 + player][i_hole] += 1
                        i_hole += 1
                else:
                    i_hole += 1
            if n_stones == 0:
                break
            if i_hole == len(self.holes[0 + player]):
                self.players[0 + player].points += 1
                n_stones -= 1
                next_player = player
                if n_stones > 0:
                    next_player = 1 - player
                    j_hole = 0
                    while j_hole < len(self.holes[1 - player]):
                        self.holes[1 - player][j_hole] += 1
                        n_stones -= 1
                        j_hole += 1
                        if n_stones == 0:
                            break
                    if n_stones == 0:
                        break
                    else:
                        i_hole = 0
                else:
                    break
        return next_player


mg1 = MancalaGame(RandomPlayer([]), RandomPlayer([]), 6, 4, True)
mg1.print_actual_board('start board, counter: 0')
mg1.play(0)
