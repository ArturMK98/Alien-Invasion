import json

class GameStats:
    """Track stats for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        # High scores should never be reset
        self.high_scores = self.load_high_scores()

    
    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.settings.alien_height = 70
        self.settings.alien_width = 70

    def load_high_scores(self):
        """Load the high scores from a JSON file."""
        try:
            with open('high_scores.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'easy': 0, 'medium': 0, 'hard': 0}


    def save_high_scores(self):
        """Save the high score to a JSON file."""
        with open('high_scores.json', 'w') as file:
            json.dump(self.high_scores, file)