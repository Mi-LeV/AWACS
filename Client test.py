import socket 

hote = 'localhost'
port = 6969
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
connexion_avec_serveur.connect((hote, port))


msg_a_envoyer = b''
while msg_a_envoyer =! b'disconnect'
    msg_a_envoyer = input("> ")
    msg_a_envoyer.encode()
    connexion_avec_serveur.send(msg_a_envoyer)
    msg_a_envoyer = connexion_avec_serveur.recv(1024)
    msg_recu = msg_recu.decode()
    position(x, y)
    position = msg_recu

print("disconnected")
connexion_avec_serveur.close()
