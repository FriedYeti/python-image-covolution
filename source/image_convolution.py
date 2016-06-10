import os
# import PIL.Image
from LoadedImage import LoadedImage

if os.path.isfile("test.png"):
    os.remove("test.png")

image = LoadedImage("bumbleKoda.png")
image.save_copy("test.png")