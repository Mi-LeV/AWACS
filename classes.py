import pygame
import math
import variables as var
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
    
    @staticmethod
    def getBearing(pointA,pointB):
        # if (a1 = b1 and a2 = b2) throw an error 
        theta = math.atan2(pointB[0] - pointA[0], pointA[1] - pointB[1])
        if (theta < 0):
            theta += 2*math.pi
        angle = 360-math.degrees(theta)
        angle %= 360
        return angle
    
    @staticmethod

    def getCoords(angleDegree):
        angle = math.radians(angleDegree)
        x = math.cos(angle)
        y = math.sin(angle)
        return x,y
    
    @staticmethod
    def rotate(objet,angle):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        objet.sprite = pygame.transform.rotozoom(objet.orig_sprite, angle, 1)
        # Create a new rect with the center of the old rect.
        objet.rect = objet.sprite.get_rect(center=objet.rect.center)
    @staticmethod
    def respawn():#fonction de test, recrée un player
        if not var.playerList:
            global Player
            Player = PlayerPlane(250,230,'blue',True)
    
    @staticmethod
    def getDistance(objet,objet2):
        diffX = objet2.x - objet.x
        diffY = objet2.y - objet.y
        distance = math.sqrt(diffX**2+diffY**2)
        return distance
        
    @staticmethod
    def delete(objet):
        if objet in var.hitList:
            var.hitList.remove(objet)
        if objet in var.refreshList:
            var.refreshList.remove(objet)
        if objet in var.playerList:
            var.playerList.remove(objet)
        del objet

class Plane:
    def __init__(self,x,y):
        print("Plane created")
        self.MAXSPEED = 3
        self.xVector=0
        self.yVector=0
        self.xDest = x
        self.yDest = y
        self.x = x
        self.y = y
        self.orig_sprite = pygame.image.load("sprite_plane.png").convert_alpha()
        self.sprite = pygame.image.load("sprite_plane.png").convert_alpha()
        self.rect = self.sprite.get_rect(center=(x,y))
        self.angle = 90
        self.missileList = []
        var.refreshList.append(self)


    def __del__(self):
        self.sprite.fill((0,0,0,0))

    def vectorTo(self,vector,distanceToDest):

        if distanceToDest > 0:
            distanceToDest = utility.plafonne(distanceToDest,2,True)
        else:
            distanceToDest = utility.plafonne(distanceToDest,-2,False)
        
        if (vector + distanceToDest)*abs((distanceToDest/1.5)) > 0:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),self.MAXSPEED,True)
        else:
            vector = utility.plafonne((vector + distanceToDest)*abs((distanceToDest/1.5)),-self.MAXSPEED,False)
        
        return vector
    
    def goTo(self,xDistanceToDest,yDistanceToDest):

        self.xVector = self.vectorTo(self.xVector,xDistanceToDest)
        self.yVector = self.vectorTo(self.yVector,yDistanceToDest)
        
        self.x += self.xVector
        self.y += self.yVector

        xDistanceToDest -= self.xVector
        yDistanceToDest -= self.yVector


    def goTick(self):
        if not self.xDest or not self.yDest:# si la dest n'est pas définie, rien faire
            return
        xDistanceToDest=self.xDest-self.x
        yDistanceToDest=self.yDest-self.y
        if not((3 > xDistanceToDest > -3) and (3 > yDistanceToDest > -3)):
            self.goTo(xDistanceToDest,yDistanceToDest)
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            return True


    def shoot(self):
        print("player shoot")
        self.missileList.append(Missile(self,self.x,self.y,self.angle,self.xVector,self.yVector))
    
    def turn(self):
        self.angle = (utility.getBearing((self.x,self.y),(self.xDest,self.yDest))+90)%360 #calcul de l'angle de l'ojet par rapport à sa dest
        utility.rotate(self,self.angle)# on le tourne de cet angle

class PlayerPlane(Plane):
    def __init__(self,x,y,color,friend):
        super().__init__(x,y)
        var.playerList.append(self)
        if friend:pass
            #mettre le sprite ami
        else:pass
            #mettre le sprite ennemi  
        self.friendly = friend
    
    def __del__(self):
        try:var.playerList.remove(self)
        except:pass

    def clic(self,event): 
        print("clic")
        self.xDest = event.pos[0]
        self.yDest = event.pos[1]

class IaPlane(Plane):
    def __init__(self,x,y,friend,active):
        super().__init__(x,y)
        self.MAXSPEED = 1
        self.agro = None
        self.active = active
        if friend:pass
            #mettre le sprite ami
        else:pass
            #mettre le sprite ennemi  
        self.friendly = friend
    
    def goTick(self):
        if self.active:
            super().goTick()
            self.searchAgro()
            self.goAgro()

    def goAgro(self):
        if not self.agro:# si la dest n'est pas définie, rien faire
            return
        self.xDest = self.agro.x
        self.yDest = self.agro.y
        
    def searchAgro(self):
        ennemyList = []
        for objet in var.refreshList:
            if type(objet)!= Missile and objet.friendly != self.friendly:#test si objet non missile et si il est pas de son camp
                ennemyList.append(objet)

        if ennemyList:#si la liste n'est pas vide
            minima = 99999999 #valeur très haute
            minObj = None
            for objet in ennemyList:#test de la distance minimlale
                temp = utility.getDistance(self,objet)#calcul distance
                if temp < minima:
                    minima = temp
                    minObj = objet
            self.agro = minObj
        else:
            self.agro = None

class Missile:
    def __init__(self,creator,x,y,angle,xVector,yVector):

        print("Missile created")
        self.creator = creator
        xAngle,yAngle = utility.getCoords(angle)
        self.xVector=utility.plafonne(xVector*2 + xAngle*20,20,True)
        self.xVector=utility.plafonne(xVector*2 + xAngle*20,-20,False)
        self.yVector=utility.plafonne(yVector*2 + yAngle*20,20,True)
        self.yVector=utility.plafonne(yVector*2 + yAngle*20,-20,False)
        self.x = x
        self.y = y
        self.speed = 0
        self.timeAlive = 0
        self.orig_sprite = pygame.image.load("sprite_missile.png").convert_alpha()
        self.sprite = self.orig_sprite
        self.rect = self.sprite.get_rect(center=(x,y))
        self.angle = angle#l'angle natif de l'image
        var.refreshList.append(self)
    
    def vectorTo(self,vector):#décélération proressive du missile
        return vector/((self.timeAlive/30)+1)
    
    def goTo(self):

        self.xVector = self.vectorTo(self.xVector)
        self.yVector = self.vectorTo(self.yVector)
        
        self.x += self.xVector
        self.y -= self.yVector #c'est un moins car l'origine des y n'est pas en bas mais en haut
    
    def goTick(self):
        self.timeAlive += 1
        #si vecteurs pas trop faibles, et timeAlive pas trop grand, bouger sinon s'arrete
        if not(((-1.5<self.xVector < 1.5) and (-1.5<self.yVector < 1.5))or ( self.timeAlive > 500)):
            self.goTo()
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            self.sprite.fill((0,0,0,0))
            utility.delete(self)
    
    def turn(self):
        utility.rotate(self,self.angle)# on le tourne de cet angle
