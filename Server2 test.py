import socket 
import select


hote = ''
port = 6969

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Famille d'adresses, type du socket et de protocole
connexion_principale.bind((hote, port)) #Permet d'attendre des connexions de clients en utilisant le tuple (nom_hote, port)
connexion_principale.listen(5)

serveur_lance = True
clients_connectes = []

while serveur_lance:
    connexion_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)

    for connexion in connexion_demandees:
        connexion_avec_client, infos_connexion = connexion_principale.accept()
        clients_connectes.append(connexion_avec_client)
    
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], 0.05)
    except select.error
        pass
    else:
        for client in clients_a_lire:
            msg_recu = client.recv(1024)
            msg_recu = msg_recu.decode()
            client.send(b"recu")
            if msg_recu == "disconnect":
                serveur_lance = False
            position(x, y)
            position = msg_recu
            msg_a_envoyer = position
            msg_a_envoyer = msg_a_envoyer.encode()
            client.send(msg_a_envoyer)


print("disconnected")
for client in clients_connectes:
    client.close()

connexion_principale.close()