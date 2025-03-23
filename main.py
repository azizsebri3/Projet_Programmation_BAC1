import time
from blessed import Terminal
from colored import fg, bg, attr
import random
#from remote_play import create_connection, get_remote_orders, notify_remote_orders, close_connection

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
        "eggs": {} ,
        "tours_sans_damage" : 0,
        "dragons" : {}
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
    

    return data

def check_position(x : int, y: int, data : list, errors : list):
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
    
    if (x, y) in data["altars"] :
        errors.append(f"Position déjà occupée par un altar : ({x}, {y})")
    
    elif (x,y) in data["apprentices"] :
        errors.append(f"Position déjà occupée par un apprenti: ({x}, {y})")
    
    else:
        errors.append(f"Position déjà occupée par un œuf : ({x}, {y})")

def create_board(file_name: str) -> list:
    """ 
    initalizes the board with the data read from the file.drk.

    Parameters:
    ------------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    list: a list of lists representing the board
    """
    data = read_file(file_name)
    data["tours"] = 1
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

    return board , data


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
            print(f"Erreur: Coordonnées invalides pour l'altar du joueur {joueur} : ({x}, {y})")


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
        




def horizontal_line(largeur : int, left_char :str, mid_char:str, right_char:str) -> str:
    """this function returns a horizontal line with the specified characters.

    Args:
        largeur (int): the width of the line.
        left_char (str): the character to use for the left side.
        mid_char (str): the middle character to use.
        right_char (str): the character to use for the right side.

    Returns:
        line(str): the horizontal line.
    """
    line = left_char
    for col in range(largeur - 1):
        line += "═══" + mid_char
    line += "═══" + right_char
    return line

def get_cell_content(cell):
    """this function returns the content of a cell on the board.
   by prioritizing the elements to display. altars > apprentices > eggs > dragons.
   
    parameters:
    ------------
        cell (list): the content of the cell.
    """
    
    if not cell:
        return " . "  # Case vide
    
    # On parcourt les éléments pour décider lequel afficher
    content = " . "
    for element in cell:
        if element["type"] == "altar":
            # On met un break pour prioriser l'autel s'il est présent
            return term.bold_red("🏰 ")
        elif element["type"] == "apprenti":
            # On remplace le contenu, mais on ne break pas (au cas où un autel apparaît après ?)
            content = term.bold_blue("🧙 ")
        elif element["type"] == "egg":
            # On remplace le contenu, si pas d'apprenti ni d'autel
            content = term.bold_yellow("🥚 ")
        elif element["type"] == "dragon":
            # On remplace le contenu, si pas d'autel/apprenti/oeuf
            content = term.bold_green("🐉 ")
    return content

