import unittest
import numpy as np
from Sudoku_Board import Sudoku_Board
from Sudoku_History import *

class Test_Board(unittest.TestCase):

    def test_board_init(self):
        his = Sudoku_History()
        board = Sudoku_Board(his)
        self.assertFalse(np.any(board.get_board()), 'Board should be empty')
        self.assertTrue(np.all(board.get_possible_values()), 'Pencil marks should be all True')

    def test_set_board(self):
        test_board = np.array([[0,0,3,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,3,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,2,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,4,0],
                    [0,0,0,0,0,0,0,0,0]])
        his = Sudoku_History()
        board = Sudoku_Board(his)
        board.set_board(test_board)
        self.assertEqual(board.get_board()[0,2], test_board[0,2], 'Should be the equal with the given test board')
        self.assertEqual(board.get_board()[1,1], test_board[1,1], 'Should be the equal with the given test board')
        self.assertEqual(board.get_board_at((3,1)), test_board[3,1], 'Should be the equal with the given test board')
        self.assertEqual(board.get_board_at((7,7)), test_board[7,7], 'Should be the equal with the given test board')

    def test_set_board_at(self):
        his = Sudoku_History()
        board = Sudoku_Board(his)
        board.set_board_at(5, (1,1))
        self.assertEqual(board.get_board_at((1,1)), 5, 'Should be equal with 5 after changes pos 1,1 to 5')
    
    def test_set_pv(self):
        his = Sudoku_History()
        board = Sudoku_Board(his)
        board.get_possible_values()[0,:,:] = False
        self.assertFalse(np.any(board.get_possible_values()[0,:,:]), 'Should be False')
        self.assertFalse(np.any(board.get_pv_at((0))), 'Should be False')

        board.set_pv_at((5,5), False)
        self.assertFalse(np.any(board.get_pv_at((5,5))), 'Should be False')

    def test_clear(self):
        test_board = np.array([[0,0,3,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,3,0,0,0,0,0,0,0],
                    [0,0,0,0,1,0,0,0,0],
                    [0,0,0,0,0,0,2,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,4,0],
                    [0,0,0,0,0,0,0,0,0]])
        his = Sudoku_History()
        board = Sudoku_Board(his)        
        board.set_pv_at((5,5), False)
        self.assertFalse(np.any(board.get_pv_at((5,5))), 'Should be False')
        board.set_board(test_board)
        self.assertEqual(board.get_board()[0,2], test_board[0,2], 'Should be the equal with the given test board')
        board.clear()        
        self.assertFalse(np.any(board.get_board()), 'Board should be empty after clear')
        self.assertTrue(np.all(board.get_possible_values()), 'Pencil marks should be all True aflter clear')
        
