"""Logic for selecting pairs for users to vote on."""

import random
from typing import List, Optional, Tuple, Set

from storage.models import RankedItem


class PairSelector:
    """Selects pairs of items for users to compare."""
    
    @staticmethod
    def get_next_pair(items: List[RankedItem], 
                     voted_pairs: Set[Tuple[str, str]]) -> Optional[Tuple[RankedItem, RankedItem]]:
        """
        Get the next pair of items for a user to vote on.
        
        Strategy:
        1. Find all pairs the user hasn't voted on yet
        2. Prioritize pairs with similar Elo ratings (more informative)
        3. Return None if user has voted on all pairs
        
        Args:
            items: List of all items
            voted_pairs: Set of (id_a, id_b) tuples the user has already voted on
            
        Returns:
            Tuple of two RankedItem objects, or None if no pairs remain
        """
        if len(items) < 2:
            return None
        
        # Find all unvoted pairs
        unvoted_pairs = []
        
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                p_a, p_b = items[i], items[j]
                pair_key = tuple(sorted([p_a.id, p_b.id]))
                
                if pair_key not in voted_pairs:
                    elo_diff = abs(p_a.elo - p_b.elo)
                    unvoted_pairs.append((p_a, p_b, elo_diff))
        
        if not unvoted_pairs:
            return None
        
        # Sort by Elo difference (prefer closer matches for more informative comparisons)
        unvoted_pairs.sort(key=lambda x: x[2])
        
        # Take one of the top 3 closest matches (adds some randomness)
        top_pairs = unvoted_pairs[:min(3, len(unvoted_pairs))]
        selected = random.choice(top_pairs)
        
        return (selected[0], selected[1])
    
    @staticmethod
    def get_random_pair(items: List[RankedItem]) -> Optional[Tuple[RankedItem, RankedItem]]:
        """
        Get a random pair of items.
        
        Args:
            items: List of all items
            
        Returns:
            Tuple of two random RankedItem objects, or None if not enough items
        """
        if len(items) < 2:
            return None
        
        pair = random.sample(items, 2)
        return (pair[0], pair[1])
    
    @staticmethod
    def count_remaining_pairs(num_items: int, num_voted: int) -> int:
        """
        Calculate how many pairs remain for a user to vote on.
        
        Args:
            num_items: Total number of items
            num_voted: Number of pairs the user has already voted on
            
        Returns:
            Number of remaining pairs
        """
        if num_items < 2:
            return 0
        
        total_pairs = (num_items * (num_items - 1)) // 2
        return total_pairs - num_voted