def display_board(data : dict , board : list[list]):
    """show the board on the screen.
    
    parameters:
    -----------
        board (list): the board of the game.
    
    returns:
    --------
        None
    
    version : 2.0
     specifications : Ahmed Feki (v1 21/02/2025)
     implementation : Mohamed Aziz Sebri (v2 19/03/2025)
    """
    print(term.home + term.clear)  # Nettoyer l'écran, cacher le curseur
    print(term.center(term.bold(term.red(f"La Tour Actuelle : {data["tours"]} "))))
    hauteur = len(board)
    largeur = 0
    if hauteur > 0 :
        largeur = len(board[0])
    else:
        largeur = 0

    # Lignes de bordure (haut, séparateur intermédiaire, bas)
    top_line    = horizontal_line(largeur, '╔', '╦', '╗')
    mid_line    = horizontal_line(largeur, '╠', '╬', '╣')
    bottom_line = horizontal_line(largeur, '╚', '╩', '╝')

    # Collecter les informations sur les cases avec plusieurs éléments
    multi_element_cases = []
    for i in range(hauteur):
        for j in range(largeur):
            if len(board[i][j]) > 1:  # Si plus de 2 éléments
                case_info = f"Case ({i+1},{j+1}): "
                elements = {}
                for element in board[i][j]:
                    if element["type"] not in elements:
                        elements[element["type"]] = 1
                    else:
                        elements[element["type"]] += 1
                
                for elem_type, count in elements.items():
                    if elem_type == "apprenti":
                        case_info += f"🧙 x {count} "
                    elif elem_type == "dragon":
                        case_info += f"🐉 x {count} "
                    elif elem_type == "egg":
                        case_info += f"🥚 x {count} "
                    elif elem_type == "altar":
                        case_info += f"🏰 x {count} "
                
                multi_element_cases.append(case_info)
   
    print(top_line)

    for i in range(hauteur):
        # Construire la ligne de contenu : ex: ║ . ║ 🏰 ║ 🧙 ║
        row_str = ""
        for j in range(largeur):
            cell_content = get_cell_content(board[i][j])
            row_str += "║" + cell_content
        row_str += "║"  # Fin de la ligne
        print(row_str)

        # time.sleep(0.01)  # Petite pause pour effet "dynamique"

        # Après chaque rangée, si ce n'est pas la dernière, on affiche une ligne intermédiaire
        if i < hauteur - 1:
            print(mid_line)

    
    print(bottom_line)

    # ─────────────────────────────────────────────────────────────────────────
    # 4) Affichage de la légende
    print()
    print(term.bold("Légende :"))
    print(
        term.red("🏰 = Autel  "),
        term.blue("🧙 = Apprenti  "),
        term.yellow("🥚 = Œuf  "),
        term.green("🐉 = Dragon"),
        sep="\n"
    )
    
    # 5) Affichage des cases avec plusieurs éléments (si nécessaire)
    if multi_element_cases:
        print()
        print(term.bold("Cases avec plusieurs éléments :"))
        for case_info in multi_element_cases:
            print(case_info)

    # 6) Attente des ordres du joueur
    print()

    print("En attente des ordres du joueur... ", end="", flush=True)
    time.sleep(0.5)
    
def get_orders(data: list[dict], board: list[list], current_player: int ,player_type:str) -> list[dict]:
    """ this function receives the orders from the player or the AI and returns a list of dictionaries containing the orders to be applied on the board.
    
    Parameters:
    -----------
    data (list[dict]): the data of the game.
    board (list[list]): the board of the game.
    current_player (int): the current player.
    player_type (str): the type of the player (AI or human).
    
    Returns:
    --------
    list[dict]: a list of dictionaries containing the orders to be applied on the board.
    
    version : 2.0
    specifiations : Mohamed aziz Sebri 
    implementation : Mohamed Aziz Sebri (v2 23/03/2025)
    """
    if player_type == "AI":
        orders = naive_ai(data, board, current_player)  # IA génère ses ordres sous forme de texte
        print(f"\nIA (Joueur {current_player}) a joué : {orders}")  # Afficher les actions de l'IA
    else:
        orders = input(f"\nTour du Joueur {current_player} : Entrez vos ordres :")
        
    orders = orders.split(" ")
    orders_sorted = []
    player_has_errors = False 

    # Vérifier si "summon" est en premier
    if "summon" in orders:
        if orders[0] != "summon":
            player_has_errors = True

    # Vérifier si ":@" vient après ":x" (mauvais ordre) maroc:@12-13 
    index_at = -1
    index_x = -1

    for i in range(len(orders)):
        if ":@" in orders[i]:
            index_at = i
        if ":x" in orders[i]:
            index_x = i

    if index_at != -1 and index_x != -1 and index_at < index_x:
        player_has_errors = True

    # Parcourir chaque ordre pour l'analyser
    for order in orders:
        order = order.strip()
        
        
        if ":x" in order:#maroc:xN
            parts = order.split(":x")
            if len(parts) == 2:
                name = parts[0]
                direction = parts[1]
                directions_valides = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                if direction in directions_valides:
                    orders_sorted.append({
                        "type": "attack",
                        "name": name,
                        "direction": direction
                    })
                else:
                    player_has_errors = True
            else:
                player_has_errors = True


        elif ":@" in order:
            parts = order.split(":@")
            if len(parts) == 2:
                name = parts[0]
                position = parts[1]

                if check_propre_apprenti(data, current_player, name) == False:
                    player_has_errors = True

                
                if "-" in position:
                    coords = position.split("-")
                    if len(coords) == 2 and coords[0].isdigit() and coords[1].isdigit():
                        row = int(coords[0]) - 1
                        col = int(coords[1]) - 1
                        if check_valid_move(board, name, row, col):
                            orders_sorted.append({
                                "type": "move",
                                "name": name,
                                "row": row,
                                "col": col
                            })
                        else:
                            player_has_errors = True
                    else:
                        player_has_errors = True
                else:
                    player_has_errors = True
            else:
                player_has_errors = True


        elif order == "summon":
            orders_sorted.append({"type": "summon"})

    # Si une erreur est détectée, on ignore le tour du joueur
    if player_has_errors:
        return None  

    return orders_sorted

    
