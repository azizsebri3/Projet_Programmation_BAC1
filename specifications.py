def read_file(file_name: str) -> dict:

    """ 
        This function reads the file type .drk and returns a dictionary containing the data ( map, altars, apprentices, eggs).
    
        Parameters:
        -----------
         file_name (str): the name of the file to read. 
    
        returns:
        --------
         data (dict): a dictionary containing the various data of the file (map, altars, apprentices, eggs)
         
         version
         --------
         sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    """

def check_position(x : int, y: int, positions : dict, errors: list) -> None:
    """ This function checks if the position is valid or not. 
    
        Parameters:
        -----------
         x (int): the x coordinate of the position to check.
         y (int): the y coordinate of the position to check.
         dict (list): a dictionary that contains all the positions of the elements on the board.
         errors (list): a list that contains all the errors detected during the reading of the file.
    
        Returns:
        --------
         None : The function will return directly the errors list.
        
        version
        --------
        sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    """
    
def create_board(file_name:str) -> list:
    """ 
    initalizes the board with the data read from the file.drk.

    Parameters:
    ------------
    file_name (str): the name of the file

    Returns:
    --------
    list: a list of lists representing the board
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    """
    
def place_apprentices(data:dict):
    """ 
    This function initializes the apprentices on the board.

    Parameters:
    -----------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
   None : The altars will be placed directly on the game board.
   
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    
    """

def place_altars(data : dict):
    """ 
    This function initializes the altars on the board.

    Parameters:
    -----------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    None : The altars will be placed directly on the game board.
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    
    """

def place_eggs(data : dict):
    """ 
    This function initializes the eggs on the board.

    Parameters:
    -----------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    None : The altars will be placed directly on the game board.
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    """

def display_board(board :list[list]):
    """
    This functions allows us to print the board in the terminal with UTF-8 emojis and colors.

    Parameters:
    ----------
        board (list): a list of lists representing the board game.
    
    Returns:
    --------
        None: The board will be displayed in the terminal.
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    
        
    """

def get_orders(data : list[dict] , board: list[list], current_player: int, errors: list) -> list[dict]:
     """ 
      This function will allow us to sort out the different instructions received by the player. 
    
    Parameters : 
    ------------
    data : list[dict] : a list of the instructions received by the player
    board : list[list] : the game board with all it's elements
    current_player : int : the current player
    errors : list : a list that contains all the errors detected during the reading of the file
    
    Returns : 
    ---------
    orders_sorted (list[dict]) : a list of the instructions by order 
    
    version
    --------
    sepecifications : Ahmed Feki (v1 21/02/2025)

    """

def apply_order(board: list[list] , order : list[dict]):
    """
    This function receives the order to move and allows the dragon to move on the board.
    
    Parameters :
    ------------
    board (list[list]): the game board with all it's elements.
    order (str): the order received by the player to move his dragon.
    
    Returns :
    ---------
    None 
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 23/02/2025)
    """

def move(data: dict, element : str, direction : str):
    """ 
    This function allows us to move the element in the direction given by the player. 
    
    Parameters : 
    ------------
    data (dict): a dictionnary that contains all the board informations. 
    element (str): the element to move 
    direction (str): the direction in which the element will move 

   version
    --------
    sepecifications : Hiba bargi (v1 21/02/2025)
    
    """
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
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 21/02/2025)
    """
    
    
    

def attack(data :dict , order : str , board :list):
    """ 
    This function receives the order to attack and allows the dragon to attack the other dragons or the apprentices within his range. 
    
    Parameters : 
    ------------
    order (str): the order received by the player to attack (dragon_name:x(direction))

    Returns : 
    ---------
    None
    
    version
    --------
    sepecifications : Ahmed feki (v1 21/02/2025)
    """

def magic_bond(board: list,data: dict):
    """ 
    This function sets the magical bond between the apprentices and their dragons according to the eggs they have hatched.

    Parameters:
    -----------
    board (list): The game board with all it's components. 
    data (dict): The data of the game.

    Returns:
    --------
    None 
    
    version
    --------
    sepecifications : Hiba bargi (v1 21/02/2025)
    """

def summon(order : str , board : list):
    """ This function receives the order to summon the player's dragons and apprentices to his altar.

    Parameters : 
    ------------
    data : a dictionnary that contains all the board informations. 

    Returns : 
    ---------
    None 
    
    version
    --------
    sepecifications : Hiba bargi (v1 21/02/2025)

    """ 

def check_valid_move (x : int, y : int)->bool:
    """ 
    This function checks if the move is valid or not. 

    Parameters : 
    ------------
    x (int): the x coordinate of the move 
    y (int): the y coordinate of the move 

    Returns : 
    ---------
    bool : True if the move is valid, False otherwise
    
    version
    --------
    sepecifications : Aziz Slimi (v1 21/02/2025)
    """

def egg_prep_time(egg: dict, apprentice_pos: list) -> bool:
      """ 
    This function checks if there is an apprentice that is with the egg on the same game board case 
    and reduces the hatching time by 1 game tour.

    Parameters:
    -----------
    egg (dict): The egg's various informations. 
    apprentice_pos (list): The list of (x,y) positions of the apprentices. list[(),(),()]

    Returns:
    --------
    bool: True if the egg is ready to hatch and False if otherwise.
    
    version
    --------
    sepecifications : Hiba bargi (v1 21/02/2025)
    """

def egg_eclosion(board: list[list]) :
    """ 
    This function allows the eggs to hatch and the dragons to appear on the board.

    Parameters:
    -----------
    board (list): The game board with all it's components. 

    Returns:
    --------
    None: The hatching of the eggs will be executed directly on the game board.
    
    version
    --------
    sepecifications : Aziz Slimi (v1 21/02/2025)
    """

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

def game_is_over(board: list[list], data : dict) -> bool:
      """ 
    This function checks if the game is over or not. 

    Parameters:
    -----------
    board (list): The game board 
    dragons (list): The list of the dragons informations.

    Returns:
    --------
    bool: True if the game is over, False otherwise.
    
    version
    --------
    sepecifications : Ahmed Feki (v1 21/02/2025)
    """
    
def check_winner(data: dict) -> str:
      
    """ 
    This function checks the winner of the game. 

    Parameters:
    -----------
    data (dict): the informations of the game.

    Returns:
    --------
    str: The name of the winner.
    
    version
    --------
    sepecifications : Mohamed Aziz Sebri (v1 20/02/2025)
    """

def count_dragons(board : list[list] , id_joueur : int) -> int:
    """ 
    This function counts the number of dragons on the board. 

    Parameters:
    -----------
    board (list[list]): The game board.
    id_joueur (int): The player's id.

    Returns:
    --------
    int: The number of dragons on the board.
    
    version
    --------
    sepecifications : Ahmed Feki (v1 21/02/2025)
    """

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
    
    
    
    
    
    