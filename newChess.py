from __future__ import annotations 
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
        '''
        Initializes Chess; initializes everything needed from Arcade
        '''
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
        '''
        Draw everything on the chessboard and display legal moves / takes (called every frame by Arcade)
        '''
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
        '''
        Displays the material advantage (in pawns) for each player e.g. if white is up 2 pawns,
        "+2" will be displayed beside white and "-2" will be displayed beside black
        '''
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
        '''
        Displays whose turn it is at the top of the board, or checkmate / stalemate message
        '''
        if self.game_state == PLAY:
            turn = "White" if self.color_to_move == WHITE else "Black"
            arcade.draw_text(f"{turn} to move", 0, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center")

        elif self.game_state == CHECKMATE:
            turn = "White" if self.color_to_move == BLACK else "Black"
            arcade.draw_text(f"{turn} wins by Checkmate", 0, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center")

        elif self.game_state == STALEMATE:
            turn = "White" if self.color_to_move == BLACK else "Black"
            arcade.draw_text(f"Draw by Stalemate", 0, 9.1 * PIXELS_PER_SQUARE, arcade.color.WHITE, 24, width=SCREEN_WIDTH, align="center")

    def add_sprite(self, coords: tuple(int, int), image_path: str, sizing: float = 0.1) -> arcade.Sprite:
        '''
        Adds sprite to the scene and returns a reference to it

        Paramters:
            coords:        tuple representing x,y coordinates for where the piece is located (0 to 7)
            image_path:    the file path to the sprite image e.g. chesssprites/bP for black pawn
            sizing:        the scale at which to render the image (defaults to 0.1 for 100 x 100 pixel squares)

        Returns:
            the created sprite
        '''
        sprite = arcade.Sprite(image_path, sizing)
        sprite.center_x = (coords[0] + 1.5)* PIXELS_PER_SQUARE
        sprite.center_y = (coords[1] + 1.5) * PIXELS_PER_SQUARE
        self.scene.add_sprite(image_path, sprite)
        return sprite

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        '''
        Lets user select pieces, move, etc. with mouse clicks (called by Arcade every time mouse is clicked)

        Parameters:
            x, y:                   the pixel coordinates of mouse click where 0 is bottom left of the window (0 to SCREEN_WIDTH/SCREEN_HEIGHT respectively)
            button (not used):      right or left mouse button or other (1 corresponds to right; 4 corresponds to left)
            modifiers (not used):   0 normally, 2 if shift pressed, 4 if ctrl pressed, etc.
        '''

        # check if undo button pressed
        if x > 9 * PIXELS_PER_SQUARE and x < 10 * PIXELS_PER_SQUARE and y < 2 * PIXELS_PER_SQUARE and y > 1 * PIXELS_PER_SQUARE:
            # undo last move, check conditional variables, re-generate fen
            self.undo_move()
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

    def check_legal_moves(self) -> int:
        '''
        Iterate through all pieces and ensure that a legal move exists; otherwise end the game
        and note checkmate / stalemate

        Returns:
            int corresponding to the gamestate constants (PLAY, CHECKMATE, etc.)
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

    def generate_fen(self) -> str:
        '''
        Generates a FEN string (standard way to represent the state of a chess board in a single string).
        The locations of all pieces, legality of castling, and who is to move is all stored; the position
        can be then exported to a website or engine.

        Returns:
            The generated FEN string
        '''
        fen = ""
        board = [[0 for x in range(8)] for y in range(8)] 
        self.initialize_board(board)

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
        print(fen)
        return fen

    def initialize_board(self, board: list[list]):
        '''
        Fills board with references to the pieces that occupy the corresponding squares
        
        Parameters:
            board: 2-dimensional list representing the chess board (should be 8 x 8 and empty when passed in)
        '''
        for piece in self.pieces:
            board[piece.x][piece.y] = piece

    def promote_selected_pawn(self):
        '''
        Promotes the selected piece (self.selected_piece) to a queen, meant to be called by Chess.move() or Chess.take() when a pawn reaches the last rank of the board
        '''
        self.selected_piece.__class__ = Queen
        self.selected_piece.sprite.kill()
        sprite_image = "chesssprites/wQ.png" if self.selected_piece.color == WHITE else "chesssprites/bQ.png"
        self.selected_piece.add_sprite(self.scene, sprite_image)

    def take_piece(self, x_coord: int, y_coord: int, cur_piece: Piece):
        '''
        Takes a piece on the chessboard - removes the taken piece from the sprite list and piece list, udpates the position & sprite position of the piece taking (self.selected_piece)

        Parameters:
            x_coord, y_coord:   the coordinates the piece to be taken is on (0 to 7)
            cur_piece:          the piece to be taken
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

    def move_piece(self, x_coord: int, y_coord: int):
        '''
        Moves self.selected_piece to a new square and updates the sprite location

        Parameters:
            x_coord, y_coord:   new location of self.selected_piece
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

    def try_castle(self, rook: Rook) -> bool:
        '''
        Checks if castling is legal - rook hasn't moved, king hasn't moved, none of the castling squares are in check

        Parameters:
            rook:  the rook to be castled with

        Returns:
            False if castling with the selected king & rook is illegal, pieces do not move
            True if castling is legal, pieces moved to castled positions
        '''
        # can't castle if rook moved or rook is not same color as king
        if self.selected_piece.moved or rook.moved or self.selected_piece.color != rook.color: return False

        king = self.selected_piece

        # determine whether to attempt kingside or queenside castle
        kingside_castle = rook.x > king.x

        # return false if castling through check
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

        # return false if any pieces between the king & rook
        if piece_1 is not None or piece_2 is not None or piece_3 is not None: return False

        # record the move
        castle_move = Move(king.x, king.y, rook.x, rook.y, king, rook, None, None, None)

        # swap pieces
        temp_x, temp_y = king.x, king.y
        king.x, king.y = rook.x, rook.y
        rook.x, rook.y = temp_x, temp_y
        king.moved, rook.moved = True, True

        if kingside_castle:
            king.x -= 1
            rook.x += 1
        else:
            king.x += 1
            rook.x -= 2

        # update sprites
        king.sprite.center_x = (king.x + 1.5) * PIXELS_PER_SQUARE
        king.sprite.center_y = (king.y + 1.5) * PIXELS_PER_SQUARE
        rook.sprite.center_x = (rook.x + 1.5) * PIXELS_PER_SQUARE
        rook.sprite.center_y = (rook.y + 1.5) * PIXELS_PER_SQUARE

        # record the move & reset values pertaining to selected piece
        self.move_list.append(castle_move)

        self.king_in_check = self.in_check()
        self.legal_moves = []
        self.legal_takes = []   
        self.color_to_move *= -1
        self.selected_piece = None
        return True

    def in_check(self, x: int = None, y: int = None) -> bool:
        '''
        Checks whether a given square or king is in check. If x, y supplied checks that square, otherwise,
        checks the current king

        Parameters:
            x, y:   coordinates of the square to check (defaults to None)

        Returns:
            True if square is in check, False otherwise
        '''
        # back up currently displayed moves & takes
        backup_legal = []
        backup_takes = []
        for move in self.legal_moves:
            backup_legal.append(move)

        for move in self.legal_takes:
            backup_takes.append(move)

        self.legal_takes = []
        self.legal_moves = []

        # check the square containing the current king for checks if no coordinates specified
        if x is None or y is None:
             (x,y) = (self.white_king.x, self.white_king.y) if self.color_to_move == WHITE else (self.black_king.x, self.black_king.y)

        to_return = False
        # check every piece that could attack the square (of the color not currently moving)
        for piece in self.pieces:
            if piece.color == self.color_to_move: continue
            piece.move(self)
            # break if the square is in check
            if (x, y) in self.legal_takes:
                to_return = True
                break
    
            self.legal_takes = []

        # restore currently displayed moves & takes, return whether the square is in check
        self.legal_moves = backup_legal
        self.legal_takes = backup_takes
        return to_return

    def undo_move(self):
        '''
        Undo the last move in self.move_list; clears self.legal_takes and self.legal_moves
        '''
        # check if there are moves to undo
        if len(self.move_list) == 0: return

        # record values of last move
        last_move = self.move_list[-1]
        (prev_x, prev_y, new_x, new_y, moved_piece, taken_piece, moved_piece_moved, taken_piece_moved, taken_sprite, promotion) = last_move.return_data()

        # undo move / take
        if moved_piece is not None:
            
            if promotion:
                # unpromote pawn
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

        # undo castle
        else:
            # swap positions of king & rook and update sprites
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

        # update move_list and who is to move
        self.move_list.pop()
        self.color_to_move *= -1

        # clear legal move and takes as board state has changed; unselect if anything was selected
        self.legal_moves = []
        self.legal_takes = []
        self.selected_piece = None

    def display_legal_moves(self, piece: Piece):
        '''
        Adds all legal moves & takes for the specified piece to self.legal_moves & self.legal_takes (respectively)

        Parameters:
            piece:  the piece to display moves for (Piece)
        '''
        # add all possible moves / takes to self.legal_moves / self.legal_takes
        piece.move(self)

        # remove moves that are outside the board
        to_remove = []
        for move in self.legal_moves:
            (x,y) = move
            if x < 0 or x > 7 or y < 0 or y > 7: to_remove.append(move)
        for entry in to_remove:
            self.legal_moves.remove(entry)

        # if king is in check after piece moves, move is not legal thus remove it
        for move in self.legal_moves:
            (x,y) = move
            if self.in_check_after_move(x, y, piece): self.legal_moves.remove(move)

        # if king is in check after piece takes, move is not legal thus remove it
        for move in self.legal_takes:
            (x,y) = move
            piece_to_take = self.get_piece_at(x, y)
            if self.in_check_after_move(x, y, piece, piece_to_take): self.legal_takes.remove(move)

    def in_check_after_move(self, x: int, y: int, piece: Piece, piece_to_take: Piece = None) -> bool:
        '''
        Performs the specified move and returns whether the king is in check after making the move. If 
        taking another piece piece_to_take should be specified, otherwise, it should not be given & default to None.

        Parameters:
            x, y:           coordinates to which the piece is going to move / take (int, 0 to 7)
            piece:          the piece that is going to move / take (Piece)
            piece_to_take:  the piece that is going to be taken (Piece, defaults to None)

        Returns:
            True if king is in check after making the move, otherwise False
        '''
        to_return = False
        prev_x, prev_y = piece.x, piece.y

        # temporarily update positions of piece and piece_to_take
        piece.x = x
        piece.y = y

        # remove piece_to_take from the board if specified
        if piece_to_take:
            piece_to_take.x = -1
            piece_to_take.y = -10

        # note if in check after making move
        if self.in_check(): to_return = True

        # put pieces back
        piece.x = prev_x
        piece.y = prev_y

        if piece_to_take:
            piece_to_take.x = x
            piece_to_take.y = y

        return to_return

    def get_piece_at(self, x: int, y: int) -> Piece:
        '''
        Returns the piece at specified x, y coordinates on the board

        Parameters:
            x, y:   square to check on the board (int, 0 to 7)
        
        Returns:
            None if square is unoccupied, otherwise a reference to the piece occupying the square
        '''
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece

        return None

    def check_moves_on_square(self, cur_piece: Piece, x_offset: int, y_offset: int, can_take: bool = True, can_move: bool = True) -> bool:
        '''
        Given a square and piece, checks if that piece could move / take on that square and if so,
        appends the move to self.legal_moves or self.legal_takes. Returns True if the square is occupied
        by a piece of either color, False otherwise. Takes will only be appended if
        can_take is True, Moves will only be appended if can_move is True. The square's coordinate
        are calculated by adding the offsets to the current coordinates of cur_piece.

        Parameters:
            cur_piece:          the piece to move (Piece)
            x_offset, y_offset: which square to check relative to cur_piece's positions (int, 0 to 7)
                                ex. x_offset = 2, y_offset = 2, cur_piece is at 2,3 -> the coordinates to check would be 4,5
            can_take:           indicates whether the piece should be allowed to take (Boolean, defaults to True)
            can_move:           indicates whether the piece should be allowed to move (Boolean, defaults to True)
        
        Returns:
            True if a piece is located on the square to check, False otherwise.

        Example use:   for checking pawn moves, pawns can take diagonally but cannot move diagonally -> call with can_take = True, can_move = False
        '''
        x_coord = cur_piece.x + x_offset
        y_coord = cur_piece.y + y_offset

        other_piece = self.get_piece_at(x_coord, y_coord)

        if other_piece is None and can_move: 
            self.legal_moves.append((x_coord, y_coord))
            return False
        elif other_piece is not None and other_piece.color != cur_piece.color and can_take: 
            self.legal_takes.append((x_coord, y_coord))
        
        return True

        
    def initialize_pieces(self) -> list[Piece]:
        '''
        Initializes a full board of chess pieces at the correct starting locations & adds the proper sprites.

        Returns:
            piece_list, a list of references to all Piece objects created.
        '''
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

    def create_piece(self, piece_list: list[Piece], piece_class: type, color: int, x: int, y: int, sprite_image: str) -> Piece:
        '''
        Helper function for initialize_pieces. Creates a Piece object of the specified type (Rook, Knight, etc.),
        adds the specified sprite image, and adds it to piece_list.

        Parameters:
            piece_list:     the list to append the piece to (List[Piece])
            piece_class:    the class of the Piece (Rook, Knight, etc.)
            color:          color of the piece to create (int, based on WHITE / BLACK constants)
            x, y:           coordinates of the piece (int, 0 to 7)
            sprite_image:   path to the image for the sprite (String)

        Returns:
            reference to the created piece (Rook, Knight, etc.)
        '''
        piece = piece_class(color, x, y)
        piece.add_sprite(self.scene, sprite_image)
        piece_list.append(piece)
        return piece

    def init_board(self):
        '''
        Draws the squares of the board, highlights the square self.selected_piece is on, highlights the square king is on if in check,
        draws the rank / file letters and numbers
        '''
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

        # draw the rank / file letters and numbers
        self.draw_rank_file_names()
        
    def draw_rank_file_names(self):
        '''
        Helper function for init_board. Draws A B C D ... in the bottom right of the bottom row of squares (the files) and
        1 2 3 4 ... in the top left of the leftmost column of squares (the ranks)
        '''
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
        '''
        Creates sprite images for the legal move / legal take indicators then instantly removes them. If this is not done,
        then the first time a piece is clicked, there will be a half-second delay before the legal moves are displayed as the
        images are not "loaded in".
        '''
        load_move_indicator = self.add_sprite((-1, -1), "chesssprites/brown_circle.png")
        load_take_indicator = self.add_sprite((-1, -1), "chesssprites/red_circle.png")
        load_move_indicator.kill()
        load_take_indicator.kill()

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

    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes Piece; sprite, sprite_image, moved initialized to None, None, False automatically

        Parameters:
            color:  integer representing the piece's color
            x, y:   coordinates representing the piece's location
        '''
        self.color = color
        self.x = x
        self.y = y
        self.sprite = None
        self.sprite_image = None
        self.moved = False

    def add_sprite(self, scene: arcade.scene, sprite_image: str):
        '''
        Adds sprite to the arcade scene; does not return
        
        Parameters:
            scene:          the scene to render the sprite
            sprite_image:   url of the image to use e.g. Chesssprites/bP.png for black pawn
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
    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes Rook; uses Piece constructor
        '''
        Piece.__init__(self, color, x, y)
        self.value = ROOK_VALUE
    
    def __str__(self):
        '''
        Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black
        '''
        return "R" if self.color == WHITE else "r"

    # Adds all potential "moves" to self.legal_moves and all potential "takes"
    # to self.legal_takes. Moves and takes later evaluated to ensure they do
    # not move king into check by Chess.display_legal_moves
    def move(self, game_object: Chess):
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
    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes Knight; uses Piece constructor
        '''
        Piece.__init__(self, color, x, y)
        self.value = KNIGHT_VALUE

    def __str__(self):
        '''
        Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black
        '''
        return "N" if self.color == WHITE else "n"

    def move(self, game_object: Chess):
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
    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes Bishop; uses Piece constructor
        '''
        Piece.__init__(self, color, x, y)
        self.value = BISHOP_VALUE

    def __str__(self):
        '''
        Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black
        '''
        return "B" if self.color == WHITE else "b"

    def move(self, game_object: Chess):
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
    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes Pawn; uses Piece constructor
        '''
        Piece.__init__(self, color, x, y)
        self.value = PAWN_VALUE

    def __str__(self):
        '''
        Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black
        '''
        return "P" if self.color == WHITE else "p"

    def move(self, game_object: Chess):
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
    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes Queen; uses Piece constructor
        '''
        Piece.__init__(self, color, x, y)
        self.value = QUEEN_VALUE

    def __str__(self):
        '''
        Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black
        '''
        return "Q" if self.color == WHITE else "q"

    def move(self, game_object: Chess):
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
    def __init__(self, color: int, x: int, y: int):
        '''
        Initializes King; uses Piece constructor
        '''
        Piece.__init__(self, color, x, y)
        self.value = 0

    def __str__(self):
        '''
        Standard string representation of a chess piece for generating FEN
        strings - lowercase for white, uppercase for black
        '''
        return "K" if self.color == WHITE else "k"

    def move(self, game_object: Chess):
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

    def __init__(self, prev_x: int, prev_y: int, new_x: int, new_y: int, moved_piece: Piece, taken_piece: Piece, moved_piece_moved: bool,
                    taken_piece_moved: bool, taken_piece_sprite_img: str, promotion: bool = False):
        '''
        Initializes Move
        '''
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
        '''
        Returns tuple consisting of all class variables for easy unpacking
        '''
        return (self.prev_x, self.prev_y, self.new_x, self.new_y, self.moved_piece, self.taken_piece, self.moved_piece_moved,
                    self.taken_piece_moved, self.taken_piece_sprite_img, self.promotion)

def main():
    # run the game; run arcade to render everything
    Chess()
    arcade.run()

if __name__ == "__main__":
    main()
