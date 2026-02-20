from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


# определяем путь к текущему файлу (src/utils/images.py)
CURRENT_DIR = Path(__file__).parent 

# src/utils/images.py -> utils -> src -> корень -> assets
PROJECT_ROOT = CURRENT_DIR.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

# создаем глобально, чтобы не открывать при каждом вызове функции
BASE_OTP_IMG = Image.open(ASSETS_DIR / "otp_blank_low.jpg").convert("RGB")
FONT = ImageFont.truetype(str(ASSETS_DIR / "fonts/AverageMono/AverageMono.ttf"), 32)


def generate_otp_image(text: str) -> BytesIO:
    img = BASE_OTP_IMG.copy()
    draw = ImageDraw.Draw(img)
    
    # рисуем текст
    draw.text((115, 550), text, fill="black", font=FONT)
    
    img_byte_arr = BytesIO()
    # сохраняем в jpeg со сжатием
    img.save(img_byte_arr, format='JPEG', quality=70, optimize=True)
    img_byte_arr.seek(0)
    return img_byte_arr
