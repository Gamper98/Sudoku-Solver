import numpy as np

class Sudoku_Board():
    def __init__(self):
        self.__board = np.zeros(81, dtype=np.uint8).reshape(9, -1)
        self.__possible_values = np.full((9,9,9), fill_value=True, dtype=np.bool8)
    
    def get_board(self):
        return self.__board

    def get_possible_values(self):
        return self.__possible_values

    def get_board_at(self, pos):
        return self.__board[pos].copy()

    def get_pv_at(self, pos):
        return self.__possible_values[pos].copy()
    
    def set_pv_at(self, pos, value):
        self.__possible_values[pos] = value

    def set_board_at(self, num, pos):
        self.__board[pos] = num

    def set_board(self, board):
        self.__board = np.array(board, dtype=np.uint8)

    def clear(self):
        self.__board[:] = 0
        self.__possible_values[:] = True