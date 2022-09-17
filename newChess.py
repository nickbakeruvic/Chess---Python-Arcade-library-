import arcade

# Colors
WHITE = 1
BLACK = -1

# Standard piece values for displaying evaluation
PAWN_VALUE = 1
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 8

# Game states
PLAY = 0
CHECKMATE = 1
STALEMATE = 2
INSUFFICIENT_MATERIAL = 3

# Screen size settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIXELS_PER_SQUARE = 100

class Piece:
    '''
    Piece class - represents a Piece on the chess board and is parent class to Pawn, Bishop, Knight, Rook, Queen, King

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        sprite:         sprite object to visually represent the piece for rendering through Arcade (Arcade.Sprite, initialized to None until add_sprite called)
        sprite_image:   url of the image to use (String, initialized to None until add_sprite called)
        moved:          repreents whether or not the piece has moved (Boolean, initialized to False)
    '''

    def __init__(self, color, x, y):
        '''Initializes Piece; sprite, sprite_image, moved initialized to None, None, False automatically'''
        self.color = color
        self.x = x
        self.y = y
        self.sprite = None
        self.sprite_image = None
        self.moved = False

    def add_sprite(self, scene, sprite_image):
        '''
        Adds sprite to the arcade scene; does not return
        
        Parameters:
            scene:          the scene to render the sprite (Arcade.Scene)
            sprite_image:   url of the image to use e.g. Chesssprites/bP.png for black pawn (String)
        '''
        self.sprite = arcade.Sprite(sprite_image, PIXELS_PER_SQUARE / 1000)
        self.sprite.center_x = (self.x + 1.5) * PIXELS_PER_SQUARE
        self.sprite.center_y = (self.y + 1.5) * PIXELS_PER_SQUARE
        scene.add_sprite(f"Piece at {self.x}, {self.y}", self.sprite)
        self.sprite_image = sprite_image

class Rook(Piece):
    '''
    Rook class - child class of Piece, represents a rook on the chessboard

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        value:          represents the "value in pawns" of the piece (int, corresponds to ROOK_VALUE constant)
    '''
    def __init__(self, color, x, y):
        '''Initializes Rook; uses Piece constructor'''
        Piece.__init__(self, color, x, y)
        self.value = ROOK_VALUE
    
    def __str__(self):
        '''Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black'''
        return "R" if self.color == WHITE else "r"

    # Adds all potential "moves" to self.legal_moves and all potential "takes"
    # to self.legal_takes. Moves and takes later evaluated to ensure they do
    # not move king into check by Chess.display_legal_moves
    def move(self, game_object):
        '''
        Adds all empty squares the rook could possibly move to to game_object.legal_moves
        and all pieces the piece could possibly take to game_object.legal_takes

        Parameters:
            game_object:    instance of Chess
        '''
        for i in range(1, 8):
            if game_object.check_moves_on_square(self, i, 0): break
            
        for i in range(1, 8):
            if game_object.check_moves_on_square(self, -i, 0): break

        for i in range(1, 8):
            if game_object.check_moves_on_square(self, 0, -i): break

        for i in range(1, 8):
            if game_object.check_moves_on_square(self, 0, i): break

class Knight(Piece):
    '''
    Knight class - child class of Piece, represents a rook on the chessboard

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        value:          represents the "value in pawns" of the piece (int, corresponds to KNIGHT_VALUE constant)
    '''
    def __init__(self, color, x, y):
        '''Initializes Knight; uses Piece constructor'''
        Piece.__init__(self, color, x, y)
        self.value = KNIGHT_VALUE

    def __str__(self):
        '''Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black'''
        return "N" if self.color == WHITE else "n"

    def move(self, game_object):
        '''
        Adds all empty squares the knight could possibly move to to game_object.legal_moves
        and all pieces the piece could possibly take to game_object.legal_takes

        Parameters:
            game_object:    instance of Chess
        '''
        game_object.check_moves_on_square(self, 1, 2)
        game_object.check_moves_on_square(self, 1, -2)
        game_object.check_moves_on_square(self, -1, 2)
        game_object.check_moves_on_square(self, -1, -2)
        game_object.check_moves_on_square(self, 2, 1)
        game_object.check_moves_on_square(self, 2, -1)
        game_object.check_moves_on_square(self, -2, 1)
        game_object.check_moves_on_square(self, -2, -1)

