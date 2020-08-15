import pyglet
import resources
import abc

DEFAULT_PIECE_SCALE = 0.8
DEFAULT_BOARD_SCALE = 1
BOARD_LEFTMOST = 63*DEFAULT_BOARD_SCALE
BOARD_BOTTOMOST = 62*DEFAULT_BOARD_SCALE
BOARD_SQUARE_WIDTH = 59.25*DEFAULT_BOARD_SCALE
BOARD_SQUARE_HEIGHT = 60*DEFAULT_BOARD_SCALE


class Board:
    def __init__(self):
        self.sprite = resources.board_sprite
        self.leftmost_x = BOARD_LEFTMOST
        self.bottomost_y = BOARD_BOTTOMOST
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
        rank = round((ty-self.bottomost_y)/self.square_height - 0.5)
        return (file, rank)

    def square_of_xy(self, tx, ty):
        f, r = self.file_rank_of_xy(tx, ty)
        return self.square_of_fr(f, r)




class Piece():
    def __init__(self, file, rank, player, chessgame):
        self.chessgame = chessgame
        self.player = player
        self.type = type
        self.file = file
        self.rank = rank
        self.letter = "P"

        self.is_selected = False

    def __str__(self):
        return self.letter + chr(self.file+97) + str(self.rank+1)

    def get_sprite(self):
        image = resources.all_pieces[self.player][self.letter]
        resources.center_image(image)
        sprite = pyglet.sprite.Sprite(image)
        sprite.scale *= DEFAULT_PIECE_SCALE
        sprite.x = self.chessgame.board.leftmost_x + (self.file + 0.5)*self.chessgame.board.square_width
        sprite.y = self.chessgame.board.bottomost_y + (self.rank + 0.5)*self.chessgame.board.square_height
        return sprite

    def update_sprite_position(self):
        self.sprite.x = self.chessgame.board.leftmost_x + (self.file + 0.5)*self.chessgame.board.square_width
        self.sprite.y = self.chessgame.board.bottomost_y + (self.rank + 0.5)*self.chessgame.board.square_height

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
        if self.guards(square):
            file, rank = self.chessgame.board.file_rank_of_sq(square)
            self.file = file
            self.rank = rank
            self.update_sprite_position()


    def guards(self, square):
        return False


class King(Piece):
    def __init__(self, file, rank, player, chessgame):
        super().__init__(file, rank, player, chessgame)
        self.letter = "K"
        self.sprite = self.get_sprite()
        print(self.sprite.width)

    def guards(self, square):
        file, rank = self.chessgame.board.file_rank_of_sq(square)
        print(file, rank)
        print(abs(file-self.file), abs(rank-self.rank))
        return (abs(self.rank - rank) == 1 or abs(self.file - file) == 1) and abs(self.rank - rank) < 2 and abs(self.file - file) < 2



class Queen(Piece):
    def __init__(self, file, rank, player, chessgame):
        super().__init__(file, rank, player, chessgame)
        self.letter = "Q"
        self.sprite = self.get_sprite()

    def guards(self, square):
        return Rook.guards(square) or Bishop.guards(square)

class Bishop(Piece):
    def __init__(self, file, rank, player, chessgame):
        super().__init__(file, rank, player, chessgame)
        self.letter = "B"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.chessgame.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        if abs(df) == abs(dr):
            return True
        return False

class Knight(Piece):
    def __init__(self, file, rank, player, chessgame):
        super().__init__(file, rank, player, chessgame)
        self.letter = "N"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.chessgame.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        if abs(df) == 2:
            return abs(dr) == 1
        if abs(dr) == 2:
            return abs(df) == 1
        return False

class Rook(Piece):
    def __init__(self, file, rank, player, chessgame):
        super().__init__(file, rank, player, chessgame)
        self.letter = "R"
        self.sprite = self.get_sprite()

    def guards(self, square):
        file, rank = self.chessgame.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        if dr == 0:
            return df != 0
        if df == 0:
            return dr != 0
        return False

class Pawn(Piece):
    def __init__(self, file, rank, player, chessgame):
        super().__init__(file, rank, player, chessgame)
        self.letter = "P"
        self.sprite = self.get_sprite()


    def can_reach(square):
        file, rank = self.chessgame.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        if abs(dr) == 2:
            pass
        if abs(dr) == 1:
            pass
        if abs(df) == 1:
            pass
        return False

    def guards(self, square):
        file, rank = self.chessgame.board.file_rank_of_sq(square)
        df = file - self.file
        dr = rank -self.rank

        if abs(df) == 1 and abs(dr) == 1:
            if self.player == 0:
                return dr > 0
            if self.player == 1:
                return dr < 0
        return False

