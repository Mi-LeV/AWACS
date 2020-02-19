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
        return 360-math.degrees(theta)
    
    @staticmethod
    def rotate(objet,angle):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        objet.sprite = pygame.transform.rotozoom(objet.orig_sprite, objet.angle + angle, 1)
        # Create a new rect with the center of the old rect.
        objet.rect = objet.sprite.get_rect(center=objet.rect.center)

class Plane:
    def __init__(self,x,y):
        print("Plane created")
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
        var.refreshList.append(self)


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
        print("gotick")
        xDistanceToDest=self.xDest-self.x
        yDistanceToDest=self.yDest-self.y
        if not((3 > xDistanceToDest > -3) and (3 > yDistanceToDest > -3)):
            self.goTo(xDistanceToDest,yDistanceToDest)
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            return True


    def shoot(self,x,y):
        print("player shoot")
        self.Mymissile = Missile(self.x,self.y)
        self.Mymissile.xDest = x
        self.Mymissile.yDest = y

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
        self.sprite
        self.xVector=0
        self.yVector=0
        self.xDest = x
        self.yDest = y
        self.x = x
        self.y = y
        var.refreshList.append(self)
    

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
        print("gotick")
        xDistanceToDest=self.xDest-self.x
        yDistanceToDest=self.yDest-self.y
        if not((3 > xDistanceToDest > -3) and (3 > yDistanceToDest > -3)):
            self.goTo(xDistanceToDest,yDistanceToDest)
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            #self.sprite = pygame.image.fromstring("")
            del self