class Bishop(Piece):
    '''
    Bishop class - child class of Piece, represents a bishop on the chessboard

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        value:          represents the "value in pawns" of the piece (int, corresponds to BISHOP_VALUE constant)
    '''
    def __init__(self, color, x, y):
        '''Initializes Bishop; uses Piece constructor'''
        Piece.__init__(self, color, x, y)
        self.value = BISHOP_VALUE

    def __str__(self):
        '''Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black'''
        return "B" if self.color == WHITE else "b"

    def move(self, game_object):
        '''
        Adds all empty squares the bishop could possibly move to to game_object.legal_moves
        and all pieces the piece could possibly take to game_object.legal_takes

        Parameters:
            game_object:    instance of Chess
        '''
        for i in range(1, 8):
            if game_object.check_moves_on_square(self, i, i): break

        for i in range(1, 8):
            if game_object.check_moves_on_square(self, -i, i): break

        for i in range(1, 8):
            if game_object.check_moves_on_square(self, i, -i): break

        for i in range(1, 8):
            if game_object.check_moves_on_square(self, -i, -i): break

class Pawn(Piece):
    '''
    Pawn class - child class of Piece, represents a pawn on the chessboard

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        value:          represents the "value in pawns" of the piece (int, corresponds to PAWN_VALUE constant)
    '''
    def __init__(self, color, x, y):
        '''Initializes Pawn; uses Piece constructor'''
        Piece.__init__(self, color, x, y)
        self.value = PAWN_VALUE

    def __str__(self):
        '''Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black'''
        return "P" if self.color == WHITE else "p"

    def move(self, game_object):
        '''
        Adds all empty squares the pawn could possibly move to to game_object.legal_moves
        and all pieces the piece could possibly take to game_object.legal_takes

        Parameters:
            game_object:    instance of Chess
        '''
        game_object.check_moves_on_square(self, 0, 1 * self.color, False)
        
        # allow pawn to move forward 2 squares (can only move, not capture) if it hasn't moved
        if not self.moved:
            game_object.check_moves_on_square(self, 0, 2 * self.color, False)
        
        # allow pawn to capture (not move) to squares diagonally in front of it
        game_object.check_moves_on_square(self, 1, 1 * self.color, True, False)
        game_object.check_moves_on_square(self, -1, 1 * self.color, True, False)

class Queen(Piece):
    '''
    Queen class - child class of Piece, represents a queen on the chessboard

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        value:          represents the "value in pawns" of the piece (int, corresponds to QUEEN_VALUE constant)
    '''
    def __init__(self, color, x, y):
        '''Initializes Queen; uses Piece constructor'''
        Piece.__init__(self, color, x, y)
        self.value = QUEEN_VALUE

    def __str__(self):
        '''Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black'''
        return "Q" if self.color == WHITE else "q"

    def move(self, game_object):
        '''
        Adds all empty squares the queen could possibly move to to game_object.legal_moves
        and all pieces the piece could possibly take to game_object.legal_takes

        Parameters:
            game_object:    instance of Chess
        '''
        temp_rook = Rook(self.color, self.x, self.y)
        temp_bishop = Bishop(self.color, self.x, self.y)

        temp_rook.move(game_object)
        temp_bishop.move(game_object)

class King(Piece):
    '''
    King class - child class of Piece, represents a king on the chessboard

    Attributes:
        color:          represents the color of the piece (int, 1 or -1 corresponding to WHITE / BLACK constants)
        x, y:           coordinates on the chess board of the peice (int, 0 to 7)
        value:          represents the "value in pawns" of the piece (int, set to 0 as the value of a king is ambiguous)
    '''
    def __init__(self, color, x, y):
        '''Initializes King; uses Piece constructor'''
        Piece.__init__(self, color, x, y)
        self.value = 0

    def __str__(self):
        '''Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black'''
        return "K" if self.color == WHITE else "k"

    def move(self, game_object):
        '''
        Adds all empty squares the king could possibly move to to game_object.legal_moves
        and all pieces the piece could possibly take to game_object.legal_takes

        Parameters:
            game_object:    instance of Chess
        '''
        game_object.check_moves_on_square(self, 1, 1)
        game_object.check_moves_on_square(self, 1, 0)
        game_object.check_moves_on_square(self, 1, -1)
        game_object.check_moves_on_square(self, 0, -1)
        game_object.check_moves_on_square(self, -1, -1)
        game_object.check_moves_on_square(self, -1, 0)
        game_object.check_moves_on_square(self, -1, 1)
        game_object.check_moves_on_square(self, 0, 1)

