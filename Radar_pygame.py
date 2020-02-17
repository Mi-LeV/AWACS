import pygame
from time import sleep
from pygame.locals import *#les variables de pygame

refreshList = []

class utility:
    @staticmethod
    def plafonne(nombre,plafond,plafondMax):
        if plafondMax:
            if nombre > plafond:
                return plafond
        else:
            if nombre < plafond:
                return plafond
        return nombre
    
class Plane:
    def __init__(self,x,y):

        print("Plane created")
        self.xVector=0
        self.yVector=0
        self.xDest = x
        self.yDest = y
        self.x = x
        self.y = y
        self.sprite = pygame.image.load("sprite_plane.png").convert_alpha()

    def vectorTo(self,vector,distanceToDest):

        if distanceToDest > 0:
            distanceToDest = utility.plafonne(distanceToDest,2,True)
        else:
            distanceToDest = utility.plafonne(distanceToDest,-2,False)
        
        if (vector + distanceToDest)*abs((distanceToDest/1.5)) > 0:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),3,True)
        else:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),-3,False)
        
        return vector
    
    def goTo(self,xDistanceToDest,yDistanceToDest):

        self.xVector = self.vectorTo(self.xVector,xDistanceToDest)
        self.yVector = self.vectorTo(self.yVector,yDistanceToDest)
        
        self.x += self.xVector
        self.y += self.yVector

        xDistanceToDest -= self.xVector
        yDistanceToDest -= self.yVector


    def goTick(self,xDest,yDest):
        print("tick")
        xDistanceToDest=self.xDest-self.x
        yDistanceToDest=self.yDest-self.y
        if not((3 > xDistanceToDest > -3) and (3 > yDistanceToDest > -3)):
            self.goTo(xDistanceToDest,yDistanceToDest)
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            return True


    def shoot(self,x,y):
        if not(hasattr(self,"Mymissile")):
            print("player shoot")
            self.Mymissile = Missile(self.x,self.y)
            refreshList.append(self.Mymissile)
            self.Mymissile.xDest = x
            self.Mymissile.yDest = y
            if not self.Mymissile.goTo(self.Mymissile.xDest,self.Mymissile.yDest):
                self.shootLoop()

    def shootLoop(self):
        if  not self.Mymissile.goTo(self.Mymissile.xDest,self.Mymissile.yDest):
            self.shootLoop()
        else:
            print("fin shoot")
            del self.Mymissile

class PlayerPlane(Plane):
    def __init__(self,x,y,color):
        super().__init__(x,y)
        #self.graphicPlane = Canevas.create_rectangle(x,y,x+10,y+10,outline=color,fill=color)

    def clic(self,event): 
        print("clic")
        self.xDest = event.pos[0]
        self.yDest = event.pos[1]

    def shootClic(self,event):
        self.shoot(event.pos[0],event.pos[1])

class IaPlane(Plane):
    def __init__(self,x,y,friend):
        super().__init__(x,y)
        if friend:pass
            #mettre le sprite ami
        else:pass
            #mettre le sprite ennemi  
        self.friendly = friend
        

    def trajectoirePatterne(self,x1,y1,x2,y2,nombre = 10):
        if nombre > 1:
            self.goTo(x1,x2)
            self.goTo(x2,y2)
            self.trajectoirePatterne(x1,y1,x2,y2,nombre-1)

class Missile:
    def __init__(self,x,y):

        print("Missile created")
        self.sprite = pygame.image.load("sprite_missile.png").convert_alpha()
        self.xVector=0
        self.yVector=0
        self.xDest = 0
        self.yDest = 0
        self.x = x
        self.y = y

    def __del__(self):
        #Canevas.delete(self.ovalMissile) ## supprime l'objet tkinter
        pass
    
    def go(self,x,y):
        self.x = x
        self.y = y

    def vectorTo(self,dest,vector,distanceToDest):

        if distanceToDest>0 and vector<4:
            vector += 2
        elif distanceToDest<0 and vector > -4:
            vector -= 2
        return vector
    
    def goTo(self,xDest,yDest):
        x,y=self.sprite.get_rect()
        xDistanceToDest=xDest-x
        yDistanceToDest=yDest-y
        if ((xDistanceToDest>5 or xDistanceToDest<-5)or(yDistanceToDest>5 or yDistanceToDest<-5)):
            x,y=self.sprite.get_rect()

            self.xVector = self.vectorTo(xDest,self.xVector,xDistanceToDest)
            self.yVector = self.vectorTo(yDest,self.yVector,yDistanceToDest)

            xDistanceToDest=xDest-x
            yDistanceToDest=yDest-y

            self.x += self.xVector
            self.y += self.yVector
            return True
        else:
            self.xVector = 0
            self.yVector = 0
            return False


##creation de la fenetre

pygame.init()
fenetre = pygame.display.set_mode((640,480))
fond = pygame.image.load("hackeur thibault.jpg").convert()
fenetre.blit(fond, (0,0))
affFenetre = True
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play()



##debut des evenements

Player = PlayerPlane(250,230,'blue')
refreshList.append(Player)
Ennemy = IaPlane(250,270,False)
refreshList.append(Ennemy)

while affFenetre:
    pygame.display.flip()
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:
            affFenetre = False      #On arrête la boucle
        if event.type == MOUSEBUTTONDOWN and event.button == 1:## clic gauche : graphicPlane bouge
            Player.clic(event)
        if event.type == MOUSEBUTTONDOWN and event.button == 2:##clic molette : graphicPlane lance un missile
            Player.shootClic(event)
    
    for avion in refreshList:
        avion.goTick(avion.xDest,avion.yDest)
    
    sleep(0.1)#delai graphique
    #Re-collage
    fenetre.blit(fond,(0,0))
    for avion in refreshList:
        fenetre.blit(avion.sprite,(avion.x,avion.y))
    #Rafraichissement
    pygame.display.flip()