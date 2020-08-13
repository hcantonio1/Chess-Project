import pyglet
import resources
#import abc

DEFAULT_PIECE_SCALE = 0.8

class Piece():
    def __init__(self, file, rank, player):
        self.player = player
        self.type = type
        self.file = file
        self.rank = rank
        self.letter = "P"

    def __str__(self):
        return self.letter + chr(self.file+97) + str(self.rank+1)

    def get_sprite(self):
        image = resources.all_pieces[self.player][self.letter]
        resources.center_image(image)
        sprite = pyglet.sprite.Sprite(image)
        sprite.scale *= DEFAULT_PIECE_SCALE

        sprite.x = 63 + (self.file + 0.5)*(59.25)       # we don't want magic numbers
        sprite.y = 62 + (self.rank + 0.5)*(60)          # we don't want magic numbers

        return sprite

    #@abc.abstractmethod
    def move(self, square):
        # if self.guards(square):
        # file = x rank = y
        pass

    #@abc.abstractmethod
    def guards(self, square):
        return False


class King(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "K"
        self.sprite = self.get_sprite()

class Queen(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "Q"
        self.sprite = self.get_sprite()

class Bishop(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "B"
        self.sprite = self.get_sprite()

class Knight(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "N"
        self.sprite = self.get_sprite()

class Rook(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "R"
        self.sprite = self.get_sprite()

class Pawn(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "P"
        self.sprite = self.get_sprite()


def get_pieces(position_str):
    pieces = []
    rows = position_str.split('/')
    i = 0
    while (i < 8):
        j = 0
        while (j < 8):
            char = rows[i][j]
            is_int = True
            try:
                int(char)
            except ValueError:
                is_int = False
            if not is_int:
                pieces.append(create_piece(char, j, 7-i))
                j += 1
            else:
                j += int(char)
        i += 1
    return pieces


def create_piece(letter, file, rank):
    piece = letter.upper()
    player = 0 if piece == letter else 1
    if piece == "K":
        return King(file, rank, player)
    if piece == "Q":
        return Queen(file, rank, player)
    if piece == "B":
        return Bishop(file, rank, player)
    if piece == "N":
        return Knight(file, rank, player)
    if piece == "R":
        return Rook(file, rank, player)
    if piece == "P":
        return Pawn(file, rank, player)



def file_rank_of(square):
    return (ord(square[0])-97, int(square[1]))

if __name__ == '__main__':
    k = King(7, 0)
    print(k)
