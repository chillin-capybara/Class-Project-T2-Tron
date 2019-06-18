from Player import Player

# todo: Implement the Human player according to the UML

class HumanPlayer(Player):
    
    """
    implementation of Human Player Class
    """

    __Name = "" # Name of the player
    
    def getName(self) -> str:
        """
        get the Name from the Sever

        Returns:
            str: Name of the player
        """
        return self.__Name
    
    def setName(self, name: str):
        """
        TODO: DOKU
        ...
        ...
        Raises:
            TypeError
        """
        if type(name) == str:
            self.__Name = name
        else:
            raise TypeError
    
    def getColor(self):
    	"""
		get the Color from the Sever
        
        Args: 
        player ID
        
        Returns:
        int
        
        """
        raise NotImplementedError
    
    def getPosition(self):
        """
		get the Position from the Sever
        
        Args: 
        player ID
        
        Returns:
        Vect2D
        
        """
        raise NotImplementedError
    
    def getTrack (self):
        """
		get the Track from the Sever
        
        Args: 
        player ID
        
        Returns:
        Vect2D
        
        """
        raise NotImplementedError
        

	pass