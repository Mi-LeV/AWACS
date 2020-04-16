from time import sleep

import pygame
from pygame.locals import *  # les var de pygame

import classes  # importation des classes
import variables as var  # importion des variables globales

##creation de la fenetre
pygame.init()
pygame.font.init()
infoObject = pygame.display.Info()
if var.FULLSCREEN:
    fenetre = pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.FULLSCREEN)
else:
    fenetre = pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.RESIZABLE)





pygame.display.set_caption("AWACS")
pygame.display.set_icon(pygame.image.load(var.img_icon))#icone de la fenetre


#musique de fond




clock = pygame.time.Clock()
clock.tick(60)

classes.utility.screenReso(var.SCREEN_TYPE)

while var.globalLoop:
    if var.menuLoop:
        var.refreshList = []
        var.playerList = []
        var.buttonList = []
        if var.SCREEN_TYPE==169:
            menu = classes.Fond(var.img_menu169)
        else:
            menu = classes.Fond(var.img_menu43)
        butGame = classes.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2-100),'var.menuLoop=False\nvar.gameLoop=True\n')
        butOptions = classes.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+60),'var.menuLoop=False\nvar.optionsLoop = True')
        butExit = classes.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+215),'var.menuLoop=False\nvar.globalLoop=False')
        
        if var.MUSIC and not(var.playlist == "menu_music"):
            pygame.mixer.music.set_volume(var.volume/100)
            var.playlist = "menu_music"
            pygame.mixer.init()
            pygame.mixer.music.load(var.music_top_gun)
            pygame.mixer.music.play(-1)

    while var.menuLoop:

        for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):#si on appuie sur la croix de la fenetre ou echap
                var.menuLoop = False      #On arrête la boucle
                var.globalLoop = False
            if event.type ==MOUSEBUTTONUP and event.button == 1:
                for bouton in var.buttonList:
                    bouton.checkclic(pygame.mouse.get_pos())
            
        for objet in var.refreshList:
            objet.tick()
        fenetre.blit(menu.image,menu.rect)
        for bouton in var.buttonList:
            if bouton.aff:
                fenetre.blit(bouton.image,bouton.rect)
        pygame.display.flip()

    if var.optionsLoop:
        var.refreshList = []
        var.buttonList = []
        
        cursVolume = classes.Cursor(var.img_cursor,var.img_cursor_c,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+60),'var.volume = round((self.rect_c.left/self.rect.left-1)*54.4)\npygame.mixer.music.set_volume(var.volume/100)')
        butReso = classes.ButtonReso(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2-100),"Definition : ",'utility.resoSwitch()')
        butMenu = classes.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+215),'var.optionsLoop=False\nvar.menuLoop=True')
    while var.optionsLoop:
        for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
            if event.type == QUIT:#si on appuie sur la croix de la fenetre 
                var.optionsLoop = False      #On arrête la boucle
                var.globalLoop = False
            if event.type ==MOUSEBUTTONUP and event.button == 1:
                for bouton in var.buttonList:
                    bouton.checkclic(pygame.mouse.get_pos())
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                var.optionsLoop = False      #On arrête la boucle
                var.menuLoop = True
        for objet in var.refreshList:
            objet.tick()
        fenetre.blit(menu.image,menu.rect)

        for bouton in var.buttonList:

            if bouton.aff:
                fenetre.blit(bouton.image,bouton.rect)
            if type(bouton) == classes.ButtonReso:
                fenetre.blit(bouton.textAff,(bouton.rect[0]-50,bouton.rect[1]+100))
            if type(bouton) == classes.Cursor:
                fenetre.blit(bouton.image_c,bouton.rect_c)
        pygame.display.flip()

    ##debut des evenements gameloop
    if var.gameLoop:
        var.refreshList = []
        var.buttonList = []
        if var.SCREEN_TYPE==169:
            overlay = classes.Fond(var.img_overlay169)
        else:
            overlay = classes.Fond(var.img_overlay43)
        Player = classes.PlayerPlane(150,200,True)
        fond = classes.Fond(var.img_fond)
        fondNoir = classes.Fond(var.img_fondNoir)
        if var.MUSIC and not(var.playlist == "game_music"):
                pygame.mixer.music.set_volume(var.volume/100)
                var.playlist = "game_music"
                pygame.mixer.stop()
                pygame.mixer.music.load(var.music_hell_march)
                pygame.mixer.music.load(var.music_face_the_enemy2)
                pygame.mixer.music.load(var.music_face_the_enemy1)
                pygame.mixer.music.load(var.music_bigfoot)
                pygame.mixer.music.load(var.music_smash)
                pygame.mixer.music.play(-1)

    while var.gameLoop:

        for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
            if event.type == QUIT:#si on appuie sur la croix de la fenetre 
                var.gameLoop = False      #On arrête la boucle
                var.globalLoop = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                var.gameLoop = False      #On arrête la boucle
                var.menuLoop = True
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:##clic gauche
                try:
                    var.playerList[0].shoot()#le 1er player de playerlist tire si la liste est pas vide
                except IndexError:pass
            if event.type == KEYDOWN and event.key == K_SPACE:#on crée un nouv player et on le met dans playerlist
                classes.utility.respawn()
            if event.type == KEYDOWN and event.key == K_k:#on crée un nouv player et on le met dans playerlist
                try:var.playerList[0].delete()
                except IndexError:pass
            if event.type == KEYDOWN and event.key == K_n:
                classes.utility.spawnGroup(1000,1000,False,5)
            if event.type == KEYDOWN and event.key == K_b:
                classes.utility.spawnGroup(100,100,True,5)
        
        
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
                    if not(type(objet)==classes.Missile and objet.creator == objet2 and objet.timeAlive < 5) and not(type(objet2)==classes.Missile and objet2.creator == objet and objet2.timeAlive < 5):
                        #si 1 et 2 sont pas des missiles dans la phase d'invincibilité touchant leur créateur
                        var.hitList.append(objet) #on ajoute l'objet 1 à la hitList
        
        for objet in var.hitList[::-1]:#boucle delete(on déréférence les objets de toute liste pour pouvoir les supprimer)
            objet.delete()

        for notif in var.refreshNotifList:
            notif.tick()


        ###########rafraichissement, affichage

        sleep(var.DELAI)#delai graphique

        

        try:
            var.playerList[0].camera.update(var.playerList[0])#on update la position de la caméra
        except IndexError:pass

        #calcul des icones à afficher
        try:
            for objet in var.refreshList: #test si un ennemi est hors de vue du joueur
                if type(objet) != classes.Missile and objet.friendly != var.playerList[0].friendly:
                    newIconList = list(filter(lambda x: x<-10 or x > var.SCREEN_SIZE+10, var.playerList[0].camera.apply(objet.rect)))
                    if newIconList:
                        classes.Icon(var.playerList[0].camera.apply((objet.x,objet.y)),"ennemy")#creation de l'icone
                
                #test si un ami est hors de vue du joueur
                if type(objet) != classes.Missile and objet.friendly == var.playerList[0].friendly:
                    newIconList = list(filter(lambda x: x<-10 or x > var.SCREEN_SIZE+10, var.playerList[0].camera.apply(objet.rect)))
                    if newIconList:
                        classes.Icon(var.playerList[0].camera.apply((objet.x,objet.y)),"friend")#creation de l'icone
        except IndexError:pass

        #####fonds, avions,missiles
        
        try:
            fenetre.blit(fondNoir.image,var.playerList[0].camera.apply(fondNoir.rect,-var.MAP_LIMITS/2+var.XCAM_MODIF,-var.MAP_LIMITS/2+var.YCAM_MODIF))
            fenetre.blit(fond.image,var.playerList[0].camera.apply(fond.rect,var.XCAM_MODIF,var.YCAM_MODIF))
            

            for objet in var.refreshList:
                fenetre.blit(objet.image,var.playerList[0].camera.apply(objet.rect,var.XCAM_MODIF,var.YCAM_MODIF))
        
        except IndexError:

            fenetre.blit(fondNoir.image,(fondNoir.rect[0]-var.MAP_LIMITS/2,fondNoir.rect[0]-var.MAP_LIMITS/2))
            fenetre.blit(fond.image,fond.rect)


            for objet in var.refreshList:
                fenetre.blit(objet.image,objet.rect)
            
        
        #####HUD
        
        for icon in var.refreshIconlist:
            fenetre.blit(icon.corps,(icon.x,icon.y))#on affiche les icones
            icon.delete()#puis on les delete
        
        
        fenetre.blit(overlay.image,overlay.rect)#affichage image du HUD



        for notif in var.refreshNotifList:#affichage des notifs
            fenetre.blit(notif.corps,(var.SCREEN_LENGHT/2-480,var.SCREEN_HEIGHT/2-280))
        
        

        #Rafraichissement
        pygame.display.flip()
pygame.quit()