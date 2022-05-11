import os
from pathlib import Path
from shutil import rmtree
from threading import Thread
from urllib import request
from sys import exit

from PySimpleGUI import WIN_CLOSED

from player import Player


def criar_arq_locais():         # baixa icones e os coloca na pasta do programa na appdata
    arqs = {"padrao.png": "https://i.imgur.com/BIwtdPV.png", "anterior.png": "https://i.imgur.com/zR5ipb0.png", "pause.png": "https://i.imgur.com/TgaiItf.png",
            "play.png": "https://i.imgur.com/DZS8uSg.png", "proximo.png": "https://i.imgur.com/ellbdlv.png", "mudo.png": "https://i.imgur.com/Di2NhDZ.png",
            "baixo.png": "https://i.imgur.com/UnUxdj3.png", "medio.png": "https://i.imgur.com/FkgKiIv.png", "alto.png": "https://i.imgur.com/2o93beu.png",
            "icone.ico": "https://drive.google.com/uc?export=download&id=1CfBUVfOW8FeNMgRSG-lGofRAGY85lM83"}


    if not os.path.isdir(f"{path_local}/icones") or len(os.listdir(f"{path_local}/icones")) < 10:
        try:
            if len(os.listdir(f"{path_local}/icones")) < 10:
                rmtree(f"{path_local}/icones")
        except:
            pass

        os.makedirs(f"{path_local}/icones")
        player.tela.msg_baixando()
        request.urlretrieve(arqs["padrao.png"], f"{path_local}/icones/padrao.png")
        request.urlretrieve(arqs["anterior.png"], f"{path_local}/icones/anterior.png")
        request.urlretrieve(arqs["pause.png"], f"{path_local}/icones/pause.png")
        request.urlretrieve(arqs["play.png"], f"{path_local}/icones/play.png")
        request.urlretrieve(arqs["proximo.png"], f"{path_local}/icones/proximo.png")
        request.urlretrieve(arqs["mudo.png"], f"{path_local}/icones/mudo.png")
        request.urlretrieve(arqs["baixo.png"], f"{path_local}/icones/baixo.png")
        request.urlretrieve(arqs["medio.png"], f"{path_local}/icones/medio.png")
        request.urlretrieve(arqs["alto.png"], f"{path_local}/icones/alto.png")
        request.urlretrieve(arqs["icone.ico"], f"{path_local}/icones/icone.ico")


if __name__ == "__main__":
    player = Player()

    path_local = f"{Path.home()}\AppData\Roaming\Player de Pobre"           # local onde ficarao os arquivos (pode ser alterado)
    criar_arq_locais()

    player.path_dados = path_local
    player.path_icones = f"{path_local}/icones"
    player.tela.path_icones = f"{path_local}/icones"
    player.playpause = "play"

    player.tela.init_tela_principal()
    player.carregar_sessao()
    player.listen_botoes_midia()
    
    while True:
        botao, valores = player.tela.abrir()

        if botao == WIN_CLOSED:
            exit()

        player.alt_volume(valores["sl"]/10)

        player.check_botao(botao, valores)

        # roda na primeira vez que tocar uma musica (cria processo para passar passar musica ao terminar uma, alem de atualizar o slider e o timer)
        if player.k == 0 and botao in {0,1,2,"musicas"} and valores["musicas"] != []:
            thread = Thread(target=player.passar_musica_infinito)
            thread.daemon = True
            thread.start()
            player.k = 1        
