import PySimpleGUI as sg

layout = [[sg.Text('What is your name')],
            [sg.InputText()],
            [sg.Button('Ok')]]

window = sg.Window('Test Title').Layout(layout)

button, values = window.Read()

sg.Popup('Hello {} welcome to PySimpleGUI'.format(values[0]))
