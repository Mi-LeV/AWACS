from time import sleep

from pygame.locals import *  # les var de cl.pygame

import classes as cl  # importation des cl
import variables as var  # importion des variables globales

##creation de la fenetre
cl.pygame.init()
cl.pygame.font.init()
infoObject = cl.pygame.display.Info()
if var.FULLSCREEN:# si c'est true, la fenetre est en fullscreen
    var.fenetre = cl.pygame.display.set_mode((infoObject.current_w, infoObject.current_h),cl.pygame.FULLSCREEN)
    var.fullscreen = True #et on met son mode actuel en True
else:# sinon, elle est redimensionnable
    var.fenetre = cl.pygame.display.set_mode((infoObject.current_w, infoObject.current_h),cl.pygame.RESIZABLE)
    var.fullscreen = False #et on met son mode actuel en False


cl.pygame.display.set_caption("AWACS")#titre de la fenetre
cl.pygame.display.set_icon(cl.pygame.image.load(var.img_icon))#icone de la fenetre


#musique de fond


clock = cl.pygame.time.Clock()
clock.tick(60)#on met un fps maximum à 60 (le cycle du jeu est de toute façon de 20 hZ)

cl.utility.screenReso(var.SCREEN_TYPE)# on trouve le définition de l'écran avec son format

