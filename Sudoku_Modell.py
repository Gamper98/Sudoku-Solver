#%%
from Sudoku_Board import *
from Sudoku_Solver import *
import json

class Sudoku_Modell:
    def __init__(self):
        self.__board = Sudoku_Board()
        self.__solver = Sudoku_Solver(self.__board)
        self.__file = {}
        self.__active_board = None

    def get_board(self):
        return self.__board

    def get_solver(self):
        return self.__solver

    def get_board_keys(self):
        return self.__file.keys()
    
    def get_board_locked(self, key):
        return self.__file[key]['locked']

    def get_board_history(self, key):
        return self.__file[key]['history']
    
    def get_active_board(self):
        return self.__active_board

    def solve(self):
        self.__solver.setup_possible_values()
        solution = self.__solver.solve()
        while solution is not None and np.any(solution.flatten()!=0) and np.any(self.__board.get_board().flatten()==0):
            indeces = np.nonzero(solution)
            values = solution[indeces]
            self.__board.get_board()[indeces] = values
            [self.__board.append_to_history([index[0], index[1], value]) for index, value in zip(np.transpose(indeces), values)]
            self.__solver.setup_possible_values()
            solution = self.__solver.solve()
        print(self.__board.get_history())
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
                self.__file[key]['locked']  = {(item[0], item[1]) for item in temp[key]['locked']}
                self.__file[key]['history'] = temp[key]['history']
            f.close()
            return True
        except:
            return False

    def load_board(self, key):
        self.__board.clear()
        self.__board.set_board(self.__file[key]['board'].copy(), self.__file[key]['history'].copy())
        self.__active_board = key
        print(self.get_locked())
        
    def get_locked(self):
        return np.argwhere(self.__file[self.__active_board]['board'])

if __name__ == '__main__':


    m = Sudoku_Modell()
    board_2 = np.array([
        [7,0,4,0,0,6,0,0,9],
        [0,8,0,0,1,0,0,0,0],
        [0,0,3,0,2,0,4,5,0],
        [0,0,0,0,0,0,0,0,2],
        [0,5,6,0,0,0,7,8,0],
        [1,0,0,0,0,0,0,0,0],
        [0,2,5,0,3,0,1,0,0],
        [0,0,0,0,4,0,0,6,0],
        [9,0,0,5,0,0,3,0,7]
    ], dtype=np.int8)


# %%