import random
from blessed import Terminal
from colored import fg, bg, attr

# Initialisation du terminal
term = Terminal()

def read_file(file_name: str) -> dict:
    """ read file type .drk and return a dictionary of data ( map, altars, apprentices, eggs)
    
    parameters:
        file_name (str): the name of the file to read 
    
    returns:
        dict: a dictionary containing the data of the file (map, altars, apprentices, eggs)
    """
    
    data = {
        "map": None,
        "altars": {},
        "apprentices": {},
        "eggs": {}
    }

    section = None  # Suivi de la section active
    errors = []  # Liste pour stocker les erreurs au lieu d'utiliser return immédiatement
    file = open(file_name, "r")  # Ouvrir le fichier
    
    # Dictionnaire des positions déjà occupées
    positions = {
        "altars": [],
        "apprentices": [],
        "eggs": []
    }

    for line in file:
        line = line.strip()  # Supprimer les espaces
        
        if line != "":
            if line in ["map:", "altars:", "apprentices:", "eggs:"]:
                section = line  # Mise à jour de la section
            else:
                # Lire les données selon la section actuelle
                if section == "map:":
                    parties = line.split()
                    largeur = int(parties[0])
                    hauteur = int(parties[1])
                    data["map"] = (largeur, hauteur)

                elif section == "altars:":
                    parties = line.split()
                    id_joueur = int(parties[0])
                    x = int(parties[1])
                    y = int(parties[2])
                    
                    # Vérification des conflits
                    if (x, y) in positions["altars"]:
                        errors.append(f"❌ Erreur: Autel du joueur {id_joueur} en conflit avec un autre autel à ({x}, {y})")
                    if (x, y) in positions["apprentices"]:
                        errors.append(f"❌ Erreur: Autel du joueur {id_joueur} en conflit avec un apprenti à ({x}, {y})")
                    if (x, y) in positions["eggs"]:
                        errors.append(f"❌ Erreur: Autel du joueur {id_joueur} en conflit avec un œuf à ({x}, {y})")

                    data["altars"][id_joueur] = (x, y)
                    positions["altars"].append((x, y))

                elif section == "apprentices:":
                    parties = line.split()   
                    id_joueur = int(parties[0])
                    nom = parties[1]
                    x = int(parties[2])
                    y = int(parties[3])
                    pv = int(parties[4])
                    regen = int(parties[5])
                    
                    # Vérification des conflits
                    if (x, y) in positions["altars"]:
                        errors.append(f"❌ Erreur: Apprenti {nom} en conflit avec un autel à ({x}, {y})")
                    if (x, y) in positions["apprentices"]:
                        errors.append(f"❌ Erreur: Apprenti {nom} en conflit avec un autre apprenti à ({x}, {y})")
                    if (x, y) in positions["eggs"]:
                        errors.append(f"❌ Erreur: Apprenti {nom} en conflit avec un œuf à ({x}, {y})")

                    if id_joueur not in data["apprentices"]:
                        data["apprentices"][id_joueur] = []

                    data["apprentices"][id_joueur].append({
                        "nom": nom, "position": (x, y), "pv": pv, "regen": regen
                    })
                    positions["apprentices"].append((x, y))

                elif section == "eggs:":
                    parties = line.split()
                    nom = parties[0]
                    x = int(parties[1])
                    y = int(parties[2])
                    tours = int(parties[3])
                    pv = int(parties[4])
                    attaque = int(parties[5])
                    portee = int(parties[6])
                    regen = int(parties[7])
                    
                    # Vérification des conflits
                    if (x, y) in positions["altars"]:
                        errors.append(f"❌ Erreur: Œuf {nom} en conflit avec un autel à ({x}, {y})")
                    if (x, y) in positions["apprentices"]:
                        errors.append(f"❌ Erreur: Œuf {nom} en conflit avec un apprenti à ({x}, {y})")
                    if (x, y) in positions["eggs"]:
                        errors.append(f"❌ Erreur: Œuf {nom} en conflit avec un autre œuf à ({x}, {y})")

                    data["eggs"][(x, y)] = {
                        "nom": nom, "tours": tours, "pv": pv,
                        "attaque": attaque, "portee": portee, "regen": regen
                    }
                    positions["eggs"].append((x, y))

    file.close()  # Fermer le fichier après lecture

    # Afficher toutes les erreurs si elles existent
    if errors:
        for error in errors:
            print(error)
        return None  # Retourner None pour indiquer un problème

    print(data)





# Lire le file de données
read_file("plateau.drk")




