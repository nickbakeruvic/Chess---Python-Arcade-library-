from ast import Return
import arcade

# constants
WHITE = 1
BLACK = -1

PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5

PAWN_VALUE = 1
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 8

PIXELS_PER_SQUARE = 100
PIXELS_FROM_BOTTOM_TO_BOARD = 150
PIXELS_FROM_SIDE_TO_BOARD = 150


class Move:

    def __init__(self, prev_x, prev_y, new_x, new_y, moved_piece, taken_piece, moved_piece_moved, taken_piece_moved, taken_piece_sprite_img, promotion = False):
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
    
    def __str__(self):
        return f"moved {self.moved_piece} from ({self.prev_x}, {self.prev_y}) to ({self.new_x}, {self.new_y}) taking {self.taken_piece}"

    def return_data(self):
        return (self.prev_x, self.prev_y, self.new_x, self.new_y, self.moved_piece, self.taken_piece, self.moved_piece_moved, self.taken_piece_moved, self.taken_piece_sprite_img, self.promotion)

class Piece:
    
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.sprite = None
        self.moved = False

    def add_sprite(self, scene, sprite_image):
        self.sprite = arcade.Sprite(sprite_image, 0.1)
        self.sprite.center_x = self.x * PIXELS_PER_SQUARE + PIXELS_FROM_SIDE_TO_BOARD
        self.sprite.center_y = self.y * PIXELS_PER_SQUARE + PIXELS_FROM_BOTTOM_TO_BOARD
        scene.add_sprite(f"Piece at {self.x}, {self.y}", self.sprite)
        self.sprite_image = sprite_image

class Rook(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)
    
    def __str__(self):
        return f"Rook at {self.x}, {self.y}"

    def move(self, game_object):

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x + i, self.y)

            if piece_1 is None: game_object.legal_moves.append((self.x + i, self.y))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x + i, self.y))
                break
            else:
                break

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x - i, self.y)

            if piece_1 is None: game_object.legal_moves.append((self.x - i, self.y))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x - i, self.y))
                break
            else:
                break

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x, self.y - i)

            if piece_1 is None: game_object.legal_moves.append((self.x, self.y - i))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x, self.y - i))
                break
            else:
                break

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x, self.y + i)

            if piece_1 is None: game_object.legal_moves.append((self.x, self.y + i))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x, self.y + i))
                break
            else:
                break

class Knight(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)

    def move(self, game_object):
        
        piece_1 = game_object.get_piece_at(self.x + 1, self.y + 2)
        piece_2 = game_object.get_piece_at(self.x + 1, self.y - 2)

        piece_3 = game_object.get_piece_at(self.x - 1, self.y + 2)
        piece_4 = game_object.get_piece_at(self.x - 1, self.y - 2)

        piece_5 = game_object.get_piece_at(self.x + 2, self.y + 1)
        piece_6 = game_object.get_piece_at(self.x + 2, self.y - 1)

        piece_7 = game_object.get_piece_at(self.x - 2, self.y + 1)
        piece_8 = game_object.get_piece_at(self.x - 2, self.y - 1)

        if piece_1 is None: game_object.legal_moves.append((self.x + 1, self.y + 2))
        if piece_2 is None: game_object.legal_moves.append((self.x + 1, self.y - 2))
        if piece_3 is None: game_object.legal_moves.append((self.x - 1, self.y + 2))
        if piece_4 is None: game_object.legal_moves.append((self.x - 1, self.y - 2))
        if piece_5 is None: game_object.legal_moves.append((self.x + 2, self.y + 1))
        if piece_6 is None: game_object.legal_moves.append((self.x + 2, self.y - 1))
        if piece_7 is None: game_object.legal_moves.append((self.x - 2, self.y + 1))
        if piece_8 is None: game_object.legal_moves.append((self.x - 2, self.y - 1))

        if piece_1 is not None and piece_1.color != self.color: game_object.legal_takes.append((self.x + 1, self.y + 2))
        if piece_2 is not None and piece_2.color != self.color: game_object.legal_takes.append((self.x + 1, self.y - 2))
        if piece_3 is not None and piece_3.color != self.color: game_object.legal_takes.append((self.x - 1, self.y + 2))
        if piece_4 is not None and piece_4.color != self.color: game_object.legal_takes.append((self.x - 1, self.y - 2))
        if piece_5 is not None and piece_5.color != self.color: game_object.legal_takes.append((self.x + 2, self.y + 1))
        if piece_6 is not None and piece_6.color != self.color: game_object.legal_takes.append((self.x + 2, self.y - 1))
        if piece_7 is not None and piece_7.color != self.color: game_object.legal_takes.append((self.x - 2, self.y + 1))
        if piece_8 is not None and piece_8.color != self.color: game_object.legal_takes.append((self.x - 2, self.y - 1))

