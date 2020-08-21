import pyglet
from math import copysign
import resources
import abc

DEFAULT_PIECE_SCALE = 0.8
DEFAULT_BOARD_SCALE = 1
BOARD_LEFTMOST = 63*DEFAULT_BOARD_SCALE
BOARD_BOTTOMMOST = 62*DEFAULT_BOARD_SCALE
BOARD_SQUARE_WIDTH = 59.25*DEFAULT_BOARD_SCALE
BOARD_SQUARE_HEIGHT = 60*DEFAULT_BOARD_SCALE


class Board:
    def __init__(self):
        self.sprite = resources.board_sprite
        self.leftmost_x = BOARD_LEFTMOST
        self.bottommost_y = BOARD_BOTTOMMOST
        self.square_width = BOARD_SQUARE_WIDTH
        self.square_height = BOARD_SQUARE_HEIGHT

    def draw(self):
        self.sprite.draw()

    def file_rank_of_sq(self, square):
        return (ord(square[0])-97, int(square[1])-1)

    def square_of_fr(self, file, rank):
        return chr(file+97) + str(rank+1)

    def file_rank_of_xy(self, tx, ty):
        file = round((tx-self.leftmost_x)/self.square_width - 0.5)
        rank = round((ty-self.bottommost_y)/self.square_height - 0.5)
        return (file, rank)

    def square_of_xy(self, tx, ty):
        f, r = self.file_rank_of_xy(tx, ty)
        return self.square_of_fr(f, r)




class Piece():
    def __init__(self, square, player, chessgame):
        self.chessgame = chessgame
        self.board = chessgame.board
        self.player = player
        self.type = type
        self.letter = "P"

        file, rank = self.board.file_rank_of_sq(square)
        self.square = square
        self.file = file
        self.rank = rank


        self.is_selected = False

    def __str__(self):
        return self.letter + chr(self.file+97) + str(self.rank+1)

    def get_sprite(self):
        image = resources.all_pieces[self.player][self.letter]
        resources.center_image(image)
        sprite = pyglet.sprite.Sprite(image)
        sprite.scale *= DEFAULT_PIECE_SCALE
        sprite.x = self.board.leftmost_x + (self.file + 0.5)*self.board.square_width
        sprite.y = self.board.bottommost_y + (self.rank + 0.5)*self.board.square_height
        return sprite

    def update_sprite_position(self):
        self.sprite.x = self.board.leftmost_x + (self.file + 0.5)*self.board.square_width
        self.sprite.y = self.board.bottommost_y + (self.rank + 0.5)*self.board.square_height

    def square_has_enemy(self, square):
        piece = self.chessgame.piece_at_square(square)
        if piece is None: return False
        return piece.player != self.player

    def square_has_friendly(self, square):
        piece = self.chessgame.piece_at_square(square)
        if piece is None: return False
        return piece.player == self.player

    def is_on(self, tx, ty):
        return abs(self.sprite.x - tx) < self.sprite.width//2 and abs(self.sprite.y - ty) < self.sprite.height//2

    def on_click(self, tx, ty):
        if self.is_on(tx, ty):
            if not self.is_selected:
                self.is_selected = True
            else:
                self.is_selected = False
        else:
            if self.is_selected:
                self.move(self.chessgame.board.square_of_xy(tx, ty))
                self.is_selected = False

    def move(self, square):
        if self.is_legal_move(square):
            file, rank = self.chessgame.board.file_rank_of_sq(square)
            self.file = file
            self.rank = rank
            self.square = square
            self.update_sprite_position()

    def guards(self, square):
        return False

    def is_legal_move(self, square):
        return self.guards(square) and not self.square_has_friendly(square)


class King(Piece):
    def __init__(self, square, player, chessgame):
        super().__init__(square, player, chessgame)
        self.letter = "K"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank - self.rank

        return (abs(dr) == 1 or abs(df) == 1) and abs(dr) < 2 and abs(df) < 2



class Queen(Piece):
    def __init__(self, square, player, chessgame):
        super().__init__(square, player, chessgame)
        self.letter = "Q"
        self.sprite = self.get_sprite()

    def guards(self, square):
        return Rook.guards(self, square) or Bishop.guards(self, square)

class Bishop(Piece):
    def __init__(self, square, player, chessgame):
        super().__init__(square, player, chessgame)
        self.letter = "B"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        is_basic_attack = abs(df) == abs(dr)
        is_blocked = False
        if not is_basic_attack: return False

        stepf = int(copysign(1, df))
        stepr = int(copysign(1, dr))
        f = self.file
        r = self.rank

        for i in range(max(abs(df), abs(dr))):
            if i == 0: continue
            sq = self.board.square_of_fr(f + stepf*i, r + stepr*i)
            if self.chessgame.piece_at_square(sq) is not None:
                is_blocked = True
                break

        return is_basic_attack and not is_blocked

class Knight(Piece):
    def __init__(self, square, player, chessgame):
        super().__init__(square, player, chessgame)
        self.letter = "N"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        return (abs(df) == 2 and abs(dr) == 1) or (abs(dr) == 2 and abs(df) == 1)

class Rook(Piece):
    def __init__(self, square, player, chessgame):
        super().__init__(square, player, chessgame)
        self.letter = "R"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        is_basic_attack = (df == 0 and dr != 0) or (dr == 0 and df != 0)
        is_blocked = False
        if not is_basic_attack: return False

        stepf = int(copysign(1, df)) if df else 0
        stepr = int(copysign(1, dr)) if dr else 0
        f = self.file
        r = self.rank

        for i in range(max(abs(df), abs(dr))):
            if i == 0: continue
            sq = self.board.square_of_fr(f + stepf*i, r + stepr*i)
            if self.chessgame.piece_at_square(sq) is not None:
                is_blocked = True
                break

        return is_basic_attack and not is_blocked

class Pawn(Piece):
    def __init__(self, square, player, chessgame):
        super().__init__(square, player, chessgame)
        self.letter = "P"
        self.sprite = self.get_sprite()


    def can_advance(self, square):
        file, rank = self.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank
        is_white = self.player == 0
        is_black = self.player == 1
        stepr = int(copysign(1, dr))

        if df != 0: return False
        on_file = df == 0
        is_forward = (dr > 0 and is_white) or (dr < 0 and self.player == is_black)
        is_initial = abs(dr) == 2 and ((is_white and self.rank == 1) or (is_black and self.rank == 6))
        is_initial_not_blocked = is_initial and self.chessgame.piece_at_square(self.board.square_of_fr(self.file, self.rank + stepr)) is None
        is_empty = self.chessgame.piece_at_square(square) is None
        return on_file and is_forward and is_empty and (is_initial_not_blocked or abs(dr) == 1)

    def guards(self, square):
        file, rank = self.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        is_diag = abs(df) == 1 and abs(dr) == 1
        return is_diag and ((self.player == 0 and dr > 0) or (self.player == 1 and dr < 0))

    def is_legal_move(self, square):
        is_capturing = self.guards(square) and self.square_has_enemy(square)
        is_advancing = self.can_advance(square)
        return is_capturing or is_advancing
