import PySimpleGUI as sg

layout = [[sg.Text('Source')],
          [sg.InputText(), sg.FolderBrowse()],
          [sg.Text('Destination')],
          [sg.InputText(), sg.FolderBrowse()],
          [sg.Text('Delete', size=(20, 1)), sg.Text('Copy')],
          [sg.Checkbox('Files', size=(17, 1)), sg.Checkbox('If New')],
          [sg.Checkbox('Folders')],
          [sg.Text('Scheduling')],
          [sg.Radio('Run Once', 'loss', size=(17, 1)), sg.Radio('Daily', 'loss'), sg.InputText(size=(12, 1))],
          [sg.Radio('Hourly', 'loss', size=(17, 1)), sg.Radio('Interval', 'loss'), sg.InputText(size=(10, 1))],
          [sg.Submit()]]

window = sg.Window('Pivot Backup').Layout(layout)

button, values = window.Read()