class Bishop(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)

    def move(self, game_object):

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x + i, self.y + i)

            if piece_1 is None: game_object.legal_moves.append((self.x + i, self.y + i))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x + i, self.y + i))
                break
            else:
                break

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x - i, self.y + i)

            if piece_1 is None: game_object.legal_moves.append((self.x - i, self.y + i))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x - i, self.y + i))
                break
            else:
                break

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x + i, self.y - i)

            if piece_1 is None: game_object.legal_moves.append((self.x + i, self.y - i))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x + i, self.y - i))
                break
            else:
                break

        for i in range(1, 8):
            piece_1 = game_object.get_piece_at(self.x - i, self.y - i)

            if piece_1 is None: game_object.legal_moves.append((self.x - i, self.y - i))
            elif piece_1.color != self.color: 
                game_object.legal_takes.append((self.x - i, self.y - i))
                break
            else:
                break

class Pawn(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)

    def move(self, game_object):
        
        piece_1 = game_object.get_piece_at(self.x, self.y + 1 * self.color)
        piece_2 = game_object.get_piece_at(self.x, self.y + 2 * self.color)
        piece_3 = game_object.get_piece_at(self.x + 1, self.y + 1 * self.color)
        piece_4 = game_object.get_piece_at(self.x - 1, self.y + 1 * self.color)

        if piece_1 is None: game_object.legal_moves.append((self.x, self.y + 1 * self.color))
        if piece_1 is None and piece_2 is None and not self.moved: game_object.legal_moves.append((self.x, self.y + 2 * self.color))

        if piece_3 is not None and piece_3.color != self.color: game_object.legal_takes.append((self.x + 1, self.y + 1 * self.color))
        if piece_4 is not None and piece_4.color != self.color: game_object.legal_takes.append((self.x - 1, self.y + 1 * self.color))

class Queen(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)

    def move(self, game_object):

        temp_rook = Rook(self.color, self.x, self.y)
        temp_bishop = Bishop(self.color, self.x, self.y)

        temp_rook.move(game_object)
        temp_bishop.move(game_object)

class King(Piece):

    def __init__(self, color, x, y):
        Piece.__init__(self, color, x, y)

    def move(self, game_object):
        piece_1 = game_object.get_piece_at(self.x + 1, self.y + 1)
        piece_2 = game_object.get_piece_at(self.x , self.y + 1)
        piece_3 = game_object.get_piece_at(self.x - 1, self.y + 1)

        piece_4 = game_object.get_piece_at(self.x + 1, self.y)
        piece_5 = game_object.get_piece_at(self.x - 1, self.y)

        piece_6 = game_object.get_piece_at(self.x + 1, self.y - 1)
        piece_7 = game_object.get_piece_at(self.x , self.y - 1)
        piece_8 = game_object.get_piece_at(self.x - 1, self.y - 1)

        if piece_1 is None: game_object.legal_moves.append((self.x + 1, self.y + 1))
        elif piece_1.color != self.color: game_object.legal_takes.append((self.x + 1, self.y + 1))

        if piece_2 is None: game_object.legal_moves.append((self.x, self.y + 1))
        elif piece_2.color != self.color: game_object.legal_takes.append((self.x, self.y + 1))

        if piece_3 is None: game_object.legal_moves.append((self.x - 1,self. y + 1))
        elif piece_3.color != self.color: game_object.legal_takes.append((self.x - 1, self.y + 1))

        if piece_4 is None: game_object.legal_moves.append((self.x + 1, self.y))
        elif piece_4.color != self.color: game_object.legal_takes.append((self.x + 1, self.y))

        if piece_5 is None: game_object.legal_moves.append((self.x - 1, self.y))
        elif piece_5.color != self.color: game_object.legal_takes.append((self.x - 1, self.y))

        if piece_6 is None: game_object.legal_moves.append((self.x + 1,self. y - 1))
        elif piece_6.color != self.color: game_object.legal_takes.append((self.x + 1, self.y - 1))

        if piece_7 is None: game_object.legal_moves.append((self.x, self.y - 1))
        elif piece_7.color != self.color: game_object.legal_takes.append((self.x, self.y - 1))

        if piece_8 is None: game_object.legal_moves.append((self.x - 1, self.y -1))
        elif piece_8.color != self.color: game_object.legal_takes.append((self.x - 1, self.y - 1))

