import time
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
        "eggs": {} ,
        "tours_sans_damage" : 0
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

def check_position(x : int, y: int, dict : list, errors : list):
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
        errors.append(f"Position déjà occupée par un altar : ({x}, {y})")
    
    elif (x,y) in dict["apprentices"] :
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
    """
    Retourne le contenu à afficher dans la case (icône + couleur).
    S'il y a plusieurs éléments dans la case, on affiche
    celui qui a la priorité (ex: altar > apprenti > egg > dragon).
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

def display_board(board):
    """show the board on the screen.
    
    parameters:
    -----------
        board (list): the board of the game.
    
    returns:
    --------
        None
    
    version : 1.0
     sepecifications : Ahmed Feki (v1 21/02/2025)
     implementation : Mohamed Aziz Sebri (v1 27/02/2025)
    """
    print(term.home + term.clear)  # Nettoyer l'écran, cacher le curseur

    hauteur = len(board)
    largeur = len(board[0]) if hauteur > 0 else 0

    # Lignes de bordure (haut, séparateur intermédiaire, bas)
    top_line    = horizontal_line(largeur, '╔', '╦', '╗')
    mid_line    = horizontal_line(largeur, '╠', '╬', '╣')
    bottom_line = horizontal_line(largeur, '╚', '╩', '╝')

    # ─────────────────────────────────────────────────────────────────────────
    # 1) Affichage de la ligne supérieure
    print(top_line)

    # 2) Pour chaque rangée du board
    for i in range(hauteur):
        # Construire la ligne de contenu : ex: ║ . ║ 🏰 ║ 🧙 ║
        row_str = ""
        for j in range(largeur):
            cell_content = get_cell_content(board[i][j])
            row_str += "║" + cell_content
        row_str += "║"  # Fin de la ligne
        print(row_str)

        time.sleep(0.01)  # Petite pause pour effet "dynamique"

        # Après chaque rangée, si ce n'est pas la dernière, on affiche une ligne intermédiaire
        if i < hauteur - 1:
            print(mid_line)

    # 3) Affichage de la ligne inférieure
    print(bottom_line)

    # ─────────────────────────────────────────────────────────────────────────
    # 4) Affichage de la légende
    print()
    print(term.bold("📜 Légende :"))
    print(
        term.red("🏰 = Autel  "),
        term.blue("🧙 = Apprenti  "),
        term.yellow("🥚 = Œuf  "),
        term.green("🐉 = Dragon"),
        sep="\n"
    )
    

    # 5) Attente des ordres du joueur
    print()
    print("🎮 En attente des ordres du joueur... ", end="", flush=True)
    time.sleep(0.5)
    print(term.blink("⌛"))

def get_orders(data: list[dict], board: list[list], current_player: int) -> list[dict]:
    """ this function receives the orders from the player and returns a list of dictionaries containing the orders to be applied on the board.
    
    Parameters:
    -----------
    data (list[dict]): the data of the game.
    board (list[list]): the board of the game.
    current_player (int): the current player.
    
    Returns:
    --------
    list[dict]: a list of dictionaries containing the orders to be applied on the board.
    
    version : 1.0
    specifiations : Mohamed aziz Sebri 
    """
    
    orders = input(f"\n🎮 Tour du Joueur {current_player} : Entrez vos ordres :")
    orders = orders.split(" ")  # Convertir en liste
    orders_sorted = []
    player_has_errors = False  # Variable pour vérifier les erreurs

    # Vérifier si "summon" est en premier
    if "summon" in orders:
        if orders[0] != "summon":
            player_has_errors = True

    # Vérifier si ":@" vient après ":x" (mauvais ordre)
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

        # Ordre d'attaque "name:xDirection"
        if ":x" in order:
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

        # Ordre de déplacement "name:@row-col"
        elif ":@" in order:
            parts = order.split(":@")
            if len(parts) == 2:
                name = parts[0]
                position = parts[1]

                if check_propre_apprenti(data, current_player, name) == False:
                    player_has_errors = True

                # Vérifier si la position est valide (ex: "1-2")
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

        # Ordre d'invocation "summon"
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
            print(f"{order['name']} a été déplacé à la position ({order['row']}, {order['col']})")
        
        elif order["type"] == "attack":
            attack(board , order["name"], order["direction"])
            print(f"{order['name']} a attaqué dans la direction {order['direction']}")
        
        elif order["type"] == "summon":
            summon(board , data , current_player)
            print("Le joueur a activé le summon !")
        
        else:
            print(f" Erreur: Instruction invalide : {order}")
    
    

def move_element(board, name, row, col):
    """ Déplace un apprenti ou un dragon sur le plateau. """

    for i in range(len(board)):
        for j in range(len(board[i])):
            case = board[i][j]
            for element in case:
                if element.get("nom") == name:
                    # Effectuer le déplacement
                    case.remove(element)
                    board[row][col].append(element)  # Déplacer l'élément
                    return  # Le déplacement est terminé
    


def check_valid_move(board: list[list], name: str, row: int, col: int) -> bool:
    """Verify if the move is valid or not.

    Args:
        board (list[list]): the board of the game.
        name (str): name of element to move.
        row (int): the row to move to.
        col (int): the column to move to.

    Returns:
        bool: True if the move is valid, False otherwise.
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




