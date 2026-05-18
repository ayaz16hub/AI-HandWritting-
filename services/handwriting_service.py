from PIL import Image, ImageDraw, ImageFont


def text_to_handwriting(text, output_path):

    # Create white page
    img = Image.new("RGB", (1240, 1754), "white")
    draw = ImageDraw.Draw(img)

    # ===== BORDER =====
    draw.rectangle(
        [(20, 20), (1220, 1734)],
        outline=(180, 180, 180),
        width=3
    )

    # ===== LEFT MARGIN LINE =====
    draw.line(
        [(120, 20), (120, 1734)],
        fill=(255, 100, 100),
        width=3
    )

    # ===== HORIZONTAL NOTEBOOK LINES =====
    y_line = 100

    while y_line < 1700:
        draw.line(
            [(20, y_line), (1220, y_line)],
            fill=(200, 220, 255),
            width=2
        )

        y_line += 60

    # ===== FONT =====
    font = ImageFont.truetype("fonts/handwriting.ttf", 40)

    # ===== TEXT START POSITION =====
    x = 150
    y = 50

    # ===== DRAW TEXT =====
    for line in text.split("\n"):
        draw.text((x, y), line, fill="black", font=font)
        y += 60

    # ===== SAVE IMAGE =====
    img.save(output_path)

    return output_path