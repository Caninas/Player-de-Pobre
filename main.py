from threading import Thread

from PySimpleGUI import WIN_CLOSED

from player import Player

if __name__ == "__main__":
    player = Player()
    player.tela.init_tela_principal()
    player.playpause = "play"

    player.k = 0

    player.listen_botoes_media()
    
    
    while True:

        botao, valores = player.tela.abrir()

        if botao == WIN_CLOSED:
            exit(0)

        player.alt_volume(valores["sl"]/10)


        player.check_botao(botao, valores)


        #roda na primeira vez que tocar uma musica (cria processo para passar passar musica ao terminar uma, alem de atualizar o slider e o timer)
        if player.k == 0 and botao in {0,1,2,"musicas"} and valores["musicas"] != []:
            thread = Thread(target=player.passar_musica_infinito)
            thread.daemon = True
            thread.start()
            player.k = 1        
        