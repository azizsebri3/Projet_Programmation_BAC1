def tri_orders (orders : str) -> list:
    """ This function will allow us to sort out the different instructions received by the player. 

    Parameters : 
    ------------
    orders (str): the orders received by the player 

    Returns : 
    ---------
    orders_tri (list) : a list of the instructions by order
"""
    orders = orders.split(" ") #[Lea:@10-11,kraar:@12-13,Lea:xN,kraar:xSL,summon]
    orders_tri = []
    
    for order in orders:
        order = order.strip()
        
        if ":x" in order:
            try : 
                name , direction = order.split(":x")
                directions_valides = ["N", "NE", "E", "SE", "S", "SW", "W" , "NW"]
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

print(tri_orders(input("Entrez les ordres : ")))