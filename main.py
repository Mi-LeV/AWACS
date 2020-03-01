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
        objet.angle = (classes.utility.getBearing((objet.x,objet.y),(objet.xDest,objet.yDest))+90)%360
        classes.utility.rotate(objet,objet.angle)
        objet.goTick(objet.xDest,objet.yDest)
    
    var.hitList = []

    for objet in var.refreshList:
        objet.rect = objet.sprite.get_rect(center = (objet.x,objet.y))
    
    for objet in var.refreshList:
        for objet2 in var.refreshList:#boucle de test hitbox
            if objet.rect.colliderect(objet2.rect) and objet != objet2:
                if not(type(objet)==classes.Missile and objet.timeAlive < 3) and not(type(objet2)==classes.Missile and objet2.timeAlive < 3):
                    print("col")
                    var.hitList.append(objet) 
    
    for objet in var.hitList[::-1]:#boucle delete
        var.refreshList.remove(objet)
        var.hitList.remove(objet)
        try:var.playerList.remove(objet)
        except:pass
        del objet
    
    print(var.playerList[0].angle)
    sleep(0.1)#delai graphique
    #Re-collage
    fenetre.blit(fond,(0,0))
    for objet in var.refreshList:
        fenetre.blit(objet.sprite,(objet.x-10,objet.y-10))
    #Rafraichissement
    pygame.display.flip()

pygame.quit()