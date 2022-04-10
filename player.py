from io import BytesIO
from os import listdir, path, scandir
from os.path import isdir
from random import randrange
from time import gmtime, sleep, strftime

import PySimpleGUI as sg
import stagger
from mutagen import File
from mutagen.mp3 import MP3
from PIL import Image
from PIL.Image import open
from pygame import mixer
from pynput.keyboard import Key, Listener

from tela import Tela


class Player:
    def __init__(self):
        mixer.init()
        self.musica_tocando = ""
        self.k = 0
        self.indice_playlist = []
        self.indice_selecionado = 0

        self.mixer = mixer.music
        self.mixer_puro = mixer
        self.mixer.set_volume(0.5)

        self.path_pastas = ""
        self.pastas = ""
        self.pasta_selecionada = ""
        self.lista_musicas = ""

        self.historico_musicas_indice = []
        self.random_hist = []

        self.aleatorio = False
        self.trocou = False
        self.playpause = ""
        self.volume_padrao = 0.5
        self.volume = 0.5

        self.tela = Tela(self)
        #self.tela.tela_principal[1].bind(bind_string, key)

    def mostrar_playlists(self, path):
        self.path_pastas = path

        self.pastas = [[y.split("\\")[1]] for y in [x.path for x in scandir(f"{path}") if isdir(x)]]

        self.tela.tela_principal["playlist"].update(values=self.pastas)

    def selecionar_playlist(self, pasta_selecionada: int):
        excp = 0
        self.pasta_selecionada = f"{self.path_pastas}/{self.pastas[pasta_selecionada[0]][0]}/"
        self.lista_musicas = [[x] for x in listdir(self.pasta_selecionada) if x.split(".")[1] == "mp3"]
        
        self.tela.tabela_musicas = []


        for i in range(len(self.lista_musicas)):

            musica_atual = self.pasta_selecionada + self.lista_musicas[i][0]

            try:
                artista = stagger.read_tag(musica_atual)

            except stagger.errors.NoTagError:
                self.tela.tabela_musicas.append([self.lista_musicas[i][0].split(".mp3")[0]])
                excp = 1

            else:
                if artista.artist != "":
                    self.tela.tabela_musicas.append([artista.artist + " - " + self.lista_musicas[i][0].split(".mp3")[0]])
                else:
                    self.tela.tabela_musicas.append([self.lista_musicas[i][0].split(".mp3")[0]])

        for i in range(len(self.lista_musicas)):
            try:
                self.lista_musicas[i].append(stagger.read_tag(self.pasta_selecionada + self.lista_musicas[i][0]).artist)
            except:
                self.lista_musicas[i].append("")


        if excp == 1:
            self.tela.msg("Existem arquivos nesta pasta que não estão em formato MP3 ou suas tags não estão corretamente configuradas, portanto, eles não serão exibidos.")


        self.tela.tela_principal["musicas"].update(values=self.tela.tabela_musicas)

            


    def tocar_especifica(self, indice=None):
        if indice != None:
            self.indice_selecionado  = self.transformar_indice(indice)

        if self.lista_musicas[self.indice_selecionado][0] != "":
            musica_atual = self.pasta_selecionada + self.lista_musicas[self.indice_selecionado][0]
        
            self.mixer.load(musica_atual)
            self.mixer.play()
            self.musica_tocando = MP3(musica_atual)


            artista = self.lista_musicas[self.indice_selecionado][1]

            self.tela.nome_musica = musica_atual.split("/")[len(musica_atual.split("/"))-1].split(".mp3")[0]
            self.tela.tela_principal["musica"].update(self.tela.nome_musica)
            self.tela.tela_principal["artista"].update(artista)

            self.tela.tela_principal["musicas"].update(select_rows=([self.indice_selecionado]))
            self.img_album()

    def tocar_aleatorio(self):
        indice_selecionado_antigo = self.indice_selecionado

        if len(self.random_hist) == len(self.lista_musicas):
            self.random_hist.clear()
        
        random = randrange(0,len(self.lista_musicas))

        while random in self.random_hist:
            random = randrange(0,len(self.lista_musicas))
    
        self.indice_selecionado = random
        self.random_hist.append(self.indice_selecionado)

        musica_atual = self.pasta_selecionada + self.lista_musicas[self.indice_selecionado][0]
        self.mixer.load(musica_atual)
        self.mixer.play()
        self.musica_tocando = MP3(musica_atual)


        artista = self.lista_musicas[self.indice_selecionado][1]

        self.tela.nome_musica = musica_atual.split("/")[len(musica_atual.split("/"))-1].split(".mp3")[0]

        #self.tela.tela_principal.refresh()

        self.tela.tela_principal["musica"].update(self.tela.nome_musica)
        self.tela.tela_principal["artista"].update(artista)

        self.tela.tela_principal["musicas"].update(select_rows=([self.indice_selecionado]))

        self.historico_musicas_indice.insert(0, indice_selecionado_antigo)
        self.img_album()


    def alt_volume(self, volume: float):
        self.mixer.set_volume(volume)
        self.volume = volume

        if self.volume == 0:
            self.tela.tela_principal["vol"].update(image_filename=f"spotify de pobre/icones/mudo.png", image_subsample=16)
            
        else:
            if self.volume <= 0.3:
                self.tela.tela_principal["vol"].update(image_filename=f"spotify de pobre/icones/baixo.png", image_subsample=16)
            elif self.volume <= 0.7:
                self.tela.tela_principal["vol"].update(image_filename=f"spotify de pobre/icones/medio.png", image_subsample=16)
            elif self.volume <= 1:
                self.tela.tela_principal["vol"].update(image_filename=f"spotify de pobre/icones/alto.png", image_subsample=16)


    def proximo_aleatorio(self):
        self.mixer.unload()
        self.tocar_aleatorio()

    def proximo_normal(self):
        if self.indice_selecionado == len(self.lista_musicas)-1:
            self.indice_selecionado = 0
            self.tocar_especifica()
        else:
            self.mixer.unload()
            self.indice_selecionado += 1
            self.tocar_especifica()


    def anterior_aleatorio(self):

        if len(self.historico_musicas_indice) != 0:
            self.indice_selecionado = self.historico_musicas_indice[0]
            self.historico_musicas_indice.pop(0)

            self.mixer.unload()
            self.tocar_especifica()

        else:
            self.tocar_aleatorio()
            self.historico_musicas_indice = []

    def anterior_normal(self):
        if self.indice_selecionado != 0:
            self.mixer.unload()
            self.indice_selecionado -= 1
            self.tocar_especifica()
        else:
            self.indice_selecionado = len(self.lista_musicas)-1
            self.tocar_especifica()


    def passar_musica_infinito(self):
        adctempo = 0

        while True:
            tempo100 = 100/self.musica_tocando.info.length
            
            if self.mixer.get_busy() == False and self.playpause != "play":
                self.trocou = True

                if self.aleatorio == True: 
                    self.proximo_aleatorio()
                else:
                    self.proximo_normal()
            
            if self.trocou == True:
                adctempo = 0
                self.tela.tela_principal["pb"].update(0)
                self.trocou = False

            if self.mixer.get_busy() != False and self.playpause != "play":
                adctempo += tempo100
                self.tela.tela_principal["pb"].update(adctempo)

            try:
                self.tela.tela_principal["tempo"].update(strftime("%M:%S", gmtime(int(str(self.mixer.get_pos())[:(len(str(self.mixer.get_pos()))-3)]))))
            except:
                self.tela.tela_principal["tempo"].update(strftime("%M:%S", gmtime(0)))
            
            
            sleep(1)


    def transformar_indice(self, indice):
        if indice == [] or indice == None:
            indice = 0
        else:
            indice = indice[0]

        return indice


    def img_album(self):
        try:
            audio = File(self.pasta_selecionada + self.lista_musicas[self.indice_selecionado][0])
            img = Image.open(BytesIO(audio['APIC:e'].data))
            img = img.resize((265,265))
            img.save("spotify de pobre/icones/temp.png", "PNG")
            self.tela.tela_principal["img"].update(source="spotify de pobre/icones/temp.png", subsample=2)
            self.tela.tela_principal["frame_img"].update(visible=True)
        except KeyError:
            self.tela.tela_principal["img"].update(source="spotify de pobre/icones/padrao.png", subsample=2)
            self.tela.tela_principal["frame_img"].update(visible=True)



    def check_botao(self, botao, valores = None):
        #if valores != None:
        self.indice_playlist = valores["playlist"]
        self.aleatorio = valores["aleatorio"]

        if botao == "vol":                                          #mutar (clicar icone som)
            if self.volume != 0:
                self.volume_padrao = self.volume
                self.alt_volume(0)
                self.tela.tela_principal["sl"].update(0)
            else:
                self.alt_volume(self.volume_padrao)
                self.tela.tela_principal["sl"].update(self.volume*10)
        

        elif botao == 1 and self.indice_playlist != []:                # play \ pausar
            if self.playpause == "play":
                self.playpause = "pause"
                if valores["aleatorio"] == True and self.mixer.get_busy() == False:           #aleatorio
                    if valores["musicas"] == []:
                        self.tocar_aleatorio()
                    elif valores["musicas"] != []:
                        self.mixer.unpause()

                elif valores["aleatorio"] == False and self.mixer.get_busy() == False:        #normal
                    if self.k == 0:                            #enquanto nao der play na musica seta o valor para 0, evita erros com o indice selecionado
                        valores["musicas"] = [0]          #e toca a primeira
                        self.tocar_especifica()   
                    else:
                        self.mixer.unpause()

            else:
                self.playpause = "play"
                self.mixer.pause()
        

        elif botao == 0 and self.indice_playlist != []:                 #anterior
            self.trocou = True

            if self.playpause == "play":                     #muda botao se estiver pausado
                self.playpause = "pause"

            if self.k == 0:                              #enquanto nao der play na musica seta o valor para 0, evita erros com o indice selecionado
                valores["musicas"] = [0]

            if valores["aleatorio"] == True:                    #aleatorio
                self.anterior_aleatorio()

            elif valores["aleatorio"] == False:                 #normal
                self.anterior_normal()


        elif botao == 2 and self.indice_playlist != []:                  #proximo
            
            self.trocou = True

            if self.playpause == "play":
                self.playpause = "pause"

            if valores["aleatorio"] == True:                        #aleatorio
                self.proximo_aleatorio()

            elif valores["aleatorio"] == False and self.k == 0:      #normal 1º
                valores["musicas"] = [0]
                self.indice_selecionado = -1
                self.proximo_normal()

            elif valores["aleatorio"] == False:                     #normal
                self.proximo_normal()


        if botao == "browse":                                       #abrir pasta com as playlists(mostra playlists na esquerda)
            if valores["browse"] != "":
                self.mostrar_playlists(valores["browse"])

        if botao == "playlist" and self.indice_playlist != []:       #selecionou uma playlist, mostra na direita
            self.selecionar_playlist(self.indice_playlist)

        if botao == "musicas" and valores["musicas"] != []:         #play na coluna selecionada
            self.trocou = True
            if self.playpause == "play" or self.playpause == "pause":
                self.playpause = "pause"
                self.tocar_especifica(valores["musicas"])
         

        #update na imagem do botao play/pause se ele mudar        
        self.tela.tela_principal[1].update(image_filename=f"spotify de pobre/icones/{self.playpause}.png", image_subsample=40, image_size=(30,30), button_color=(sg.theme_background_color(), sg.theme_background_color()))


    def listen_botoes_media(self):
        def on_press(key):
            valores = {'playlist': self.indice_playlist, 'musicas': self.indice_selecionado, 'aleatorio': self.aleatorio, 'browse': '', 'sl': self.volume*10}

            if key == Key.media_play_pause:
                self.check_botao(1, valores)

            elif key == Key.media_next:
                self.check_botao(2, valores)

            elif key == Key.media_previous:
                self.check_botao(0, valores)



        botoes_media = Listener(on_press=on_press, onrelease=None)
        botoes_media.start()
