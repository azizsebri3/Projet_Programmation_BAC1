def display_board(board):
    """
    Affiche dynamiquement le plateau de jeu en utilisant `blessed`.

    Parameters:
    -----------
    board (list): Une liste de listes représentant le plateau du jeu.
    """
    print(term.home + term.clear + term.hide_cursor)  # Effacer l'écran et cacher le curseur

    largeur = len(board[0])
    hauteur = len(board)

    # 🏰 Dessiner la bordure supérieure du plateau
    print(term.move_yx(0, 0) + term.bold_white("╔" + "═" * (largeur * 3) + "╗"))

    for i, row in enumerate(board):
        print(term.bold_white("║"), end=" ")  # Bordure gauche
        
        for j, cell in enumerate(row):
            afficher_element = term.on_black + " . "  # Case vide par défaut avec fond noir
            
            for element in cell:
                if element["type"] == "altar":
                    afficher_element = term.on_black + term.bold_red(" 🏰 ")  # Autel rouge
                    break
                elif element["type"] == "apprenti":
                    afficher_element = term.on_black + term.bold_blue(" 🧙 ")  # Apprenti bleu
                elif element["type"] == "egg":
                    afficher_element = term.on_black + term.bold_yellow(" 🥚 ")  # Œuf jaune
                elif element["type"] == "dragon":
                    afficher_element = term.on_black + term.bold_green(" 🐉 ")  # Dragon vert

            print(afficher_element, end="", flush=True)  # Affichage immédiat
        
        print(term.bold_white("║"))  # Bordure droite
        time.sleep(0.02)  # Animation fluide

    # 🏰 Dessiner la bordure inférieure du plateau
    print(term.move_yx(hauteur + 1, 0) + term.bold_white("╚" + "═" * (largeur * 3) + "╝"))

    # 📜 Affichage de la légende
    print(term.move_yx(hauteur + 3, 0) + term.bold("📜 Légende :"))
    print(term.red(" 🏰 = Autel "), term.blue(" 🧙 = Apprentis "), 
          term.yellow(" 🥚 = Œufs "), term.green(" 🐉 = Dragons "), flush=True)

    # 🎮 Effet de chargement avant les ordres du joueur
    print(term.move_yx(hauteur + 5, 0) + "🎮 En attente des ordres du joueur... ", end="", flush=True)
    time.sleep(0.5)
    print(term.blink("⌛"))