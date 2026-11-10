import taichi as ti

try:
    ti.init(arch=ti.gpu, default_fp=ti.f64)

    @ti.kernel
    def test_f64() -> ti.f64:
        x: ti.f64 = 1.0
        return x
    test_f64()
    print("Running on GPU with 64-bit precision")
except Exception as e:

    print(f"GPU not supported for 64-bit floats ({e}). Using multithreaded CPU")
    ti.init(arch=ti.cpu, default_fp=ti.f64)
    print("Running on CPU with 64-bit precision")

width, height = 1200, 800
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))


@ti.func
def calc_color(iters, max_iters, colorful):
    col = ti.Vector([0.0, 0.0, 0.0])
    if iters < max_iters:
        if colorful:
            hue = 0.95 + 10 * (ti.log(ti.log(float(iters) + 1)))
            r = 0.5 * ti.cos(3.14159 * (hue + 0.0)) + 0.5
            g = 0.5 * ti.cos(3.14159 * (hue + 0.4)) + 0.5
            b = 0.5 * ti.cos(3.14159 * (hue + 0.8)) + 0.5
            col = ti.Vector([r,g,b])
        else:
            a = 1.0 - (iters / max_iters)
            col = ti.Vector([a,a,a])
    return col


@ti.kernel
def paint(xmin: ti.f64, ymin: ti.f64, xmax: ti.f64, ymax: ti.f64, max_iters: int, colorful: bool):
    for i, j in pixels:
        zr = xmin + (xmax-xmin) * i/width
        zi = ymin + (ymax-ymin) * j/height

        cr = zr
        ci = zi

        iterations = 0
        # zoom_depth = 3.0 / (xmax - xmin)
        # # 0.43... = inverse ln(10). this computes the log base 10 of zoom_depth
        # max_iterations = int(250 + 50 * max(0.0, ti.log(zoom_depth)*0.4342944819))
        while (zr*zr + zi*zi) < 4.0 and iterations < max_iters:
            nextr = (zr*zr - zi*zi) + cr
            nexti = (2 * zr*zi) + ci
            zr = nextr
            zi = nexti
            iterations += 1

        pixels[i, j] = calc_color(iterations, max_iters, colorful)



def main():
    # gui = ti.GUI("Mandelbrot Fractal", res=(width, height))
    window = ti.ui.Window(
        "Mandelbrot Fractal",
        (width, height),
        vsync=True
    )
    canvas = window.get_canvas()

    xmin = -2.7
    ymin = -1.25
    xmax = 1.4
    ymax = 1.25

    show_help = True
    colorful = True

    ctrl_down = False
    alt_down = False
    shift_down = False


    while window.running:
        zoom = 1.0

        for event in window.get_events(ti.ui.PRESS):
            if event.key in ("h","H","/","?"):
                show_help = not show_help
            elif event.key in ("c","C"):
                colorful = not colorful
            elif event.key == ti.ui.CTRL:
                ctrl_down = True
            elif event.key == ti.ui.ALT:
                alt_down = True
            elif event.key == ti.ui.SHIFT:
                shift_down = True

        for event in window.get_events(ti.ui.RELEASE):
            if event.key == ti.ui.CTRL:
                ctrl_down = False
            elif event.key == ti.ui.ALT:
                alt_down = False
            elif event.key == ti.ui.SHIFT:
                shift_down = False
        
        if window.is_pressed(ti.ui.ESCAPE):
            window.running = False

        factor = 0.005
        if ctrl_down:
            factor = 0.040
        elif alt_down:
            factor = 0.025
        elif shift_down:
            factor = 0.012
        

        if window.is_pressed("i", "=", ti.ui.LMB):
            zoom = 1.0 - factor  # Zoom in
        elif window.is_pressed("o", "-", ti.ui.RMB):
            zoom = 1.0 + factor  # Zoom out

        if window.is_pressed("r"):
            xmin = -2.7
            ymin = -1.25
            xmax = 1.4
            ymax = 1.25

       

        if zoom != 1.0:
            pos = window.get_cursor_pos()
            centx = xmin + (xmax - xmin) * pos[0]
            centy = ymin + (ymax - ymin) * pos[1]

            w = (xmax - xmin) * zoom
            h = (ymax - ymin) * zoom
            
            xmin = centx - w * pos[0]
            xmax = centx + w * (1.0 - pos[0])
            ymin = centy - h * pos[1]
            ymax = centy + h * (1.0 - pos[1])
            

        zoom_depth = 3.0 / (xmax - xmin)
        # 0.43... = inverse ln(10). this computes the log base 10 of zoom_depth
        max_iters = int(250 + 75 * max(0.0, ti.log(zoom_depth)*0.4342944819))

        paint(xmin, ymin, xmax, ymax, max_iters, colorful)
        canvas.set_image(pixels)

        if window.is_pressed(" ", ti.ui.RETURN, "s"):
            window.save_image('mandelbrot-screenshot.png')

        if show_help:
            gui = window.get_gui()

            with gui.sub_window("Controls (Press 'h' to hide)", 0.007, 0.01, 0.22, 0.27):
                gui.text("Esc: Quit\nLeft-Click: Zoom in\nRight-Click: Zoom out\n'h': Show/hide help (this window)\n's': Save current window as png\n'r': Reset zoom\n'c': Toggle fun mode (color)")
                gui.text("\nZoom Speed Modifier Keys:")
                gui.text("[No Key]: Zoom Speed 1x\nShift: Zoom Speed 2x\nAlt: Zoom Speed 5x\nCtrl: Zoom Speed 8x")

        window.show()


if __name__ == "__main__":
  main()