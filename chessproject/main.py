import pyglet
from chessgame import ChessGame

class AppWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = ChessGame("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", 0, "KQkq", [])

        #more stuff
        pyglet.clock.schedule_interval(self.update, 1.0 / 120.0)

    def update(self, dt):
        #self.menu.update_batch()
        #self.game.update(dt)
        pass

    def on_draw(self):
        app_window.clear()
        self.game.on_draw()
        #some_x = -425 if app_window.state in [app_window.states['PLAYING'], app_window.states['GAME_OVER']] else 0
        #resources.background_image.blit(some_x, 0)

    def on_mouse_motion(self, x, y, button, modifiers):
        #self.menu.on_hover(x, y, button, modifiers)
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        #self.menu.on_click(x, y, button, modifiers)
        #self.game.on_click(x, y, button, modifiers)
        pass

app_window = AppWindow(600, 600, "Chess")
pyglet.app.run()
