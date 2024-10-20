import unittest
from unittest.mock import patch, MagicMock
from winner import connect_to_db, get_all_prizes, choose_winner, main
import os


class TestScriptMethods(unittest.TestCase):
    @patch("winner.pymongo.MongoClient")
    def test_connect_to_db(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value = mock_db
        db = connect_to_db()
        self.assertEqual(db, mock_db[os.getenv("DB_NAME")])

    @patch("winner.connect_to_db")
    def test_get_all_prizes(self, mock_connect_to_db):
        mock_db = MagicMock()
        mock_connect_to_db.return_value = mock_db
        mock_db["f24-points-syst"].distinct.return_value = [
            "prize-123",
            "prize-456",
            "prize-789",
        ]
        prizes = get_all_prizes(mock_db)
        self.assertEqual(prizes, ["prize-123", "prize-456", "prize-789"])

    @patch("winner.pymongo.MongoClient")
    @patch("winner.random.uniform")
    def test_choose_winner(self, mock_random_uniform, mock_client):
        # Set up mock database and collections
        mock_db = MagicMock()
        mock_client.return_value = mock_db

        mock_points_collection = mock_db["f24-points-syst"]
        mock_users_collection = mock_db["users"]

        # Mock the aggregate response for points collection
        mock_points_collection.aggregate.return_value = [
            {"email": "winner@example.com", "buy_in": 100},
            {"email": "runner-up@example.com", "buy_in": 50},
            {"email": "participant@example.com", "buy_in": 25},
        ]

        # Mock the find_one response for users collection
        mock_users_collection.find_one.side_effect = [
            {
                "first_name": "Winner",
                "last_name": "User",
                "school": "Sample University",
                "major": "Computer Science",
                "registration_status": "Registered",
            },
            {
                "first_name": "Runner-Up",
                "last_name": "User",
                "school": "Sample University",
                "major": "Computer Science",
                "registration_status": "Registered",
            },
            {
                "first_name": "Participant",
                "last_name": "User",
                "school": "Sample University",
                "major": "Computer Science",
                "registration_status": "Registered",
            },
        ]

        # Mock the winning ticket to be within the range of the winner
        mock_random_uniform.return_value = 50  # Adjust accordingly

        # Run the choose_winner function
        winner = choose_winner("prize-123", mock_db)

        # Assert the expected winner's email
        self.assertEqual(winner["email"], "winner@example.com")


if __name__ == "__main__":
    unittest.main()
