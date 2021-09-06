import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import SELECT_MODE_SINGLE
from Sudoku_Modell import *

def set_history(window, model):
    his = model.get_board().get_history()
    his_len = model.get_board().get_current_his_pos()
    window['history'].update(his, set_to_index=[his_len])

def update_board(window, model):
    for row in range(9):
        for col in range(9):
            if model.get_board().get_board()[row, col] != 0:
                window[(row, col)].update(model.get_board().get_board()[row, col])
            else: window[(row, col)].update('')

def get_layout(model):
    p_name = model.get_solver().get_patterns_name()
    pattern_checkbox_list = [[sg.Text('Használni kivánt minták:')]] +\
            [[sg.Checkbox('{}'.format(p_name[i]), default=True, k=i+10)]
            for i in range(len(p_name))]

    sudoku_input_grid = [[sg.Button(
                            size=(2,1), 
                            pad=((0,int(col%3==2)*3),(0,int(row%3==2)*3)),
                            k=(row,col),
                            disabled=False,
                            enable_events=True)                        
                for col in range(9)] 
                    for row in range(9)] +\
        [[sg.Button(i+1, k=i+1) for i in range(9)]] +\
        [[
        sg.Button('Clear', k='clear'),
        #sg.Button('Lock', k='lock'),
        #sg.Button('Unlock', k='unlock'),
        sg.Button('Solve', k='solve')
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
            sg.Listbox(values=[], enable_events=True, size =(31,15), k='sudoku_list', select_mode=SELECT_MODE_SINGLE, )
        ]]

    history_column = [
        [
            sg.Text('Eddigi lépések')
        ],
        [
            sg.Listbox(values=[], enable_events=False, size=(15,15), k='history', select_mode=SELECT_MODE_SINGLE)
        ],
        [
            sg.Button('Visszalép', k='back'),
            sg.Button('Előrelép', k='forward')
        ]]

    layout = [[
        sg.Column(pattern_checkbox_list),
        sg.VSeperator(k='vs1'),
        sg.Column(sudoku_input_grid, element_justification='center'),
        sg.VSeperator(k='vs2'),
        sg.Column(file_load_and_choose_list),
        sg.VSeperator(k='vs3'),
        sg.Column(history_column)
        ]]

    return layout

model = Sudoku_Modell()
window = sg.Window("Sudoku megoldó", get_layout(model))

active_sudoku_sqare = None
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if isinstance(event, tuple):
        if active_sudoku_sqare is not None:
            window[active_sudoku_sqare].update(button_color='#283b5b')
        active_sudoku_sqare = event
        window[event].update(button_color='grey')
    elif isinstance(event, int):
        if  1 <= event <= 9 and active_sudoku_sqare is not None:
            model.get_board().insert_to_board(event, active_sudoku_sqare)
            window[active_sudoku_sqare].update(event)
            set_history(window, model)
    elif isinstance(event, str):
        if active_sudoku_sqare is not None and event == 'clear':
            window[active_sudoku_sqare].update(button_color='#283b5b')
            active_sudoku_sqare = None
        if event == 'clear':
            [[window[(row, col)].update('', disabled=False) for row in range(9)] for col in range(9)]
            model.clear()
            window['history'].update([])
        if event == 'solve':
            model.get_solver().set_patterns([values[key] for key in values.keys() if isinstance(key, int)])
            model.solve()
            [[window[(row, col)].update(model.get_board().get_board()[row, col]) for row in range(9) if model.get_board().get_board()[row, col] != 0] for col in range(9)]
            set_history(window, model)
        if event == 'folder':
            if not model.load_file(values['folder']): sg.popup('Nem lehet betölteni a fájl!', title='Hiba!')
            else:
                window['sudoku_list'].update(list(model.get_board_keys()))
        if event == 'sudoku_list':
            if values['sudoku_list']:
                model.load_board(values['sudoku_list'][0])
                [[window[(row, col)].update('', disabled=False) for row in range(9)] for col in range(9)]
                locked_fields = model.get_board_locked(values['sudoku_list'][0])
                for row in range(9):
                    for col in range(9):
                        if model.get_board().get_board()[row, col] != 0:
                            window[(row, col)].update(model.get_board().get_board()[row, col])
                        if (row, col) in locked_fields:
                            window[(row, col)].update(disabled=True)
                set_history(window, model)
        if event == 'back':
            model.get_board().step_back_history()
            print(model.get_board().get_board())
            update_board(window, model)
            set_history(window, model)
        if event == 'forward':
            model.get_board().step_forward_history()
            [[window[(row, col)].update(model.get_board().get_board()[row, col]) for row in range(9) if model.get_board().get_board()[row, col] != 0] for col in range(9)]
            set_history(window, model)


    print(event)
    print(values)
    #print(' ')
    #print(window.key_dict)