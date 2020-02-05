from tkinter import *
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
        
        vector = utility.plafonne(vector + distanceToDest,3,True)
        vector = utility.plafonne(vector + distanceToDest,-3,False)
        
        return vector

    def scalaireToVector(self,xDistanceToDest,yDistanceToDest):
        norme = math.sqrt(xDistanceToDest**2+yDistanceToDest**2)
        try:
            angle = math.asin( yDistanceToDest/norme)
        except:
            angle = math.asin(yDistanceToDest)
        vector = (norme,angle)
        print((norme,angle))
        return vector

    def vectorToScalaire(self,vector):
        norme,angle = vector
        if 0.5 < angle < 1.5 or -1.5 < angle < -0.5:
            xDistance = math.cos(-angle+math.pi)*norme
        else:
            xDistance = math.cos(-angle)*norme
        
        yDistance = math.sin(-angle+math.pi)*norme
        return xDistance,yDistance

    def vectorTo(self,vector):
        norme,angle = vector


    
    def goTo(self,xDest,yDest):
        x,y,xosef,yosef=Canevas.coords(self.graphicPlane)
        xDistanceToDest=xDest-x
        yDistanceToDest=yDest-y
            
        self.xVector = self.scalaireTo(self.xVector,xDistanceToDest)
        self.yVector = self.scalaireTo(self.yVector,yDistanceToDest)

        #test vecteur
        #vectorToDest = self.scalaireToVector(xDistanceToDest,yDistanceToDest)
        #xVectorToDest,yVectorToDest = self.vectorToScalaire(vectorToDest)
        #print(xVectorToDest,yVectorToDest)

        self.x += self.xVector
        self.y += self.yVector

        xDistanceToDest -= self.xVector
        yDistanceToDest -= self.yVector

        Canevas.move(self.graphicPlane,self.xVector,self.yVector)

        if not((5 > xDistanceToDest > -5) and (5 > yDistanceToDest > -5)):
            return False #continue
        else:# s'arrete
            self.xVector = 0
            self.yVector = 0
            return True

    def shoot(self,x,y):
        if not(hasattr(self,"Mymissile")):
            print("player shoot")
            self.Mymissile = Missile(Canevas,self.x,self.y)
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
        self.graphicPlane = Canevas.create_rectangle(x,y,x+10,y+10,outline='black',fill=color)

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
    def __init__(self,x,y,color,friend):
        super().__init__(x,y,color)
        self.graphicPlane = Canevas.create_oval(x-50,y-50,x+50,y+50,outline='black')
        self.friendly = friend
        

    def trajectoirePatterne(self,x1,y1,x2,y2,nombre = 10):
        if nombre > 1:
            self.goTo(x1,x2)
            self.goTo(x2,y2)
            fenetre.after_idle(self.trajectoirePatterne(x1,y1,x2,y2,nombre-1))

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

fenetre = Tk()
fenetre.title("Yatangaki")
Canevas = Canvas(fenetre, width = 500, height =500, bg ='white')
Canevas.focus_set()
Canevas.pack(padx =5, pady =5)


##debut des evenements

Player = PlayerPlane(250,230,'blue')
#Ennemy = IaPlane(250,270,"red",False)
#fenetre.after_idle(Ennemy.trajectoirePatterne(150,230,350,370))

Canevas.bind('<Button-1>',Player.clic)## clic gauche : graphicPlane bouge
Canevas.bind('<Control-Button-1>',Player.shootClic)##control clic gauche : graphicPlane lance un missile



## fin des evenements
fenetre.mainloop()