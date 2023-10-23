import sys

print(sys.path)
import flask_sqlalchemy
import json
from app import create_app
from flask_testing import TestCase
from config.config import TestingConfig  # Adjust the import path according to your file structure
import pytest

import sys
print(sys.path)

class TestGame(TestCase):

    def create_app(self):
        app = create_app('config.config.TestingConfig')
        return app

    def test_create_game(self):
        response = self.client.post("/create")
        self.assert200(response)
        data = json.loads(response.data.decode())
        self.assertIn('match_id', data)

    def test_make_move(self):
        # Create game first
        response = self.client.post("/create")
        data = json.loads(response.data.decode())
        match_id = data['match_id']

        # Make move
        move_data = {
            'match_id': match_id,
            'player_id': 'X',
            'square': {'x': 1, 'y': 1}
        }
        response = self.client.post("/move", data=json.dumps(move_data), content_type='application/json')
        self.assert200(response)
        data = json.loads(response.data.decode())
        self.assertIn('match_id', data)

    # Add more tests for other scenarios and edge cases

if __name__ == '__main__':
    pytest.main()
