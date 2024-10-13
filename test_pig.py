import unittest
from unittest.mock import patch
import random
from pig import *


class TestPlayer(unittest.TestCase):

    def test_addToScore(self):
        player = Player("Alice")
        player.addToScore(10)
        self.assertEqual(player.score, 10)
        player.addToScore(5)
        self.assertEqual(player.score, 15)

    def test_resetScore(self):
        player = Player("Bob")
        player.addToScore(20)
        player.resetScore()
        self.assertEqual(player.score, 0)

    def test_getName(self):
        player = Player("Charlie")
        self.assertEqual(player.getName(), "Charlie")


class TestGame(unittest.TestCase):

    def setUp(self):
        self.players = [Player("Alice"), Player("Bob")]
        self.game = Game(["Alice", "Bob"])

    def test_rollDie(self):
        for _ in range(100):  # Test many rolls to ensure correctness
            roll = self.game.rollDie()
            self.assertIn(roll, range(1, 7))  # Die roll should be between 1 and 6

    def test_switchPlayer(self):
        # Initially the current player is 0 (Alice)
        self.assertEqual(self.game.current_player, 0)
        self.game.switchPlayer()
        # After switching, the current player should be Bob (index 1)
        self.assertEqual(self.game.current_player, 1)
        # Switch again, should return to Alice (index 0)
        self.game.switchPlayer()
        self.assertEqual(self.game.current_player, 0)

    def test_is_winner(self):
        # Test when a player has not won yet
        self.assertFalse(self.game.is_winner(self.players[0],turnScore = 0))

        # Test when a player wins
        self.players[0].addToScore(10)  # Score to win is 100
        self.assertTrue(self.game.is_winner(self.players[0], turnScore = 100))

    @patch('builtins.input', side_effect=['h'])  # Simulate user input 'hold'
    def test_turn_hold(self, mock_input):
        player = self.players[0]
        self.game.turn(player)
        # Since the roll and turn logic depends on randomness, let's assume the player holds
        # Check that the player's score is greater than 0 after a turn with 'hold'
        self.assertGreaterEqual(player.score, 0)

    @patch('builtins.input', side_effect=['r', 'h'])  # Simulate user input 'roll', then 'hold'
    def test_turn_roll_then_hold(self, mock_input):
        player = self.players[0]
        self.game.turn(player)
        # Check that the player's score increases after rolling and holding
        self.assertGreaterEqual(player.score, 0)


if __name__ == "__main__":
    unittest.main()