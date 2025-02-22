def read_file(file_name: str) -> dict:

    """ 
        This function reads the file type .drk and returns a dictionary containing the data ( map, altars, apprentices, eggs).
    
        Parameters:
        -----------
         file_name (str): the name of the file to read. 
    
        returns:
        --------
         data (dict): a dictionary containing the various data of the file (map, altars, apprentices, eggs)
    """

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

def place_apprentices(data):
    """ 
    This function initializes the apprentices on the board.

    Parameters:
    -----------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    dict: a dictionary containing the apprentices informations.
    """

def place_altars(data):
    """ 
    This function initializes the altars on the board.

    Parameters:
    -----------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    dict: a dictionary containing the altars informations.
    """

def place_eggs(data):
    """ 
    This function initializes the eggs on the board.

    Parameters:
    -----------
    data (dict): a dictionary containing the data of the file (map, altars, apprentices, eggs)

    Returns:
    --------
    dict: a dictionary containing the eggs informations.
    """



def display_board(board):
    """
    This functions allows us to print the board in the terminal with UTF-8 emojis and colors.

    Parameters:
    ----------
        board (list): a list of lists representing the board game.
        Each game board square is a list of dictionaries that could contain one or more elements of the game in the board. 
        
    """




def tri_orders (orders : str) -> list:
    """ 
    This function will allow us to sort out the different instructions received by the player. 
    Parameters : 
    ------------
    orders (str): the orders received by the player 

    Returns : 
    ---------
    instruction (list) : a list of the instructions by order 

    """

def move (order : str , board : list):
    """
    This function receives the order to move and allows the dragon to move on the board.
    
    Parameters :
    ------------
    order (str): the order received by the player to move (dragon_name:x(direction))
    
    Returns :
    ---------
    None :
    The movement will be executed directly on the game board.
    """


def attack (order : str , board :list):
    """ 
    This function receives the order to attack and allows the dragon to attack the other dragons or the apprentices within his range. 
    
    Parameters : 
    ------------
    order (str): the order received by the player to attack (dragon_name:x(direction))

    Returns : 
    ---------
    None : The attack will be executed directly on the game board.

    """

def magic_bond (board: list, apprentices: dict, dragons: list):
    """ 
    This function sets the magical bond between the apprentices and their dragons according to the eggs they have hatched.

    Parameters:
    -----------
    board (list): The game board with all it's components. 
    apprentices (dict): a dictionary that contains the apprentices infromations.
    dragons (list): a list of the dragons informations. 

    Returns:
    --------
    None : This action will take place during the game directly on the game board. 
    """


def summon (order : str , board : list):
    """ This function receives the order to summon the player's dragons and apprentices to his altar.

    Parameters : 
    ------------
    data : a dictionnary that contains all the board informations. 

    Returns : 
    ---------
    None : Summoning the player's dragon's and apprentices will be executed directly on the game board. 

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
    """


def egg_prep_time (egg: dict, apprentice_pos: list) -> bool:

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
    """

def egg_eclosion (board: list) :
    """ 
    This function allows the eggs to hatch and the dragons to appear on the board.

    Parameters:
    -----------
    board (list): The game board with all it's components. 

    Returns:
    --------
    None: The hatching of the eggs will be executed directly on the game board.
    """


def game_is_over (board: list, dragons: list) -> bool:
    
    """ 
    This function checks if the game is over or not. 

    Parameters:
    -----------
    board (list): The game board 
    dragons (list): The list of the dragons informations.

    Returns:
    --------
    bool: True if the game is over, False otherwise.
    """
    
def check_winner (board: list) -> str:
    
    
    """ 
    This function checks the winner of the game. 

    Parameters:
    -----------
    board (list): The list of the board informations.

    Returns:
    --------
    str: The name of the winner.
    """


    
    
    
    
    
    