class Test_History(unittest.TestCase):

    def test_history_init(self):
        his = Sudoku_History()
        self.assertFalse(his.get_history(), 'History array should be empty') 
        self.assertEqual(his.get_his_pos(), -1, 'Should be -1 at the start')

    def test_append_one(self):
        his = Sudoku_History()
        his.append_history_one(Op_Type.Add, 1, 1, 5, 'Test')
        self.assertEqual(his.get_history()[0], History(Op_Type.Add, 1, 1, 5, 'Test'), 'Should be equal with the appended value')
        self.assertEqual(his.get_his_pos(), 0, 'Should be 0 after first append')
        his.append_history_one(Op_Type.Remove, 2, 2, 4, 'Test_2')
        self.assertEqual(his.get_his_pos(), 1, 'Should be 1 after second append')
        self.assertEqual(his.get_history()[1], History(Op_Type.Remove, 2, 2, 4, 'Test_2'), 'Should be equal with the appended value')

    def test_reset(self):
        his = Sudoku_History()        
        his.append_history_one(Op_Type.Remove, 2, 2, 4, 'Test')
        self.assertEqual(his.get_his_pos(), 0, 'Should be 1 after first append')
        his.reset()
        self.assertFalse(his.get_history(), 'History array should be empty after reset') 
        self.assertEqual(his.get_his_pos(), -1, 'Should be -1 after reset')
    
    def test_append_list_add(self):
        his = Sudoku_History()  
        test_board = np.array([[0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,2,0,0,0,0,0,0,0],
                    [0,0,0,0,3,0,0,0,0],
                    [0,0,0,0,0,0,4,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,5,0],
                    [0,0,0,0,0,0,0,0,0]])
        his.append_history_array(Op_Type.Add, test_board, 'Test_array_add')
        self.assertEqual(his.get_his_pos(), 4, 'Should be 4 after appending and array')
        self.assertEqual(his.get_history()[2],History(Op_Type.Add, 4, 4, 2, 'Test_array_add'),'Should be 2 at pos(4,4), his pos is at 2')
        self.assertEqual(his.get_history()[4],History(Op_Type.Add, 7, 7, 4, 'Test_array_add'),'Should be 4 at pos(7,7), his pos is at 4')
    
    def test_append_list_rm(self):
        his = Sudoku_History()  
        test_pv = np.array([[[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                    [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,1]]])
        his.append_history_array(Op_Type.Remove, test_pv, 'Test_array_remove')
        self.assertEqual(his.get_his_pos(), 3, 'Should be 4 after appending and array')
        self.assertEqual(his.get_history()[0],History(Op_Type.Remove, 0, 4, 0, 'Test_array_remove'),'Should be 0 at pos(0,4), his pos is at 5')
        self.assertEqual(his.get_history()[2],History(Op_Type.Remove, 3, 4, 4, 'Test_array_remove'),'Should be 4 at pos(3,4), his pos is at 7')
    
    def test_step_back(self):
        his = Sudoku_History()  
        test_board = np.array([[0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,2,0,0,0,0,0,0,0],
                    [0,0,0,0,3,0,0,0,0],
                    [0,0,0,0,0,0,4,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,5,0],
                    [0,0,0,0,0,0,0,0,0]])
        his.append_history_array(Op_Type.Add, test_board, 'Test_array_add')        
        self.assertEqual(his.get_his_pos(), 4, 'Should be 4 after appending and array')
        r = his.step_back_his()
        self.assertEqual(his.get_his_pos(), 3, 'Should be 3 after stepping back once')
        self.assertEqual(r,History(Op_Type.Add, 7, 7, 4, 'Test_array_add'),'Should be 3 at pos(5,7) after stepping back once')
        r = his.step_back_his()
        r = his.step_back_his()        
        self.assertEqual(his.get_his_pos(), 1, 'Should be 1 after stepping back 3 times')
        self.assertEqual(r,History(Op_Type.Add, 4, 4, 2, 'Test_array_add'),'Should be 2 at pos(4,4) after stepping back once')
        r = his.step_back_his()
        r = his.step_back_his()
        r = his.step_back_his()
        r = his.step_back_his()        
        self.assertEqual(his.get_his_pos(), -1, 'Should be -1 after stepping back too many times')
        self.assertEqual(r,History(Op_Type.Add, 0, 2, 0, 'Test_array_add'),'Should be the first history element after stepping back too many times, 0 at (0,2)')

    def test_step_forward(self):
        his = Sudoku_History()  
        test_board = np.array([[0,0,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,2,0,0,0,0,0,0,0],
                    [0,0,0,0,3,0,0,0,0],
                    [0,0,0,0,0,0,4,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,5,0],
                    [0,0,0,0,0,0,0,0,0]])
        his.append_history_array(Op_Type.Add, test_board, 'Test_array_add')
        r = his.step_back_his()
        r = his.step_back_his()
        r = his.step_back_his()
        r = his.step_back_his()
        r = his.step_back_his()
        rf = his.step_forward_his()
        self.assertEqual(his.get_his_pos(), 0, 'Should be 0 after stepping back to the begining and forward once')
        self.assertEqual(rf,History(Op_Type.Add, 0, 2, 0, 'Test_array_add'),'Should be the first history element, 0 at (0,2)')
        rf = his.step_forward_his()
        rf = his.step_forward_his()
        self.assertEqual(his.get_his_pos(), 2, 'Should be 2 after stepping back to the begining and forward 3 times')
        self.assertEqual(rf,History(Op_Type.Add, 4, 4, 2, 'Test_array_add'),'Should be the third history element after stepping forward 3 times from -1, 2 at (4,4)')
        rf = his.step_forward_his()
        rf = his.step_forward_his()
        rf = his.step_forward_his()
        rf = his.step_forward_his()
        self.assertEqual(his.get_his_pos(), 4, 'Should be at the end after stepping back to the begining and forward too many times(4)')
        self.assertEqual(rf,History(Op_Type.Add, 7, 7, 4, 'Test_array_add'),'Should be the last history element after stepping forward too many times from, 4 at (7,7)')

if __name__ == '__main__':
    unittest.main()