import pygame
from pygame.locals import *#les variables de pygame
import math
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
    def __init__(self,x,y,color):

        print("Plane created")
        self.xVector=0
        self.yVector=0
        self.xDest = 0
        self.yDest = 0
        self.x = x
        self.y = y
        self.graphicPlane = None

    def scalaireTo(self,vector,distanceToDest):

        if distanceToDest > 0:
            distanceToDest = utility.plafonne(distanceToDest,2,True)
        else:
            distanceToDest = utility.plafonne(distanceToDest,-2,False)
        
        if (vector + distanceToDest)*abs((distanceToDest/1.5)) > 0:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),3,True)
        else:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),-3,False)
        
        return vector
    
    def goTo(self,xDest,yDest):
        #x,y,xosef,yosef=Canevas.coords(self.graphicPlane)
        xDistanceToDest=xDest-x
        yDistanceToDest=yDest-y
            
        self.xVector = self.scalaireTo(self.xVector,xDistanceToDest)
        self.yVector = self.scalaireTo(self.yVector,yDistanceToDest)


        self.x += self.xVector
        self.y += self.yVector

        xDistanceToDest -= self.xVector
        yDistanceToDest -= self.yVector

        #Canevas.move(self.graphicPlane,self.xVector,self.yVector)

        if not((3 > xDistanceToDest > -3) and (3 > yDistanceToDest > -3)):
            return False #continue
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            return True

    def shoot(self,x,y):
        if not(hasattr(self,"Mymissile")):
            print("player shoot")
            #self.Mymissile = Missile(Canevas,self.x,self.y)
            self.Mymissile.xDest = x
            self.Mymissile.yDest = y
            if self.Mymissile.goTo(self.Mymissile.xDest,self.Mymissile.yDest):
                fenetre.after(100,self.shootLoop)

    def shootLoop(self):
        if  self.Mymissile.goTo(self.Mymissile.xDest,self.Mymissile.yDest):
            fenetre.after(100,self.shootLoop)
        else:
            print("fin shoot")
            del self.Mymissile

class PlayerPlane(Plane):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        #self.graphicPlane = Canevas.create_rectangle(x,y,x+10,y+10,outline=color,fill=color)

    def clic(self,event): 
        if self.xVector == 0 and self.yVector == 0:
            print("clic")
            self.xDest = event.x
            self.yDest = event.y
            if not self.goTo(self.xDest,self.yDest):
                fenetre.after(100,self.clicLoop)
        else:
            print("en mouvement")

    def clicLoop(self):
        print("cloc")
        if not (self.goTo(self.xDest,self.yDest)):
            fenetre.after(100,self.clicLoop)
        else:
            print("fin")

    def shootClic(self,event):
        self.shoot(event.x,event.y)

class IaPlane(Plane):
    def __init__(self,x,y,friend,color = False):
        super().__init__(x,y,color)
        if not color:
            if friend:
                colorAff = 'blue'
            else:
                colorAff = 'red'
        else:
            colorAff = color
        #self.graphicPlane = Canevas.create_oval(x-5,y-5,x+5,y+5,outline=colorAff,fill=colorAff)
        self.friendly = friend
        

    def trajectoirePatterne(self,x1,y1,x2,y2,nombre = 10):
        if nombre > 1:
            self.goTo(x1,x2)
            self.goTo(x2,y2)
            self.trajectoirePatterne(x1,y1,x2,y2,nombre-1)

class Missile:
    def __init__(self,Canvas,x,y):

        print("Missile created")
        self.ovalMissile = Canevas.create_oval(x,y,x+8,y+8,outline='black',fill='black')
        self.xVector=0
        self.yVector=0
        self.xDest = 0
        self.yDest = 0
        self.x = x
        self.y = y

    def __del__(self):
        Canevas.delete(self.ovalMissile) ## supprime l'objet tkinter
        
    def go(self,x,y):
        Canevas.move(self.ovalMissile,x,y)

    def vectorTo(self,dest,vector,distanceToDest):

        if distanceToDest>0 and vector<4:
            vector += 2
        elif distanceToDest<0 and vector > -4:
            vector -= 2
        return vector
    
    def goTo(self,xDest,yDest):
        x,y,xosef,yosef=Canevas.coords(self.ovalMissile)
        xDistanceToDest=xDest-x
        yDistanceToDest=yDest-y
        if ((xDistanceToDest>5 or xDistanceToDest<-5)or(yDistanceToDest>5 or yDistanceToDest<-5)):
            x,y,xosef,yosef=Canevas.coords(self.ovalMissile)

            self.xVector = self.vectorTo(xDest,self.xVector,xDistanceToDest)
            self.yVector = self.vectorTo(yDest,self.yVector,yDistanceToDest)

            xDistanceToDest=xDest-x
            yDistanceToDest=yDest-y

            self.x += self.xVector
            self.y += self.yVector
            Canevas.move(self.ovalMissile,self.xVector,self.yVector)
            return True
        else:
            self.xVector = 0
            self.yVector = 0
            return False


##creation de la fenetre

pygame.init()
fenetre = pygame.display.set_mode((640,480))
fond = pygame.image.load("issou.jpg").convert()
fenetre.blit(fond, (0,0))
affFenetre = True



##debut des evenements

Player = PlayerPlane(250,230,'blue')
Ennemy = IaPlane(250,270,False)

#Canevas.bind('<Button-1>',Player.clic)## clic gauche : graphicPlane bouge
#Canevas.bind('<Control-Button-1>',Player.shootClic)##control clic gauche : graphicPlane lance un missile
#Canevas.bind('<Control-Button-3>',Ennemy.trajectoirePatterne(150,230,350,370))

while affFenetre:
    pygame.display.flip()
    for event in pygame.event.get():    #On parcours la liste de tous les événements reçus
        if event.type == QUIT:
            affFenetre = 0      #On arrête la boucle
        if event.type == KEYDOWN and event.key == K_SPACE:
            print("a")
