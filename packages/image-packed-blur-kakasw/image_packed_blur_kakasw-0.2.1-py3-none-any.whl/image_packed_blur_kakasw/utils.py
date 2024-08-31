from PIL import Image

def load_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
    image.save(output_path)
