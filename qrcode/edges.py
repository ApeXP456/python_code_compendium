from PIL import Image, ImageFilter

# replace"bridge.bmp" with your image
before = Image.open("qr.png")

after = before.filter(ImageFilter.FIND_EDGES)

after.save("Edged.png")