import pyglet
import resources
import board_and_pieces as bp


class ChessGame:
    initial_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    def __init__(self, position_str, current_turn, castling_posibilities, en_passant_coordinates):
        self.board = bp.Board()
        self.pieces = self.get_pieces(position_str)
        self.current_turn = current_turn
        self.castling_posibilities = castling_posibilities
        self.en_passant_coordinates = en_passant_coordinates

        self.batch = pyglet.graphics.Batch()
        for piece in self.pieces:
            piece.sprite.batch = self.batch

        self.a_piece_is_selected = False
        self.selected_piece = None

    def __str__(self):
        return [str(piece) for piece in self.pieces]

    def get_pieces(self, position_str):
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
                    pieces.append(self.create_piece(char, j, 7-i))
                    j += 1
                else:
                    j += int(char)
            i += 1
        return pieces


    def create_piece(self, letter, file, rank):
        piece = letter.upper()
        player = 0 if piece == letter else 1
        if piece == "K":
            return bp.King(file, rank, player, self)
        if piece == "Q":
            return bp.Queen(file, rank, player, self)
        if piece == "B":
            return bp.Bishop(file, rank, player, self)
        if piece == "N":
            return bp.Knight(file, rank, player, self)
        if piece == "R":
            return bp.Rook(file, rank, player, self)
        if piece == "P":
            return bp.Pawn(file, rank, player, self)

    def on_draw(self):
        self.board.draw()
        self.batch.draw()

    def on_click(self, x, y):
        print(self.board.square_of_xy(x, y))
        if self.a_piece_is_selected:
            self.selected_piece.on_click(x, y)
            self.a_piece_is_selected = False
            self.selected_piece = None
        else:
            for piece in self.pieces:
                if piece.is_on(x, y):
                    self.selected_piece = piece
                    self.a_piece_is_selected = True
                    print(str(piece) + " is selected")
                    piece.on_click(x, y)
                    break

