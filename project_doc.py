import asyncio
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import TOKEN
from database import cur

bot = Bot(token = TOKEN)
dp = Dispatcher()


async def metro_fastfoods():
    '''
    Функция для создания клавиатуры с reply кнопками для фастфуда.

    Извлекает данные о фастфуд-заведениях из базы данных, формирует клавиатуру
    с кнопками станций метро.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками станций 
        метро для фастфуд-заведений.
    
    Examples:
        
        >>> metro_fastfoods()
        keyboard.as_markup()    
    '''
    keyboard = ReplyKeyboardBuilder()
    cur.execute('SELECT * FROM fastfoods')
    buttons = cur.fetchall()
    for button in buttons[:25]:
        keyboard.add(KeyboardButton(text=f'{button[1]}'))
    return keyboard.as_markup()


async def metro_coffeeshops():
    '''
    Функция для создания клавиатуры с reply кнопками для кофеен.

    Извлекает данные о кофейнях из базы данных, формирует клавиатуру
    с кнопками станций метро.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками станций 
        метро для кофеен.
    Examples:
        
        >>> metro_coffeeshops()
        keyboard.as_markup()
    '''
    keyboard = ReplyKeyboardBuilder()
    cur.execute('SELECT * FROM coffeeshops')
    buttons = cur.fetchall()
    for button in buttons[:25]:
        keyboard.add(KeyboardButton(text=f'{button[1]}'))
    return keyboard.as_markup()


async def metro_restaurants():
    '''
    Функция для создания клавиатуры с reply кнопками для ресторанов.

    Извлекает данные о ресторанах из базы данных, формирует клавиатуру
    с кнопками станций метро.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками станций 
        метро для ресторанов.
    
    Examples:
        
        >>> metro_restaurants()
        keyboard.as_markup()
    '''
    keyboard = ReplyKeyboardBuilder()
    cur.execute('SELECT * FROM restaurants')
    buttons = cur.fetchall()
    for button in buttons[:25]:
        keyboard.add(KeyboardButton(text=f'{button[1]}'))
    return keyboard.as_markup()


@dp.callback_query(F.data == 'restart')
async def restart(callback: CallbackQuery):
    '''
    Обработчик CallData 'restart', отправляющий сообщение.

    Функция принимает Callback 'restart' и отправляет сообщение: 
    'Чтобы начать заново, наберите: /start'

    Args:
        callback(CallbackQuery): callback запрос от пользователя.
    
    Returns:
        None: Отправка сообщения 'Чтобы начать заново, наберите: /start'

    Examples:
        Пользователь нажимает кнопку "Начать сначала", бот отправляет сообщение.

        >>> callback='restart'
        >>> restart(callback)
        'Чтобы начать заново, наберите: /start'
    '''
    await callback.answer('')
    await callback.message.answer('Чтобы начать заново, наберите: /start')


@dp.callback_query(F.data == 'else')
async def smthelse(callback: CallbackQuery):
    '''
    Обработчик CallData 'else', отправляющий сообщение.

    Функция принимает Callback 'else' и отправляет сообщение: 
    'Чтобы начать заново, наберите: /start'

    Args:
        callback(CallbackQuery): callback запрос от пользователя.
    
    Returns:
        None: Отправка сообщения 'Чтобы начать заново, наберите: /start'

    Examples:
        Пользователь нажимает кнопку "Выбрать что-то другое", бот отправляет сообщение.

        >>> callback='else'
        >>> smthelse(callback)
        'К сожалению, можно выбрать станцию и тип заведения только из предложенных. 
        Чтобы начать заново, наберите /start'
    '''
    await callback.answer('')
    await callback.message.answer(
        'К сожалению, можно выбрать станцию и тип заведения только из предложенных.'
        'Чтобы начать заново, наберите /start'
    )


@dp.message(CommandStart())
async def start(message: Message):
    '''
    Обработчик команды /start.

    Обработчик приветствует пользователя и выводит reply клавиатуру 
    для выбора типа заведений.

    Args:
        message(Message): Сообщение от пользователя.
    
    Returns:
        None: Отправляется сообщение и reply клавиатура.
    
    Examples:
        Пользователь нажимает/отправляет сообщение /start, бот 
        отправляет сообщение с reply клавиатурой.

        >>> message='/start'
        >>> start(message)
        'Привет, {first_name}! Выберите тип заведения.', ReplyKeyboardMarkup
    '''
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
    '''
    Обработчик сообщения 'Фастфуд.

    Обработчик предлагает выбрать станцию метро по выбранному типу заведения
    и выводит reply клавиатуру со станциями из базы данных.

    Args:
        message(Message): Сообщение от пользователя.
    
    Returns:
        None: Отправляется сообщение с reply клавиатурой для выбора станции.
    
    Examples: 
        Пользователь выбирает тип заведения 'Фастфуд', бот отправляет 
        сообщение с reply клавиатурой.

        >>> message='Фастфуд'
        >>> choose_metro_fastfoods(message)
        'Выберите станцию метро из предложенных!', ReplyKeyboardMarkup
    '''
    await message.reply('Выберите станцию метро из предложенных!', reply_markup=await metro_fastfoods())


