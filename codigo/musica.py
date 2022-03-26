from pygame import mixer
import os
import time
import random
import stagger
from musica_tela import Tela


class Player:
    def __init__(self):
        mixer.init()
        self.musica_tocando = ""
        self.mixer = mixer.music
        self.mixer.set_volume(0.05)
        self.path_musicas = os.listdir(fr"C:/Users/rasen/Documents/TunesKit Spotify Converter/Converted/Tranquilão_ROCK/")
        self.path_atual = ""
        self.tela = Tela()

    def tocar_especifica(self, musica_selecionada: musica.mp3):
        musica_atual = f"C:/Users/rasen/Documents/TunesKit Spotify Converter/Converted/Tranquilão_ROCK/{musica_selecionada}"
        self.mixer.load(musica_atual)
        self.mixer.play()
        artista = stagger.read_tag(musica_atual)
        print(f"Tocando:",  artista.artist, "-", musica_atual.split("/")[7].split(".mp3")[0])

    def tocar_aleatorio(self, musica_selecionada: musica.mp3):
        musica_atual = f"C:/Users/rasen/Documents/TunesKit Spotify Converter/Converted/Tranquilão_ROCK/{self.path_musicas[random.randrange(0,len(self.path_musicas))]}"
        self.mixer.load(musica_atual)
        self.mixer.play()


        artista = stagger.read_tag(musica_atual)
        print(f"Tocando:",  artista.artist, "-", musica_atual.split("/")[7].split(".mp3")[0])


    def volume(self, volume: int):
        self.mixer.set_volume(volume)


    def skip(self):
        self.mixer.unload()
        self.tocar_aleatorio()

    def iniciar(self):
        self.tocar_aleatorio()

    def parar(self):
        exit(0)


player = Player()

while True:
    menu = {0: player.parar, 1:  player.iniciar, 2: player.skip}

    botao, valor = self.tela.init_tela_principal()
    
    if valor 
    #comandos = int(input("0- Sair 1- Iniciar 2- Skip\n"))

    menu[comandos]()


