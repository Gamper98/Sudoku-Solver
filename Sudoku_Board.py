import numpy as np

class Sudoku_Board():
    def __init__(self):
        self.__board = np.zeros(81, dtype=np.uint8).reshape(9, -1)
        self.__possible_values = np.full((9,9,9), fill_value=True, dtype=np.bool8)
        self.__history = []
        self.__current_his_pos = -1
    
    def get_board(self):
        return self.__board

    def get_possible_values(self):
        return self.__possible_values

    def get_history(self):
        return self.__history.copy()

    def get_his_pos(self):
        return self.__current_his_pos

    def get_board_at(self, pos):
        return self.__board[pos].copy()

    def get_pv_at(self, pos):
        return self.__possible_values[pos].copy()

    def append_to_history(self, value):
        self.__history.append(value)
        self.__current_his_pos += 1

    def set_board_at(self, num, pos):
        self.__board[pos] = num
        self.__history.append([pos[0], pos[1], num])
        self.__current_his_pos += 1

    def set_board(self, board, history):
        self.__board = np.array(board, dtype=np.uint8)
        self.__history = history
        self.__current_his_pos = len(history) - 1

    def clear(self):
        self.__board[:] = 0
        self.__possible_values[:] = True
        self.__history = []
        self.__current_his_pos = -1

    def step_back_history(self):  
        if self.__current_his_pos > -1:
            x, y, value = self.__history[self.__current_his_pos]
            new_value = 0
            for item in self.__history[self.__current_his_pos-1::-1]:
                if [x,y,value] != item and item[0] == x and item[1] == y:
                    new_value = item[2]
            self.__board[x,y] = new_value
            self.__current_his_pos -= 1
    
    def step_forward_history(self):   
        if self.__current_his_pos < len(self.__history)-1:
            x, y, value = self.__history[self.__current_his_pos+1]
            self.__board[x,y] = value
            self.__current_his_pos += 1