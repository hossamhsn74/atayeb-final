from PIL import Image


def get_resized_image(obj, req_width=300, req_height=300):
    img = Image.open(obj.image.path)
    if img.width > req_width or img.height > req_height:
        output_size = (req_width, req_height)
        img.thumbnail(output_size)
    return img