@dp.message(F.text == 'Кофейни')
async def choose_metro_coffeeshops(message: Message):
    '''
    Обработчик сообщения 'Кофейни'.

    Обработчик предлагает выбрать станцию метро по выбранному типу заведения
    и выводит reply клавиатуру со станциями из базы данных.

    Args:
        message(Message): Сообщение от пользователя.
    
    Returns:
        None: Отправляется сообщение с reply клавиатурой для выбора станции.
    
    Examples: 
        Пользователь выбирает тип заведения 'Кофейни', бот отправляет 
        сообщение с reply клавиатурой.

        >>> message='Кофейни'
        >>> choose_metro_coffeeshops(message)
        'Выберите станцию метро из предложенных!', ReplyKeyboardMarkup
    '''
    await message.reply('Выберите станцию метро из предложенных!', reply_markup=await metro_coffeeshops())


@dp.message(F.text == 'Рестораны')
async def choose_metro_restaurants(message: Message):
    '''
    Обработчик сообщения 'Рестораны'.

    Обработчик предлагает выбрать станцию метро по выбранному типу заведения
    и выводит reply клавиатуру со станциями из базы данных.

    Args:
        message(Message): Сообщение от пользователя.
    
    Returns:
        None: Отправляется сообщение с reply клавиатурой для выбора станции.
    
    Examples: 
        Пользователь выбирает тип заведения 'Рестораны', бот отправляет 
        сообщение с reply клавиатурой.

        >>> message='Рестораны'
        >>> choose_metro_restaurants(message)
        'Выберите станцию метро из предложенных!', ReplyKeyboardMarkup
    '''
    await message.reply('Выберите станцию метро из предложенных!', reply_markup=await metro_restaurants())


cur.execute('SELECT * FROM fastfoods')
fastfoods = cur.fetchall()
for fastfood in fastfoods:
    @dp.message(F.text == f'{fastfood[1]}')
    async def choose_place_fastfoods(message: Message):
       '''
        Обработчик для вывода фастфуд-заведений.

        Функция сравнивает сообщение со значениями из базы данных в столбике
        с названиями станций, в случае совпадения отправляет сообщение со 
        списком заведений и inline клавиатуру, по которой можно посмотреть меню,
        узнать как начать заново и можно ли выбрать что-то другое.

        Args:
            message(Message): Сообщение от пользователя

        Returns:
            None: Отправка сообщения с inline клавиатурой.
        
        Examples:
            Пользователь выбирает станцию 'Павелецкая (1)', бот отправляет 
            сообщение с inline клавиатурой.

            >>> message='Павелецкая (1)'
            >>> choose_place_fastfoods(message)
            'Текст', InlineKeyboardMarkup
        '''
       cur.execute('SELECT * FROM fastfoods')
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


cur.execute('SELECT * FROM coffeeshops')
coffeeshops = cur.fetchall()
for coffeeshop in coffeeshops:
    @dp.message(F.text == f'{coffeeshop[1]}')
    async def choose_place_coffeeshops(message: Message):
        '''
        Обработчик для вывода заведений-кофеен.

        Функция сравнивает сообщение со значениями из базы данных в столбике
        с названиями станций, в случае совпадения отправляет сообщение со 
        списком заведений и inline клавиатуру, по которой можно посмотреть меню,
        узнать как начать заново и можно ли выбрать что-то другое.

        Args:
            message(Message): Сообщение от пользователя

        Returns:
            None: Отправка сообщения с inline клавиатурой.
        
        Examples:
            Пользователь выбирает станцию 'Китай-город (2)', бот отправляет 
            сообщение с inline клавиатурой.

            >>> message='Китай-город (2)'
            >>> choose_place_coffeeshops(message)
            'Текст', InlineKeyboardMarkup
        '''
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
        '''
        Обработчик для вывода заведений-ресторанов.

        Функция сравнивает сообщение со значениями из базы данных в столбике
        с названиями станций, в случае совпадения отправляет сообщение со 
        списком заведений и inline клавиатуру, по которой можно посмотреть меню,
        узнать как начать заново и можно ли выбрать что-то другое.

        Args:
            message(Message): Сообщение от пользователя

        Returns:
            None: Отправка сообщения с inline клавиатурой.
        
        Examples:
            Пользователь выбирает станцию 'Полянка (3)', бот отправляет 
            сообщение с inline клавиатурой.

            >>> message='Полянка (3)'
            >>> choose_place_restaurants(message)
            'Текст', InlineKeyboardMarkup
        '''
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
                    ])
                )
                break


@dp.message(Command('help'))
async def get_help(message:Message):
    '''
    Обработчик команды /help.

    Обработчик команды /help предоставляет контакты для техничекой поддержки.

    Args:
        message(Message):

    Returns:
        None:
    
    Examples:
        bnn

        >>> message='/'
        >>> get_help(message)
        'Если у вас возникли проблемы с работой бота, напишите @slaydx.'
    '''
    await message.answer('Если у вас возникли проблемы с работой бота, напишите @slaydx.')

async def main():
    '''
    Функция для запуска бота.

    Функция постоянно запращивает обновления от Телеграмма для бота
    и начинает обработку входящих данных.

    Returns:
        None
    '''
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
