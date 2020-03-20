import socket 

hote = 'localhost'
port = 6969
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Famille d'adresses, type du socket et de protocole
connexion_avec_serveur.connect((hote, port)) #Permet d'attendre des connexions de clients en utilisant le tuple (nom_hote, port)
print("Connecte")


msg_a_envoyer = b''
while msg_a_envoyer != b'disconnect':
    msg_a_envoyer = input("> ")
    msg_a_envoyer.encode() #transforme une chaine str en chaine bytes
    connexion_avec_serveur.send(msg_a_envoyer) #la chaine doit etre en bytes pour que send fonctionne
    msg_a_envoyer = connexion_avec_serveur.recv(1024)
    msg_recu = msg_recu.decode() #transforme une chaine bytes en chaine str
    position = msg_recu

print("disconnected")
connexion_avec_serveur.close()