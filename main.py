import random
from blessed import Terminal
from colored import fg, bg, attr

# Initialisation du terminal
term = Terminal()

def read_file(file_name: str) -> dict:
    
    """ This function reads the file type .drk and returns a dictionary containing the data ( map, altars, apprentices, eggs).
    
        Parameters:
        -----------
         file_name (str): the name of the file to read. 
    
        returns:
        --------
         data (dict): a dictionary containing the various data of the file (map, altars, apprentices, eggs)
    """
    
    
    
    data = {
        "map": None,
        "altars": {},
        "apprentices": {},
        "eggs": {}
    }
    
    
    section = None  # Suivi de la section active
    errors = []  # Liste pour stocker les erreurs 
    file = open(file_name, "r") 
    
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
                    check_position(x,y,positions,errors)

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
                    check_position(x,y,positions,errors)

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
                    check_position(x,y,positions,errors)

                    data["eggs"][(x, y)] = {
                        "nom": nom, "tours": tours, "pv": pv,
                        "attaque": attaque, "portee": portee, "regen": regen
                    }
                    positions["eggs"].append((x, y))

    file.close()  # Fermer le fichier après lecture

    # Afficher toutes les erreurs si elles existent
    if errors:
        error_messages = "\n".join(errors)
        raise ValueError(f" Erreurs détectées lors de la lecture du fichier:\n{error_messages}")

    return data

def check_position(x : int, y: int, dict : list, errors):
    """ This function checks if the position is valid or not. 
    
        Parameters:
        -----------
         x (int): the x coordinate of the position to check.
         y (int): the y coordinate of the position to check.
         dict (list): a dictionary that contains all the positions of the elements on the board.
         errors (list): a list that contains all the errors detected during the reading of the file.
    
        Returns:
        --------
         None
    """
    
    if (x, y) in dict["altars"] :
        errors.append(f"❌ Position déjà occupée par un altar : ({x}, {y})")
    
    elif (x,y) in dict["apprentices"] :
        errors.append(f"❌ Position déjà occupée par un apprenti: ({x}, {y})")
    
    else:
        errors.append(f"❌ Position déjà occupée par un œuf : ({x}, {y})")

def init_board(data):
    """ 
    initalizes the board with the data read from the file.drk.

    Parameters:
    ------------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    list: a list of lists representing the board
    """
    largeur = data["map"][0]
    hauteur = data["map"][1]

    board = []  # Initialiser le plateau vide
    for i in range(hauteur):
        board.append([])
        for j in range(largeur):
            board[i].append([])
        

    # Placer les différents éléments sur le plateau
    place_altars(board, data)
    place_apprentices(board, data)
    place_eggs(board, data)

    return board


def place_altars(board, data):
    """
    place the alrars on the board.

    Parameters:
    ------------
    board (list): the board of the game.
    data (dict):  the data containing the altars.
    """
    for joueur, (x, y) in data["altars"].items():
        if 1 <= x <= len(board) and 1 <= y <= len(board[0]):  # Vérifier les coordonnées
            board[x-1][y-1].append({
                "type": "altar",
                "player": joueur
            })
        else:
            print(f"❌ Erreur: Coordonnées invalides pour l'altar du joueur {joueur} : ({x}, {y})")


def place_apprentices(board, data):
    """
    place the apprentices on the board.

    Parameters:
    ------------
    board (list): the board of the game.
    data (dict): the data containing the apprentices.
    """
    for joueur, apprentices in data["apprentices"].items():
        for apprentice in apprentices:
            x, y = apprentice["position"]
            if 1 <= x <= len(board) and 1 <= y <= len(board[0]):  # Vérifier les coordonnées
                board[x-1][y-1].append({
                    "type": "apprenti",
                    "nom": apprentice["nom"],
                    "joueur": joueur,
                    "pv": apprentice["pv"],
                    "regen": apprentice["regen"]
                })
            else:
                print(f"❌ Erreur: Coordonnées invalides pour l'apprenti {apprentice['nom']} : ({x}, {y})")


def place_eggs(board, data):
    """
    place the eggs on the board.
    
    Parameters:
    ------------
    board (list): the board of the game.
    data (dict): the data containing the eggs.
    """
    for (x, y), egg in data["eggs"].items():
        if 1 <= x <= len(board) and 1 <= y <= len(board[0]):  # Vérifier les coordonnées
            board[x-1][y-1].append({
                "type": "egg",
                "nom": egg["nom"],
                "tours": egg["tours"],
                "pv": egg["pv"],
                "attaque": egg["attaque"],
                "portee": egg["portee"],
                "regen": egg["regen"]
            })
        else:
            print(f"❌ Erreur: Coordonnées invalides pour l'œuf {egg['nom']} : ({x}, {y})")