def check_propre_apprenti(data : dict, current_player : int, name : str) -> bool:
    """ This function checks if the player has the apprentice he wants to move. 

    Parameters : 
    ------------
    data (dict): the data of the game. 
    current_player (int): the current player. 
    name (str): the name of the apprentice to check. 

    Returns : 
    ---------
    bool : True if the player has the apprentice, False otherwise. 
    """
    
    for apprenti in data["apprentices"][current_player]:
        if apprenti["nom"] == name:
            return True
    return False

def check_propre_element(data : dict, current_player : int, name : str) -> bool:
    """ This function checks if the player has the element he wants to move. 

    Parameters : 
    ------------
    data (dict): the data of the game. 
    current_player (int): the current player. 
    name (str): the name of the element to check. 

    Returns : 
    ---------
    bool : True if the player has the apprentice, False otherwise. 
    """
    
    if check_propre_apprenti(data , current_player , name) :
        return True
    elif len(data["dragons"]) > 0 and current_player in data["dragons"]:
        for dragon in data["dragons"][current_player]:
            if dragon["nom"] == name:
                return True
    return False
    
def apply_order(board : dict, orders : list[dict] , data : list[list] , current_player : int): 
    """ This function receives the order to move the player's dragons and apprentices to the desired position. 

    Parameters :
    ------------
    order (list[dict]): the order received by the player to be applied on the board.
    
    Returns :
    ---------
    None 

    """
    
    for order in orders : 
        if order["type"] == "move":
            move_element(board, order["name"], order["row"], order["col"])
            
        elif order["type"] == "attack":
            attack(board , order["name"], order["direction"])
            
        
        elif order["type"] == "summon":
            summon(board , data , current_player)
    
    

def move_element(board, name, row, col):
    """ move the element to the desired position.

    Args:
        board (list[list]): the board of the game.
        name (str): the name of the element
        row (int): the row to move to.
        col (int): the column to move to.

    Returns:
        None
    
    version : 1.0
    specifications :hiba bargi (v1 21/02/2025)
    implementation : Mohamed Aziz Sebri , ahmed feki (v1 24/02/2025)
    """

    # Parcourir le plateau pour trouver l'élément
    for i in range(len(board)):
        for j in range(len(board[i])):
            case = board[i][j]
            for element in case:
                if element.get("nom") == name:
                    # Vérifier si la position cible est valide
                    if 0 <= row < len(board) and 0 <= col < len(board[0]):
                        # Effectuer le déplacement
                        case.remove(element)
                        board[row][col].append(element)
                        print(f"{name} a été déplacé à ({row}, {col}).")
                    else:
                        print(f"Erreur : La position ({row}, {col}) est invalide.")
                    return  # Arrêter la recherche après le déplacement
    print(f"Erreur : L'élément '{name}' n'a pas été trouvé sur le plateau.")
    


