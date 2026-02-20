from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def generate_otp_image(text: str) -> BytesIO:
    img = Image.open('assets/otp_blank.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("assets/fonts/AverageMono/AverageMono.ttf", 76)
    
    # рисуем текст
    draw.text((375, 2050), text, fill="black", font=font)
    
    img_byte_arr = BytesIO()
    # Сохраняем в PNG (или JPEG), чтобы передать в письмо
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr