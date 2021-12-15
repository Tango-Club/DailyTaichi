from MovedStar.Entitys import BaseEntity, Player
from MovedStar.Utils2D import Point2D, Vector2D
import taichi as ti
import math


def main():
    ti.init(arch=ti.gpu)

    eps = 0.00001
    board_size = 1000

    self_size = 100

    player = Player(self_size, board_size / 2, board_size / 2)

    pixels = ti.field(dtype=float, shape=(board_size, board_size))

    gui = ti.GUI("Moved Star", res=(board_size, board_size))

    @ti.func
    def check_inner(x, y, p):
        q = 180 * p
        zeta = 2 * ti.atan2(ti.cast(y, ti.f32), ti.cast(x, ti.f32))

        while zeta > (90 + q) * math.pi / 180:
            zeta -= q * math.pi / 90
        while zeta < (90 - q) * math.pi / 180:
            zeta += q * math.pi / 90

        zeta = abs(math.pi / 2 - zeta)

        da = 2 * ti.sqrt(x * x + y * y) / self_size
        db = ti.sin(math.pi * q / 360) / ti.sin(math.pi * q / 360 + zeta)

        return da / db

    @ti.func
    def check(c_x, c_y, x, y, p):
        x -= c_x
        y -= c_y

        return 1.0 if (abs(x) > self_size
                       or abs(y) > self_size) else check_inner(x, y, p)

    @ti.kernel
    def paint(c_x: float, c_y: float, t: float):
        speed = 0.05
        p = 2 * abs(0.5 - (t * speed - int(t * speed)))
        p = max(p, eps)
        p = min(p, 0.5)
        for i, j in pixels:  # Parallelized over all pixels
            pixels[i, j] = check(c_x, c_y, i, j, p)

    def update_self(player):
        gui.get_event()

        if gui.is_pressed(ti.GUI.LEFT):
            player.update_speed(Vector2D(-1, 0))
        if gui.is_pressed(ti.GUI.RIGHT):
            player.update_speed(Vector2D(1, 0))
        if gui.is_pressed(ti.GUI.UP):
            player.update_speed(Vector2D(0, 1))
        if gui.is_pressed(ti.GUI.DOWN):
            player.update_speed(Vector2D(0, -1))
        return player

    for i in range(1000000000):
        player = update_self(player)
        player.update_position()
        paint(player.position.x(), player.position.y(), i * 0.03)
        gui.set_image(pixels)
        gui.show()