def check_valid_move(board: list[list], name: str, row: int, col: int) -> bool:
    """Verify if the move is valid or not.

    parameters:
        board (list[list]): the board of the game.
        name (str): name of element to move.
        row (int): the row to move to.
        col (int): the column to move to.

    Returns:
        bool: True if the move is valid, False otherwise.
    
    version : 1.0
    specifications :hiba bargi (v1 21/02/2025)
    implementation : Mohamed Aziz Sebri , ahmed feki (v1 24/02/2025)
    """

    # Vérifier si la position cible est dans les limites du plateau
    if not (0 <= row < len(board) and 0 <= col < len(board[0])):
        return False

    # Trouver la position actuelle de l'élément
    current_position = None
    for r in range(len(board)):
        for c in range(len(board[r])):
            for element in board[r][c]:
                if element.get("nom") == name:
                    current_position = (r, c)
    

    if current_position:
        current_row, current_col = current_position
        # Calculer la différence entre les positions actuelle et cible
        row_diff = abs(current_row - row)
        col_diff = abs(current_col - col)

        # Vérifier que le déplacement est d'une seule case dans l'une des huit directions adjacentes
        if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1) or (row_diff == 1 and col_diff == 1):
            return True

    return False


def get_attacked_positions(dragon : dict) -> list:
    """get the attacked positions by the dragon.
    
    parameters:
    -----------
    dragon (dict): the dragon that attacks.
    
    returns:
    --------
    list: a list of attacked positions.
    
    version : 1.0
    specifications :hiba bargi (v1 21/02/2025)
    implementation :  ahmed feki , mohamed aziz slimi , mohamed aziz sebri (v1 24/02/2025)
    """
    
    directions = {
        "N": (0, -1),
        "NE": (1, -1),
        "E": (1, 0),
        "SE": (1, 1),
        "S": (0, 1),
        "SW": (-1, 1),
        "W": (-1, 0),
        "NW": (-1, -1)
    }
    x, y = dragon["position"]  # Coordonnées du dragon
    dx, dy = directions[dragon["direction"]]  # Déplacement en x et y selon la direction
    portee = dragon["portee"]  # Portée de l'attaque
    
    positions = []  # Liste des cases attaquées
    for i in range(1, portee + 1):  # On avance case par case
        positions.append((x + i * dx, y + i * dy))  # Ajoute la case touchée
    
    return positions  # Retourne la liste des cases attaquées

def get_apprenti_by_dragon(dragon_id : int, data : dict) -> dict:
    """ Trouve l'apprenti qui a créé un dragon """
    for apprenti in data["apprentices"][1] + data["apprentices"][2]:
        if apprenti["type"] == "apprenti" and apprenti["id"] == data["dragons"][dragon_id]["creator_id"]:
            return apprenti
    return None

def attack(board: list[list], data: dict):
    """This function receives the order to attack and allows the dragon to attack the other dragons or the apprentices within his range. 

    parameters: :
    ------------
    board (list): the board of the game.
    data (dict): the data of the game.

    returns :
    --------
    None
    
    version : 2.0
    specifications :hiba bargi (v1 21/02/2025) / Mohamed Aziz Sebri (v2 23/03/2025)
    implementation : Mohamed Aziz Sebri , ahmed feki (v1 24/02/2025)
    
    """

    attaques = []  # Liste des attaques à appliquer

    #Récupérer toutes les attaques des dragons
    for apprenti, dragons in data["dragons"].items():
        for dragon in dragons:
            attacked_positions = get_attacked_positions(dragon)  # Cases attaquées
            attaques.append((dragon, attacked_positions))

    #Appliquer les attaques à tous les personnages sur le plateau
    for dragon, attacked_positions in attaques:
        for i in range(len(board)):
            for j in range(len(board[i])):
                elements = board[i][j]

                for target in elements:
                    if target["position"] in attacked_positions:
                        target["pv"] -= dragon["attaque"]

                        # Si la cible meurt
                        if target["pv"] <= 0:
                            target["status"] = "dead"
                            print(f"{target['nom']} est mort.")

                            # Supprimer ses dragons s'il est un apprenti
                            if target["type"] == "apprenti" and target["nom"] in data["dragons"]:
                                for d in data["dragons"][target["nom"]]:
                                    d["status"] = "dead"
                                    print(f"Le dragon {d['nom']} de {target['nom']} est mort.")
                                del data["dragons"][target["nom"]]

                            # Si c'est un dragon, l'apprenti créateur perd 10 PV
                            if target["type"] == "dragon":
                                creator_name = target["name_apprenti"]
                                for apprenti in data["apprentices"]:
                                    if apprenti["nom"] == creator_name:
                                        apprenti["pv"] -= 10
                                        if apprenti["pv"] <= 0:
                                            apprenti["status"] = "dead"
                                            print(f"L'apprenti {creator_name} est mort.")

