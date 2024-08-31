from PIL import Image, ImageFilter

def apply_blur(image_path, output_path, radius=2):
    """
    Aplica um efeito de blur (desfoque) a uma imagem e salva o resultado em um novo arquivo.

    :param image_path: Caminho para a imagem original.
    :param output_path: Caminho onde a imagem borrada será salva.
    :param radius: Raio do blur. Maior valor significa mais desfoque.
    """
    try:
        # Abre a imagem no caminho especificado
        image = Image.open(image_path)
        
        # Aplica o filtro GaussianBlur com o raio especificado
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
        
        # Salva a imagem borrada no caminho de saída especificado
        blurred_image.save(output_path)
        
        # Mensagem opcional para indicar sucesso
        print(f"Imagem borrada salva em: {output_path}")
    
    except Exception as e:
        # Tratamento de erros, exibindo uma mensagem caso algo dê errado
        print(f"Ocorreu um erro ao aplicar o blur: {e}")
