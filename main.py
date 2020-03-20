import pygame
from time import sleep
from pygame.locals import * #les var de pygame
import variables as var #importion des variables globales
import classes #importation des classes

##creation de la fenetre

pygame.init()
pygame.font.init()
fenetre = pygame.display.set_mode((640,640))
fond = classes.Fond(var.img_fond)
fondNoir = classes.Fond(var.img_fondNoir)

pygame.display.set_caption("AWACS")
pygame.display.set_icon(pygame.image.load(var.img_icon))#icone de la fenetre
affFenetre = True

#pygame.mixer.music.load("background_music.mp3")#musique de fond
#pygame.mixer.music.play()

##debut des evenements
Player = classes.PlayerPlane(150,200,'blue',True)
#Ennemy = classes.IaPlane(500,500,False)
#Friend = classes.IaPlane(200,200,True)
classes.Notif('issou',999999)

while affFenetre:
    clock = pygame.time.Clock()
    clock.tick(60)
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:#si on appuie sur la croix de la fenetre 
            affFenetre = False      #On arrête la boucle
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:##clic droit
            try:
                var.playerList[0].shoot()#le 1er player de playerlist tire si la liste est pas vide
            except IndexError:pass
        if event.type == KEYDOWN and event.key == K_SPACE:#on crée un nouv player et on le met dans playerlist
            classes.utility.respawn()
        if event.type == KEYDOWN and event.key == K_k:#on crée un nouv player et on le met dans playerlist
            try:var.playerList[0].delete()
            except IndexError:pass
        if event.type == KEYDOWN and event.key == K_n:#on crée un nouv player et on le met dans playerlist
            Ennemy = classes.IaPlane(250,270,False)
    try:
        var.playerList[0].clic(pygame.mouse.get_pos())
    except IndexError:pass
    
    for objet in var.refreshList:#boucle de mouvement
        objet.turn()# on lance la fonction turn de l'objet
        objet.tick()#on lance la fonction tick de l'objet
    

    for objet in var.refreshList:
        objet.rect = objet.image.get_rect(center = (objet.x,objet.y))
        #on remet les co de l'objet à son centre(évite bug de rotate)
    
    var.hitList = []

    for objet in var.refreshList:
        for objet2 in var.refreshList:#boucle de test hitbox
            if pygame.sprite.collide_mask(objet,objet2) and objet != objet2:
                #si 1 touche 2 et 1 différent de 2
                if not(type(objet)==classes.Missile and objet.creator == objet2 and objet.timeAlive < 5) and not(type(objet2)==classes.Missile and objet2.creator == objet and objet2.timeAlive < 5):#si 1 et 2 sont pas des missiles dans la phase d'invincibilité touchant leur créateur
                    var.hitList.append(objet) #on ajoute l'objet 1 à la hitList
    
    for objet in var.hitList[::-1]:#boucle delete(on déréférence les objets de toute liste pour pouvoir les supprimer)
        objet.delete()

    for notif in var.notifList:
        notif.tick()


    ###########rafraichissement, affichage

    sleep(0.05)#delai graphique

    

    try:
        var.playerList[0].camera.update(var.playerList[0])
    except IndexError:pass

    #####HUD
    try:
        for notif in var.notifList:
            fenetre.blit(notif.corps,(var.playerList[0].x,var.playerList[0].y))
#            fenetre.blit(notif.corps,var.playerList[0].camera.apply((100,100)))

    except IndexError:
        for notif in var.notifList:pass
#            fenetre.blit(notif.corps,(100,100))

    #####fonds, avions,missiles
    try:
    #Re-collage
        fenetre.blit(fondNoir.image,var.playerList[0].camera.apply(fondNoir.rect,-var.MAP_LIMITS/2,-var.MAP_LIMITS/2))
        fenetre.blit(fond.image,var.playerList[0].camera.apply(fond.rect))

        for objet in var.refreshList:
            fenetre.blit(objet.image,var.playerList[0].camera.apply(objet.rect))
    
    except IndexError:

        fenetre.blit(fondNoir.image,(fondNoir.rect[0]-var.MAP_LIMITS/2,fondNoir.rect[0]-var.MAP_LIMITS/2))
        fenetre.blit(fond.image,fond.rect)

        for objet in var.refreshList:
            fenetre.blit(objet.image,objet.rect)
    
    #Rafraichissement
    pygame.display.flip()

pygame.quit()