def summon(board: list[list], data: dict, current_player: int):
    """This function allows the player to summon a dragon or the apprentices on the board.

    Parameters:
    ------------
    board (list): The board of the game.
    data (dict): The data of the game.
    current_player (int): The current player.

    Returns:
        None
    """

    # Parcourir chaque apprenti du joueur
    for apprenti in data["apprentices"][current_player]:
        # Récupérer la position initiale de l'apprenti
        initial_position = apprenti["position"]  # position sous forme de (x, y)
        initial_x, initial_y = initial_position

        trouve = False
        row = 0
        while row < len(board) and not trouve:
            col = 0
            while col < len(board[row]) and not trouve:
                for element in board[row][col]:
                    if element.get("nom") == apprenti["nom"] and element.get("joueur") == current_player:
                        move_element(board, apprenti["nom"], initial_x - 1, initial_y - 1)
                        trouve = True
                col += 1
            row += 1

def naive_ai(data: dict, board: list[list], current_player: int) -> list[dict]:
    """ 
    this function allow the AI to play the game.
    
    Parameters:
    -----------
    data (dict): the data of the game.
    board (list[list]): the board of the game
    current_player (int): the current player. here is the IA 
    
    Returns:
    --------
    string: the orders to be applied on the board.
    
    version : 1.0
    specifications : Ahmed Feki (v1 13/03/2025)
    implementation : Mohamed Aziz Sebri ,Mohamed Aziz Slimi (v1 23/03/2025)
    """
    
    orders = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            for element in board[i][j]:
                if element["type"] in ["apprenti" , "dragon"] and check_propre_element(data, current_player, element["nom"]) :
                    # Récupérer toutes les cases où l'élément peut se déplacer
                        x, y = i, j
                        possibles_actions = []
                        valides_moves = []
                        possible_moves = [
                        (x-1,y+1), (x,y+1), (x+1,y+1),
                        (x-1,y ),            (x+1,y),
                        (x-1,y-1), (x,y-1), (x+1,y-1)
                        ]
                        
                        for dx, dy in possible_moves:
                            if check_valid_move(board, element["nom"], dx, dy):
                                valides_moves.append((dx, dy))
                                
                        if element["type"] == "dragon" and current_player in data["dragons"]:
                            attacked_directions = get_attacked_positions(element)
                            valides_directions = convert_positions_to_directions(attacked_directions, (i, j))
                        
                        if valides_moves:
                            row, col = random.choice(valides_moves)
                            possibles_actions.append(f"{element['nom']}:@{row+1}-{col+1}")
                            
                        elif valides_directions :
                            direction = random.choice(valides_directions)
                            possibles_actions.append(f"{element['nom']}:x{direction}")
                            
                        else:
                            possibles_actions.append("summon")
                        
                        if possibles_actions:
                            order = random.choice(possibles_actions)
                            orders.append(order)
    
    return order

