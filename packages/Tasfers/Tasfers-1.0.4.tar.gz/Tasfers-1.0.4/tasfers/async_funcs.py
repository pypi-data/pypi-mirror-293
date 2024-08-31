import aiofiles
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


async def write_text_to_file(file_path: str, text: str):
    """
    Асинхронно записывает текст в файл. Если файл существует, добавляет текст с новой строки.
    Если файла нет, создаёт его и записывает текст.

    :param file_path: Путь к файлу
    :param text: Текст для записи
    """
    try:
        async with aiofiles.open(file_path, mode='a', encoding='utf-8') as file:
            await file.write(text + '\n')
    except IOError as e:
        print(f"Ошибка при работе с файлом: {e}")


async def encrypt_async(data, encryption_key, nonce):
    """
        Асинхронно записывает текст в файл. Если файл существует, добавляет текст с новой строки.
        Если файла нет, создаёт его и записывает текст.

        :param file_path: Путь к файлу
        :param text: Текст для записи
        """
    if len(nonce) != 16:
        raise ValueError("Nonce (IV) must be 16 bytes long for AES-CBC.")

    combined_key = encryption_key + nonce

    cipher = Cipher(algorithms.AES(combined_key[:32]), modes.CBC(nonce), backend=default_backend())
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_data


async def decrypt_async(encrypted_data, encryption_key, nonce):
    if len(nonce) != 16:
        raise ValueError("Nonce (IV) must be 16 bytes long for AES-CBC.")

    combined_key = encryption_key + nonce

    cipher = Cipher(algorithms.AES(combined_key[:32]), modes.CBC(nonce), backend=default_backend())

    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode('utf-8')
