import unittest
from image_packed_blur_kakasw.utils import load_image, save_image
from PIL import Image
import os

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Cria uma imagem de teste
        self.image_path = 'test_image.jpg'
        self.saved_image_path = 'saved_image.jpg'
        image = Image.new('RGB', (100, 100), color = 'blue')
        image.save(self.image_path)

    def test_load_image(self):
        # Testa se a imagem é carregada corretamente
        image = load_image(self.image_path)
        self.assertIsInstance(image, Image.Image)

    def test_save_image(self):
        # Testa se a imagem é salva corretamente
        image = load_image(self.image_path)
        save_image(image, self.saved_image_path)
        self.assertTrue(os.path.exists(self.saved_image_path))

    def tearDown(self):
        # Remove as imagens de teste
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.saved_image_path):
            os.remove(self.saved_image_path)

if __name__ == '__main__':
    unittest.main()
