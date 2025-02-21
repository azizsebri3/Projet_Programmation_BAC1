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
                        errors.append(f"❌ Erreur: altar du joueur {id_joueur} en conflit avec un autre altar à ({x}, {y})")
                    if (x, y) in positions["apprentices"]:
                        errors.append(f"❌ Erreur: altar du joueur {id_joueur} en conflit avec un apprenti à ({x}, {y})")
                    if (x, y) in positions["eggs"]:
                        errors.append(f"❌ Erreur: altar du joueur {id_joueur} en conflit avec un œuf à ({x}, {y})")

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
                        errors.append(f"❌ Erreur: Apprenti {nom} en conflit avec un altar à ({x}, {y})")
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
                        errors.append(f"❌ Erreur: Œuf {nom} en conflit avec un altar à ({x}, {y})")
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

    return data

def initialiser_plateau(data):
    """initilze the board with the data read from the file
    

    Args:
        data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
        list: a list of lists representing the board
    """
    largeur,hauteur = data["map"]

    # Créer le plateau vide
    plateau = []
    
    for i in range(hauteur):
        ligne = []
        for j in range(largeur):
            ligne.append([]) # chaque case de plateu est un list (car on peut trouver deux element sur la meme case :) ) 
        plateau.append(ligne)

    # Placer les altars
    for joueur, (x, y) in data["altars"].items():
        if 1 <= x <= hauteur and 1 <= y <= largeur:  # Vérifier les coordonnées
            plateau[x-1][y-1].append({
                "type" : "altar",
                "player" :joueur 
            })
        else:
            print(f"❌ Erreur: Coordonnées invalides pour l'altar du joueur {joueur} : ({x}, {y})")

    # Placer les apprentis
    for joueur, apprentices in data["apprentices"].items():
        for apprentice in apprentices:
            x, y = apprentice["position"]
            if 1 <= x <= hauteur and 1 <= y <= largeur:  # Vérifier les coordonnées
                plateau[x-1][y-1].append({
                    "type" : "apprenti" ,
                    "nom": apprentice["nom"],
                    "joueur": joueur,
                    "pv": apprentice["pv"],
                    "regen": apprentice["regen"]
                })
            else:
                print(f"❌ Erreur: Coordonnées invalides pour l'apprenti {apprentice['nom']} : ({x}, {y})")

    # Placer les œufs
    for (x, y), egg in data["eggs"].items():
        if 1 <= x <= hauteur and 1 <= y <= largeur:  # Vérifier les coordonnées
            plateau[x-1][y-1].append({
                "type" : "egg" ,
                "nom": egg["nom"],
                "tours": egg["tours"],
                "pv": egg["pv"],
                "attaque": egg["attaque"],
                "portee": egg["portee"],
                "regen": egg["regen"]
            })
        else:
            print(f"❌ Erreur: Coordonnées invalides pour l'œuf {egg['nom']} : ({x}, {y})")

    return plateau
 

def afficher_plateau(plateau):
    """
    Affiche le plateau de jeu dans le terminal avec des emojis et des couleurs.
    Cette version est conçue pour être facile à comprendre pour des étudiants.

    Parameters:
        plateau (list): Une liste de listes représentant le plateau de jeu.
                       Chaque case du plateau est une liste de dictionnaires décrivant les éléments présents.
    """
    # 1. Effacer l'écran pour un affichage propre
    print(term.clear)

    # 2. Parcourir chaque ligne du plateau
    for i in range(len(plateau)):  # i est l'indice de la ligne
        # 3. Parcourir chaque case de la ligne
        for j in range(len(plateau[i])):  # j est l'indice de la colonne
            # 4. Déplacer le curseur à la position (j * 2, i)
            # Cela permet d'afficher les éléments au bon endroit dans le terminal.
            print(term.move_xy(j * 2, i), end="")

            # 5. Vérifier ce qui se trouve dans la case et l'afficher
            # On parcourt manuellement les éléments de la case pour déterminer ce qui doit être affiché.
            afficher_element = "."  # Par défaut, la case est vide
            case = plateau[i][j]  # Récupérer la case actuelle
            for element in case:
                if element["type"] == "altar":
                    afficher_element = term.bold_red("🏰")  # altar en rouge
                    break  # On affiche l'altar en priorité
                elif element["type"] == "apprenti":
                    afficher_element = term.bold_blue("🧙")  # Apprenti en bleu
                elif element["type"] == "egg":
                    afficher_element = term.bold_yellow("🥚")  # Œuf en jaune
                elif element["type"] == "dragon":
                    afficher_element = term.bold_green("🐉")  # Dragon en vert

            # 6. Afficher l'élément de la case avec un espace pour la lisibilité
            print(afficher_element, end=" ")

        # 7. Passer à la ligne suivante après avoir affiché une ligne du plateau
        print()

    # 8. Afficher une légende pour expliquer les symboles
    print(term.move_xy(0, len(plateau) + 1))  # Déplacer le curseur en bas du plateau
    print(term.bold("Légende :"))  # Titre de la légende en gras
    print(term.red("🏰 = altar"), term.blue("🧙 = Apprentis"), term.yellow("🥚 = Œufs"), term.green("🐉 = Dragons"))

def main():
    # Lire les données du fichier
    data = read_file("plateau.drk")
    if data is None:
        return

    # Initialiser le plateau
    plateau = initialiser_plateau(data)

    # Afficher le plateau
    afficher_plateau(plateau)

if __name__ == "__main__":
    main()