def convert_positions_to_directions(attacked_positions : list[tuple] , dragon_position : tuple) -> list:
    """convert a list of positions to a list directions.
    
    Parameters:
    -----------
    positions (list): a list of positions.
    
    Returns:
    --------
    list: a list of directions.
    
    version : 1.0
    specifications : Mohamed Aziz Sebri (v1 15/03/2025)
    implementation : Mohamed Aziz Sebri (v1 15/03/2025)
    
    example:
    --------
    convert_positions_to_directions([x, y+1), (x+1, y-1), (x-1, y)]) => ["N", "NE", "W"]
    
    """

    directions_map = {
        (0, -1): "N", (1, -1): "NE", (1, 0): "E", (1, 1): "SE",
        (0, 1): "S", (-1, 1): "SW", (-1, 0): "W", (-1, -1): "NW"
    }
    
    valid_directions = []
    x0 , y0 = dragon_position
    
    for x, y in attacked_positions:
        dx , dy = x -x0 , y - y0
        if (dx, dy) in directions_map:
            valid_directions.append(directions_map[(dx, dy)])
    return valid_directions
def regenerate(data: dict):
    """ 
    This function allows the dragons and appprentices to regenerate their health point (point de vie) .

    Parameters:
    -----------
    data (list): the data of the game.(and here i need just the apprenctices and dragons informations)

    Returns:
    --------
    None: The dragons will regenerate their health points directly.
    
    version
    --------
    sepecifications : Aziz Slimi (v1 21/02/2025)
    """
    
    # Régénérer les points de vie des apprentis
    for player in [1, 2]:
        if player in data["apprentices"]:
            for apprenti in data["apprentices"][player]:
                apprenti["pv"] = min(apprenti["pv"] + apprenti["regen"], apprenti["pv"])
    
    # Vérifier si des dragons existent avant d'y accéder
    if len(data["dragons"]) > 0:
        for player in [1, 2]:
            if player in data["dragons"]:
                for dragon in data["dragons"][player]:
                    dragon["pv"] = min(dragon["pv"] + dragon["regen"], dragon["pv"])

    

    

def check_game_over(data : dict) -> bool:
    """ This function checks if the game is over or not.
    
    Parameters:
    
    -----------
    data (dict): The data of the game.
    
    Returns:
    --------
    bool: True if the game is over, False otherwise.
    
    version : 1.0
    sepecifications : Ahmed Feki (v1 21/02/2025)
    implementation : Mohamed Aziz Sebri  , ahmed feki (v1 27/02/2025)
    """
    nombre_apprenti_joueur1 = len(data["apprentices"][1])
    nombre_apprenti_joueur2 = len(data["apprentices"][2])
    
    if nombre_apprenti_joueur1 == 0 or nombre_apprenti_joueur2 == 0:
        return True
    
    elif data["tours_sans_damage"] >= 100:
        return True

def check_winner(data : dict) -> int:
    """ This function checks the winner of the game. 

    Parameters : 
    ------------
    data (dict): The data of the game. 

    Returns : 
    ---------
    int : the number of the winner player
    
    version : 1.0
    sepecifications : Mohamed Aziz Sebri (v1 20/02/2025)
    implementation : Mohamed Aziz Sebri (v1 27/02/2025)
    """
    nombre_apprenti_joueur1 = len(data["apprentices"][1])
    nombre_apprenti_joueur2 = len(data["apprentices"][2])
    
    if nombre_apprenti_joueur1 == 0:
        return 2
    elif nombre_apprenti_joueur2 == 0:
        return 1
    elif data["tours_sans_damage"] <= 100:
        if nombre_apprenti_joueur1 > nombre_apprenti_joueur2:
            return 1
        else:
            return 2
        
    
        
    
        

