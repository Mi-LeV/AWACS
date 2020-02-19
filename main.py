import pygame
from time import sleep
from pygame.locals import * #les var de pygame
import variables as var #importion des variables globales
import classes #importation des classes

##creation de la fenetre

pygame.init()
fenetre = pygame.display.set_mode((500,500))
fond = pygame.image.load(var.img_fond).convert()
fenetre.blit(fond, (0,0))

pygame.display.set_icon(pygame.image.load(var.img_icon))#icone de la fenetre
affFenetre = True

pygame.mixer.music.load("background_music.mp3")
#pygame.mixer.music.play()

##debut des evenements
global Player
Player = classes.PlayerPlane(250,230,'blue')
Ennemy = classes.IaPlane(250,270,False)


while affFenetre:
    clock = pygame.time.Clock()
    clock.tick(60)
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:
            affFenetre = False      #On arrête la boucle
        if event.type == MOUSEBUTTONDOWN and event.button == 1:# # clic gauche : sprite bouge
            try:var.playerList[0].clic(event)
            except:pass
        if event.type == MOUSEBUTTONDOWN and event.button == 2:##clic molette : sprite lance un missile
            try:var.playerList[0].shootClic(event)
            except:pass
        if event.type == KEYDOWN and event.key == K_SPACE:
            classes.utility.respawn()
    
    for objet in var.refreshList:#boucle de mouvement
        angle = classes.utility.getBearing((objet.x,objet.y),(objet.xDest,objet.yDest))
        classes.utility.rotate(objet,angle)
        objet.goTick(objet.xDest,objet.yDest)
    
    var.spriteList = []
    var.hittedList = []

    for objet in var.refreshList:
        objet.rect = objet.sprite.get_rect(center = (objet.x,objet.y))
    
    for objet in var.refreshList:
        for objet2 in var.refreshList:#boucle de test hitbox
            if objet.rect.colliderect(objet2.rect) and objet != objet2:
                print("col")
                var.hittedList.append(objet) 
    
    for objet in var.hittedList[::-1]:#boucle delete
        var.refreshList.remove(objet)
        var.hittedList.remove(objet)
        try:var.playerList.remove(objet)
        except:pass
        del objet
            
    sleep(0.1)#delai graphique
    #Re-collage
    fenetre.blit(fond,(0,0))
    for objet in var.refreshList:
        fenetre.blit(objet.sprite,(objet.x-10,objet.y-10))
    #Rafraichissement
    pygame.display.flip()

pygame.quit()