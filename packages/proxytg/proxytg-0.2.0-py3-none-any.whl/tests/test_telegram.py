import os
import time
import unittest
import yaml
from proxytg.telegram import TelegramAccount


class TestTelegramAccount(unittest.TestCase):

    def test_login(self):
        obj = TelegramAccount("account", "sss", "http://localhost:4444/wd/hub")
        time.sleep(200)


if __name__ == '__main__':
    unittest.main()