def egg_eclosion_check(board: list[list], data: dict , current_player:int):
    """this function checks if the egg is ready to hatch or not.

    parameters:
    ------------
    board (list): the board of the game.
    data (dict): the data of the game, including the list of dragons per apprentice.
    current_player(int) : number (1 or 2 ) to precise the current player .

    returns:
    -------
    None
    
    version : 1.0
    specifications : Aziz Slimi (v1 21/02/2025)
    implementation : Mohamed Aziz Sebri (v1 27/02/2025)
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            # Vérifier si la case contient exactement un œuf et un apprenti
            elements = board[i][j]
            egg_count = 0
            apprentice_count = 0
            egg = None
            apprentice = None
            
            for element in elements:
                if element["type"] == "egg":
                    egg_count += 1
                    egg = element  # Garder une référence à l'œuf
                elif element["type"] == "apprenti":
                    apprentice_count += 1
                    apprentice = element  # Garder une référence à l'apprenti
            
            # Si la case contient exactement un œuf et un apprenti
            if egg_count == 1 and apprentice_count == 1:
                # Vérifier si l'œuf et l'apprenti sont sur la même case
                if egg and apprentice:
                    # Décrémenter les tours de l'œuf
                    egg["tours"] -= 1
                    
                    # Vérifier si l'œuf est prêt à éclore
                    if egg["tours"] == 0:
                        # L'œuf éclot en dragon
                        board[i][j].remove(egg)
                        dragon = {
                            "type": "dragon",
                            "name_apprenti": apprentice["nom"],
                            "nom": egg["nom"],
                            "pv": egg["pv"],
                            "attaque": egg["attaque"],
                            "portee": egg["portee"],
                            "regen": egg["regen"]
                        }
                        board[i][j].append(dragon)
                        
                        # Ajouter le dragon dans la liste des dragons de l'apprenti
                        if apprentice["nom"] not in data["dragons"]:
                            data["dragons"][current_player] = []  # Créer une liste si elle n'existe pas
                        data["dragons"][current_player].append(dragon)  # Ajouter le dragon
                  
                        
    
    
def play_game(file_name: str, type_1: str, type_2: str):
    """
    This function allows us to play the game with local, AI, and remote players.

    Parameters:
    -----------
    file_name (str): The name of the file to read.
    type_1 (str): Type of player 1 ('human', 'AI', or 'remote').
    type_2 (str): Type of player 2 ('human', 'AI', or 'remote').
    
    Returns:
    --------
    None
    
    version : 1.0
    sepecifications : Mohamed Aziz Sebri (v1 20/02/2025)
    implementation : Mohamed Aziz Sebri , ahmed feki , mohamed aziz slimi (v1 23/03/2025)
    """
    board, data = create_board(file_name)
    display_board(data , board)
    players = [1, 2]
    current_turn = 0
    # Create remote connection if necessary
    connection = None
    if type_1 == 'remote':
        #connection = create_connection(2, 1)
        pass
    elif type_2 == 'remote':
        #connection = create_connection(1, 2)
        pass

    while not check_game_over(data):
        current_player = players[current_turn]
        player_type = type_1 if current_player == 1 else type_2
        orders = get_orders(data , board , current_player , player_type)
        if orders is None:
            print(f"Joueur {current_player} : Ordres non valides, passage au joueur suivant.")
        else:
            apply_order(board, orders, data, current_player)
            egg_eclosion_check(board, data ,current_player)
            regenerate(data)
            display_board(data , board)
            
            if (current_player == 1 and type_2 == 'remote') or (current_player == 2 and type_1 == 'remote'):
                #notify_remote_orders(connection, orders)
                pass

        current_turn = (current_turn + 1) % len(players)
        if current_turn == 0:
            data["tours"] += 1
    # Close remote connection if necessary
    if type_1 == 'remote' or type_2 == 'remote':
        #close_connection(connection)
        pass

    print("\nGame Over !")
    winner = check_winner(data)
    print(f"\U0001F3C6 Le joueur {winner} a gagné la partie !")

# Example usage:
play_game("plateau.drk", "human", "AI")
