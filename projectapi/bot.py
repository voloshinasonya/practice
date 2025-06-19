Import logging
Import aiohttp
Import asyncio

From aiogram import Bot, Dispatcher, types
From aiogram.filters import Command
From aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = «Your-Bot-Token»

Logging.basicConfig(level=logging.INFO)

Bot = Bot(token=BOT_TOKEN)
Dp = Dispatcher()

Keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=»Дата», callback_data=»дата»),
        InlineKeyboardButton(text=»Місце», callback_data=»місце»),
    ],
    [
        InlineKeyboardButton(text=»Персона», callback_data=»персона»),
        InlineKeyboardButton(text=»Подія», callback_data=»подія»),
    ],
    [
        InlineKeyboardButton(text=»Термін», callback_data=»термін»),
    ],
])

@dp.message(Command(commands=[«start»]))
Async def cmd_start(message: types.Message):
    Await message.answer(
        «Привіт! Я бот, що знаходить цікаву випадкову інформацію на Вікіпедії. Вибери нижче!»,
        Reply_markup=keyboard,
    )

# Фільтр по callback_data (проста лямбда функція)
@dp.callback_query(lambda c: c.data in [«дата», «місце», «персона», «подія», «термін»])
Async def handle_topic(callback: types.CallbackQuery):
    Topic = callback.data
    Await callback.answer()  # Прибираємо «loading» у UI

    url = f»http://127.0.0.1:8000/wiki/{topic}»

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await bot.send_message(callback.from_user.id, «⚠️ Не вдалося знайти інформацію. Спробуй ще раз.»)
                    return
                data = await resp.json()

        if «error» in data:
            await bot.send_message(callback.from_user.id, f»⚠️ Помилка: {data['error']}»)
            return

        text = f»{data['title']}\n\n{data['summary']}\n\n🔗 [Читати на Вікіпедії]({data['url']})»
        await bot.send_message(callback.from_user.id, text, parse_mode=»Markdown»)

    except Exception as e:
        logging.error(f»Error fetching wiki data: {e}»)
        await bot.send_message(callback.from_user.id, «⚠️ Помилка з'єднання з API.»)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == «__main__»:
    asyncio.run(main())
