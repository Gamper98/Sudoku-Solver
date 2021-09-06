#%%
import numpy as np

class Sudoku_Solver():
    def __init__(self, board):
        self.__boardClass = board
    
    def solve(self): #return board and history list
        indeces = [key for key, item in self.__pattern_methods.items() if item[1]]
        for pos in indeces:
            solution = self.__pattern_methods[pos][0](self)
            if np.any(solution.flatten()!=0):
                return solution
        return np.zeros((9,9), dtype=np.uint8)

    def set_patterns(self, values):
        for i in range(len(values)):
            self.__pattern_methods[i][1] = values[i]

    def get_patterns_name(self):
        return [item[2] for item in self.__pattern_methods.values()]

    def setup_possible_values(self):
        not_filled_squared_mask = self.__boardClass.get_board() == 0 
        self.__boardClass.get_possible_values()[:] *= not_filled_squared_mask
        self.__apply_col_mask()
        self.__apply_row_mask()
        self.__apply_sq_mask()

    def __apply_row_mask(self):
        self.__boardClass.get_possible_values()[:] = (self.__boardClass.get_possible_values().T * self.__rows_to_mask(self.__boardClass.get_board())).T # .swapaxes(2,0)

    def __apply_col_mask(self): 
        self.__boardClass.get_possible_values()[:] = (self.__boardClass.get_possible_values().T.swapaxes(0,1) * self.__rows_to_mask(self.__boardClass.get_board().T)).swapaxes(0,1).T

    def __apply_sq_mask(self):
        possible_values_sqares_to_rows = self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        sq_mask = self.__rows_to_mask(self.__boardClass.get_board().reshape(3,3,3,3).swapaxes(1,2).reshape(9,9))
        possible_values_sqares_to_rows = possible_values_sqares_to_rows * sq_mask.T[:,:,None]
        self.__boardClass.get_possible_values()[:] = possible_values_sqares_to_rows.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)

    def __rows_to_mask(self, board):
        mask = np.full((9,9), fill_value=True)
        first_index = np.full((9,9), fill_value=np.arange(0,9))
        board = board.astype(np.int8)
        board -= 1
        board_stacked = np.stack((first_index.T, board), axis=1)

        board_stacked_in_pairs = board_stacked.swapaxes(1,2)
        not_negative_index_mask = board_stacked_in_pairs[:,:,1] != -1
        indeces = board_stacked_in_pairs[not_negative_index_mask]
        x,y = indeces.T
        mask[x,y] = False

        return mask

    def get_naked_singles_matrix(self):
        max_values = np.argmax(self.__boardClass.get_possible_values(), axis=0)
        count_zeros = np.count_nonzero(self.__boardClass.get_possible_values()==False, axis=0)
        not_only_one_value_mask = count_zeros != 8
        max_values += 1
        max_values[not_only_one_value_mask] = 0
        return max_values

    def get_hidden_singles_matrix(self):
        values = np.zeros((9,9), dtype=np.int8)
        is_zero_mask = self.__boardClass.get_possible_values() == 0
        row_mask = np.count_nonzero(is_zero_mask, axis=2) != 8
        col_mask = np.count_nonzero(is_zero_mask, axis=1) != 8
        row_max = np.argmax(self.__boardClass.get_possible_values(), axis = 2)
        col_max = np.argmax(self.__boardClass.get_possible_values(), axis = 1)
        row_max[row_mask] = 0
        col_max[col_mask] = 0
        x, y = np.where(row_max != 0)
        values[y, row_max[x,y]] = x+1        
        x, y = np.where(col_max != 0)
        values[col_max[x,y], y] = x+1   

        sq_to_rows_is_zero_mask = is_zero_mask.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        sq_to_rows_mask = np.count_nonzero(sq_to_rows_is_zero_mask, axis=2) != 8        
        sq_to_rows = self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)

        sq_max = np.argmax(sq_to_rows, axis=2)
        sq_max[sq_to_rows_mask] = 0
        x, y = np.where(sq_max != 0)
        values = values.reshape(3,3,3,3).swapaxes(1,2).reshape(9,9)
        values[y, sq_max[x,y]] = x+1          
        values = values.reshape(3,3,3,3).swapaxes(1,2).reshape(9,9)

        return values

    def get_pointing_pairs(self):
        sq_to_rows = self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        sq_to_rows_to_3x3col = sq_to_rows.reshape(9,9,3,3)
        sqr_3x3col_sum = np.sum(sq_to_rows_to_3x3col, axis=3, dtype=np.bool8)
        pp_sqr = np.count_nonzero(sqr_3x3col_sum, axis=2)
        pos = np.argmax(sqr_3x3col_sum, axis=2)
        pos[pp_sqr != 1] = -1
        nums , sqrs = np.where(pos != -1)
        cols = [pos[nums, sqrs]*3,pos[nums, sqrs]*3+1, pos[nums, sqrs]*3+2 ]
        rows = [sqrs//3*3 + (sqrs-1)%3, sqrs//3*3 + (sqrs+1)%3]
        cols = np.column_stack(cols)
        rows = np.column_stack(rows)
        '''
        func_array = np.zeros((9,9,3), dtype=np.bool8)
        to_mult = [[1,1,0], [1,0,1], [0,1,1]]
        for i in range(3):
            temp = sqr_3x3col_sum * to_mult[i]
            func_array[:,:,i] = np.prod(temp, axis=2)
        f_result = np.sum(func_array, axis=2)
        valid_rows = sq_to_rows * ~f_result.astype(np.bool8)
        nums_raw = np.argmax(valid_rows, axis=2)
        row_ids = nums_raw // 3 % 3
        row_ids = row_ids + [[0,3,6,0,3,6,0,3,6]]
        col_ids = np.full((9,9), [0,0,0,1,1,1,2,2,2])
        np.where(nums_raw !=0, (row_ids, col_ids))
        sq_to_rows.reshape(9,9,3,3)'''
        pass

    __pattern_methods = {0:[get_hidden_singles_matrix, True, 'Hidden Singles'], 
                        1:[get_naked_singles_matrix, False, 'Naked Singles']}

if __name__ == '__main__':
    from Sudoku_Board import *
    board = Sudoku_Board()
    board.set_board([[0,0,0,0,0,0,4,7,0],
                    [7,9,3,0,0,4,2,8,0],
                    [8,4,0,0,7,2,0,9,0],
                    [3,5,7,4,9,1,6,2,8],
                    [0,0,9,8,2,5,3,4,7],
                    [4,2,8,7,3,6,0,1,0],
                    [0,0,4,5,0,0,0,6,2],
                    [5,0,6,2,4,0,8,3,0],
                    [0,0,0,0,6,0,7,5,4]], [[0,6,4],[1,0,7],[3,3,4],[7,3,2],[8,7,5],[5,0,4],[6,2,4],[3,2,7],[5,5,6],[3,1,5],[3,4,9],[3,7,2],[4,4,2],[1,6,2],[1,7,8],[3,8,8],[4,3,8],[7,7,3],[4,6,3],[5,7,1],[3,0,3]])
    s = Sudoku_Solver(board)
    s.setup_possible_values()



def possible_values_plot(s):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x_pos, y_pos, z_pos = np.where(s.get_possible_values() == False)
    ax.view_init(180, 270)
    #ax.view_init(170, 260)
    ax.scatter(z_pos, x_pos[::-1], y_pos, c=x_pos)

# %%
