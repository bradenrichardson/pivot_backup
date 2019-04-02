import PySimpleGUI as sg

sg.ChangeLookAndFeel('Dark')

layout = [[sg.Text('Source')],
          [sg.InputText(background_color='Light Grey', text_color='Black'), sg.FolderBrowse(button_color=('Black', 'Grey'))],
          [sg.Text('Destination')],
          [sg.InputText(background_color='Light Grey', text_color='Black'), sg.FolderBrowse(button_color=('Black', 'Grey'))],
          [sg.Text('Delete', size=(20, 1)), sg.Text('Copy')],
          [sg.Checkbox('Files', size=(17, 1)), sg.Checkbox('If New')],
          [sg.Checkbox('Folders')],
          [sg.Text('Scheduling')],
          [sg.Radio('Run Once', 'loss', size=(17, 1)),
           sg.Radio('Daily', 'loss', size=(5, 1)),
           sg.InputText(background_color='Light Grey', text_color='Black', size=(10, 1))],
          [sg.Radio('Hourly', 'loss', size=(17, 1)), sg.Radio('Interval', 'loss'),
           sg.InputText(background_color='Light Grey', text_color='Black', size=(10, 1))],
          [sg.Text('Reporting', justification='centre')],
          [sg.Checkbox('Console', size=(17, 1)), sg.Checkbox('Text')],
          [sg.Checkbox('Email'), sg.InputText(background_color='Light Grey', text_color='Black', size=(36, 1))],
          [sg.Submit(button_text='Run Backup', button_color=('Green', 'White'))]]


window = sg.Window('Pivot Backup', default_element_size=(40, 1)).Layout(layout)

button, values = window.Read()

print(button, values)