class Move:
    '''
    Move class - represents a chess move & stores enough information to undo the move (used by Chess.undo_move())
    
    Attributes:
        prev_x, prev_y:     coordinates of piece that moved before moving (int, 0 to 7)
        new_x, new_y:       coordinates of piece that moved after moving (int, 0 to 7)
        moved_piece:        reference to piece that moved (Piece)
        taken_piece:        reference to piece that was taken (Piece / None if no piece taken)
        moved_piece_moved:  stores moved_piece.moved before the move / take (Boolean)
        taken_piece_moved:  stores taken_piece.moved before the move / take (Boolean / None if no piece taken)
        promotion:          whether this move promoted a pawn (Boolean, defaults to False)
    '''

    def __init__(self, prev_x, prev_y, new_x, new_y, moved_piece, taken_piece, moved_piece_moved, taken_piece_moved, taken_piece_sprite_img, promotion = False):
        '''Initializes Move'''
        self.prev_x = prev_x
        self.prev_y = prev_y
        self.new_x = new_x
        self.new_y = new_y
        self.moved_piece = moved_piece
        self.taken_piece = taken_piece
        self.moved_piece_moved = moved_piece_moved
        self.taken_piece_moved = taken_piece_moved
        self.taken_piece_sprite_img = taken_piece_sprite_img
        self.promotion = promotion

    def return_data(self):
        '''Returns tuple consisting of all class variables for easy unpacking'''
        return (self.prev_x, self.prev_y, self.new_x, self.new_y, self.moved_piece, self.taken_piece, self.moved_piece_moved, self.taken_piece_moved, self.taken_piece_sprite_img, self.promotion)

