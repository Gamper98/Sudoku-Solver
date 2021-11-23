from dataclasses import dataclass
from enum import Enum
import numpy as np

class Op_Type(Enum):
    Remove = 1
    Add = 2

@dataclass
class History:
    op_type: Op_Type
    row: int
    col: int
    num: int
    p_name: str

    def __str__(self):
        return f'Pattern name={self.p_name}, Operation={self.op_type.name}, row={self.row+1}, col={self.col+1}, num={self.num+1}'

    def __eq__(self, o):
        if isinstance(o, History):
            return self.op_type == o.op_type and \
                    self.row == o.row and \
                    self.col == o.col and \
                    self.num == o.num and \
                    self.p_name == o.p_name
        return False

class Sudoku_History:
    def __init__(self):
        self.__history = []
        self.__pos = -1

    def get_history(self):
        return self.__history.copy()

    def get_his_pos(self):
        return self.__pos

    def reset(self):
        self.__history = []
        self.__pos = -1

    def append_history_one(self, op_type, row, col, num, name):
        self.__history.append(History(op_type, row, col, num, name))
        self.__pos += 1

    def append_history_array(self, op_type, board, name):
        if op_type == Op_Type.Add:
            row, col = np.nonzero(board)
            for i, r_idx in enumerate(row):
                self.__history.append(History(Op_Type.Add, r_idx, col[i], board[r_idx, col[i]]-1, name))
        else:
            num, row, col  = np.nonzero(board)
            for i, r_idx in enumerate(row):
                self.__history.append(History(Op_Type.Remove, r_idx, col[i], num[i], name))
        self.__pos = len(self.__history) - 1
        
    def step_back_his(self):
        if self.__pos >= 0:
            self.__pos -= 1
        return self.__history[self.__pos+1]

    def step_forward_his(self):
        if self.__pos < len(self.__history)-1:
            self.__pos += 1
        return self.__history[self.__pos]