while var.globalLoop:##################### boucle globale, qui fait le lien entre le menu, les options et le jeu

    if var.menuLoop:######## début de la boucle du menu, on réinitialise les listes,et on fait apparaitre les boutons
        var.refreshList = []
        var.playerList = []
        var.buttonList = []
        if var.SCREEN_TYPE==169:
            menu = cl.Fond(var.img_menu169)#on met le l'image de menu approprié au format
        else:
            menu = cl.Fond(var.img_menu43)
        #on fait apparaitre les boutons(avec l'image qu'il doivent prendre, les x,y et le code à exec si ils sont pressés)
        butGame = cl.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2-100),'var.menuLoop=False\nvar.gameLoop=True\n')
        butOptions = cl.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+60),'var.menuLoop=False\nvar.optionsLoop = True')
        butExit = cl.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+215),'var.menuLoop=False\nvar.globalLoop=False')
        #on initie la playlist si elle ne se joue pas déja
        if var.MUSIC and not(var.playlist == "menu_music"):
            cl.pygame.mixer.music.set_volume(var.volume/100)
            var.playlist = "menu_music"
            cl.pygame.mixer.init()
            cl.pygame.mixer.music.load(var.music_top_gun)
            cl.pygame.mixer.music.play(-1)

    while var.menuLoop:######## boucle du menu, chaque tour on calcule les boutons cliqués

        for event in cl.pygame.event.get():#On parcours la liste de tous les événements reçus
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #si on appuie sur la croix de la fenetre ou echap
                var.menuLoop = False      #On arrête la boucle
                var.globalLoop = False
            if event.type ==MOUSEBUTTONUP and event.button == 1:# au clic gauche
                for bouton in var.buttonList:#pour chaque bouton
                    bouton.checkclic(cl.pygame.mouse.get_pos())#on teste si la souris ne le touchait pas au clic
                                                            #si oui, il exec son code
        for objet in var.refreshList:#pour chaque objet visible(avion, missile, notif,icone)
            objet.tick()#on appelle sa methode tick qui recalcule son x,y en f son environnement, sa durée de vie,...
                        #cette méthode est différente pour chaque type d'objet
        var.fenetre.blit(menu.image,menu.rect)#on blit l'image du menu
        for bouton in var.buttonList:#pour chaque bouton
            if bouton.aff:#si on doit les afficher
                var.fenetre.blit(bouton.image,bouton.rect)#on les blit
        cl.pygame.display.flip()#puis on flip, cad on affiche les objets blités

    if var.optionsLoop:########################## début de la boucle des options réinitialise les listes,
                                                    #et on fait apparaitre les boutons
        var.refreshList = []
        var.buttonList = []
        if var.SCREEN_TYPE==169:
            options = cl.Fond(var.img_options169)
        else:
            options = cl.Fond(var.img_options43)
        
        cursVolume = cl.Cursor(var.img_cursor,var.img_cursor_c,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+60),'var.volume = round((self.rect_c.left/self.rect.left-1)*54.4)\ncl.pygame.mixer.music.set_volume(var.volume/100)')
        butReso = cl.ButtonReso(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2-200),"Definition : ",'utility.resoSwitch()')
        butMenu = cl.Button(var.img_highlbutt_s,(var.SCREEN_LENGHT/2-550,var.SCREEN_HEIGHT/2-420),'var.optionsLoop=False\nvar.menuLoop=True')
        butFullscreen = cl.Button(var.img_highlbutt,(var.SCREEN_LENGHT/2,var.SCREEN_HEIGHT/2+215),'utility.fullscreenSwitch(var.fenetre)')

    while var.optionsLoop:#################### boucle des options

        for event in cl.pygame.event.get():    #On parcours la liste de tous les événements reçus
            if event.type == QUIT:#si on appuie sur la croix de la fenetre 
                var.optionsLoop = False      #On arrête la boucle
                var.globalLoop = False
            if event.type ==MOUSEBUTTONUP and event.button == 1:# au clic gauche
                for bouton in var.buttonList:#pour chaque bouton
                    bouton.checkclic(cl.pygame.mouse.get_pos())#on teste si la souris ne le touchait pas au clic
                                                            #si oui, il exec son code
            if event.type == KEYDOWN and event.key == K_ESCAPE:#si touche ECHAP appuyée
                var.optionsLoop = False      #On arrête la boucle
                var.menuLoop = True
        for objet in var.refreshList:#pour chaque objet visible(avion, missile, notif,icone)
            objet.tick()#on appelle sa methode tick qui recalcule son x,y en f son environnement, sa durée de vie,...
                        #cette méthode est différente pour chaque type d'objet
        var.fenetre.blit(options.image,options.rect)#on blit l'image de fond de options

        for bouton in var.buttonList:#pour chaque bouton
            if bouton.aff:# si il doit etre affiché
                var.fenetre.blit(bouton.image,bouton.rect)#on le blit
            if type(bouton) == cl.ButtonReso:#on blit aussi les ecritures en dessous des options de résolution
                var.fenetre.blit(bouton.textAff,(bouton.rect[0]-50,bouton.rect[1]+150))
            if type(bouton) == cl.Cursor:#on blit aussi le centre du curseur si c'en est un
                var.fenetre.blit(bouton.image_c,bouton.rect_c)
        cl.pygame.display.flip()

    ########## debut de la boucle du jeu(là où on tire, piou piou): on reset les listes, on fait apparaitre les fonds
    if var.gameLoop:
        var.refreshList = []
        var.buttonList = []
        if var.SCREEN_TYPE==169:#on fait apparaitre chaque fond en f de son format
            overlay = cl.Fond(var.img_overlay169)
        else:
            overlay = cl.Fond(var.img_overlay43)

        Player = cl.PlayerPlane(150,200,True)#on fait apparaitre le player en 150,200 et c'est un ami
        fond = cl.Fond(var.img_fond)#apparition du fond
        fondNoir = cl.Fond(var.img_fondNoir)#apparition du fond
        if var.MUSIC and not(var.playlist == "game_music"):#on reset la playlist et on y remet les musiques
                cl.pygame.mixer.music.set_volume(var.volume/100)
                var.playlist = "game_music"
                cl.pygame.mixer.stop()
                cl.pygame.mixer.music.load(var.music_hell_march)
                cl.pygame.mixer.music.load(var.music_face_the_enemy2)
                cl.pygame.mixer.music.load(var.music_face_the_enemy1)
                cl.pygame.mixer.music.load(var.music_bigfoot)
                cl.pygame.mixer.music.load(var.music_smash)
                cl.pygame.mixer.music.play(-1)

    while var.gameLoop:################# boucle du jeu

        for event in cl.pygame.event.get():    #On parcours la liste de tous les événements reçus
            if event.type == QUIT:#si on appuie sur la croix de la fenetre 
                var.gameLoop = False      #On arrête la boucle
                var.globalLoop = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:#si touche ECHAP pressée
                var.gameLoop = False      #On arrête la boucle
                var.menuLoop = True
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:##clic gauche
                try:
                    var.playerList[0].shoot()#le 1er player de playerlist tire si la liste est pas vide
                except IndexError:pass
            if event.type == KEYDOWN and event.key == K_SPACE:#on crée un nouv player et on le met dans playerlist
                cl.utility.respawn()
            if event.type == KEYDOWN and event.key == K_k:#on delete le player si il existe
                try:var.playerList[0].delete()
                except IndexError:pass
            if event.type == KEYDOWN and event.key == K_n:#on fait spawn un groupe de 5 ennemi en 1000,1000
                cl.utility.spawnGroup(1000,1000,False,5)
            if event.type == KEYDOWN and event.key == K_b:#on fait spawn un groupe de 5 allié en 100,100
                cl.utility.spawnGroup(100,100,True,5)
        
        
        for objet in var.refreshList:#pour chaque objet physique(avion, missile)
            objet.turn()# on appelle la méthode turn de l'objet, qui calcule l'angle de l'objet, et qui tourne son image
            objet.tick()#on appelle sa methode tick qui recalcule son x,y en f son environnement, sa durée de vie,...
                        #cette méthode est différente pour chaque type d'objet

        for objet in var.refreshList:
            objet.rect = objet.image.get_rect(center = (objet.x,objet.y))
            #on remet les co de l'objet à son centre(évite bug de rotate)
        
        var.hitList = []#reset de la liste des objets touchés
        

        for objet in var.refreshList:#pour chaque objet physique(avion, missile)
            for objet2 in var.refreshList:#boucle de test hitbox
                if cl.pygame.sprite.collide_mask(objet,objet2) and objet != objet2:
                    #si 1 touche 2 et 1 différent de 2
                    if not(type(objet)==cl.Missile and objet.creator == objet2 and objet.timeAlive < 5) and not(type(objet2)==cl.Missile and objet2.creator == objet and objet2.timeAlive < 5):
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

        try:#si la caméra existe
            for objet in var.refreshList: #pour chaque objet physique
                if type(objet) != cl.Missile and objet.friendly != var.playerList[0].friendly:#si c'est un avion ennemi
                    newIconList = list(filter(lambda x: x<-10 or x > var.SCREEN_SIZE+10,\
                    var.playerList[0].camera.apply(objet.rect)))# si l'avion est hors de vue du joueur sur x ou y
                    if newIconList:
                        cl.Icon(var.playerList[0].camera.apply((objet.x,objet.y)),"ennemy")#creation de l'icone de l'ennemi
                
                #test si un ami est hors de vue du joueur
                if type(objet) != cl.Missile and objet.friendly == var.playerList[0].friendly:#si c'est un avion ami
                    newIconList = list(filter(lambda x: x<-10 or x > var.SCREEN_SIZE+10,\
                     var.playerList[0].camera.apply(objet.rect)))# si l'avion est hors de vue du joueur sur x ou y
                    if newIconList:
                        cl.Icon(var.playerList[0].camera.apply((objet.x,objet.y)),"friend")#creation de l'icone de l'ami
        except IndexError:pass

        #####on blit fonds puis avions,missiles
        
        try:#si la caméra existe
            var.fenetre.blit(fondNoir.image,var.playerList[0].camera.apply(fondNoir.rect,-var.MAP_LIMITS/2+var.XCAM_MODIF,-var.MAP_LIMITS/2+var.YCAM_MODIF))
            #on blit le fondNoir, par rapport à la camera
            var.fenetre.blit(fond.image,var.playerList[0].camera.apply(fond.rect,var.XCAM_MODIF,var.YCAM_MODIF))
            #on blit le fond, par rapport à la camera
            

            for objet in var.refreshList:#pour chaque objet physique
                var.fenetre.blit(objet.image,var.playerList[0].camera.apply(objet.rect,var.XCAM_MODIF,var.YCAM_MODIF))#on le blit, par rapport à la camera
        
        except IndexError:#si la camera existe pas, on blit tout par rapport au 0,0

            var.fenetre.blit(fondNoir.image,(fondNoir.rect[0]-var.MAP_LIMITS/2,fondNoir.rect[0]-var.MAP_LIMITS/2))
            #on blit le fondNoir
            var.fenetre.blit(fond.image,fond.rect)
            #on blit le fond
            for objet in var.refreshList:#pour chaque objet physique
                var.fenetre.blit(objet.image,objet.rect)#on le blit
            
        
        #####HUD
        
        for icon in var.refreshIconlist:
            var.fenetre.blit(icon.corps,(icon.x,icon.y))#on blit les icones
            icon.delete()#puis on les delete
        
        
        var.fenetre.blit(overlay.image,overlay.rect)#affichage image du HUD



        for notif in var.refreshNotifList:#affichage des notifs
            var.fenetre.blit(notif.corps,(var.SCREEN_LENGHT/2-250,var.SCREEN_HEIGHT/2-350))
        
        

        cl.pygame.display.flip() # on affche les objets blités
cl.pygame.quit()#arret du module pygame