class Chess(arcade.Window):
    '''
    Chess class - visual representation of chess game

    Attributes:
        color_to_move:                      whose turn it is currently (int, 1 or -1 corresponding to WHITE / BLACK constants)
        king_in_check:                      whether king is in check (Boolean)
        selected_piece:                     the piece last clicked on; displays legal moves for this piece (Piece or None)
        game_state:                         whether game should proceed or is stopped e.g. checkmate / draw (int, corresponds to PLAY, STALEMATE, etc.)
        move_list:                          list of all moves played thus far in the game, used to undo moves (List[Move])
        legal_moves:                        list of legal squares that selected piece can legally move to stored as coordinate tuples (List[(x: int, y: int)])
        legal_takes:                        list of legal squares that selected piece can legally take on stored as coordinate tuples (List[(x: int, y: int)])
        white_king, black_king:             references to each player's king (Piece)
        white_king_rook, black_king_rook:   references to each player's kingside rook for checking castling legality (Piece)
        white_queen_rook, black_queen_rook: references to each player's queenside rook for checking castling legality (Piece)
        scene:                              the scene where sprites are rendered (Arcade.Scene)
        pieces:                             list of all pieces currently on the board (List[Piece])
    '''

    def __init__(self):
        '''Initializes Chess; initializes everything needed from Arcade'''
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title="Nick Baker's Chess")

        self.color_to_move = WHITE
        self.king_in_check = False
        self.selected_piece = None
        self.game_state = PLAY
        self.move_list, self.legal_moves, self.legal_takes = [], [], []
        self.white_king, self.black_king = None, None
        self.white_king_rook, self.white_queen_rook, self.black_king_rook, self.black_queen_rook = None, None, None, None

        self.scene = arcade.Scene()
        self.pieces = self.initialize_pieces()

        # start drawing the scene, load in all the images
        arcade.start_render()
        self.load_indicators()

        # draw first frame
        self.on_draw()

    def on_draw(self):
        '''Draw everything on the chessboard and display legal moves / takes (called every frame by Arcade)'''
        arcade.start_render()
        # draw chessboard, value analysis, and whose turn it is
        self.init_board()
        self.display_value()
        self.display_turn()

        # add undo button to scene
        temp_sprite_list = []
        temp_sprite = self.add_sprite((8, 0), "chesssprites/undo.png")
        temp_sprite_list.append(temp_sprite)

        # add legal moves to scene
        for entry in self.legal_moves:
            temp_sprite = self.add_sprite(entry, "chesssprites/brown_circle.png")
            temp_sprite_list.append(temp_sprite)

        # add legal takes to scene
        for entry in self.legal_takes:
            temp_sprite = self.add_sprite(entry, "chesssprites/red_circle.png", PIXELS_PER_SQUARE / 2222)
            temp_sprite_list.append(temp_sprite)

        # draw everything in the scene then remove everything temporary (moves / takes for selected piece)
        self.scene.draw()
        for sprite in temp_sprite_list:
            if sprite is not None: sprite.kill()

    def display_value(self):
        '''Displays the material advantage (in pawns) for each player e.g. if white is up 2 pawns,
            "+2" will be displayed beside white and "-2" will be displayed beside black'''
        value = 0
        for piece in self.pieces:
            if isinstance(piece, Pawn):
                value += PAWN_VALUE * piece.color
            elif isinstance(piece, Knight):
                value += KNIGHT_VALUE * piece.color
            elif isinstance(piece, Bishop):
                value += BISHOP_VALUE * piece.color
            elif isinstance(piece, Rook):
                value += ROOK_VALUE * piece.color
            elif isinstance(piece, Queen):
                value += QUEEN_VALUE * piece.color
        
        # draw the text beside each player
        if value < 0:
            arcade.draw_text(f"White: {value}", 8 * PIXELS_PER_SQUARE, 0.6 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width = PIXELS_PER_SQUARE, align="left")
            arcade.draw_text(f"Black: +{-value}", 8 * PIXELS_PER_SQUARE, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width = PIXELS_PER_SQUARE, align="left")

        elif value > 0:
            arcade.draw_text(f"White: +{value}", 8 * PIXELS_PER_SQUARE, 0.6 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width = PIXELS_PER_SQUARE, align="left")
            arcade.draw_text(f"Black: -{value}", 8 * PIXELS_PER_SQUARE, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width = PIXELS_PER_SQUARE, align="left")
    
    def display_turn(self):
        '''Displays whose turn it is at the top of the board, or checkmate / stalemate message'''
        if self.game_state == PLAY:
            turn = "White" if self.color_to_move == WHITE else "Black"
            arcade.draw_text(f"{turn} to move", 0, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center")

        elif self.game_state == CHECKMATE:
            turn = "White" if self.color_to_move == BLACK else "Black"
            arcade.draw_text(f"{turn} wins by Checkmate", 0, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center")

        elif self.game_state == STALEMATE:
            turn = "White" if self.color_to_move == BLACK else "Black"
            arcade.draw_text(f"Draw by Stalemate", 0, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center")

    def add_sprite(self, coords, image_path, sizing = 0.1):
        '''
        Adds sprite to the scene and returns a reference to it

        Paramters:
            coords:        tuple representing x,y coordinates for where the piece is located ((x: int, y: int) 0 to 7)
            image_path:    the file path to the sprite image e.g. chesssprites/bP for black pawn (String)
            sizing:        the scale at which to render the image (float, defaults to 0.1)
        '''
        sprite = arcade.Sprite(image_path, sizing)
        sprite.center_x = (coords[0] + 1.5)* PIXELS_PER_SQUARE
        sprite.center_y = (coords[1] + 1.5) * PIXELS_PER_SQUARE
        self.scene.add_sprite(image_path, sprite)
        return sprite

    def on_mouse_press(self, x, y, button, modifiers):
        '''
        Lets user select pieces, move, etc. with mouse clicks (called by Arcade every time mouse is clicked)

        Parameters:
            x, y:                   the pixel coordinates of mouse click where 0 is bottom left of the window (int, 0 to SCREEN_WIDTH/SCREEN_HEIGHT respectively)
            button (not used):      right or left mouse button (int, 1 corresponds to right; 4 corresponds to left)
            modifiers (not used):   0 normally, 2 if shift pressed, 4 if ctrl pressed, etc. (int)
        '''

        # check if undo button pressed
        if x > 9 * PIXELS_PER_SQUARE and x < 10 * PIXELS_PER_SQUARE and y < 2 * PIXELS_PER_SQUARE and y > 1 * PIXELS_PER_SQUARE:
            # undo last move, check conditional variables, re-generate fen
            self.undo_move(1)
            self.king_in_check = self.in_check()
            self.game_state = PLAY
            self.generate_fen()
            return
        
        # stop play if game is over
        if self.game_state != PLAY: return

        # convert x and y in pixels to integer representing square clicked (both 0 to 7)
        x_coord = x // PIXELS_PER_SQUARE - 1
        y_coord = y // PIXELS_PER_SQUARE - 1

        # set cur_piece to be the piece clicked
        cur_piece = self.get_piece_at(x_coord, y_coord)

        # check if user is trying to castle
        if self.selected_piece is not None and isinstance(self.selected_piece, King) and cur_piece is not None and isinstance(cur_piece, Rook): 
            # try castle (may fail because king moved, trying to castle through check, etc.)
            if self.try_castle(cur_piece):
                self.generate_fen()
                return
        
        # check if legal move has been selected
        if self.selected_piece is not None and self.selected_piece.color == self.color_to_move and cur_piece is None and (x_coord, y_coord) in self.legal_moves:
            self.move_piece(x_coord, y_coord)

        # check if legal take has been selected
        elif self.selected_piece is not None and self.selected_piece.color == self.color_to_move and cur_piece is not None and self.selected_piece.color != cur_piece.color and (x_coord, y_coord) in self.legal_takes:
            self.take_piece(x_coord, y_coord, cur_piece)

        # check if a new piece that can move has been selected
        elif cur_piece is not None and cur_piece.color == self.color_to_move:
            # select piece and show legal moves for it
            self.selected_piece = cur_piece
            self.legal_moves, self.legal_takes = [], []
            self.display_legal_moves(self.selected_piece)

        # deselect piece, toggle off legal moves
        else:
            self.selected_piece = None
            self.legal_moves = []
            self.legal_takes = []

        # record whether king in check
        self.king_in_check = self.in_check()

        # generate fen string for analysis purposes / exporting the board
        self.generate_fen()

        # check for checkmate / stalemate / draw by insufficient material
        self.game_state = self.check_legal_moves()
        if self.game_state == PLAY: self.game_state == self.check_sufficient_material()

    def check_sufficient_material(self):
        return PLAY
        for piece in self.pieces: 
            if piece.color == WHITE:
                white_value += piece.Value

    def check_legal_moves(self):
        '''
        Iterate through all pieces and ensure that a legal move exists; otherwise end the game
        and note checkmate / stalemate
        '''

        backup_moves = self.legal_moves
        backup_takes = self.legal_takes
        self.legal_moves, self.legal_takes = [], []

        found_legal_moves = False

        for piece in self.pieces:
            if piece.color == self.color_to_move:
                self.display_legal_moves(piece)
                if len(self.legal_moves) + len(self.legal_takes) != 0: 
                    found_legal_moves = True
                    break
        
        self.legal_moves = backup_moves
        self.legal_takes = backup_takes
        if found_legal_moves: return PLAY
        return CHECKMATE if self.in_check() else STALEMATE

    def generate_fen(self):
        '''
        Generates a FEN string (standard way to represent the state of a chess board in a single string).
        The locations of all pieces, legality of castling, and who is to move is all stored; the position
        can be then exported to a website or engine.
        '''

        fen = ""
        board = [[0 for x in range(8)] for y in range(8)] 
        board = self.initialize_board(board)

        # iterate through every square in the chessboard, noting whether it is blank or occupied
        for y in range(7, -1, -1):
            count = 0
            # for every row of the chessboard, generate a string the represents the pieces (e.g. 3b2R means 3 blank spaces,
            # then lowercase is black and b for bishop so black bishop, then 2 blank spaces, then a white rook)
            cur_fen_line = ""
            for x in range(8):
                if board[x][y] == 0: 
                    count += 1
                else:
                    if count != 0: 
                        cur_fen_line += str(count)
                        count = 0
                    cur_fen_line += str(board[x][y])
            
            if count != 0: cur_fen_line += str(count)
            
            # strings representing ranks (rows) of the chessboard are separated by slashes
            if len(fen) != 0: fen += "/"
            fen += f"{cur_fen_line}"

        # note who is to move
        fen += " w " if self.color_to_move == WHITE else " b "

        white_cant_castle = self.white_king.moved or (self.white_king_rook.moved and self.white_queen_rook.moved)
        black_cant_castle = self.black_king.moved or (self.black_king_rook.moved and self.black_queen_rook.moved)
        
        # note who can castle, and what side: uppercase is for white, 'k' is for kingside, 'q' for queenside, '-' means can't castle either side
        # e.g. -q means white cannot castle and black can only castle queenside
        if (white_cant_castle and black_cant_castle):
            fen += "-"
            
        elif not white_cant_castle:
            if not self.white_king_rook.moved: fen += "K"
            if not self.white_queen_rook.moved: fen += "Q"

        if not black_cant_castle:
            if not self.black_king_rook.moved: fen += "k"
            if not self.black_queen_rook.moved: fen += "q"

        # move count etc. which is not necessary for engine analysis or exporting position but required to be included in the string sometimes
        fen += " - 0 1"
        return fen

    def initialize_board(self, board):
        '''
        Fills board with references to the pieces that occupy the corresponding squares
        
        Parameters:
            board: 2-dimensional list representing the chess board (list[list[]], should be 8 x 8 and empty when passed in)
        '''
        for piece in self.pieces:
            board[piece.x][piece.y] = piece

        return board

    def promote_selected_pawn(self):
        '''
        Promotes the selected piece (self.selected_piece) to a queen, meant to be called by Chess.move() or Chess.take() when a pawn reaches the last rank of the board
        '''
        self.selected_piece.__class__ = Queen
        self.selected_piece.sprite.kill()
        sprite_image = "chesssprites/wQ.png" if self.selected_piece.color == WHITE else "chesssprites/bQ.png"
        self.selected_piece.add_sprite(self.scene, sprite_image)

    def take_piece(self, x_coord, y_coord, cur_piece):
        '''
        Takes a piece on the chessboard - removes the taken piece from the sprite list and piece list, udpates the position & sprite position of the piece taking (self.selected_piece)

        Parameters:
            x_coord, y_coord:   the coordinates the piece to be taken is on (int, 0 to 7)
            cur_piece:          the piece to be taken (Piece)
        '''

        # get pixel position of where the sprite should be
        normalized_x  = (x_coord + 1) * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE / 2
        normalized_y  = (y_coord + 1) * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE / 2
        
        # record info to create Move record
        prev_x, prev_y, moved = self.selected_piece.x, self.selected_piece.y, self.selected_piece.moved

        # update position of piece taking
        self.selected_piece.x = x_coord
        self.selected_piece.y = y_coord
        self.selected_piece.sprite.center_x = normalized_x
        self.selected_piece.sprite.center_y = normalized_y
        self.selected_piece.moved = True

        # promote pawn if needed
        if (y_coord == 0 or y_coord == 7) and isinstance(self.selected_piece, Pawn):
            self.promote_selected_pawn()

            # record the move
            current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, cur_piece, moved, cur_piece.moved, cur_piece.sprite_image, True)
            self.move_list.append(current_move)
        else:
            # record the move
            current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, cur_piece, moved, cur_piece.moved, cur_piece.sprite_image)
            self.move_list.append(current_move)
            
        # remove the taken piece
        self.selected_piece = None
        cur_piece.sprite.kill()
        self.pieces.remove(cur_piece)

        # reset legal moves & takes
        self.legal_moves = []
        self.legal_takes = []

        # move to next turn
        self.color_to_move *= -1

    def move_piece(self, x_coord, y_coord):
        '''
        Moves self.selected_piece to a new square and updates the sprite location
        '''

        # get pixel position of where the sprite should be
        normalized_x  = (x_coord + 1) * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE / 2
        normalized_y  = (y_coord + 1) * PIXELS_PER_SQUARE + PIXELS_PER_SQUARE / 2

        # record info to create Move record
        prev_x, prev_y, moved = self.selected_piece.x, self.selected_piece.y, self.selected_piece.moved

        # update position of piece
        self.selected_piece.x = x_coord
        self.selected_piece.y = y_coord
        self.selected_piece.sprite.center_x = normalized_x
        self.selected_piece.sprite.center_y = normalized_y
        self.selected_piece.moved = True
        
        # promote pawns if necessary
        if isinstance(self.selected_piece, Pawn) and (y_coord == 0 or y_coord == 7):
            self.promote_selected_pawn()

            # record the move
            current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, None, moved, None, None, True)
            self.move_list.append(current_move)
        else:
            # record the move
            current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, None, moved, None, None)
            self.move_list.append(current_move)
            
        # deselect the piece; reset legal moves & takes
        self.selected_piece = None
        self.legal_moves = []
        self.legal_takes = []

        # move to next turn
        self.color_to_move *= -1

    def try_castle(self, cur_piece):
        if self.selected_piece.moved or cur_piece.moved or self.selected_piece.color != cur_piece.color: return False

        king = self.selected_piece
        rook = cur_piece

        kingside_castle = rook.x > king.x

        if kingside_castle:
            if self.in_check(king.x + 1, king.y) or self.in_check(king.x + 2, king.y) or self.in_check(king.x + 3, king.y): return False

            piece_1 = self.get_piece_at(king.x + 1, king.y)
            piece_2 = self.get_piece_at(king.x + 2, king.y)
            piece_3 = None
        else:
            if self.in_check(king.x - 1, king.y) or self.in_check(king.x - 2, king.y) or self.in_check(king.x - 3, king.y) or self.in_check(king.x - 4, king.y): return False

            piece_1 = self.get_piece_at(king.x - 1, king.y)
            piece_2 = self.get_piece_at(king.x - 2, king.y)
            piece_3 = self.get_piece_at(king.x - 3, king.y)

        if piece_1 is not None or piece_2 is not None or piece_3 is not None: return False

        castle_move = Move(king.x, king.y, rook.x, rook.y, king, rook, None, None, None)

        temp_x, temp_y = king.x, king.y

        king.x, king.y = rook.x, rook.y
        rook.x, rook.y = temp_x, temp_y

        if kingside_castle:
            king.x -= 1
            rook.x += 1
        else:
            king.x += 1
            rook.x -= 2

        king.sprite.center_x = (king.x + 1.5) * PIXELS_PER_SQUARE
        king.sprite.center_y = (king.y + 1.5) * PIXELS_PER_SQUARE

        rook.sprite.center_x = (rook.x + 1.5) * PIXELS_PER_SQUARE
        rook.sprite.center_y = (rook.y + 1.5) * PIXELS_PER_SQUARE

        king.moved, rook.moved = True, True

        self.move_list.append(castle_move)

        self.king_in_check = self.in_check()
        self.legal_moves = []
        self.legal_takes = []   
        self.color_to_move *= -1
        self.selected_piece = None
        return True

    def in_check(self, x = None, y = None):

        backup_legal = []
        backup_takes = []

        # unnecessary ?
        for move in self.legal_moves:
            backup_legal.append(move)

        for move in self.legal_takes:
            backup_takes.append(move)

        self.legal_takes = []
        self.legal_moves = []

        if x is None or y is None:
             (x,y) = (self.white_king.x, self.white_king.y) if self.color_to_move == WHITE else (self.black_king.x, self.black_king.y)

        to_return = False

        for piece in self.pieces:
            if piece.color == self.color_to_move: continue
            piece.move(self)

            if (x, y) in self.legal_takes:
                to_return = True
                break
    
            self.legal_takes = []

        self.legal_moves = backup_legal
        self.legal_takes = backup_takes
        return to_return

    def undo_move(self, remove_indicators = None):

        # store undone moves ?
        if len(self.move_list) == 0: return

        last_move = self.move_list[-1]
        (prev_x, prev_y, new_x, new_y, moved_piece, taken_piece, moved_piece_moved, taken_piece_moved, taken_sprite, promotion) = last_move.return_data()

        if moved_piece_moved is None:
            # undo castling
            taken_piece.x = new_x
            taken_piece.y = new_y
            taken_piece.sprite.center_x = (new_x + 1.5) * PIXELS_PER_SQUARE
            taken_piece.sprite.center_y = (new_y + 1.5) * PIXELS_PER_SQUARE

            moved_piece.x = prev_x
            moved_piece.y = prev_y
            moved_piece.sprite.center_x = (prev_x + 1.5) * PIXELS_PER_SQUARE
            moved_piece.sprite.center_y = (prev_y + 1.5) * PIXELS_PER_SQUARE

            moved_piece.moved = False
            taken_piece.moved = False
        else:
            
            if promotion:
                moved_piece.__class__ = Pawn
                moved_piece.sprite.kill()
                sprite_image = "chesssprites/wP.png" if moved_piece.color == WHITE else "chesssprites/bP.png"
                moved_piece.add_sprite(self.scene, sprite_image)

            # return moved piece to previous position
            moved_piece.x = prev_x
            moved_piece.y = prev_y
            moved_piece.sprite.center_x = (prev_x + 1.5) * PIXELS_PER_SQUARE
            moved_piece.sprite.center_y = (prev_y + 1.5) * PIXELS_PER_SQUARE

            moved_piece.moved = moved_piece_moved

            # return taken piece to previous position IF piece was taken
            if taken_piece is not None:
                self.pieces.append(taken_piece)
                taken_piece.add_sprite(self.scene, taken_sprite)
                taken_piece.moved = taken_piece_moved

        self.move_list.pop()
        self.color_to_move *= -1

        if remove_indicators is not None:
            self.legal_moves = []
            self.legal_takes = []
            self.selected_piece = None

    def display_legal_moves(self, piece):
        piece.move(self)

        to_remove = []
        for move in self.legal_moves:
            (x,y) = move
            if x < 0 or x > 7 or y < 0 or y > 7: to_remove.append(move)
        
        for entry in to_remove:
            self.legal_moves.remove(entry)

        for move in self.legal_moves:
            (x,y) = move
            if self.in_check_after_move(x, y, piece): self.legal_moves.remove(move)

        for move in self.legal_takes:
            (x,y) = move
            piece_to_take = self.get_piece_at(x, y)
            if self.in_check_after_move(x, y, piece, piece_to_take): self.legal_takes.remove(move)

    def in_check_after_move(self, x, y, piece, piece_to_take=None):
        
        to_return = False
        prev_x, prev_y = piece.x, piece.y

        piece.x = x
        piece.y = y

        if piece_to_take:
            piece_to_take.x = -1
            piece_to_take.y = -1

        if self.in_check(): to_return = True

        piece.x = prev_x
        piece.y = prev_y

        if piece_to_take:
            piece_to_take.x = x
            piece_to_take.y = y

        return to_return

    def get_piece_at(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece

        return None

    def check_moves_on_square(self, cur_piece, x_offset, y_offset, can_take = True, can_move = True):

        x_coord = cur_piece.x + x_offset
        y_coord = cur_piece.y + y_offset

        other_piece = self.get_piece_at(x_coord, y_coord)

        if other_piece is None and can_move: 
            self.legal_moves.append((x_coord, y_coord))
            return False
        elif other_piece is not None and other_piece.color != cur_piece.color and can_take: 
            self.legal_takes.append((x_coord, y_coord))
        
        return True

        
    def initialize_pieces(self):

        piece_list = []
        
        for x in range(8):
            
            self.create_piece(piece_list, Pawn, WHITE, x, 1, "chesssprites/wP.png")
            self.create_piece(piece_list, Pawn, BLACK, x, 6, "chesssprites/bP.png")

            if x == 0:
                self.white_queen_rook = self.create_piece(piece_list, Rook, WHITE, x, 0, "chesssprites/wR.png")
                self.black_queen_rook = self.create_piece(piece_list, Rook, BLACK, x, 7, "chesssprites/bR.png")
                
            elif x == 7:
                self.white_king_rook = self.create_piece(piece_list, Rook, WHITE, x, 0, "chesssprites/wR.png")
                self.black_king_rook = self.create_piece(piece_list, Rook, BLACK, x, 7, "chesssprites/bR.png")

            elif x == 1 or x == 6:
                self.create_piece(piece_list, Knight, WHITE, x, 0, "chesssprites/wN.png")
                self.create_piece(piece_list, Knight, BLACK, x, 7, "chesssprites/bN.png")
                
            elif x == 2 or x == 5:
                self.create_piece(piece_list, Bishop, WHITE, x, 0, "chesssprites/wB.png")
                self.create_piece(piece_list, Bishop, BLACK, x, 7, "chesssprites/bB.png")

            elif x == 3:
                self.create_piece(piece_list, Queen, WHITE, x, 0, "chesssprites/wQ.png")
                self.create_piece(piece_list, Queen, BLACK, x, 7, "chesssprites/bQ.png")
            
            elif x == 4:
                self.white_king = self.create_piece(piece_list, King, WHITE, x, 0, "chesssprites/wK.png")
                self.black_king = self.create_piece(piece_list, King, BLACK, x, 7, "chesssprites/bK.png")
            
        return piece_list

    def create_piece(self, piece_list, piece_class, color, x, y, sprite_image):
        
        piece = piece_class(color, x, y)
        piece.add_sprite(self.scene, sprite_image)
        piece_list.append(piece)
        return piece

    def init_board(self):
        
        x = PIXELS_PER_SQUARE
        y = 2 * PIXELS_PER_SQUARE
        count = 0

        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, arcade.color.BISTRE)

        while x < SCREEN_WIDTH - PIXELS_PER_SQUARE:
            while y < SCREEN_HEIGHT:
                if count % 2 == 0:
                    arcade.draw_lrtb_rectangle_filled(x, x + PIXELS_PER_SQUARE, y, y - PIXELS_PER_SQUARE, arcade.color.CAMEL)
                else:
                    arcade.draw_lrtb_rectangle_filled(x, x + PIXELS_PER_SQUARE, y, y - PIXELS_PER_SQUARE, arcade.color.CHAMPAGNE)
                count += 1
                y += 100
            count += 1
            x += PIXELS_PER_SQUARE
            y = 2 * PIXELS_PER_SQUARE


        if self.selected_piece is not None:
                temp_x = (self.selected_piece.x + 1) * PIXELS_PER_SQUARE
                temp_y = (self.selected_piece.y + 1) * PIXELS_PER_SQUARE
                arcade.draw_lrtb_rectangle_filled(temp_x, temp_x + PIXELS_PER_SQUARE, temp_y + PIXELS_PER_SQUARE, temp_y, arcade.color.LIGHT_SALMON)

        if self.king_in_check:
            
            king = self.white_king if self.color_to_move == WHITE else self.black_king

            temp_x = (king.x + 1) * PIXELS_PER_SQUARE
            temp_y = (king.y + 1) * PIXELS_PER_SQUARE
            arcade.draw_lrtb_rectangle_filled(temp_x, temp_x + PIXELS_PER_SQUARE, temp_y + PIXELS_PER_SQUARE, temp_y, arcade.color.CAMEO_PINK)

        self.draw_rank_file_names()
        
    def draw_rank_file_names(self):
        arcade.draw_text("A", 1.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("B", 2.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("C", 3.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("D", 4.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("E", 5.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("F", 6.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("G", 7.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("H", 8.75 * PIXELS_PER_SQUARE, 1.05 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")

        arcade.draw_text("1", 1.05 * PIXELS_PER_SQUARE, 1.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("2", 1.05 * PIXELS_PER_SQUARE, 2.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("3", 1.05 * PIXELS_PER_SQUARE, 3.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("4", 1.05 * PIXELS_PER_SQUARE, 4.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("5", 1.05 * PIXELS_PER_SQUARE, 5.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("6", 1.05 * PIXELS_PER_SQUARE, 6.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("7", 1.05 * PIXELS_PER_SQUARE, 7.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("8", 1.05 * PIXELS_PER_SQUARE, 8.75 * PIXELS_PER_SQUARE, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")


    def load_indicators(self):
        # when initializing the window, load these sprites into memory before they are needed
        # to eliminate lag when displaying them for the first time
        load_move_indicator = self.add_sprite((-1, -1), "chesssprites/brown_circle.png")
        load_take_indicator = self.add_sprite((-1, -1), "chesssprites/red_circle.png")
        load_move_indicator.kill()
        load_take_indicator.kill()

Chess()
arcade.run()
