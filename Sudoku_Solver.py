import numpy as np

class Sudoku_Solver():
    def __init__(self, board):
        self.__boardClass = board
    
    def solve(self):
        indeces = [key for key, item in self.__pattern_methods.items() if item[1]]
        for pos in indeces:
            solution = self.__pattern_methods[pos][0](self)
            if pos in (0, 1) and np.any(solution.flatten()!=0):
                self.__change_pv(solution)
                return True, solution
            if pos not in (0, 1) and solution:
                return True, None
        return False, None

    def set_pattern_names(self, values):
        for i in range(len(values)):
            self.__pattern_methods[i][1] = values[i]

    def get_patterns_names(self):
        return [item[2] for item in self.__pattern_methods.values()]

    def setup_possible_values(self):
        not_filled_squared_mask = self.__boardClass.get_board() == 0 
        self.__boardClass.get_possible_values()[:] *= not_filled_squared_mask
        self.__apply_masks(self.__boardClass.get_board())

    def __change_pv(self, max_values):   
        self.__boardClass.get_possible_values()[np.repeat(max_values[None] != 0, 9, axis=0)] = False
        self.__apply_masks(max_values)

    def __apply_masks(self, board):
        self.__apply_row_mask(board)
        self.__apply_col_mask(board)
        self.__apply_sq_mask(board)

    def __apply_row_mask(self, board):
        self.__boardClass.get_possible_values()[:] = (self.__boardClass.get_possible_values().T * self.__rows_to_mask(board)).T

    def __apply_col_mask(self, board): 
        self.__boardClass.get_possible_values()[:] = (self.__boardClass.get_possible_values().T.swapaxes(0,1) * self.__rows_to_mask(board.T)).swapaxes(0,1).T

    def __apply_sq_mask(self, board):
        possible_values_sqares_to_rows = self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        sq_mask = self.__rows_to_mask(board.reshape(3,3,3,3).swapaxes(1,2).reshape(9,9))
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
    
    def pointing_pairs(self):
        lines_ppairs = self.get_pointing_pairs(self.__boardClass.get_possible_values())
        column_ppairs = self.get_pointing_pairs(self.__boardClass.get_possible_values().swapaxes(1,2))
        pv = self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        cond_1 = np.any(pv[lines_ppairs])
        pv[lines_ppairs] = False
        pv = pv.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        self.__boardClass.get_possible_values()[:] = pv
        pv = self.__boardClass.get_possible_values().swapaxes(1,2).reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        cond_2 = np.any(pv[column_ppairs])
        pv[column_ppairs] = False
        self.__boardClass.get_possible_values()[:] = pv.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9).swapaxes(1,2)
        return cond_1 or cond_2
        
    def get_pointing_pairs(self, pv):
        sq_to_rows = pv.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
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
        return (nums.T[None,None], rows.T[None], np.repeat(cols[:,None], 2, axis=1).T)

    def box_line_reduction(self):
        pass

    __pattern_methods = {
        0:[get_naked_singles_matrix, True, 'Naked Singles'],
        1:[get_hidden_singles_matrix, True, 'Hidden Singles'], 
        2:[pointing_pairs, True, 'Pointing Pairs']
        }

