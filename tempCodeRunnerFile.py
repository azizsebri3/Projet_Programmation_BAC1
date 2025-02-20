
            key = term.inkey()

            # Gérer les déplacements avec les flèches du clavier
            if key.code == term.KEY_LEFT:
                move_player(0, -1)