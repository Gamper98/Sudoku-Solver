from Sudoku_Board import Sudoku_Board
from Sudoku_Solver import Sudoku_Solver
from Sudoku_History import *
import numpy as np
import json

class Sudoku_Modell:
    def __init__(self):
        self.__history = Sudoku_History()
        self.__board = Sudoku_Board()
        self.__solver = Sudoku_Solver(self.__board, self.__history)
        self.__file = {}
        self.__active_board = None
#TODO miden vissza alaphelyzetbe mehet
#TODO solver csak függvényekből álljon, de legalább visszaadja a kiszámolt boardot és ne az állítsa be
#TODO Rövid leirás az osztályokhoz doksi
    #board methods    
    def get_board(self):
        return self.__board.get_board().copy()

    def get_board_at(self, pos):
        return self.__board.get_board_at(pos)

    def get_pv_at(self, pos):
        return self.__board.get_pv_at(pos)
    
    def get_possible_values(self):
        return self.__board.get_possible_values().copy()

    def set_board_at(self, num, pos):
        self.__board.set_board_at(num, pos)

    #solver methods
    def get_pattern_names(self):
        return self.__solver.get_patterns_names()

    def set_pattern(self, values):
        self.__solver.set_pattern(values)

    def setup_possible_values(self):
        if np.all(self.__board.get_possible_values()):
            self.__solver.setup_possible_values()

    #history methods
    def get_history(self):
        return self.__history.get_history()

    def get_his_pos(self):
        return self.__history.get_his_pos()

    #model methods
    def get_keys(self):
        return self.__file.keys()
    
    def get_active_board(self):
        return self.__active_board

    def solve(self):        
        self.setup_possible_values()
        while True:
            is_found, solution = self.__solver.solve()
            if not is_found: return
            if solution is None : continue
            #if solution is None : return
            indeces = np.nonzero(solution)
            values = solution[indeces]
            self.__board.get_board()[indeces] = values
            #return

    def clear(self):
        self.__board.clear()
        self.__active_board = None
        self.__history.reset()

    def load_file(self, path):
        try:
            f = open(path)
            temp = json.load(f)
            for key in temp.keys():
                self.__file[key] = {}
                self.__file[key]['board'] = np.array(temp[key]['board'], dtype=np.uint8)
            f.close()
            return True
        except:
            return False

    def load_board(self, key):
        self.__board.clear()
        self.__board.set_board(self.__file[key]['board'].copy())
        self.__active_board = key

    def step_back_his(self):
        his = self.__history.step_back_his()
        if his.op_type == Op_Type.Add:
            self.__board.set_board_at(0, (his.row, his.col))
        else:
            self.__board.set_pv_at((his.num, his.row, his.col), True)
        return his

    def step_forward_his(self):
        his = self.__history.step_forward_his()
        if his.op_type == Op_Type.Add:
            self.__board.set_board_at(his.num, (his.row, his.col))
        else:
            self.__board.set_pv_at((his.num, his.row, his.col), False)
        return his