import taichi as ti
import math

ti.init(arch=ti.gpu)

eps = 0.00001
n = 200

pixels = ti.field(dtype=float, shape=(n, n))

@ti.func
def check(x, y, p):
    q = 180*p

    x -= n/2
    y -= n/2

    zeta = 2*ti.atan2(ti.cast(y, ti.f32), ti.cast(x, ti.f32))
    
    while zeta > (90+q)*math.pi/180:
        zeta -= q*math.pi/90
    while zeta < (90-q)*math.pi/180:
        zeta += q*math.pi/90
    
    zeta = abs(math.pi/2-zeta)

    da = 2*ti.sqrt(x*x+y*y)/n
    db = ti.sin(math.pi*q/360)/ti.sin(math.pi*q/360+zeta)

    return da/db


@ti.kernel
def paint(t: float):
    speed=0.1
    p = 2 * abs(0.5 - (t*speed - int(t*speed)))
    p=max(p,eps)
    p=min(p,0.5)
    for i, j in pixels:  # Parallelized over all pixels
        pixels[i, j] = check(i, j, p)


gui = ti.GUI("Julia Set", res=(n, n))

for i in range(1000000000):
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
