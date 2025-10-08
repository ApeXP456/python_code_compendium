import qrcode

img = qrcode.make("https://www.digital---wall.com/")
img.save("qr.png", "PNG")
