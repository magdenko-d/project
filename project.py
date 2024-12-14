import asyncio
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import TOKEN
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import cur

bot = Bot(token = TOKEN)
dp = Dispatcher()


async def metro_fastfoods():
    keyboard = ReplyKeyboardBuilder()
    cur.execute('SELECT * FROM fastfoods')
    buttons = cur.fetchall()
    for button in buttons[:25]:
        keyboard.add(KeyboardButton(text=f'{button[1]}'))
    return keyboard.as_markup()


async def metro_coffeeshops():
    keyboard = ReplyKeyboardBuilder()
    cur.execute('SELECT * FROM coffeeshops')
    buttons = cur.fetchall()
    for button in buttons[:25]:
        keyboard.add(KeyboardButton(text=f'{button[1]}'))
    return keyboard.as_markup()


async def metro_restaurants():
    keyboard = ReplyKeyboardBuilder()
    cur.execute('SELECT * FROM restaurants')
    buttons = cur.fetchall()
    for button in buttons[:25]:
        keyboard.add(KeyboardButton(text=f'{button[1]}'))
    return keyboard.as_markup()


@dp.callback_query(F.data == 'restart')
async def restart(callback: CallbackQuery):
    if callback.data=='restart':
        await callback.answer('')
        await callback.message.answer('Чтобы начать заново, наберите: /start')
    else:
        None


@dp.callback_query(F.data == 'else')
async def smthelse(callback: CallbackQuery):
    if callback.data=='else':
        await callback.answer('')
        await callback.message.answer(
            'К сожалению, можно выбрать станцию и тип заведения только из предложенных. '
            'Чтобы начать заново, наберите /start'
        )
    else:
        None


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply(
        f'Привет, {message.from_user.first_name}! Выберите тип заведения.', 
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Фастфуд'), KeyboardButton(text='Кофейни'), KeyboardButton(text='Рестораны')]
            ], 
            resize_keyboard=True, 
            input_field_placeholder='Воспульзуйтесь меню для выбора'
        )
    )


@dp.message(F.text == 'Фастфуд')
async def choose_metro_fastfoods(message: Message):
    await message.reply('Выберите станцию метро из предложенных!', 
                        reply_markup=await metro_fastfoods())


@dp.message(F.text == 'Кофейни')
async def choose_metro_coffeeshops(message: Message):
    await message.reply('Выберите станцию метро из предложенных!', 
                        reply_markup=await metro_coffeeshops())


@dp.message(F.text == 'Рестораны')
async def choose_metro_restaurants(message: Message):
    await message.reply('Выберите станцию метро из предложенных!', 
                        reply_markup=await metro_restaurants())


cur.execute('SELECT * FROM fastfoods')
buttons = cur.fetchall()
for button in buttons[:25]:
    @dp.message(F.text == f'{button[1]}')
    async def choose_place_fastfoods(message: Message):
        cur.execute('SELECT * FROM fastfoods')
        buttons = cur.fetchall()
        for button in buttons:
            if message.text == f'{button[1]}':
                await message.reply(f'{button[2]}',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton(text=f'{button[3]}', url=f'{button[6]}')], 
                                        [InlineKeyboardButton(text=f'{button[4]}', url=f'{button[7]}')], 
                                        [InlineKeyboardButton(text=f'{button[5]}', url=f'{button[8]}')], 
                                        [InlineKeyboardButton(text='Начать сначала', callback_data='restart')], 
                                        [InlineKeyboardButton(text='Выбрать что-то другое', callback_data='else')]
                                    ])
                )
                break


cur.execute('SELECT * FROM coffeeshops')
coffeeshops = cur.fetchall()
for coffeeshop in coffeeshops:
    @dp.message(F.text == f'{coffeeshop[1]}')
    async def choose_place_coffeeshops(message: Message):
        cur.execute('SELECT * FROM coffeeshops')
        buttons = cur.fetchall()
        for button in buttons:
            if message.text == f'{button[1]}':
                await message.reply(
                    f'{button[2]}', 
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f'{button[3]}', url=f'{button[6]}')], 
                        [InlineKeyboardButton(text=f'{button[4]}', url=f'{button[7]}')], 
                        [InlineKeyboardButton(text=f'{button[5]}', url=f'{button[8]}')], 
                        [InlineKeyboardButton(text='Начать сначала', callback_data='restart')], 
                        [InlineKeyboardButton(text='Выбрать что-то другое', callback_data='else')]
                    ])
                )
                break


cur.execute('SELECT * FROM restaurants')
restaurants = cur.fetchall()
for restaurant in restaurants:
    @dp.message(F.text == f'{restaurant[1]}')
    async def choose_place_restaurants(message: Message):
        cur.execute('SELECT * FROM restaurants')
        buttons = cur.fetchall()
        for button in buttons:
            if message.text == f'{button[1]}':
                await message.reply(
                    f'{button[2]}', 
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f'{button[3]}', url=f'{button[6]}')], 
                        [InlineKeyboardButton(text=f'{button[4]}', url=f'{button[7]}')], 
                        [InlineKeyboardButton(text=f'{button[5]}', url=f'{button[8]}')], 
                        [InlineKeyboardButton(text='Начать сначала', callback_data='restart')], 
                        [InlineKeyboardButton(text='Выбрать что-то другое', callback_data='else')]
                    ]))
                break


@dp.message(Command('help'))
async def get_help(message:Message):
    if message.text=='/help':
        await message.answer('Если у вас возникли проблемы с работой бота, напишите @slaydx.')
    else:
        None


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
