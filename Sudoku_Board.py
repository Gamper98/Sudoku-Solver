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
        return self.__history

    def get_current_his_pos(self):
        return self.__current_his_pos

    def append_to_history(self, value):
        self.__history.append(value)
        self.__current_his_pos += 1

    def insert_to_board(self, num, pos):
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



    # not used 

    def __is_valid_placing(self, num, pos):
        if (not self.__board[pos] and 
              num not in self.__board[pos[0],] and 
              num not in self.__board[:,pos[1]] and 
              num not in self.__board[pos[0]//3*3:pos[0]//3*3+3 ,pos[1]//3*3:pos[1]//3*3+3]):
            return True
        return False

    def insert_wth_check(self, num, pos):
        if self.__is_valid_placing(num, pos):
            self.__board[pos] = num
            return True
        else: return False



