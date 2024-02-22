# testServer.py
# By: Sam Schmitz, Gavin Roy
# tests server.py

import unittest
from unittest.mock import (MagicMock, patch)

import sb.server

def querySideEffect(query):
    pass

class testServer(unittest.TestCase):
    
    @patch(sb.server.sqlite3)
    
    def setUp(self, mock_sqlite3):
        # set up the mock of sqlite3.connection
        self.connection_mock = MagicMock()
        # set up the cursor mock
        self.cursor_mock = MagicMock()
        self.cursor_mock.query.side_effect = querySideEffect
        
        # set the mocks to the patch
        self.connection_mock.cursor.return_value = self.cursor_mock
        mock_sqlite3.connect.return_value = self.connection_mock
