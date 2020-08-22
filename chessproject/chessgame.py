import pyglet
import resources
import board_and_pieces as bp


class ChessGame:
    initial_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    def __init__(self, position_str, current_turn, castling_posibilities, en_passant_squares):
        self.board = bp.Board()
        self.pieces = self.get_pieces(position_str)
        self.current_turn = current_turn
        self.castling_posibilities = castling_posibilities
        self.en_passant_squares = en_passant_squares

        self.batch = pyglet.graphics.Batch()
        for piece in self.pieces:
            piece.sprite.batch = self.batch


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
                    sq = self.board.square_of_fr(j, 7-i)
                    pieces.append(self.create_piece(char, sq))
                    j += 1
                else:
                    j += int(char)
            i += 1
        return pieces

    def is_out_of_bounds_fr(self, file, rank):
        if file > 7 or rank > 7 or file < 0 or rank < 0:
            return True


    def create_piece(self, letter, square):
        piece = letter.upper()
        player = 0 if piece == letter else 1
        if piece == "K":
            return bp.King(square, player, self)
        if piece == "Q":
            return bp.Queen(square, player, self)
        if piece == "B":
            return bp.Bishop(square, player, self)
        if piece == "N":
            return bp.Knight(square, player, self)
        if piece == "R":
            return bp.Rook(square, player, self)
        if piece == "P":
            return bp.Pawn(square, player, self)

    def on_draw(self):
        self.board.draw()
        self.batch.draw()

    def on_click(self, x, y):
        file, rank = self.board.file_rank_of_xy(x, y)
        if self.is_out_of_bounds_fr(file, rank):
            pass
        elif self.selected_piece is not None:
            self.selected_piece.on_click(x, y)
            self.selected_piece = None
        else:
            sq = self.board.square_of_xy(x, y)
            piece = self.piece_at_square(sq)
            if not piece.is_my_turn():
                return False
            print(str(piece) + " is selected")
            self.selected_piece = piece
            piece.on_click(x, y)


    def piece_at_square(self, square):
        # can be O(1) with 64 square objects
        for piece in self.pieces:
            if square == piece.square:
                return piece
        return None
        
    def finish_turn(self):
        self.current_turn += 1

    def remove_piece_at_sq(self, square):
        self.pieces.remove(self.piece_at_square(square))

    def remove_piece(self, piece):
        self.pieces.remove(piece)
