from cmath import log10

import taichi as ti

ti.init(arch=ti.gpu, default_fp=ti.f64)

size = 800
pixels = ti.field(dtype=ti.f64, shape=(size, size))


@ti.kernel
def paint(xmin: ti.f64, ymin: ti.f64, xmax: ti.f64, ymax: ti.f64):
    for i, j in pixels:
        zr = xmin + (xmax-xmin) * i/size
        zi = ymin + (ymax-ymin) * j/size

        cr = zr
        ci = zi

        iterations = 0
        zoom_depth = 3.0 / (xmax - xmin)
        # 0.43... = inverse ln(10). this computes the log base 10 of zoom_depth
        max_iterations = int(250 + 50 * max(0.0, ti.log(zoom_depth)*0.4342944819))
        while (zr*zr + zi * zi) < 4.0 and iterations < max_iterations:
            nextr = (zr*zr - zi*zi) + cr
            nexti = (2 * zr*zi) + ci
            zr = nextr
            zi = nexti
            iterations += 1

        pixels[i, j] = 1.0 - iterations / max_iterations



def main():
    gui = ti.GUI("Mandelbrot Fractal", res=(size, size))

    xmin = -2.2
    ymin = -1.5
    xmax = 0.8
    ymax = 1.5

    while gui.running:
        for e in gui.get_events(ti.GUI.WHEEL):

            wheel = e.delta[1]
            pos = e.pos
            
            if wheel == 0:
                continue

            
            zoom = 0.8 if wheel > 0 else 1.25
            
            centx = xmin + (xmax - xmin) * pos[0]
            centy = ymin + (ymax - ymin) * pos[1]

            width = (xmax - xmin) * zoom
            height = (ymax - ymin) * zoom
            
            xmin = centx - width * pos[0]
            xmax = centx + width * (1.0 - pos[0])
            ymin = centy - height * pos[1]
            ymax = centy + height * (1.0 - pos[1])


        paint(xmin, ymin, xmax, ymax)
        gui.set_image(pixels)
        gui.show()


if __name__ == "__main__":
  main()