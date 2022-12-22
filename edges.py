from PIL import Image, ImageFilter


def cropped_trans(img: Image):
    edgy = img.filter(ImageFilter.FIND_EDGES)

    cropped_trans = []
    last_edge = None
    for y in range(0, img.height):
        pixel_l = edgy.getpixel((1, y))
        # Pixels on either side have edge detection lines down them.
        pixel_r = edgy.getpixel((img.width - 1, y))

        # Skip pixels that are too dark and non-full lines.
        if sum(pixel_l) > 30 and sum(pixel_r) > 30:
            if not last_edge:
                last_edge = y
            elif (y - last_edge) > 200:
                # Check the edges are far enough apart.
                t_crop = img.crop((0, last_edge, img.width, y))
                cropped_trans.append(t_crop)

                last_edge = y
    return cropped_trans
