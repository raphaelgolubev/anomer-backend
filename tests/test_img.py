from src.utils.images import generate_otp_image


def test_image_result(test_code: str = "A-776-90"):
    """
    Тестовая функция для проверки итогового изображения
    """
    # генерируем объект BytesIO с изображением
    image_stream = generate_otp_image(test_code)
    
    # создаем файл и записываем в него содержимое потока
    try:
        with open("output.jpg", "wb") as f:
            f.write(image_stream.getvalue())
        print(f"✅ Изображение сохранено как output.jpg")
    except Exception as e:
        print(f"❌ Системная ошибка при сохранении: {e}")
    finally:
        image_stream.close() # освобождаем память


test_image_result()