class Chess(arcade.Window):
    def __init__(self):
        super().__init__(1000, 1000, title="Nick Baker's Chess")

        self.color_to_move = WHITE
        self.king_in_check = False
        self.selected_piece, self.white_king, self.black_king, self.white_king_rook, self.white_queen_rook, self.black_king_rook, self.black_queen_rook = None, None, None, None, None, None, None
        self.move_list, self.legal_moves, self.legal_takes = [], [], []

        self.scene = arcade.Scene()
        self.pieces = self.initialize_pieces()

        arcade.start_render()
        self.load_indicators()
        self.on_draw()

    def on_draw(self):
        arcade.start_render()
        self.init_board()
        self.display_value()
        self.display_turn()
        temp_sprite_list = []

        temp_sprite = self.add_sprite((8, 0), "chesssprites/undo.png")
        temp_sprite_list.append(temp_sprite)

        for entry in self.legal_moves:
            temp_sprite = self.add_sprite(entry, "chesssprites/brown_circle.png")
            temp_sprite_list.append(temp_sprite)

        for entry in self.legal_takes:
            temp_sprite = self.add_sprite(entry, "chesssprites/red_circle.png", 0.045)
            temp_sprite_list.append(temp_sprite)

        self.scene.draw()

        for sprite in temp_sprite_list:
            if sprite is not None: sprite.kill()

    def display_value(self):

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

        if value < 0:
            arcade.draw_text(f"White: {value}", 800, 60, arcade.color.WHITE, 24, width=100, align="left")
            arcade.draw_text(f"Black: +{-value}", 800, 910, arcade.color.WHITE, 24, width=100, align="left")
        elif value > 0:
            arcade.draw_text(f"White: +{value}", 800, 60, arcade.color.WHITE, 24, width=100, align="left")
            arcade.draw_text(f"Black: -{value}", 800, 910, arcade.color.WHITE, 24, width=100, align="left")
    
    def display_turn(self):
        
        turn = "White" if self.color_to_move == WHITE else "Black"
        arcade.draw_text(f"{turn} to move", 0, 910, arcade.color.WHITE, 24, width=1000, align="center")

    def add_sprite(self, coords, image_path, sizing = 0.1):

        sprite = arcade.Sprite(image_path, sizing)
        sprite.center_x = coords[0] * 100 + 150
        sprite.center_y = coords[1] * 100 + 150
        self.scene.add_sprite('legal move indicator', sprite)
        return sprite

    def on_mouse_press(self, x, y, button, modifiers):
        
        if x > 900 and y < 200 and y > 100:
            self.undo_move(1)
            self.king_in_check = self.in_check()
            return
        
        normalized_x = x//100 * 100 + 50
        normalized_y =  y//100 * 100 + 50
        x_coord = x//100 - 1
        y_coord = y//100 - 1

        if x_coord < 0 or x_coord > 7 or y_coord < 0 or y_coord > 7: return

        cur_piece = self.get_piece_at(x_coord, y_coord)

        if self.selected_piece is not None and isinstance(self.selected_piece, King) and cur_piece is not None and isinstance(cur_piece, Rook):
            # attempt castle
            if self.try_castle(cur_piece): return

        if self.selected_piece is not None and self.selected_piece.color == self.color_to_move and cur_piece is None and (x_coord, y_coord) in self.legal_moves:
            # move piece
            
            self.move_piece(x_coord, y_coord, normalized_x, normalized_y)

        elif self.selected_piece is not None and self.selected_piece.color == self.color_to_move and cur_piece is not None and self.selected_piece.color != cur_piece.color and (x_coord, y_coord) in self.legal_takes:
            # take piece
            
            prev_x, prev_y = self.selected_piece.x, self.selected_piece.y

            self.selected_piece.x = x_coord
            self.selected_piece.y = y_coord
            self.selected_piece.sprite.center_x = normalized_x
            self.selected_piece.sprite.center_y = normalized_y
            self.selected_piece.moved = True

            # promote pawns
            if (y_coord == 0 or y_coord == 7) and isinstance(self.selected_piece, Pawn):

                self.promote_selected_pawn()

                current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, cur_piece, True, cur_piece.moved, cur_piece.sprite_image, True)
                self.move_list.append(current_move)
            else:
                current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, cur_piece, self.selected_piece.moved, cur_piece.moved, cur_piece.sprite_image)
                self.move_list.append(current_move)
                

            self.selected_piece = None
            cur_piece.sprite.kill()
            self.pieces.remove(cur_piece)

            if self.in_check():
                self.undo_move()

            self.legal_moves = []
            self.legal_takes = []

            self.color_to_move *= -1

        elif cur_piece is not None and cur_piece.color == self.color_to_move:
            # select piece; show legal moves for it

            self.selected_piece = cur_piece

            self.legal_moves = []
            self.legal_takes = []
        
            self.display_legal_moves(self.selected_piece)
        
        else:
            self.selected_piece = None
            self.legal_moves = []
            self.legal_takes = []

        self.king_in_check = self.in_check()



    def promote_selected_pawn(self):
        self.selected_piece.__class__ = Queen
        self.selected_piece.sprite.kill()
        sprite_image = "chesssprites/wQ.png" if self.selected_piece.color == WHITE else "chesssprites/bQ.png"
        self.selected_piece.add_sprite(self.scene, sprite_image)

    def move_piece(self, x_coord, y_coord, normalized_x, normalized_y):

        prev_x, prev_y = self.selected_piece.x, self.selected_piece.y
        self.selected_piece.x = x_coord
        self.selected_piece.y = y_coord
        self.selected_piece.sprite.center_x = normalized_x
        self.selected_piece.sprite.center_y = normalized_y
        self.selected_piece.moved = True
        
        # promote pawns
        if isinstance(self.selected_piece, Pawn) and (y_coord == 0 or y_coord == 7):

            self.promote_selected_pawn()

            current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, None, self.selected_piece.moved, None, None, True)
            self.move_list.append(current_move)
        else:
            current_move = Move(prev_x, prev_y, x_coord, y_coord, self.selected_piece, None, self.selected_piece.moved, None, None)
            self.move_list.append(current_move)
            

        self.selected_piece = None
        
        if self.in_check():
            self.undo_move()

        self.legal_moves = []
        self.legal_takes = []
        
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

        king.sprite.center_x = king.x * 100 + 150
        king.sprite.center_y = king.y * 100 + 150

        rook.sprite.center_x = rook.x * 100 + 150
        rook.sprite.center_y = rook.y * 100 + 150

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
            self.display_legal_moves(piece)

            if (x, y) in self.legal_takes or (x,y) in self.legal_moves:
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
            # castled
            print("Castled")

            taken_piece.x = new_x
            taken_piece.y = new_y
            taken_piece.sprite.center_x = new_x * 100 + 150
            taken_piece.sprite.center_y = new_y * 100 + 150

            moved_piece.x = prev_x
            moved_piece.y = prev_y
            moved_piece.sprite.center_x = prev_x * 100 + 150
            moved_piece.sprite.center_y = prev_y * 100 + 150

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
            moved_piece.sprite.center_x = prev_x * 100 + 150
            moved_piece.sprite.center_y = prev_y * 100 + 150
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
        for entry in self.legal_moves:
            (x,y) = entry
            if x < 0 or x > 7 or y < 0 or y > 7: 
                to_remove.append(entry)
        
        for entry in to_remove:
            self.legal_moves.remove(entry)

    
    def get_piece_at(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece

        return None

    def initialize_pieces(self):

        piece_list = []
        for x in range(8):

            pawn_white = Pawn(WHITE, x, 1)
            pawn_black = Pawn(BLACK, x, 6)
            pawn_white.add_sprite(self.scene, "chesssprites/wP.png")
            pawn_black.add_sprite(self.scene, "chesssprites/bP.png")

            if x == 0 or x == 7:
                rook_white = Rook(WHITE, x, 0)
                rook_black = Rook(BLACK, x, 7)
                rook_white.add_sprite(self.scene, "chesssprites/wR.png")
                rook_black.add_sprite(self.scene, "chesssprites/bR.png")
                piece_list.append(rook_white)
                piece_list.append(rook_black)

            elif x == 1 or x == 6:
                knight_white = Knight(WHITE,  x, 0)
                knight_black = Knight(BLACK, x, 7)
                knight_white.add_sprite(self.scene, "chesssprites/wN.png")
                knight_black.add_sprite(self.scene, "chesssprites/bN.png")
                piece_list.append(knight_white)
                piece_list.append(knight_black)
                

            elif x == 2 or x == 5:
                bishop_white = Bishop(WHITE, x, 0)
                bishop_black = Bishop(BLACK, x, 7)
                bishop_white.add_sprite(self.scene, "chesssprites/wB.png")
                bishop_black.add_sprite(self.scene, "chesssprites/bB.png")
                piece_list.append(bishop_white)
                piece_list.append(bishop_black)

            elif x == 3:
                queen_white = Queen(WHITE, x, 0)
                queen_black = Queen(BLACK, x, 7)
                queen_white.add_sprite(self.scene, "chesssprites/wQ.png")
                queen_black.add_sprite(self.scene, "chesssprites/bQ.png")
                piece_list.append(queen_white)
                piece_list.append(queen_black)
            
            elif x == 4:
                king_white = King(WHITE, x, 0)
                king_black = King(BLACK, x, 7)
                king_white.add_sprite(self.scene, "chesssprites/wK.png")
                king_black.add_sprite(self.scene, "chesssprites/bK.png")
                piece_list.append(king_white)
                piece_list.append(king_black)
                self.white_king = king_white
                self.black_king = king_black
            
            piece_list.append(pawn_white)
            piece_list.append(pawn_black)

        return piece_list

    def init_board(self):
        
        x = 100
        y = 200
        count = 0

        arcade.draw_lrtb_rectangle_filled(0, 1000, 1000, 0, arcade.color.BISTRE)

        while x < 900:
            while y < 1000:
                if count % 2 == 0:
                    arcade.draw_lrtb_rectangle_filled(x, x + PIXELS_PER_SQUARE, y, y - PIXELS_PER_SQUARE, arcade.color.CAMEL)
                else:
                    arcade.draw_lrtb_rectangle_filled(x, x + PIXELS_PER_SQUARE, y, y - PIXELS_PER_SQUARE, arcade.color.CHAMPAGNE)
                count += 1
                y += 100
            count += 1
            x += 100
            y = 200


        if self.selected_piece is not None:
                temp_x = (self.selected_piece.x + 1) * PIXELS_PER_SQUARE
                temp_y = (self.selected_piece.y + 1) * PIXELS_PER_SQUARE
                arcade.draw_lrtb_rectangle_filled(temp_x, temp_x + PIXELS_PER_SQUARE, temp_y + PIXELS_PER_SQUARE, temp_y, arcade.color.LIGHT_SALMON)

        if self.king_in_check:
            
            king = self.white_king if self.color_to_move == WHITE else self.black_king

            temp_x = (king.x + 1) * PIXELS_PER_SQUARE
            temp_y = (king.y + 1) * PIXELS_PER_SQUARE
            arcade.draw_lrtb_rectangle_filled(temp_x, temp_x + PIXELS_PER_SQUARE, temp_y + PIXELS_PER_SQUARE, temp_y, arcade.color.CAMEO_PINK)

        arcade.draw_text("A", 175, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("B", 275, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("C", 375, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("D", 475, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("E", 575, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("F", 675, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("G", 775, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("H", 875, 105, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")

        arcade.draw_text("1", 105, 175, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("2", 105, 275, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("3", 105, 375, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("4", 105, 475, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("5", 105, 575, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("6", 105, 675, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("7", 105, 775, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")
        arcade.draw_text("8", 105, 875, arcade.color.BLACK, 16, width=PIXELS_PER_SQUARE, align="left")

    # when loading into game, load these sprites into memory before they are needed
    # to eliminate lag when displaying them for the first time
    def load_indicators(self):
        load_move_indicator = self.add_sprite((-1, -1), "chesssprites/brown_circle.png")
        load_take_indicator = self.add_sprite((-1, -1), "chesssprites/red_circle.png")
        load_move_indicator.kill()
        load_take_indicator.kill()

Chess()
arcade.run()
