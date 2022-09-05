# Modules
from . import window, animation

"""Sprite é uma animação que pode ser movida por input, é o "ator" do jogo"""

# Tive nem coragem de mudar ou tirar isso daqui...


class Sprite(animation.Animation):
    """
    Caso seja dado apenas o nome da imagem, será criada uma Animation
    com 1 frame apenas.
    """

    def __init__(self, image_file, frames=1):
        # Parent's constructor must be first-called
        animation.Animation.__init__(self, image_file, frames)

    """Permite a movimentação com o teclado no eixo X"""

    def move_key_x(self, speed):
        if window.Window.get_keyboard().key_pressed("left"):
            self.x -= speed

        if window.Window.get_keyboard().key_pressed("right"):
            self.x += speed

    """Permite a movimentação com o telado no eixo Y"""

    def move_key_y(self, speed):
        if window.Window.get_keyboard().key_pressed("up"):
            self.y -= speed

        if window.Window.get_keyboard().key_pressed("down"):
            self.y += speed

    """Move o Sprite no eixo X (sem input)"""

    def move_x(self, speed):
        self.x += speed

    """Move o Sprite no eixo Y (sem input)"""

    def move_y(self, speed):
        self.y += speed
