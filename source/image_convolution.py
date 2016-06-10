import os
# import PIL.Image
from LoadedImage import LoadedImage

if os.path.isfile("../images/test_save.png"):
    os.remove("../images/test_save.png")

image = LoadedImage("../images/bumbleKoda.png")
image.save_copy("../images/test_save.png")