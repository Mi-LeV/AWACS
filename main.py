import pygame
from time import sleep
from pygame.locals import * #les var de pygame
import variables as var #importion des variables globales
import classes #importation des classes

##creation de la fenetre

pygame.init()
fenetre = pygame.display.set_mode((640,480))
fond = pygame.image.load(var.img_fond).convert()
fenetre.blit(fond, (0,0))

pygame.display.set_icon(pygame.image.load(var.img_icon))#icone de la fenetre
affFenetre = True

pygame.mixer.music.load("background_music.mp3")
#pygame.mixer.music.play()



##debut des evenements

Player = classes.PlayerPlane(250,230,'blue')
Ennemy = classes.IaPlane(250,270,False)


while affFenetre:
    pygame.display.flip()
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:
            affFenetre = False      #On arrête la boucle
        if event.type == MOUSEBUTTONDOWN and event.button == 1:## clic gauche : sprite bouge
            Player.clic(event)
        if event.type == MOUSEBUTTONDOWN and event.button == 2:##clic molette : sprite lance un missile
            Player.shootClic(event)
    
    for objet in var.refreshList:#boucle de mouvement
        angle = classes.utility.getBearing((objet.x,objet.y),(objet.xDest,objet.yDest))
        classes.utility.rotate(objet,angle)
        objet.goTick(objet.xDest,objet.yDest)
    
    sleep(0.1)#delai graphique

    #Re-collage
    fenetre.blit(fond,(0,0))
    for objet in var.refreshList:
        fenetre.blit(objet.sprite,(objet.x-10,objet.y-10))
    #Rafraichissement
    pygame.display.flip()

pygame.quit()