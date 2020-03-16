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
        objet.image = pygame.transform.rotozoom(objet.orig_image, angle, 1)
        # Create a new rect with the center of the old rect.
        objet.rect = objet.image.get_rect(center=objet.rect.center)
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
        
class Plane(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        print("Plane created")
        self.MAXSPEED = 3
        self.timeAlive = 0
        self.xVector=0
        self.yVector=0
        self.xDest = x
        self.yDest = y
        self.x = x
        self.y = y
        self.orig_image = pygame.image.load(var.img_plane_default).convert_alpha()
        self.image = pygame.image.load(var.img_plane_default).convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 90
        self.missileList = []
        var.refreshList.append(self)


    def delete(self):
        self.image.fill((0,0,0,0))
        if self in var.hitList:
            var.hitList.remove(self)
        if self in var.refreshList:
            var.refreshList.remove(self)
        if self in var.playerList:
            var.playerList.remove(self)
        del self

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


    def tick(self):
        self.timeAlive += 1
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
        self.missileList.append(Missile(self))
    
    def turn(self):
        self.angle = (utility.getBearing((self.x,self.y),(self.xDest,self.yDest))+90)%360 #calcul de l'angle de l'ojet par rapport à sa dest
        utility.rotate(self,self.angle)# on le tourne de cet angle

class PlayerPlane(Plane):
    def __init__(self,x,y,color,friend):
        super().__init__(x,y)
        self.MAXMISSILE = 3
        var.playerList.append(self)
        if friend:
            #mettre le sprite ami
            self.orig_image = pygame.image.load(var.img_blue_player).convert_alpha()
            self.image = pygame.image.load(var.img_blue_player).convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
            self.mask = pygame.mask.from_surface(self.image)
        else:
            #mettre le sprite ennemi 
            self.orig_image = pygame.image.load(var.img_red_player).convert_alpha()
            self.image = pygame.image.load(var.img_red_player).convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
            self.mask = pygame.mask.from_surface(self.image)
        
        self.friendly = friend
    
    def shoot(self):
        if len(self.missileList) < self.MAXMISSILE:
            super().shoot()


    def clic(self,position):
        self.xDest = position[0]
        self.yDest = position[1]

class IaPlane(Plane):
    def __init__(self,x,y,friend,active = True):
        super().__init__(x,y)
        self.MAXSPEED = 1.5
        self.RELOADTIME = 30
        self.MAXMISSILE = 3
        self.agro = None
        self.active = active
        if friend:
            #mettre le sprite ami
            self.orig_image = pygame.image.load(var.img_blue_IA).convert_alpha()
            self.image = pygame.image.load(var.img_blue_IA).convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
            self.mask = pygame.mask.from_surface(self.image)
        else:
            #mettre le sprite ennemi
            self.orig_image = pygame.image.load(var.img_red_IA).convert_alpha()
            self.image = pygame.image.load(var.img_red_IA).convert_alpha()
            self.rect = self.image.get_rect(center=(x,y))
            self.mask = pygame.mask.from_surface(self.image)
        self.friendly = friend
    
    def tick(self):
        if self.active:
            if self.searchAgro():#cherche agro et renvoie true si trouve
                if utility.getDistance(self,self.agro) < 150 and len(self.missileList)<self.MAXMISSILE and self.timeAlive%self.RELOADTIME==0 and self.timeAlive != 0:
                    #si à moins de 150, et qu'il a moins de 3 missiles en vie et que son tmps de vie est divisible
                    #  par RELOADTIME(pour ajouter délai)
                    self.shoot()
                
            objectNear = self.testObjectNear()
            if objectNear:
                self.xDest = self.x-(objectNear.x-self.x)
                self.yDest = self.y-(objectNear.y-self.y)
            else:
                if not self.goAgro():#renvoie True si elle va à l'agro
                    self.xDest = self.x #sinon on immobilise
                    self.yDest = self.y

            super().tick()
            

    def testObjectNear(self):
        minima = 99999999 #valeur très haute, toujours supérieur à distance
        temp = 99999999 #valeur très haute, toujours supérieur à temp
        minObj = None
        for objet in var.refreshList:#test de la distance minimlale
            if objet != self:#si l'objet le plus proche n'est pas lui meme
                temp = utility.getDistance(self,objet)#calcul distance
            if temp < minima:
                minima = temp
                minObj = objet#on a l'objet le plus proche
        if minima < 75:#si l'objet est à moins de 50
            return minObj
        else:
            return None
        
    def goAgro(self):
        if not self.agro:# si la dest n'est pas définie, rien faire
            return False
        self.xDest = self.agro.x
        self.yDest = self.agro.y
        return True

    def searchAgro(self):
        ennemyList = []
        for objet in var.refreshList:
            if type(objet)!= Missile and objet.friendly != self.friendly:#test si objet non missile et si il est pas de son camp
                ennemyList.append(objet)

        if ennemyList:#si la liste n'est pas vide
            minima = 99999999 #valeur très haute, toujours supérieur à distance
            minObj = None
            for objet in ennemyList:#test de la distance minimlale
                temp = utility.getDistance(self,objet)#calcul distance
                if temp < minima:
                    minima = temp
                    minObj = objet
            self.agro = minObj
            return True
        else:
            self.agro = None
            return False
    

class Missile():
    def __init__(self,creator):

        print("Missile created")
        self.creator = creator
        angle = self.creator.angle
        xVector = self.creator.xVector
        yVector = self.creator.yVector
        x = self.creator.x
        y = self.creator.y

        xAngle,yAngle = utility.getCoords(angle)
        self.xVector=utility.plafonne(xVector*2 + xAngle*30,40,True)
        self.xVector=utility.plafonne(xVector*2 + xAngle*30,-40,False)
        self.yVector=utility.plafonne(yVector*2 + yAngle*30,40,True)
        self.yVector=utility.plafonne(yVector*2 + yAngle*30,-40,False)
        self.x = x
        self.y = y
        self.speed = 0
        self.timeAlive = 0

        pygame.sprite.Sprite.__init__(self)
        self.orig_image = pygame.image.load("sprite_missile.png").convert_alpha()
        self.image = pygame.image.load("sprite_missile.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle#l'angle natif de l'image
        var.refreshList.append(self)
    
    def vectorTo(self,vector):#décélération proressive du missile
        return vector/((self.timeAlive/20)+1)
    
    def goTo(self):

        self.xVector = self.vectorTo(self.xVector)
        self.yVector = self.vectorTo(self.yVector)
        
        self.x += self.xVector
        self.y -= self.yVector #c'est un moins car l'origine des y n'est pas en bas mais en haut
    
    def tick(self):
        self.timeAlive += 1
        #si vecteurs pas trop faibles, et timeAlive pas trop grand, bouger sinon s'arrete
        if not(((-1.5<self.xVector < 1.5) and (-1.5<self.yVector < 1.5))or ( self.timeAlive > 500)):
            self.goTo()
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            self.delete()
    
    def turn(self):
        utility.rotate(self,self.angle)# on le tourne de cet angle
    
    def delete(self):
        if self in self.creator.missileList:
            self.creator.missileList.remove(self)
        self.image.fill((0,0,0,0))
        if self in var.hitList:
            var.hitList.remove(self)
        if self in var.refreshList:
            var.refreshList.remove(self)
        if self in var.playerList:
            var.playerList.remove(self)
        del self

