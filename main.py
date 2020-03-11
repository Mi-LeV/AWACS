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

#pygame.mixer.music.load("background_music.mp3")#musique de fond
#pygame.mixer.music.play()

##debut des evenements
Player = classes.PlayerPlane(150,200,'blue',True)
Ennemy = classes.IaPlane(300,300,False,True)

while affFenetre:
    clock = pygame.time.Clock()
    clock.tick(60)
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:#si on appuie sur la croix de la fenetre 
            affFenetre = False      #On arrête la boucle
        if event.type == MOUSEBUTTONDOWN and event.button == 1:# # clic gauche
            try:var.playerList[0].clic(event)#le 1er player de playerlist enregistre nouv destination si la liste est pas vide
            except IndexError:pass
        if event.type == MOUSEBUTTONDOWN and event.button == 3:##clic droit
            try:
                var.playerList[0].shoot()#le 1er player de playerlist tire si la liste est pas vide
            except IndexError:pass
        if event.type == KEYDOWN and event.key == K_SPACE:#on crée un nouv player et on le met dans playerlist
            classes.utility.respawn()
        if event.type == KEYDOWN and event.key == K_k:#on crée un nouv player et on le met dans playerlist
            try:classes.utility.delete(var.playerList[0])
            except IndexError:pass
        if event.type == KEYDOWN and event.key == K_n:#on crée un nouv player et on le met dans playerlist
            Ennemy = classes.IaPlane(250,270,False,True)
    
    for objet in var.refreshList:#boucle de mouvement
        objet.turn()# on lance la fonction turn de l'objet
        objet.tick()#on lance la fonction tick de l'objet
    
    var.hitList = []

    for objet in var.refreshList:
        objet.rect = objet.sprite.get_rect(center = (objet.x,objet.y))#on remet les co de l'objet à son centre(évite bug de rotate)
    
    for objet in var.refreshList:
        for objet2 in var.refreshList:#boucle de test hitbox
            if objet.rect.colliderect(objet2.rect) and objet != objet2:#si 1 touche 2 et 1 différent de 2
                if not(type(objet)==classes.Missile and objet.creator == objet2 and objet.timeAlive < 5) and not(type(objet2)==classes.Missile and objet2.creator == objet and objet2.timeAlive < 5):#si 1 et 2 sont pas des missiles dans la phase d'invincibilité touchant leur créateur
                    var.hitList.append(objet) #on ajoute l'objet 1 à la hitList
    
    for objet in var.hitList[::-1]:#boucle delete(on déréférence les objets de toute liste pour pouvoir les supprimer)
        objet.delete()
    sleep(0.1)#delai graphique
    #Re-collage
    fenetre.blit(fond,(0,0))
    for objet in var.refreshList:
        fenetre.blit(objet.sprite,(objet.x-10,objet.y-10))
    #Rafraichissement
    pygame.display.flip()

pygame.quit()