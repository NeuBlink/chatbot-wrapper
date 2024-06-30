# File: tests/test_units.py

import unittest
from unittest.mock import patch, MagicMock
import os
from config import get_openai_key, get_db_creds, setup_logging
from memory import acquire_lock, release_lock, get_user_memory, save_user_memory
from User import User
from Chatbot import Chatbot
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain import PromptTemplate

class TestConfig(unittest.TestCase):
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_get_openai_key(self):
        self.assertEqual(get_openai_key(), 'test_key')

    @patch.dict(os.environ, {'MONGODB_URI': 'test_uri', 'MONGODB_DB_NAME': 'test_db'})
    def test_get_db_creds(self):
        uri, db_name = get_db_creds()
        self.assertEqual(uri, 'test_uri')
        self.assertEqual(db_name, 'test_db')

    def test_setup_logging(self):
        logger = setup_logging()
        self.assertIsNotNone(logger)
        self.assertTrue(hasattr(logger, 'info'))
        self.assertTrue(hasattr(logger, 'error'))

class TestMemory(unittest.TestCase):
    @patch('memory.locks')
    def test_acquire_release_lock(self, mock_locks):
        mock_locks.find_one.return_value = None
        self.assertTrue(acquire_lock('test_user'))
        mock_locks.update_one.assert_called_once()

        release_lock('test_user')
        mock_locks.delete_one.assert_called_once_with({'_id': 'test_user'})

    @patch('memory.memories')
    @patch('memory.pickle')
    @patch('memory.Binary')
    def test_get_save_user_memory(self, mock_Binary, mock_pickle, mock_memories):
        mock_memory = ConversationBufferWindowMemory(k=4, memory_key='chat_history', return_messages=False)
        mock_memories.find_one.return_value = {'memory': b'test_memory'}
        mock_pickle.loads.return_value = mock_memory
        mock_pickle.dumps.return_value = b'pickled_memory'
        mock_Binary.return_value = b'binary_memory'
        
        memory = get_user_memory('test_user')
        self.assertEqual(memory, mock_memory)

        save_user_memory('test_user', mock_memory)
        mock_memories.update_one.assert_called_once()

class TestUser(unittest.TestCase):
    def test_user_init(self):
        user = User('test_user')
        self.assertEqual(user.user_id, 'test_user')
        self.assertIsNone(user.memory)

    @patch('User.get_user_memory')
    @patch('User.save_user_memory')
    @patch('langchain.chains.ConversationChain.run')
    @patch('User.get_openai_callback')
    def test_ask_question(self, mock_callback, mock_run, mock_save_memory, mock_get_memory):
        mock_memory = ConversationBufferWindowMemory(k=4, memory_key='chat_history', return_messages=False)
        mock_get_memory.return_value = mock_memory
        mock_run.return_value = 'test_response'
        mock_cb = MagicMock()
        mock_cb.total_tokens = 100
        mock_callback.return_value.__enter__.return_value = mock_cb

        user = User('test_user')
        response = user.ask_question('Hello')

        self.assertEqual(response, 'test_response')
        mock_get_memory.assert_called_once_with('test_user')
        mock_save_memory.assert_called_once_with('test_user', mock_memory)
        mock_run.assert_called_once()
        self.assertEqual(mock_run.call_args[1]['input'], 'Hello')
        self.assertEqual(user.memory, mock_memory)

class TestChatbot(unittest.TestCase):
    @patch('Chatbot.MongoClient')
    def setUp(self, mock_mongo):
        self.chatbot = Chatbot()
        self.mock_db = mock_mongo.return_value[unittest.mock.ANY]
        self.chatbot.collection = self.mock_db['users']

    def test_create_get_delete_user(self):
        self.chatbot.create_user('test_user')
        self.chatbot.collection.insert_one.assert_called_once_with({'user_id': 'test_user'})

        self.chatbot.collection.find_one.return_value = {'user_id': 'test_user'}
        user = self.chatbot.get_user('test_user')
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id, 'test_user')

        self.chatbot.delete_user('test_user')
        self.chatbot.collection.delete_one.assert_called_once_with({'user_id': 'test_user'})

if __name__ == '__main__':
    unittest.main()