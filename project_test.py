import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from aiogram.types import ReplyKeyboardMarkup, CallbackQuery, Message
from project import metro_fastfoods, metro_coffeeshops, metro_restaurants, restart, smthelse, get_help

class TestMetroFastfoods(unittest.IsolatedAsyncioTestCase):
    @patch('project.cur')
    async def test_metro_fast1(self, mock_cur):
        
        test=[
            (1, 'metro01', 'desc01', 'place01', 'place02', 'place03','link01','link02','link03')
        ]
        
        mock_cur.execute = MagicMock()
        mock_cur.fetchall = MagicMock(return_value=test)

        keyboard_mark=await metro_fastfoods()

        self.assertIsInstance(keyboard_mark, ReplyKeyboardMarkup)
        self.assertEqual(len(keyboard_mark.keyboard),1)
    
    @patch('project.cur')
    async def test_metro_fast_neg(self, mock_cur):
        '''Проверка на пустой базе данных'''
        mock_cur.execute = MagicMock()
        mock_cur.fetchall = MagicMock(return_value=[])

        keyboard_mark = await metro_fastfoods()
        self.assertIsInstance(keyboard_mark, ReplyKeyboardMarkup)
        self.assertEqual(len(keyboard_mark.keyboard),0)


class TestMetroCoffeeshops(unittest.IsolatedAsyncioTestCase):
    @patch('project.cur')
    async def test_metro_coffee(self, mock_cur):
        
        test=[
            (1, 'metro01', 'desc01', 'place01', 'place02', 'place03','link01','link02','link03')
        ]
        
        mock_cur.execute = MagicMock()
        mock_cur.fetchall = MagicMock(return_value=test)

        keyboard_mark=await metro_coffeeshops()

        self.assertIsInstance(keyboard_mark, ReplyKeyboardMarkup)
        self.assertEqual(len(keyboard_mark.keyboard),1)
    
    @patch('project.cur')
    async def test_metro_coffee_neg(self, mock_cur):
        '''Проверка на пустой базе данных'''
        mock_cur.execute = MagicMock()
        mock_cur.fetchall = MagicMock(return_value=[])

        keyboard_mark = await metro_coffeeshops()
        self.assertIsInstance(keyboard_mark, ReplyKeyboardMarkup)
        self.assertEqual(len(keyboard_mark.keyboard),0)


class TestMetroRestaurants(unittest.IsolatedAsyncioTestCase):
    @patch('project.cur')
    async def test_metro_rest(self, mock_cur):
        
        test=[
            (1, 'metro01', 'desc01', 'place01', 'place02', 'place03','link01','link02','link03')
        ]
        
        mock_cur.execute = MagicMock()
        mock_cur.fetchall = MagicMock(return_value=test)

        keyboard_mark=await metro_restaurants()

        self.assertIsInstance(keyboard_mark, ReplyKeyboardMarkup)
        self.assertEqual(len(keyboard_mark.keyboard),1)
    
    @patch('project.cur')
    async def test_metro_rest_neg(self, mock_cur):
        '''Проверка на пустой базе данных'''
        mock_cur.execute = MagicMock()
        mock_cur.fetchall = MagicMock(return_value=[])

        keyboard_mark = await metro_restaurants()
        self.assertIsInstance(keyboard_mark, ReplyKeyboardMarkup)
        self.assertEqual(len(keyboard_mark.keyboard),0)


class TestRestart(unittest.IsolatedAsyncioTestCase):
    @patch.object(CallbackQuery, 'answer', new_callable=AsyncMock)
    @patch.object(Message, 'answer', new_callable=AsyncMock)
    async def test_restart(self, mock_callback, mock_message):
        mock_callback = MagicMock(spec=CallbackQuery)
        mock_message = MagicMock(spec=Message)

        mock_callback.data='restart'
        mock_callback.message = mock_message

        await restart(mock_callback)

        mock_callback.answer.assert_called_once()
        mock_message.answer.assert_called_once_with('Чтобы начать заново, наберите: /start')
    
    @patch.object(CallbackQuery, 'answer', new_callable=AsyncMock)
    @patch.object(Message, 'answer', new_callable=AsyncMock)
    async def test_restart_neg(self, mock_callback, mock_message):
        '''Если callback.data!='restart', то функция не должна отправлять callback и сообщение'''

        mock_callback = MagicMock(spec=CallbackQuery)
        mock_message = MagicMock(spec=Message)

        mock_callback.data='data'
        mock_callback.message = mock_message

        await restart(mock_callback)

        mock_callback.answer.assert_not_called()
        mock_message.answer.assert_not_called()


class TestSmthelse(unittest.IsolatedAsyncioTestCase):
    @patch.object(CallbackQuery, 'answer', new_callable=AsyncMock)
    @patch.object(Message, 'answer', new_callable=AsyncMock)
    async def test_smthelse(self, mock_callback, mock_message):
        mock_callback = MagicMock(spec=CallbackQuery)
        mock_message = MagicMock(spec=Message)

        mock_callback.data='else'
        mock_callback.message = mock_message

        await smthelse(mock_callback)

        mock_callback.answer.assert_called_once()
        mock_message.answer.assert_called_once_with('К сожалению, можно выбрать станцию и тип заведения только из предложенных. Чтобы начать заново, наберите /start')
    
    @patch.object(CallbackQuery, 'answer', new_callable=AsyncMock)
    @patch.object(Message, 'answer', new_callable=AsyncMock)
    async def test_restart_neg(self, mock_callback, mock_message):
        '''Если callback.data!='else', то функция не должна отправлять callback и сообщение'''

        mock_callback = MagicMock(spec=CallbackQuery)
        mock_message = MagicMock(spec=Message)

        mock_callback.data='data'
        mock_callback.message = mock_message

        await restart(mock_callback)

        mock_callback.answer.assert_not_called()
        mock_message.answer.assert_not_called()


class TestGetHelp(unittest.IsolatedAsyncioTestCase):
    @patch.object(Message, 'answer', new_callable=AsyncMock)
    async def test_get_help(self, mock_message):
        mock_message = MagicMock(spec=Message)
        mock_message.text = '/help'

        await get_help(mock_message)

        mock_message.answer.assert_called_once_with('Если у вас возникли проблемы с работой бота, напишите @slaydx.')

    @patch.object(Message, 'answer', new_callable=AsyncMock)
    async def test_get_help_neg(self, mock_message):
        mock_message = MagicMock(spec=Message)
        mock_message.text = '/helpp'

        await get_help(mock_message)

        mock_message.answer.assert_not_called()


if __name__=='__main__':
    unittest.main()

