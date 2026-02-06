import secrets

from src.utils.redis_client import redis_client


def generate_verification_code():
    """Генерирует 6-значный код для верификации"""
    return "".join([str(secrets.randbelow(10)) for _ in range(6)])


async def save_otp_in_redis(email: str, code: str) -> bool:
    # Сохраняем в Redis с TTL
    saved = await redis_client.set_verification_code(email, code)
    return saved


async def verify_email_code(email: str, code: str) -> bool:
    """
    Проверяет код верификации для email

    Args:
        email: Email пользователя
        code: Код верификации

    Returns:
        bool: True если код верный
    """
    stored_code = await redis_client.get_verification_code(email)
    if not stored_code:
        return False

    if stored_code == code:
        # Удаляем использованный код
        await redis_client.delete_verification_code(email)
        return True

    return False


async def remove_code(email: str) -> bool:
    return await redis_client.delete_verification_code(email)
