# test_auto_messenger.py
import unittest
from AutoMessenger.auto_messenger import AutoMessenger

class TestAutoMessenger(unittest.TestCase):
    def test_message_loading(self):
        messenger = AutoMessenger(external_messages=["Test"])
        self.assertIn("Test", messenger.messages)

if __name__ == '__main__':
    unittest.main()
