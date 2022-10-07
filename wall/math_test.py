def draw_pixel_strip(x, y, rot):
    if rot == 0:
        n = y * 20 + x
    elif rot == 90:
        n = 19 + 20 * x - y
    elif rot == 180:
        n = 399 - x - y * 20
    elif rot == -90:
        n = 380 - 20 * x + y
    print("pos:", n)

while True:
    c = input("Coords: ").split(",")
    r = input("Rot: ")
    x, y = int(c[0]), int(c[1])
    draw_pixel_strip(x, y, int(r))