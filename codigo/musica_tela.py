import PySimpleGUI as sg



class Tela:
    def __init__(self):
        self.tela_principal = None
        self.tela_player = None
        self.path_icones = r"C:/Users/rasen/Desktop/scripts/projeto musica player/icones"

    def init_tela_principal(self):
        layout = [
            
            [sg.Button("Play", key=1, size=(10,5)), sg.Button("Play", key=1, size=(10,5)), sg.Checkbox('My first Checkbox!', default=True)],
            


        ]



        self.tela_principal = sg.Window("Tela Principal", default_element_size=(50,50)).Layout(layout)

        return self.tela_principal.Read()
