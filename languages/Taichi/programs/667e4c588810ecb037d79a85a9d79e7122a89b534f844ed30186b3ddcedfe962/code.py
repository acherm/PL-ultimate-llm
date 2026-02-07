import taichi as ti

ti.init(arch=ti.cpu)

n = 320
pixels = ti.field(dtype=float, shape=(n * 2, n))

@ti.kernel
def paint(t: float):
    for i, j in pixels:
        c = ti.Vector([float(i) / n - 1, float(j) / n - 1])
        z = ti.Vector([0.0, 0.0])
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = ti.Vector([z[0]**2 - z[1]**2, 2*z[0]*z[1]]) + c
            iterations += 1
        pixels[i, j] = 1 - iterations * 0.02

gui = ti.GUI("Mandelbrot Set", res=(n * 2, n))
for i in range(1000000):
    paint(i * 0.03)
    gui.set_image(pixels)
    gui.show()
