import unittest
from image_packed_blur_kakasw.transformations import resize_image
from PIL import Image
import os

class TestTransformations(unittest.TestCase):
    def setUp(self):
        # Cria uma imagem de teste
        self.image_path = 'test_image.jpg'
        self.resized_image_path = 'resized_image.jpg'
        image = Image.new('RGB', (100, 100), color = 'red')
        image.save(self.image_path)

    def test_resize_image(self):
        # Testa se a imagem é redimensionada corretamente
        new_size = (50, 50)
        result = resize_image(self.image_path, self.resized_image_path, new_size)
        self.assertTrue(result.endswith('resized_image.jpg'))
        
        # Verifica o tamanho da imagem redimensionada
        with Image.open(self.resized_image_path) as img:
            self.assertEqual(img.size, new_size)

    def tearDown(self):
        # Remove as imagens de teste
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.resized_image_path):
            os.remove(self.resized_image_path)

if __name__ == '__main__':
    unittest.main()
