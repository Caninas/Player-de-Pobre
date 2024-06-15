from os import path, listdir, makedirs
from pathlib import Path
from shutil import rmtree
from threading import Thread
from urllib import request
from sys import exit

from PySimpleGUI import WIN_CLOSED

from player import Player


def criar_arq_locais():         # baixa icones e os coloca na pasta do programa na appdata
    arqs = {"padrao.png": "https://images2.imgbox.com/50/01/YsRTXVYA_o.png", "anterior.png": "https://images2.imgbox.com/38/f8/WHPA58Zt_o.png", "pause.png": "https://images2.imgbox.com/8b/a3/P4xKWey9_o.png",
            "play.png": "https://images2.imgbox.com/57/3e/lckshfVs_o.png", "proximo.png": "https://images2.imgbox.com/34/63/FgVzWKzV_o.png", "mudo.png": "https://images2.imgbox.com/bf/01/3gm8AIUy_o.png",
            "baixo.png": "https://images2.imgbox.com/19/76/wKJS53oh_o.png", "medio.png": "https://images2.imgbox.com/f1/a8/x55YkEpd_o.png", "alto.png": "https://images2.imgbox.com/26/7d/SblDwmnZ_o.png",
            "icone.ico": "https://drive.google.com/uc?export=download&id=1CfBUVfOW8FeNMgRSG-lGofRAGY85lM83"}


    if not path.isdir(f"{path_local}/icones") or len(listdir(f"{path_local}/icones")) < 10:
        try:
            if len(listdir(f"{path_local}/icones")) < 10:
                rmtree(f"{path_local}/icones")
        except:
            pass

        makedirs(f"{path_local}/icones")
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

        player.alt_volume(valores["sl"]/10) #!

        player.check_botao(botao, valores)

        # roda na primeira vez que tocar uma musica (cria processo para passar passar musica ao terminar uma, alem de atualizar o slider e o timer)
        if player.k == 0 and botao in {0,1,2,"musicas"} and valores["musicas"] != []:
            thread = Thread(target=player.passar_musica_infinito)
            thread.daemon = True
            thread.start()
            player.k = 1        
