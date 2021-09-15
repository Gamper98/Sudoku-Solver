from Sudoku_Board import *
from Sudoku_Solver import *
import json

class Sudoku_Modell:
    def __init__(self):
        self.__board = Sudoku_Board()
        self.__solver = Sudoku_Solver(self.__board)
        self.__file = {}
        self.__active_board = None

    #board methods    
    def get_board(self):
        return self.__board.get_board().copy()

    def get_board_at(self, pos):
        return self.__board.get_board_at(pos)

    def get_pv_at(self, pos):
        return self.__board.get_pv_at(pos)
    
    def get_possible_values(self):
        return self.__board.get_possible_values().copy()
    
    def get_history(self):
        return self.__board.get_history()

    def get_his_pos(self):
        return self.__board.get_his_pos()

    def set_board_at(self, num, pos):
        self.__board.set_board_at(num, pos)

    def append_to_history(self, his):
        self.__board.append_to_history(his)

    def step_back_history(self):
        self.__board.step_back_history()

    def step_forward_history(self): 
        self.__board.step_forward_history()

    #solver methods
    def get_pattern_names(self):
        return self.__solver.get_patterns_names()

    def set_pattern_names(self, values):
        self.__solver.set_pattern_names(values)

    def setup_possible_values(self):
        if np.all(self.__board.get_possible_values()):
            self.__solver.setup_possible_values()

    #model methods
    def get_keys(self):
        return self.__file.keys()
    
    def get_active_board(self):
        return self.__active_board

    def solve(self):
        while True:
            is_found, solution = self.__solver.solve()
            if not is_found: return
            if solution is None : continue
            #if solution is None : return
            indeces = np.nonzero(solution)
            values = solution[indeces]
            self.__board.get_board()[indeces] = values
            [self.__board.append_to_history([index[0], index[1], value]) for index, value in zip(np.transpose(indeces), values)]
            #return

    def clear(self):
        self.__board.clear()
        self.__active_board = None

    def load_file(self, path):
        try:
            f = open(path)
            temp = json.load(f)
            for key in temp.keys():
                self.__file[key] = {}
                self.__file[key]['board'] = np.array(temp[key]['board'], dtype=np.uint8)
                self.__file[key]['history'] = temp[key]['history']
            f.close()
            return True
        except:
            return False

    def load_board(self, key):
        self.__board.clear()
        self.__board.set_board(self.__file[key]['board'].copy(), self.__file[key]['history'].copy())
        self.__active_board = key