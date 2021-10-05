# Sudoku Solver with gui
Sudoku solver written in python

This program is mainly written for solving sudoku games based on strategies eg.: naked singles, swordfish, x-wing

Sudoku_Window will start a gui and through that we will get a small application, where we can play sudoku like normal or load in boards. We can choose which alogirtms to use for the solver, and with the choosen algorithms it will try to solve the given board. We can follow what steps it take and undo or redo it with the corresponding button.

Sudoku_Modell is connencts the window with the board, and the solver.

Sudoku_Board stores the board and the corresponding data, and with getter and setters it reachable.

Sudoku_Solver will manage the all that connect to solving, stores what algorithms can be used, solves the board based on which ones are choosen.
