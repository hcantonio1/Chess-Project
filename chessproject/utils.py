import pyglet
import resources
#import abc


class Piece():
    def __init__(self, file, rank, player):
        self.player = player
        self.type = type
        self.file = file
        self.rank = rank
        self.letter = "P"

    def __str__(self):
        return self.letter + chr(self.file+97) + str(self.rank+1)

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
        self.sprite = pyglet.sprite.Sprite(resources.all_pieces[player][self.letter])

class Queen(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "Q"
        self.sprite = pyglet.sprite.Sprite(resources.all_pieces[player][self.letter])

class Bishop(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "B"
        self.sprite = pyglet.sprite.Sprite(resources.all_pieces[player][self.letter])

class Knight(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "N"
        self.sprite = pyglet.sprite.Sprite(resources.all_pieces[player][self.letter])

class Rook(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "R"
        self.sprite = pyglet.sprite.Sprite(resources.all_pieces[player][self.letter])

class Pawn(Piece):
    def __init__(self, file, rank, player):
        super().__init__(file, rank, player)
        self.letter = "P"
        self.sprite = pyglet.sprite.Sprite(resources.all_pieces[player][self.letter])


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
                j = 8
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
