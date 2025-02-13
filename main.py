from blessed import Terminal
import random

# Initialisation du terminal
term = Terminal()

# Dimensions du plateau
ROWS, COLS = 20, 20

# Création du plateau vide ('.' représente une case vide)
plateau = [['.' for _ in range(COLS)] for _ in range(ROWS)]

# Position initiale du joueur
player_x, player_y = ROWS // 2, COLS // 2
plateau[player_x][player_y] = '@'  # '@' représente le joueur

# Placement aléatoire des éléments
def placer_element(plateau, element, nombre):
    for _ in range(nombre):
        while True:
            x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
            if plateau[x][y] == '.':  # Vérifier que la case est vide
                plateau[x][y] = element
                break

placer_element(plateau, 'A', 2)  # 2 autels (A)
placer_element(plateau, 'P', 5)  # 5 Apprentis (P)
placer_element(plateau, 'O', 3)  # 3 Œufs (O)

# Fonction d'affichage du plateau
def afficher_plateau():
    print(term.clear())  # Efface l'écran
    for row in plateau:
        print(" ".join(row))

# Fonction pour gérer le déplacement
def deplacer_joueur(dx, dy):
    global player_x, player_y
    new_x, new_y = player_x + dx, player_y + dy

    # Vérifier si le déplacement est dans les limites
    if 0 <= new_x < ROWS and 0 <= new_y < COLS:
        plateau[player_x][player_y] = '.'  # Effacer l'ancienne position
        player_x, player_y = new_x, new_y
        plateau[player_x][player_y] = '🐲'  # Mettre le joueur à la nouvelle position

# Boucle principale du jeu
with term.cbreak():  # Mode interactif
    afficher_plateau()
    while True:
        key = term.inkey()  # Récupère l'entrée clavier

        if key.code == term.KEY_LEFT:
            deplacer_joueur(0, -1)
        elif key.code == term.KEY_RIGHT:
            deplacer_joueur(0, 1)
        elif key.code == term.KEY_UP:
            deplacer_joueur(-1, 0)
        elif key.code == term.KEY_DOWN:
            deplacer_joueur(1, 0)
        elif key == 'q':  # Quitter avec 'q'
            break

        afficher_plateau()
