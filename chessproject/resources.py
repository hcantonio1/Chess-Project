import pyglet

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2


board_sprite = pyglet.resource.image('res/board.png')
board_sprite = pyglet.sprite.Sprite(board_sprite)


wking = pyglet.resource.image('res/wking.png')
wqueen = pyglet.resource.image('res/wqueen.png')
wbishop = pyglet.resource.image('res/wbishop.png')
wknight = pyglet.resource.image('res/wknight.png')
wrook = pyglet.resource.image('res/wrook.png')
wpawn = pyglet.resource.image('res/wpawn.png')

bking = pyglet.resource.image('res/bking.png')
bqueen = pyglet.resource.image('res/bqueen.png')
bbishop = pyglet.resource.image('res/bbishop.png')
bknight = pyglet.resource.image('res/bknight.png')
brook = pyglet.resource.image('res/brook.png')
bpawn = pyglet.resource.image('res/bpawn.png')

all_pieces = [{
    "K": wking,
    "Q": wqueen,
    "B": wbishop,
    "N": wknight,
    "R": wrook,
    "P": wpawn
},
{
    "K": bking,
    "Q": bqueen,
    "B": bbishop,
    "N": bknight,
    "R": brook,
    "P": bpawn
}]
