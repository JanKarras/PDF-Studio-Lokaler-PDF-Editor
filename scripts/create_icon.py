from pathlib import Path
from PIL import Image, ImageDraw


def createIcon():
    image = Image.new("RGBA", (512, 512))
    painter = ImageDraw.Draw(image)
    painter.rounded_rectangle((16, 16, 496, 496), radius=104, fill="#1b2b46")
    painter.rounded_rectangle((144, 88, 392, 400), radius=28, fill="#48628a")
    painter.rounded_rectangle((96, 128, 344, 440), radius=28, fill="#edf3ff")
    for position, length in [(212, 124), (268, 144), (324, 96)]:
        painter.rounded_rectangle((148, position - 10, 148 + length, position + 10), radius=10, fill="#577cc0")
    destination = Path("build/pdf-studio.ico")
    destination.parent.mkdir(exist_ok=True)
    image.save(destination, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    return destination
