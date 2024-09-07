import os

from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import SECRET_TOKEN
from bot.utils import Provider
from model import model_inference
from model.config import IMAGE_SAVE_PATH

router = Router()
router.message.filter(~F.forward_from & ~F.forward_from_chat)


# /start
@router.message(F.chat.type == ChatType.PRIVATE, CommandStart())
async def cmd_start(message: Message):
    text = Provider.get_text('messages.start')
    await message.answer(text)


@router.message(F.photo)
async def photo_msg(message: Message):
    from main import bot
    photo = message.photo[-1]

    # Получаем путь к файлу на серверах Telegram
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path

    photo_url = f'https://api.telegram.org/file/bot{SECRET_TOKEN}/{file_path}'
    image_name = os.path.join(IMAGE_SAVE_PATH, f"{photo.file_id}.jpg")

    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as response:
            if response.status == 200:
                # Сохраняем изображение на диск
                with open(image_name, 'wb') as f:
                    f.write(await response.read())

    # Задаем имя файла для сохранения
    image_name = os.path.join(IMAGE_SAVE_PATH, f"{photo.file_id}.jpg")
    print(image_name)
    text = model_inference.get_result(image_name)

    await message.answer(text)
