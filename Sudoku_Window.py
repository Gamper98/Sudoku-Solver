import PySimpleGUI as sg
from Sudoku_Modell import *

class Sudoku_Window():
    def __init__(self):
        self.__active_sq = None
        self.__model = Sudoku_Modell()
        self.__window = sg.Window("Sudoku megoldó", self.__get_layout(), return_keyboard_events=True).Finalize()
        self.__containing_sqs = []
        self.__designs = {
            'inactive_color' : '#283b5b',
            'active_color' : '#ABABAB',
            'containing_sqs' : '#7E6E5A',
        }

    def __get_layout(self):
        p_name = self.__model.get_pattern_names()
        pattern_checkbox_list = [[sg.Text('Használni kivánt minták:')]] +\
                [[sg.Checkbox('{}'.format(p_name[i]), default=False, k=i+100)]
                for i in range(len(p_name))]

        sudoku_input_grid = [[sg.Graph(
                                (36,36),
                                (0,0),
                                (36,36),
                                pad=(((1,int(col%3==2)*3+1),(1,int(row%3==2)*3+1))),
                                background_color='#283b5b',
                                k=(row,col),
                                enable_events=True)                        
                    for col in range(9)] 
                        for row in range(9)] +\
            [[
            sg.Button('Clear', k='clear'),
            sg.Button('Solve', k='solve'),
            sg.Button('Fill pencil marks', k='pen_marks')
            ]]

        file_load_and_choose_list = [
            [
                sg.Text('Sudoku fájl betöltés')
            ],
            [
                sg.In(size=(25, 1), k='folder', readonly=True, disabled=True, enable_events=True),
                sg.FilesBrowse(file_types=(('Json Files', '*.json'),('All Files', '*.*'),))
            ],
            [
                sg.Listbox(values=[], enable_events=True, size =(31,15), k='sudoku_list', select_mode=sg.SELECT_MODE_SINGLE)
            ]]

        history_column = [
            [
                sg.Text('Eddigi lépések')
            ],
            [
                sg.Listbox(values=[], enable_events=False, size=(15,15), k='history', select_mode=sg.SELECT_MODE_SINGLE)
            ],
            [
                sg.Button('Visszalép', k='back'),
                sg.Button('Előrelép', k='forward')
            ]]

        layout = [[
            sg.Column(pattern_checkbox_list),
            sg.VSeperator(k='s1'),
            sg.Column(sudoku_input_grid, element_justification='center'),
            sg.VSeperator(k='s2'),
            sg.Column(file_load_and_choose_list),
            sg.VSeperator(k='s3'),
            sg.Column(history_column)
            ]]

        return layout

    def __set_active_sq(self, event):
        if self.__active_sq is not None:
            self.__window[self.__active_sq].update(self.__designs['inactive_color'])
            for pos in self.__containing_sqs:
                self.__window[tuple(pos)].update(self.__designs['inactive_color'])
            self.__containing_sqs = []
        self.__window[event].update(self.__designs['active_color'])
        self.__active_sq = event

        num = self.__model.get_board_at(event)
        if num == 0:
            return
        sqrs = np.argwhere(self.__model.get_board() == num)
        pv_sqrs = np.argwhere(self.__model.get_pv_at(num-1))
        self.__containing_sqs = np.concatenate((sqrs, pv_sqrs))
        for pos in self.__containing_sqs:
            if tuple(pos) == self.__active_sq: continue
            self.__window[tuple(pos)].update(self.__designs['containing_sqs'])

    def __set_board_at(self, num, pos):
        self.__window[pos].erase()
        self.__window[pos].draw_text(num ,location=(18,18), font=('',15))

    def __set_pv_at(self, nums, pos):
        self.__window[pos].erase()
        for num in nums:
            self.__window[pos].draw_text(num, location=(9 * ((num-1)%3+1),36- 9 * ((num-1)//3+1)), font=('',8))

    def __set_number(self, num, pos):
        self.__set_board_at(num, pos)
        self.__model.set_board_at(num, pos)

    def __clear_board(self):
        self.__model.clear()
        self.__active_sq = None
        for row in range(9):
            for col in range(9):
                self.__window[(row,col)].erase()
                self.__window[(row,col)].update(self.__designs['inactive_color'])
        self.__window['history'].update([])
    
    def __solve_board(self, values):
        checkbox_values = [values[key] for key in values.keys() if isinstance(key, int)]
        self.__model.set_pattern_names(checkbox_values)
        his_pos = self.__model.get_his_pos()
        self.__model.solve()
        for row in range(9):
            for col in range(9):
                num = self.__model.get_board_at((row, col))
                if num:
                    self.__set_board_at(num, (row, col))
        self.__set_history()
    
    def __fill_possible_values(self):
        for row in range(9):
            for col in range(9):
                if self.__model.get_board_at((row, col)) == 0:
                    self.__set_pv_at(np.argwhere(self.__model.get_pv_at(([0,1,2,3,4,5,6,7,8],row,col))).flatten()+1,(row, col))

    def __get_file(self, path):
        if not self.__model.load_file(path): sg.popup('Nem lehet betölteni a fájl!', title='Hiba!')
        else:
            self.__window['sudoku_list'].update(list(self.__model.get_keys()))

    def __open_sudoku(self, selected_board):
        self.__clear_board()
        self.__model.load_board(selected_board)
        for row in range(9):
            for col in range(9):
                if self.__model.get_board_at((row, col)) != 0:
                    self.__set_board_at(self.__model.get_board_at((row, col)), (row, col))
        self.__model.setup_possible_values()
        self.__set_history()

    def __set_history(self):
        his = self.__model.get_history()
        his_len = self.__model.get_his_pos()
        self.__window['history'].update(his, set_to_index=[his_len])

    def __back(self):
        pass

    def __forward(self):
        self.__model.step_forward_history()
        x,y, num = self.__model.get_history()[self.__model.get_his_pos()]
        self.__set_board_at(num, (x,y))
        self.__set_history()


    def main(self):
        while True:
            event, values = self.__window.read()
            if event in ('Exit', sg.WIN_CLOSED):
                break
            elif isinstance(event, tuple):
                self.__set_active_sq(event)
            elif isinstance(event, str):
                if  event in ('1','2','3','4','5','6','7','8','9') and self.__active_sq is not None:
                    self.__set_number(int(event), self.__active_sq)
                    self.__set_history()
                elif event == 'clear':
                    self.__clear_board()
                elif event == 'solve':
                    self.__solve_board(values)
                elif event == 'pen_marks':
                    self.__fill_possible_values()
                elif event == 'folder':
                    self.__get_file(values['folder'])
                elif event == 'sudoku_list':
                    self.__open_sudoku(values['sudoku_list'][0])
                elif event == 'back':
                    self.__back()
                elif event == 'forward':
                    self.__forward()
            
            #print(values)


if __name__ == '__main__':
    window = Sudoku_Window()
    window.main()