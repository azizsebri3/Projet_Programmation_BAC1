import random
from blessed import Terminal

# Initialisation du terminal
term = Terminal()

def lire_fichier_drk(nom_fichier: str) -> dict:
    """Lire le fichier et retourner un dictionnaire contenant les données du jeu
    
    paramètres:
        nom_fichier :(str) : le nom du fichier à lire
        
        
    retourne:
        dict : un dictionnaire contenant les données du jeu (map, altars, apprentices, eggs)
    . """
    
    jeu = {
        "map": None,
        "altars": {},
        "apprentices": {},
        "eggs": {}
    }

    section = None  # Suivi de la section active
    fichier = open(nom_fichier, "r")  # Ouvrir le fichier
    
    for ligne in fichier:
        ligne = ligne.strip()  # Supprimer les espaces

        if ligne == "":
            pass  # Ignorer les lignes vides
        elif ligne.startswith("#"):
            pass  # Ignorer les commentaires
        elif ligne == "map:" or ligne == "altars:" or ligne == "apprentices:" or ligne == "eggs:":
            section = ligne  # Mise à jour de la section
        else:
            # Lire les données selon la section actuelle
            if section == "map:":
                parties = ligne.split()
                largeur = int(parties[0])
                hauteur = int(parties[1])
                jeu["map"] = (largeur, hauteur)

            elif section == "altars:":
                parties = ligne.split()
                id_joueur = int(parties[0])
                x = int(parties[1])
                y = int(parties[2])
                jeu["altars"][id_joueur] = (x, y)

            elif section == "apprentices:":
                parties = ligne.split()
                id_joueur = int(parties[0])
                nom = parties[1]
                x = int(parties[2])
                y = int(parties[3])
                pv = int(parties[4])
                regen = int(parties[5])

                if id_joueur not in jeu["apprentices"]:
                    jeu["apprentices"][id_joueur] = []

                jeu["apprentices"][id_joueur].append({
                    "nom": nom, "position": (x, y), "pv": pv, "regen": regen
                })

            elif section == "eggs:":
                parties = ligne.split()
                nom = parties[0]
                x = int(parties[1])
                y = int(parties[2])
                tours = int(parties[3])
                pv = int(parties[4])
                attaque = int(parties[5])
                portee = int(parties[6])
                regen = int(parties[7])

                jeu["eggs"][(x, y)] = {
                    "nom": nom, "tours": tours, "pv": pv,
                    "attaque": attaque, "portee": portee, "regen": regen
                }

    fichier.close()  # Fermer le fichier après lecture
    return jeu

# dessin plateau avec blessed 

def dessiner_plateau(map : tuple):
    """Dessiner le plateau de jeu 
    paramètres:
        map : tuple : la taille du plateau de jeu (largeur, hauteur)
        
    retourne:
        None
    """
    largeur, hauteur = map
    for i in range(hauteur):
        for j in range(largeur):
            print("🟦", end="")
        print()
#juste hetha test ll fonction lola temchi wala le !
#donnees = lire_fichier_drk("plateau.drk")
#dessiner_plateau(donnees["map"])

