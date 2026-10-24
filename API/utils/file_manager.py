import svgwrite
from PIL import Image


def create_any_image(image_format: str) -> None:
    """
    Создание изображения любого формата
    Args:
        image_format: формат изображения
    """
    if image_format.lower() in ["jpg", "png"]:
        image = Image.new('RGB', (500, 500), (255, 255, 255))
        if image_format.lower() == "jpg":
            image.save(f'example.{image_format}', "JPEG")
        else:
            image.save(f'example.{image_format}', "PNG")

    elif image_format.lower() == "svg":
        dwg = svgwrite.Drawing(f'example.{image_format}', size=('500px', '500px'))

        dwg.add(dwg.circle(center=(250, 250), r=200))

        dwg.save()
