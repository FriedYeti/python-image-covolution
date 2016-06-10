import PIL.Image

class LoadedImage:
    """Image loaded to memory"""

    def __init__(self, image_file_path):
        self.image = PIL.Image.open(image_file_path)
        # TODO - checking if valid file path

        self.image = self.image.convert('RGB')

        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pixels = self.image.load()

    def save_copy(self, new_file_name):
        if "." not in new_file_name:
            new_file_name = new_file_name + ".png"
        self.image.save(new_file_name)