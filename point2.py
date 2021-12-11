import taichi as ti
import math

ti.init(arch=ti.gpu)

n = 320
pixels = ti.field(dtype=float, shape=(n, n))


@ti.kernel
def paint(t: float):
    p = abs(0.5 - (t - int(t)))
    for i, j in pixels:  # Parallelized over all pixels
        if (abs(i - n / 2) ** 2)+(abs(j - n / 2) ** 2) < (0.5 - p) * 10 * n:
            pixels[i, j] = 1
        else:
            pixels[i, j] = 0


gui = ti.GUI("Point2", res=(n, n))

for i in range(1000000000):
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
