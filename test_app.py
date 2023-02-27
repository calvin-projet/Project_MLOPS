import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def test_predict(self):
        with app.test_client() as client:
            data = {
                'anime_title': 'Cowboy Bebop: Tengoku no Tobira',
                'anime_genre': ['Action', 'Space', 'Drama', 'Mystery', 'Sci-Fi'],
                'anime_description': 'Another day, another bounty—such is the life of the often unlucky crew of the Bebop. However, this routine is interrupted when Faye, who is chasing a fairly worthless target on Mars, witnesses an oil tanker suddenly explode, causing mass hysteria. As casualties mount due to a strange disease spreading through the smoke from the blast, a whopping three hundred million woolong price is placed on the head of the supposed perpetrator. \n \nWith lives at stake and a solution to their money problems in sight, the Bebop crew springs into action. Spike, Jet, Faye, and Edward, followed closely by Ein, split up to pursue different leads across Alba City. Through their individual investigations, they discover a cover-up scheme involving a pharmaceutical company, revealing a plot that reaches much further than the ragtag team of bounty hunters could have realized. \n \n[Written by MAL Rewrite]',
                'anime_type': 'Movie',
                'anime_producer': ['Sunrise', 'Bandai Visual'],
                'anime_studio': ['Bones']
            }
            response = client.post('/predict', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('rating', response.json)