def display_board(board):
    """
    This functions allows us to print the board in the terminal .

    Parameters:
    ----------
        board (list): a list of lists representing the board game.
        Each game board square is a list of dictionaries that could contain one or more elements of the game in the board. 
        
    """

    # 1. Effacer l'écran pour un affichage propre
    print(term.clear)

    # 2. Parcourir chaque ligne du board
    for i in range(len(board)):  # i est l'indice de la ligne
        # 3. Parcourir chaque case de la ligne
        for j in range(len(board[i])):  # j est l'indice de la colonne
            # 4. Déplacer le curseur à la position (j * 2, i)
            # Cela permet d'afficher les éléments au bon endroit dans le terminal.
            print(term.move_xy(j * 2, i), end="")

            # 5. Vérifier ce qui se trouve dans la case et l'afficher
            # On parcourt manuellement les éléments de la case pour déterminer ce qui doit être affiché.
            afficher_element = "."  # Par défaut, la case est vide
            case = board[i][j]  # Récupérer la case actuelle
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

        # 7. Passer à la ligne suivante après avoir affiché une ligne du board
        print()

    # 8. Afficher une légende pour expliquer les symboles
    print(term.move_xy(0, len(board) + 1))  # Déplacer le curseur en bas du board
    print(term.bold("Légende :"))  # Titre de la légende en gras
    print(term.red("🏰 = altar"), term.blue("🧙 = Apprentis"), term.yellow("🥚 = Œufs"), term.green("🐉 = Dragons"))



def tri_orders (orders : str) -> list:
    """ This function will allow us to sort out the different instructions received by the player. 

    Parameters : 
    ------------
    orders (str): the orders received by the player 

    Returns : 
    ---------
    orders_tri (list) : a list of the instructions by order
"""
    orders = orders.split(" ")
    orders_tri = []
    
    for order in orders:
        order = order.strip()
        
        if ":x" in order:
            try : 
                name , direction = order.split(":x")
                directions_valides = {"N", "NE", "E", "SE", "S", "SW", "W" , "NW"}
                if direction in directions_valides:
                    orders_tri.append({
                        "type": "attack",
                        "name": name,
                        "direction": direction
                    })
                else:
                    print(f"Direction invalide pour l'attaque : {direction}")
            
            except ValueError:
                print(f" Erreur: Attaque invalide : {order}")
        
        elif ":@" in order :
            try : 
                name , position = order.split(":@")
                r, c = position.split("-")
                orders_tri.append({
                    "type": "move",
                    "name": name,
                    "row": int(r),
                    "col": int(c)
                })
            except ValueError:
                print(f" Erreur: Déplacement invalide : {order}")
        elif order =="summon":
            orders_tri.append({
                "type": "summon"
            })
            
        else:
            print(f" Erreur: Ordre invalide ignoré : {order}")
            
    return orders_tri

    

    
    
    
def move (order : str):
    """ This function receives the order to move the player's dragons and apprentices to the desired position. 

    Parameters :
    ------------
    order (str): the order received by the player to move
    
    Returns :
    ---------
    None 

    """
    


def check_valid_move (x : int, y : int) -> bool:
    """ This function checks if the move is valid or not. 

    Parameters : 
    ------------
    x (int): the x coordinate of the move 
    y (int): the y coordinate of the move 

    Returns : 
    ---------
    bool : True if the move is valid, False otherwise
    """

def attack (order : str):
    """ This function receives the order to attack and allows the dragon to attack the other dragons or the apprentices within his range. 

    Parameters : 
    ------------
    order (str): the order received by the player to attack 

    Returns : 
    ---------
    None 

    """
    

def summon (data): 
    """ This function receives the order to summon the player's dragons and apprentices to his altar.

    Parameters : 
    ------------
    data : a dictionnary that contains all the board informations. 

    Returns : 
    ---------
    None 

    """


def regenerate(board):
    

    """ This function allows the dragons and the apprentices to regenerate their health points.

    Parameters : 
    ------------
    board (list): the board of the game. 

    Returns : 
    ---------
    None 

    """