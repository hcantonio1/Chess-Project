import pyglet
import resources
import utils

'''
ChessGame

has
    board_sprite
        is a pyglet.sprite.Sprite
    pieces
    Player(s)
    current_turn
    castling_posibilities
    en_passant_coordinates
    perspective (optional)
        either "black" or "white"; or try 0 and 1
    turns_since_last_catch (optional)
    move_number (optional)
    moves_list (optional, future, it's a stack)

events
    on_click
'''

class ChessGame:
    initial_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    def __init__(self, position_str, current_turn, castling_posibilities, en_passant_coordinates):
        self.board = resources.board_sprite
        self.pieces = utils.get_pieces(position_str)
        self.current_turn = current_turn
        self.castling_posibilities = castling_posibilities
        self.en_passant_coordinates = en_passant_coordinates

        self.batch = pyglet.graphics.Batch()
        for piece in self.pieces:
            piece.sprite.batch = self.batch

    def __str__(self):
        return [str(piece) for piece in self.pieces]

    def on_draw(self):
        self.board.draw()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass
