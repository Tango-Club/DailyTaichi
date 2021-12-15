import taichi as ti

ti.init(arch=ti.cpu)

n = 320
pixels = ti.field(dtype=float, shape=(n, n))


@ti.kernel
def paint(t: float):
    for i, j in pixels:  # Parallelized over all pixels
        if (abs(i - n / 2)**2) + (abs(j - n / 2)**2) < n:
            pixels[i, j] = 1
        else:
            pixels[i, j] = 0


gui = ti.GUI("Point", res=(n, n))

for i in range(1000000000):
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
