import unittest
from image_packed_blur_kakasw.filters import apply_blur
from PIL import Image, ImageChops
import os

class TestFilters(unittest.TestCase):
    def setUp(self):
        # Cria uma imagem de teste (100x100, cor vermelha)
        self.image_path = 'test_image.jpg'
        self.blurred_image_path = 'blurred_image.jpg'
        image = Image.new('RGB', (100, 100), color='red')
        image.save(self.image_path)

    def test_apply_blur(self):
        # Aplica o blur à imagem de teste
        apply_blur(self.image_path, self.blurred_image_path, radius=5)
        
        # Carrega a imagem original e a imagem borrada
        original_image = Image.open(self.image_path)
        blurred_image = Image.open(self.blurred_image_path)
        
        # Exibe a imagem borrada para inspeção visual
        blurred_image.show()
        
        # Verifica se a imagem borrada é diferente da original
        diff = ImageChops.difference(original_image, blurred_image)
        
        # Salve a imagem de diferença para inspeção, se necessário
        diff.save("difference_image.jpg")

        # A diferença deve existir (ou seja, as imagens não devem ser iguais)
        self.assertIsNotNone(diff.getbbox(), "Blur não foi aplicado corretamente ou as imagens são idênticas.")

    def tearDown(self):
        # Remove as imagens de teste
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.blurred_image_path):
            os.remove(self.blurred_image_path)
        if os.path.exists("difference_image.jpg"):
            os.remove("difference_image.jpg")

if __name__ == '__main__':
    unittest.main()
