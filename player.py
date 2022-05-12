import pickle
from io import BytesIO
from os import listdir, path, scandir, stat
from os.path import isdir
from random import randrange
from time import gmtime, sleep, strftime, time_ns

import PySimpleGUI as sg
from mutagen import File
from mutagen.mp3 import MP3
from PIL import Image
from pygame import mixer
from pynput.keyboard import Key, Listener

from tela import Tela


class Player:
    def __init__(self):
        mixer.init() 
        
        self.musica_tocando = ""
        self.k = 0                      # 0 = primeira run do codigo
        self.i = 0
        self.cache = {}

        self.mixer = mixer.music
        self.mixer_puro = mixer
        self.mixer.set_volume(0.5)

        self.path_pastas = ""           # path pastas (playlists)
        self.pastas = ""                # nome pastas (playlists) - formatado para tela
        self.pasta_selecionada = ""     # path da playlist selecionada

        self.lista_musicas = []         # lista nome musicas da playlist selecionada
        self.indice_playlist = []       # indice da playlist selecionada
        self.indice_selecionado = 0     # indice musica selecionada

        self.path_dados = ""
        self.path_icones = ""

        self.historico_musicas_indice = []  # historico para voltar musicas
        self.random_hist = []               # historico para ao avançar musicas no aleatorio n repetir alguma passada

        self.aleatorio = False
        self.trocou = False
        self.playpause = ""
        self.volume_padrao = 0.5
        self.volume_atual = 0.5

        self.tela = Tela()


    def carregar_sessao(self):                       # carrega playlists da sessao passada
        try:   
            self.path_pastas = pickle.load(open(f"{self.path_dados}/pasta", "rb"))
            self.mostrar_playlists()
        except:
            pass


    def mostrar_playlists(self, path = None):       # mostra playlist do browse ou historico, alem de formatar para mostrar na tela
        if path != None:
            self.path_pastas = path
            pickle.dump(self.path_pastas, open(f"{self.path_dados}/pasta", "wb"))

        self.pastas = [[y.split("\\")[1]] for y in [x.path for x in scandir(f"{self.path_pastas}") if isdir(x)]]
        self.tela.tela_principal["playlist"].update(values=self.pastas)

    def selecionar_playlist(self, pasta_selecionada: int):      # formata as musicas da playlist selecionada e mostra na tela
        excp = 0
        self.pasta_selecionada = f"{self.path_pastas}/{self.pastas[pasta_selecionada[0]][0]}/"

        if self.pastas[pasta_selecionada[0]][0] in self.cache:
            self.lista_musicas =  self.cache[self.pastas[pasta_selecionada[0]][0]][0]
            self.tela.tabela_musicas = self.cache[self.pastas[pasta_selecionada[0]][0]][1]

            self.tela.tela_principal["musicas"].update(values=self.tela.tabela_musicas)
            
        else:
            self.lista_musicas = []
            tempo1 = time_ns()
            try:
                for x in listdir(self.pasta_selecionada):
                    try:
                        x2 = x.split(".")
                        if not isdir(x) and x2[len(x2)-1] == "mp3":           #! mudar dps para poder selecionar dir
                            self.lista_musicas.append([x])
                        else:
                            raise Exception
                    except:
                        pass
                    else:
                        musica_atual = self.pasta_selecionada + x

                        try:
                            artista = str(File(musica_atual)["TPE1"])

                        except:
                            self.lista_musicas[-1].append("")

                        else:

                            self.lista_musicas[-1].append(str(File(self.pasta_selecionada + x)["TPE1"]))
            except PermissionError:
                pass

            self.tela.tabela_musicas = []

            # organizar por data de criação
            self.lista_musicas.sort(key=lambda x: stat(f"{self.pasta_selecionada}/{x[0]}").st_ctime, reverse=True)

            for i in range(len(self.lista_musicas)):
                if self.lista_musicas[i][1] == "":
                    self.tela.tabela_musicas.append([self.lista_musicas[i][0].split(".mp3")[0]])
                else:
                    self.tela.tabela_musicas.append([self.lista_musicas[i][1] + " - " + self.lista_musicas[i][0].split(".mp3")[0]])


            self.tela.tela_principal["musicas"].update(values=self.tela.tabela_musicas)

            self.cache[self.pastas[pasta_selecionada[0]][0]] = [self.lista_musicas, self.tela.tabela_musicas]


    def tocar_especifica(self, indice=None):
        if indice != None:
            self.indice_selecionado  = 0 if (indice == [] or indice == None) else indice

        if self.lista_musicas[self.indice_selecionado][0] != "":
            musica_atual = self.pasta_selecionada + self.lista_musicas[self.indice_selecionado][0]
            try:
                self.mixer.load(musica_atual)
                self.mixer.play()
                self.musica_tocando = MP3(musica_atual)

                artista = self.lista_musicas[self.indice_selecionado][1]

                self.tela.nome_musica = musica_atual.split("/")[len(musica_atual.split("/"))-1].split(".mp3")[0]
                self.tela.tela_principal["musica"].update(self.tela.nome_musica)
                self.tela.tela_principal["artista"].update(artista)

                self.tela.tela_principal["musicas"].update(select_rows=([self.indice_selecionado]))
                self.img_album()
            except:
                pass

    def tocar_aleatorio(self):
        random = randrange(0,len(self.lista_musicas))

        indice_selecionado_antigo = self.indice_selecionado

        if len(self.random_hist) == len(self.lista_musicas):        
            self.random_hist.clear()

        while random in self.random_hist:                           # se o novo indice ja tiver sido tocado tenta dnv
            random = randrange(0,len(self.lista_musicas))
    
        self.indice_selecionado = random
        self.random_hist.append(self.indice_selecionado)

        musica_atual = self.pasta_selecionada + self.lista_musicas[self.indice_selecionado][0]
        self.mixer.load(musica_atual)
        self.mixer.play()
        self.musica_tocando = MP3(musica_atual)

        artista = self.lista_musicas[self.indice_selecionado][1]

        self.tela.nome_musica = musica_atual.split("/")[len(musica_atual.split("/"))-1].split(".mp3")[0]

        self.tela.tela_principal["musica"].update(self.tela.nome_musica)
        self.tela.tela_principal["artista"].update(artista)

        self.tela.tela_principal["musicas"].update(select_rows=([self.indice_selecionado]))

        self.historico_musicas_indice.append(indice_selecionado_antigo)
        self.img_album()


    def alt_volume(self, volume: float):
        self.mixer.set_volume(volume)
        self.volume_atual = volume

        if self.volume_atual == 0:
            self.tela.tela_principal["vol"].update(image_filename=f"{self.path_icones}/mudo.png", image_subsample=16)
            
        else:
            if self.volume_atual <= 0.3:
                self.tela.tela_principal["vol"].update(image_filename=f"{self.path_icones}/baixo.png", image_subsample=16)
            elif self.volume_atual <= 0.7:
                self.tela.tela_principal["vol"].update(image_filename=f"{self.path_icones}/medio.png", image_subsample=16)
            elif self.volume_atual <= 1:
                self.tela.tela_principal["vol"].update(image_filename=f"{self.path_icones}/alto.png", image_subsample=16)


    def proximo_aleatorio(self):
        self.mixer.unload()
        self.tocar_aleatorio()


    def proximo_normal(self):
        if self.indice_selecionado == len(self.lista_musicas) - 1:
            self.indice_selecionado = 0
            self.tocar_especifica()
        else:
            self.mixer.unload()
            self.indice_selecionado += 1
            self.tocar_especifica()


    def anterior_aleatorio(self):
        if len(self.historico_musicas_indice) != 0:
            self.indice_selecionado = self.historico_musicas_indice[-1]
            self.historico_musicas_indice.pop(-1)

            self.mixer.unload()
            self.tocar_especifica()

        else:
            self.tocar_aleatorio()

    def anterior_normal(self):
        if self.indice_selecionado != 0:
            self.mixer.unload()
            self.indice_selecionado -= 1
            self.tocar_especifica()
        else:
            self.indice_selecionado = len(self.lista_musicas)-1
            self.tocar_especifica()


    def passar_musica_infinito(self):           # thread: ao acabar musica, toca a proxima
        adctempo = 0
        while True:
            tempo100 = 100/self.musica_tocando.info.length
            
            if self.mixer.get_busy() == False and self.playpause != "play":
                self.trocou = True
                self.proximo_aleatorio() if self.aleatorio == True else self.proximo_normal()
            
            if self.trocou == True:
                adctempo = 0
                self.tela.tela_principal["pb"].update(0)
                self.trocou = False

            if self.mixer.get_busy() != False and self.playpause != "play":
                adctempo += tempo100
                self.tela.tela_principal["pb"].update(adctempo)

            try:
                self.tela.tela_principal["tempo"].update(strftime("%M:%S", gmtime(int(str(self.mixer.get_pos())[:(len(str(self.mixer.get_pos()))-3)]))))
            except RuntimeError:
                sleep(2)
                self.tela.tela_principal["tempo"].update(strftime("%M:%S", gmtime(int(str(self.mixer.get_pos())[:(len(str(self.mixer.get_pos()))-3)]))))
            except:
                self.tela.tela_principal["tempo"].update(strftime("%M:%S", gmtime(0)))
            
            sleep(1)


    def img_album(self):                # muda tamanho img do album e salva como imagem para ser carregada pela tela
        try:
            audio = File(self.pasta_selecionada + self.lista_musicas[self.indice_selecionado][0])
            img = Image.open(BytesIO(audio['APIC:e'].data))
            img = img.resize((290,290))
            img.save(f"{self.path_icones}/temp.png", "PNG")
            self.tela.tela_principal["img"].update(source=f"{self.path_icones}/temp.png", subsample=2)
            self.tela.tela_principal["frame_img"].update(visible=True)
        except KeyError:
            img = Image.open(f"{self.path_icones}/padrao.png")
            img = img.resize((290,290))
            img.save(f"{self.path_icones}/padrao.png", "PNG")
            self.tela.tela_principal["img"].update(source=f"{self.path_icones}/padrao.png", subsample=2)
            self.tela.tela_principal["frame_img"].update(visible=True)


    def check_botao(self, botao, valores = None):
        self.indice_playlist = valores["playlist"]
        self.aleatorio = valores["aleatorio"]


        if botao == "vol":                                          # mutar (clicar icone som)
            if self.volume_atual != 0:
                self.volume_padrao = self.volume_atual
                self.alt_volume(0)
                self.tela.tela_principal["sl"].update(0)
            else:
                self.alt_volume(self.volume_padrao)
                self.tela.tela_principal["sl"].update(self.volume_atual*10)
        

        elif botao == 1 and self.indice_playlist != []:                # play \ pausar
            if self.playpause == "play":
                self.playpause = "pause"
                if valores["aleatorio"] == True:           # aleatorio
                    if self.k == 0:
                        self.tocar_aleatorio()
                    elif valores["musicas"] != []:
                        self.mixer.unpause()

                elif valores["aleatorio"] == False:        # normal
                    if self.k == 0:                            # enquanto nao der play na musica seta o valor para 0, evita erros com o indice selecionado
                        valores["musicas"] = [0]               # e toca a primeira
                        self.tocar_especifica()   
                    else:
                        self.mixer.unpause()

            else:
                self.playpause = "play"
                self.mixer.pause()
        

        elif botao == 0 and self.indice_playlist != []:     # anterior
            self.trocou = True

            if self.playpause == "play":                    # muda botao se estiver pausado
                self.playpause = "pause"

            if self.k == 0:                                 # enquanto nao der play na musica seta o valor para 0, evita erros com o indice selecionado
                valores["musicas"] = [0]

            if valores["aleatorio"] == True:                # aleatorio
                self.anterior_aleatorio()

            elif valores["aleatorio"] == False:             # normal
                self.anterior_normal()


        elif botao == 2 and self.indice_playlist != []:     # proximo
            
            self.trocou = True

            if self.playpause == "play":
                self.playpause = "pause"

            if valores["aleatorio"] == True:                         # aleatorio
                self.proximo_aleatorio()

            elif valores["aleatorio"] == False and self.k == 0:      # normal 1º
                valores["musicas"] = [0]
                self.indice_selecionado = -1
                self.proximo_normal()

            elif valores["aleatorio"] == False:                      # normal
                self.proximo_normal()

        if botao == "update" and self.indice_playlist != []:
            del self.cache[self.pastas[self.indice_playlist[0]][0]]
            self.selecionar_playlist(self.indice_playlist)

        if botao == "browse":                                        # abrir pasta com as playlists(mostra playlists na esquerda)
            if valores["browse"] != "":
                self.mostrar_playlists(valores["browse"])


        if botao == "playlist" and self.indice_playlist != []:       # selecionou uma playlist, mostra na direita
            self.selecionar_playlist(self.indice_playlist)


        if botao == "musicas" and valores["musicas"] != []:          # play na coluna selecionada
            self.random_hist.clear()
            self.historico_musicas_indice.clear()

            self.trocou = True
            if self.playpause == "play" or self.playpause == "pause":
                self.playpause = "pause"
                self.tocar_especifica(valores["musicas"][0])
         

        # update na imagem do botao play/pause se ele mudar        
        self.tela.tela_principal[1].update(image_filename=f"{self.path_icones}/{self.playpause}.png", image_subsample=40, image_size=(30,30), button_color=(sg.theme_background_color(), sg.theme_background_color()))


    def listen_botoes_midia(self):      #listener botoes de midia
        def on_press(key):
            valores = {'playlist': self.indice_playlist, 'musicas': self.indice_selecionado, 'aleatorio': self.aleatorio, 'browse': '', 'sl': self.volume_atual*10}

            if key == Key.media_play_pause:
                self.check_botao(1, valores)

            elif key == Key.media_next:
                self.check_botao(2, valores)

            elif key == Key.media_previous:
                self.check_botao(0, valores)


        botoes_media = Listener(on_press=on_press, onrelease=None)
        botoes_media.start()
