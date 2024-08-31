from PIL import Image, ImageFilter

def apply_blur(image_path, output_path, radius=2):
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    blurred_image.save(output_path)
    return output_path
