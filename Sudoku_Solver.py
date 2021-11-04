import numpy as np
import itertools as itr
from Sudoku_History import Op_Type

class Sudoku_Solver():
    def __init__(self, board, his):
        self.__boardClass = board
        self.__hisClass = his
    
    def solve(self):
        indeces = [key for key, item in self.__pattern_methods.items() if item[1]]
        pv_original = self.__boardClass.get_possible_values().copy()
        for pos in indeces:
            solution = self.__pattern_methods[pos][0](self)
            if pos in (0, 1) and np.any(solution.flatten()!=0):
                self.__change_pv(solution)
                self.__hisClass.append_history_array(Op_Type.Remove, pv_original != self.__boardClass.get_possible_values() , self.__pattern_methods[pos][2])
                self.__hisClass.append_history_array(Op_Type.Add, solution, self.__pattern_methods[pos][2])
                return True, solution
            if pos not in (0, 1) and solution:
                self.__hisClass.append_history_array(Op_Type.Remove, pv_original != self.__boardClass.get_possible_values() , self.__pattern_methods[pos][2])
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
        lines_ppairs = self.__get_change_pos(self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9))
        column_ppairs = self.__get_change_pos(self.__boardClass.get_possible_values().swapaxes(1,2).reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9))
        pv = self.__boardClass.get_possible_values().reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        cond_1 = np.any(pv[lines_ppairs])
        pv[lines_ppairs] = False
        self.__boardClass.get_possible_values()[:] = pv.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        pv = self.__boardClass.get_possible_values().swapaxes(1,2).reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        cond_2 = np.any(pv[column_ppairs])
        pv[column_ppairs] = False
        self.__boardClass.get_possible_values()[:] = pv.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9).swapaxes(1,2)
        return cond_1 or cond_2

    def box_line_reduction(self):
        lines_ppairs = self.__get_change_pos(self.__boardClass.get_possible_values())
        column_ppairs = self.__get_change_pos(self.__boardClass.get_possible_values().swapaxes(1,2))
        pv = self.__boardClass.get_possible_values()
        cond_1 = np.any(pv[lines_ppairs])
        pv[lines_ppairs] = False
        self.__boardClass.get_possible_values()[:] = pv
        pv = self.__boardClass.get_possible_values().swapaxes(1,2)
        cond_2 = np.any(pv[column_ppairs])
        pv[column_ppairs] = False
        self.__boardClass.get_possible_values()[:] = pv.swapaxes(1,2)
        return cond_1 or cond_2
        
    def __get_change_pos(self, pv):
        pos = self.__get_third_filled_rows(pv)
        return self.__get_sqrs_to_change_pos(pos)

    def __get_third_filled_rows(self, pv):
        rows_to_3x3sqrs = pv.reshape(9,9,3,3)
        rows_to_3x3sqrs_sum = np.sum(rows_to_3x3sqrs, axis=3, dtype=np.bool8)
        blr_sqrs = np.count_nonzero(rows_to_3x3sqrs_sum, axis=2)
        pos = np.argmax(rows_to_3x3sqrs_sum, axis=2)
        pos[blr_sqrs != 1] = -1
        return pos

    def __get_sqrs_to_change_pos(self, pos):
        nums , sqrs = np.where(pos != -1)
        cols = [pos[nums, sqrs]*3,pos[nums, sqrs]*3+1, pos[nums, sqrs]*3+2 ]
        rows = [sqrs//3*3 + (sqrs-1)%3, sqrs//3*3 + (sqrs+1)%3]
        cols = np.column_stack(cols)
        rows = np.column_stack(rows)
        return (nums.T[None,None], rows.T[None], np.repeat(cols[:,None], 2, axis=1).T)

    def naked_pairs(self):
        return self.__naked_subsets(2)

    def naked_triples(self):
        return self.__naked_subsets(3)

    def naked_quads(self):
        return self.__naked_subsets(4)

    def hidden_pairs(self):
        return self.__hidden_subsets(2)
    
    def hidden_triples(self):
        return self.__hidden_subsets(3)
        
    def hidden_quads(self):
        return self.__hidden_subsets(4)

    def __hidden_subsets(self, nc):
        pv_original = self.__boardClass.get_possible_values().copy()
        pv_rows = self.__subset_finder(pv_original.swapaxes(0,2) , nc)
        pv_cols = self.__subset_finder(pv_original.swapaxes(1,2).swapaxes(0,2), nc)
        pv_sqrs = self.__subset_finder(pv_original.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9).swapaxes(0,2), nc)
        self.__boardClass.get_possible_values()[:] *= pv_rows.swapaxes(0,2) *\
                pv_cols.swapaxes(0,2).swapaxes(1,2) *\
                pv_sqrs.swapaxes(0,2).reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        return np.any(pv_original != self.__boardClass.get_possible_values()) 

    def __naked_subsets(self, nc):
        pv_original = self.__boardClass.get_possible_values().copy()
        pv_rows = self.__subset_finder(pv_original , nc)
        pv_cols = self.__subset_finder(pv_original.swapaxes(1,2), nc)
        pv_sqrs = self.__subset_finder(pv_original.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9), nc)
        self.__boardClass.get_possible_values()[:] *= pv_rows * pv_cols.swapaxes(1,2) *\
                pv_sqrs.reshape(9,3,3,3,3).swapaxes(2,3).reshape(9,9,9)
        return np.any(pv_original != self.__boardClass.get_possible_values())

    def __subset_finder(self, pv, nc):
        pv_nc_amount_in_cell = pv.copy()
        count_nonzero = np.count_nonzero(pv_nc_amount_in_cell, axis=0)
        pv_nc_amount_in_cell[:, (count_nonzero > nc) | (count_nonzero == 1)] = False

        col_inds = [np.argwhere(data).flatten() for data in np.any(pv_nc_amount_in_cell, axis=0)]
        col_inds_combs = [  [[ind] * nc, item] for ind, data in enumerate(col_inds) for item in itr.combinations(data,nc)]
        if not col_inds_combs: return pv
        np_col_inds_combs = np.array(col_inds_combs)
        pv_col_combs = pv_nc_amount_in_cell[:,np_col_inds_combs[:,0], np_col_inds_combs[:,1]]
        pv_col_combs_any = np.any(pv_col_combs, axis=2)
        pv_count_uniques = np.count_nonzero(pv_col_combs_any, axis=0)
        x_unqiues_mask = pv_count_uniques==nc
        pv_nc_subsets = pv.copy()
        rows = np_col_inds_combs[x_unqiues_mask,0,1]
        cols = np_col_inds_combs[x_unqiues_mask,1]
        nums = np.nonzero(pv_col_combs_any[:, x_unqiues_mask].T)[1].reshape(-1,nc)
        pv_nc_subsets[nums, rows[:, None]] = False
        pv_nc_subsets[nums[:,None].T, rows[None,None], cols[:,:,None].T] = True
        return pv_nc_subsets

    def x_wing(self):
        return self.__nc_wings_apply(2)

    def swordfish(self):
        return self.__nc_wings_apply(3)


    def __nc_wings_apply(self, nc):
        pv_original = self.__boardClass.get_possible_values().copy()
        pv_rows = self.__nc_wings_finder(pv_original , nc)
        pv_cols = self.__nc_wings_finder(pv_original.swapaxes(1,2), nc)
        self.__boardClass.get_possible_values()[:] *= pv_rows *\
                pv_cols.swapaxes(1,2)
        return np.any(pv_original != self.__boardClass.get_possible_values()) 


    def __nc_wings_finder(self, pv, nc):
        pv_copy = pv.copy()
        count_rows = np.count_nonzero(pv_copy, axis=2)
        count_rows[(count_rows == 1) | (count_rows > nc)] = 0

        row_inds = [np.argwhere(row).flatten() for row in count_rows]
        row_inds_combs = [  [[ind] * nc, item] for ind, data in enumerate(row_inds)\
            for item in itr.combinations(data,nc)]
        if not row_inds_combs: return pv
        np_row_inds_combs = np.array(row_inds_combs)

        pv_row_combs = pv[np_row_inds_combs[:,0],np_row_inds_combs[:,1]]
        pv_row_combs_any = np.any(pv_row_combs, axis=1)
        pv_count_dup = np.count_nonzero(pv_row_combs_any, axis=1)
        nc_dup_mask = pv_count_dup == nc

        num = np_row_inds_combs[nc_dup_mask, 0, 1]
        row = np_row_inds_combs[nc_dup_mask, 1]
        col = np.nonzero(pv_row_combs_any[nc_dup_mask])[1].reshape(-1,nc)

        pv_copy[num[:,None], :, col] = False
        pv_copy[num[:,None,None], row[:,:,None], np.repeat(col[:,None], nc, axis=1)] = True
        return pv_copy

    __pattern_methods = {
        0:[get_naked_singles_matrix, True, 'Naked Singles'],
        1:[get_hidden_singles_matrix, True, 'Hidden Singles'], 
        2:[pointing_pairs, True, 'Pointing Pairs'],
        3:[box_line_reduction, True, 'Box Line Reduction'],
        4:[naked_pairs, True, 'Naked Pairs'],
        5:[naked_triples, True, 'Naked Triples'],
        6:[naked_quads, True, 'Naked Quads'],
        7:[hidden_pairs, True, 'Hidden Pairs'],
        8:[hidden_triples, True, 'Hidden Triples'],
        9:[hidden_quads, True, 'Hidden Quads'],
        10:[x_wing, True, 'X-wing'],
        11:[swordfish, True, 'Swordfish']
        }

