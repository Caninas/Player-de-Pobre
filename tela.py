import PySimpleGUI as sg


class Tela:
    def __init__(self, controlador):
        self.controlador = controlador
        self.tela_principal = None
        self.path_icones = ""
        self.tabela_musicas = []
        self.nome_musica = ""                   #no momento sem utilidade
        self.icone = ""

    def init_tela_principal(self):
        # sg.ChangeLookAndFeel("black")
        sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {'BACKGROUND': '#4f4a4a',
                                                    'TEXT': '#FFFFFF',
                                                    'INPUT': '#5777f7',
                                                    'TEXT_INPUT': '#000000',
                                                    'SCROLL': '#CCCCCC',
                                                    'BUTTON': ('#000000', '#5777f7'),
                                                    'PROGRESS': ('#5777f7', '#CCCCCC'),
                                                    'BORDER': 1, 'SLIDER_DEPTH': 0,
                                                    'PROGRESS_DEPTH': 0, }
        sg.theme('MyCreatedTheme')


        col_esquerda = [
            [
                sg.Table(values="",  key="playlist",
                         num_rows=15,
                         headings=[" Playlist "],
                         justification="left",
                         enable_click_events=True,
                         bind_return_key=True,
                         max_col_width=15,
                         pad=((0, 0), (0, 0)))
            ],

            [
                sg.Frame("",
                         [[sg.Image(key="img", source="", subsample=2)]], pad=((3, 0), (3, 3)), visible=False, key="frame_img", border_width=2
                         )
            ]
        ]


        col_direita = [
            [
                sg.Table(values=self.tabela_musicas, key="musicas",
                         num_rows=15,
                         display_row_numbers=True,
                         headings=[                        
                             "Música"],
                         justification="left",
                         auto_size_columns=False,
                         def_col_width=83,  
                         enable_click_events=False,
                         bind_return_key=True,)
                         #pad=((0, 0), (0, 0)))
            ],

            [
                sg.Column
                (
                    [
                        [
                            sg.Text("Nada Tocando", key="musica",
                                    font=4, pad=((0, 0), (15, 0)))
                        ],


                        [
                            sg.Text("", key="artista", pad=((0, 0), (0, 5)))
                        ],


                        [
                            sg.ProgressBar(100, key="pb", size=(35, 10))
                        ],

                        [
                            sg.Frame("", 
                                [
                                    [
                                        sg.Text("00:00", key="tempo",
                                                pad=((0, 0), (0, 0))),
                                        sg.Button(key=0, image_filename=f"{self.path_icones}/anterior.png", image_subsample=40, image_size=(30, 30),
                                                button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, pad=((80, 7), (7, 7))),
                                        sg.Button(key=1, image_filename=f"{self.path_icones}/play.png", image_subsample=40, image_size=(30, 30),
                                                button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, pad=((7, 7), (7, 7))),
                                        sg.Button(key=2, image_filename=f"{self.path_icones}/proximo.png", image_subsample=40, image_size=(30, 30),
                                                button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, pad=((7, 7), (7, 7))),
                                        sg.Checkbox("Aleatório", key="aleatorio", default=False, checkbox_color="#5777f7",
                                                    enable_events=True, pad=((30, 0), (0, 0)))
                                        
                                    ]
                                ], border_width=0),
                        ]

                    ], pad=((125, 0), (0, 0)), element_justification="c"
                ),


                sg.Column
                (
                    [
                        [
                            sg.FolderBrowse(button_text="Pasta", key="browse", auto_size_button=True,
                                            enable_events=True, pad=((10, 0), (10, 30)))
                        ],


                        [
                            sg.Frame
                            ("",
                                [[
                                    sg.Button(key="vol", image_filename=f"{self.path_icones}/medio.png", image_subsample=16, button_color=(
                                        sg.theme_background_color(), sg.theme_background_color()), border_width=0),

                                    sg.Slider(key="sl", range=(0, 10), default_value=5, disable_number_display=True, size=(
                                        15, 13), orientation='horizontal', enable_events=True, border_width=0, resolution=0.5, pad=((5, 0), (0, 0)))
                                ]],

                                pad=((125, 0), (0, 55)), border_width=0
                            )
                        ]

                    ], element_justification="right"
                )
            ]
        ]

        layout = [
            [
                sg.Column
                (
                    col_esquerda, vertical_alignment="top"
                ),


                sg.Column
                (
                    col_direita, vertical_alignment="top"
                )
            ]
        ]



        self.tela_principal = sg.Window("Player de Pobre", element_padding=(
            0, 0), resizable=False, element_justification='c', margins=(0,0), icon=f"{self.path_icones}/icone.ico").Layout(layout)
        self.tela_principal.finalize()


    def abrir(self):
        return self.tela_principal.Read()

    def msg(self, msg):
        sg.Popup(msg,)

    def msg_baixando(self):
        sg.Popup("CARREGANDO", auto_close=True, non_blocking=True)
