import socket 
import pygame
from pygame.locals import * #les var de pygame
import variables as var #importion des variables globales
import classes #importation des classes

spriteList =[]
hote = 'localhost'
port = 6969
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
connexion_avec_serveur.connect((hote, port))


command = b''
while command != b'quit':
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:
            command = "quit"      #On arrête la boucle
        if event.type == MOUSEBUTTONDOWN and event.button == 1:##clic gauche : sprite bouge
            command = "clicDest {} {}".format(event.pos[0],event.pos[1])
        if event.type == MOUSEBUTTONDOWN and event.button == 2:##clic molette : sprite lance un missile
            command = "clicShoot {} {}".format(event.pos[0],event.pos[1])
        if event.type == KEYDOWN and event.key == K_SPACE:
            command = "respawn"
    
    command.encode()
    connexion_avec_serveur.send(command)
    
    
    objetAAfficher = connexion_avec_serveur.recv(1024)#["avion","12","34"]
    objetAAficher = objetAAficher.decode()
    objetAAficher = objetAAficher.split(" ")
    if objetAAficher[0] == "del":#["del","avion"]
        objetAAficher[3].fill((0,0,0,0))
        spriteList.remove([0]objetAAficher[1])
    if objetAAficher[0] in spriteList[0]:
        spriteList[spriteList[0].find(objetAAficher[0])] = objetAAficher
    else:
        objetAAficher.append(pygame.image.load("sprite_plane.png").convert_alpha())
        spriteList.append(objetAAficher)#["avion(nom du seveur)","12","34",sprite]
        
    #Re-collage
    fenetre.blit(fond,(0,0))
    for sprite in spriteList:
        fenetre.blit(sprite[3],sprite[1],sprite[2]))
    #Rafraichissement
    pygame.display.flip()

print("disconnected")
connexion_avec_serveur.close()
