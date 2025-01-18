import json

class GameStats:
    """Track stats for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        # High score should never be reset
        self.high_score = self.load_high_score()

    
    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


    def load_high_score(self):
        """Load the high score from a JSON file."""
        try:
            with open('high_score.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0


    def save_high_score(self):
        """Save the high score to a JSON file."""
        with open('high_score.json', 'w') as file:
            json.dump(self.high_score, file)