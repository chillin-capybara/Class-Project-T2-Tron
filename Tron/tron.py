# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pygame
import numpy as np
import itertools
import time

class Logic(object):
    """ Implements the logic of TRON. This would be your server.
    
        This game is hard coded for two players, but easily extensible to
        multiple ones.
    """
    
    def __init__(self, num_x_tiles, num_y_tiles):
        """ Initializes object.
        
            Args:
                num_x_tiles (int): Width of the game board.
                num_y_tiles (int): Height of game board.
        """
        self.num_player = 2
        # Game board is represented as a matrix of zeros. A zero indicates a
        # free cell. A value different from zero indicates an barrier. Other
        # values are the other players ids.
        self.game_board = np.zeros((num_x_tiles, num_y_tiles))
        self.num_x_tiles = num_x_tiles
        self.num_y_tiles = num_y_tiles
        move_vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Set initial position of players
        x1 = np.random.randint(0, num_x_tiles)
        y1 = np.random.randint(0, num_y_tiles)
        
        # Get a starting position that is different from existing one
        x2 = x1
        y2 = y1
        while (x1 == x2) and (y1 == y2):
            x2 = np.random.randint(0, num_x_tiles)
            y2 = np.random.randint(0, num_y_tiles)
            
        # Set initial positions of players in board
        self.game_board[y1, x1] = 1
        self.game_board[y2, x2] = 2
        
        # Randomly select direction to move
        init_direction1 = move_vectors[np.random.randint(0, len(move_vectors))]
        init_direction2 = move_vectors[np.random.randint(0, len(move_vectors))]
        
        # Initialize player dictionaries. Better style (especially if you add
        # more sophisticated features) would be to create own classes.
        #colors = ["#1b9e77", "#7570b3"]
        self.players = {
                1: {
                        "posx": x1,
                        "posy": y1,
                        "vx": init_direction1[0],
                        "vy": init_direction1[1],
                        "color": (117, 112, 179),
                        "alive": True
                   },
                2: {
                        "posx": x2,
                        "posy": y2,
                        "vx": init_direction2[0],
                        "vy": init_direction2[1],
                        "color": (27, 158, 119),
                        "alive": True
                }
        }
                
    def set_direction(self, player_id, vx, vy):
        """
        Update directional vector of a player.
        
        Args:
            player_id (int): ID of player.
            vx (int): Speed in x direction.
            vy (int): Speed in y direction.
            
        Returns:
            None
        """
        # Perform updates only if new direction is orthogonal to previous one.
        # Protects player from running straight into his own tail, i.e., if
        # moving to the left and then pressing the move right key
        if vx * self.players[player_id]["vx"] + vy * self.players[player_id]["vy"] == 0:
            self.players[player_id]["vx"] = vx
            self.players[player_id]["vy"] = vy
        
    def update_player(self, player_id):
        """
        Perform one time step, i.e., calculate new position of a player based
        on his old position and current directional vector.
        It is only performed if the player is still alive. Else the player is
        ignored.
        
        Args:
            player_id (int): ID of Player.
            
        Returns:
            alive (boolean): Whether player is still alive or not
        """
        if self.players[player_id]["alive"]:
            x_new = self.players[player_id]["posx"] + self.players[player_id]["vx"]
            y_new = self.players[player_id]["posy"] + self.players[player_id]["vy"]
            
            if (x_new < 0) or (y_new < 0) or (x_new >= self.num_x_tiles) or (y_new >= self.num_y_tiles):
                self.players[player_id]["alive"] = False
            elif (self.game_board[y_new, x_new] != 0):
                self.players[player_id]["alive"] = False
            else:
                self.game_board[y_new, x_new] = player_id
                self.players[player_id]["posx"] = x_new
                self.players[player_id]["posy"] = y_new
                
        return self.players[player_id]["alive"]


class GUI(object):
    """
    Object handling drawing of the field and catching of key press events
    from the user.
    This would be implemented by your client code.
    """
    
    def __init__(self, width, height, num_x_tiles, num_y_tiles):
        """
        Initializes object.
        
        Args:
            width (int): Width in pixel of one game cell.
            height (int): Height in pixel of one game cell.
            num_x_tiles (int): Width of game board, i.e., number of cells the
                board has in horizontal direction.
            num_y_tiles (int): Height of game board, i.e., number of cells the
                board has in vertical direction.
        """
        self.width = width
        self.height = height
        self.num_x_tiles = num_x_tiles
        self.num_y_tiles = num_y_tiles
        self.logic = Logic(num_x_tiles, num_y_tiles)
        
        pygame.init()
        pygame.display.set_caption("SampleTron")
        self.screen = pygame.display.set_mode((
                self.width * self.num_x_tiles,
                self.height * self.num_y_tiles
                ))
        
    def draw(self):
        """
        Draw the current state of the board.
        
        Returns:
            None
        """
        # Fill screen with black color
        self.screen.fill((0,0,0))
        for i in range(self.num_x_tiles):
            for j in range(self.num_y_tiles):
                y = 0 if i == 0 else i * self.height
                x = 0 if j == 0 else j * self.width
            
                w = self.width - 2
                h = self.height - 2
            
                # If current cell of board is zero paint it black, else paint
                # it in the color of the respective player.
                if self.logic.game_board[i, j] == 0:
                    color = (120, 120, 120)
                else:
                    color = self.logic.players[self.logic.game_board[i, j]]["color"]
                pygame.draw.rect(self.screen, color, (x, y, w, h))
        pygame.display.update()
        
    def event_loop(self):
        """
        Advance the game one click at a time. At every klick handle the events
        that occurred. If key down events occurred, this method checks whether
        they correspond to movement keys of a player and sets the corresponding
        directional vector accordingly.
        As soon as one player dies the game is over.
        
        Returns:
            None
        """
        clock = pygame.time.Clock()
        playing = True
        
        while playing:
                self.draw()

# Start the game
if __name__ == "__main__":
    gui = GUI(20, 20, 50, 50)
    gui.event_loop()
        