def attack (data : dict , name : str, direction : str):
    """ This function receives the order to attack and allows the dragon to attack the other dragons or the apprentices within his range. 

    Parameters : 
    ------------
    name (str): the name of the dragon that will attack
    direction (str): the direction in which the dragon will attack

    Returns : 
    ---------
    None 

    """
    

def summon(board, data, current_player):
    """Cette fonction déplace les apprentis du joueur vers l'autel puis les ramène à leurs positions initiales."""
    
    # Parcourir chaque apprenti du joueur
    for apprenti in data["apprentices"][current_player]:
        # Récupérer la position initiale de l'apprenti
        initial_position = apprenti["position"]  # position sous forme de (x, y)
        initial_x, initial_y = initial_position
        
        # Chercher l'apprenti sur le plateau
        for row in range(len(board)):
            for col in range(len(board[row])):
                for element in board[row][col]:
                    if element.get("nom") == apprenti["nom"] and element.get("joueur") == current_player:
                        move_element(board, apprenti["nom"], initial_x -1, initial_y-1)
                        break



def regenerate(data : dict):
    """ This function allows the dragons and the apprentices to regenerate their health points.

    Parameters : 
    ------------
    board (list): the board of the game. 

    Returns : 
    ---------
    None 

    """

    

def check_game_over(data : dict) -> bool:
    """ This function checks if the game is over or not.
    
    Parameters:
    
    -----------
    data (dict): The data of the game.
    
    Returns:
    --------
    bool: True if the game is over, False otherwise.
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
        
    
        
    
        

def egg_eclosion_check(board: list[dict], data: list[dict]):
    """Cette fonction vérifie si les œufs sont prêts à éclore ou non et si un apprenti est sur la même case que l'œuf.

    Paramètres:
    ------------
    board (list): le plateau du jeu.
    data (list): liste des joueurs et de leurs positions.

    Retour:
    -------
    None
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            egg_found = False
            for element in board[i][j]:
                if element["type"] == "egg":
                    egg_found = True
                    
                    # Vérifie s'il y a un apprenti sur la même case avant de décrémenter les tours
                    for player in data:
                        if player["position"] == (i, j) and player["type"] == "apprenti":
                            # Si un apprenti est présent, décrémenter les tours de l'œuf
                            element["tours"] -= 1
                            if element["tours"] == 0:
                                # L'œuf éclore en dragon
                                board[i][j].remove(element)
                                board[i][j].append({
                                    "type": "dragon",
                                    "nom": element["nom"],
                                    "pv": element["pv"],
                                    "attaque": element["attaque"],
                                    "portee": element["portee"],
                                    "regen": element["regen"]
                                })
                                data["dragons"]["player"].append({
                                    "nom": element["nom"],
                                    "pv": element["pv"],
                                    "attaque": element["attaque"],
                                    "portee": element["portee"],
                                    "regen": element["regen"]
                                })
                                    
                                print(f"🥚 L'œuf {element['nom']} a éclos en dragon !")
                            break  # Arrêter de vérifier une fois qu'on a trouvé l'apprenti et traité l'éclosion

    
    
    
    
def play_game(file_name: str):
    """ 
    This function allows us to play the game. 

    Parameters:
    -----------
    file_name (str): The name of the file to read.

    Returns:
    --------
    None: The game will be played directly.
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 20/02/2025)
    """
    board, data = create_board(file_name)  # Créer le plateau de jeu et les données
    display_board(board)  # Afficher le plateau au début du jeu
    data["tours"] = 0  # Initialiser le compteur de tours sans dégâts
    players = [1, 2]  # Liste des joueurs (Joueur 1 et Joueur 2)
    current_turn = 0   # Indice pour alterner entre les joueurs
    
    while not check_game_over(data):  # Tant que le jeu n'est pas terminé
        current_player = players[current_turn]
        orders = get_orders(data, board, current_player)

        if orders is None:
            # Si les ordres sont invalides, on passe au joueur suivant sans appliquer d'ordres
            print(f"Joueur {current_player} : Ordres non valides, passage au joueur suivant.")
            current_turn = (current_turn + 1) % len(players)  # Passer au joueur suivant
        else:
            # Si les ordres sont valides, on les applique
            apply_order(board, orders,data, current_player)  # Appliquer les ordres au plateau
            egg_eclosion_check(board ,data)  # Vérifier l'éclosion des œufs
            regenerate(data)  # Régénérer les données du jeu (par exemple, recharger les ressources)

            # Afficher le plateau après l'application des ordres
            display_board(board)

            # Passer au joueur suivant (alterner entre 0 et 1)
            current_turn = (current_turn + 1) % len(players)

    # Lorsque la partie est terminée, afficher le résultat
    print("\nGame Over !")
    winner = check_winner(data)
    print(f"🏆 Le joueur {winner} a gagné la partie !")


#i gonna run the game

play_game("plateau.drk")
