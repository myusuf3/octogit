"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import unittest
import mock

from mock import patch, DEFAULT, MagicMock
from stubs import stub_requests, stub_ConfigParser

import octogit.config

class ConfigTest(unittest.TestCase):

    @patch('octogit.config.config', stub_ConfigParser.StubConfigParser())
    @patch('octogit.config.os.makedirs')
    @patch('octogit.config.os.path.exists', MagicMock(return_value=False))
    @patch('__builtin__.open')
    def test_create_config(self, mock_osmakedirs, mock_open):

        result_config = octogit.config.create_config()

        self.assertEqual(result_config.get('octogit', 'username'), '')
        self.assertEqual(result_config.get('octogit', 'token'), '')

        # mock_open.assert_called_once_with(octogit.config.CONFIG_FILE, 'w')

    @patch('octogit.config.config', stub_ConfigParser.StubConfigParser())
    @patch('octogit.config.os.makedirs')
    @patch('octogit.config.os.path.exists', MagicMock(return_value=False))
    @patch('__builtin__.open')
    def test_set_username(self, mock_osmakedirs, mock_open):

        octogit.config.set_username('dummy_user')

        self.assertEqual(octogit.config.config.get('octogit', 'username'), 'dummy_user')
        self.assertEqual(octogit.config.config.was_written, True)

         # mock_open.assert_called_once_with(octogit.config.CONFIG_FILE, 'w')



if __name__ == '__main__':
    unittest.main()
