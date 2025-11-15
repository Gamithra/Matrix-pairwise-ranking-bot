"""Elo rating system for pairwise comparisons."""

import math
from typing import Tuple


class EloRanking:
    """Elo rating system implementation."""
    
    def __init__(self, k_factor: float = 32.0):
        """
        Initialize Elo ranking system.
        
        Args:
            k_factor: The K-factor determines how much ratings change after each match.
                     Higher values mean more volatile ratings.
                     Default 32 is standard for most systems.
        """
        self.k_factor = k_factor
    
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        """
        Calculate the expected score for player A.
        
        Returns a value between 0 and 1 representing the probability
        that A will beat B.
        
        Args:
            rating_a: Current Elo rating of player A
            rating_b: Current Elo rating of player B
            
        Returns:
            Expected score (probability of A winning)
        """
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))
    
    def update_ratings(self, rating_a: float, rating_b: float, 
                      a_won: bool) -> Tuple[float, float]:
        """
        Update ratings after a match.
        
        Args:
            rating_a: Current Elo rating of player A
            rating_b: Current Elo rating of player B
            a_won: True if A won, False if B won
            
        Returns:
            Tuple of (new_rating_a, new_rating_b)
        """
        expected_a = self.expected_score(rating_a, rating_b)
        expected_b = 1.0 - expected_a
        
        # Actual scores (1 for win, 0 for loss)
        score_a = 1.0 if a_won else 0.0
        score_b = 0.0 if a_won else 1.0
        
        # Update ratings
        new_rating_a = rating_a + self.k_factor * (score_a - expected_a)
        new_rating_b = rating_b + self.k_factor * (score_b - expected_b)
        
        return new_rating_a, new_rating_b
    
    def rating_difference_to_win_probability(self, rating_diff: float) -> float:
        """
        Convert a rating difference to win probability.
        
        Args:
            rating_diff: Rating of A minus rating of B
            
        Returns:
            Probability that A beats B (0 to 1)
        """
        return 1.0 / (1.0 + math.pow(10, -rating_diff / 400.0))
