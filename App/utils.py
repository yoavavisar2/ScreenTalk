import tkinter

def create_gradient(canvas, width, height, color1, color2):
    """Draws a vertical gradient from color1 to color2"""
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))

        color = f"#{nr >> 8:02x}{ng >> 8:02x}{nb >> 8:02x}"
        canvas.create_line(0, i, width, i, fill=color)

def pixels2points(pixels):
    return int(0.75 * pixels)
