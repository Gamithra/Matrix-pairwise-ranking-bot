"""Data models for the ranking bot."""

from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Plandidate:
    """A plan candidate with Elo rating."""
    id: str
    name: str
    elo: float = 1500.0  # Default Elo rating
    votes_count: int = 0  # Number of times this plandidate has been in a comparison
    added_by: Optional[str] = None  # User ID who added it
    added_at: Optional[str] = None  # Timestamp
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Vote:
    """A pairwise vote record."""
    user_id: str
    plandidate_a_id: str
    plandidate_b_id: str
    winner_id: str  # ID of the chosen plandidate
    timestamp: str
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class UserVotingSession:
    """Tracks a user's current voting session in DM."""
    user_id: str
    current_pair: Optional[tuple[str, str]] = None  # (plandidate_a_id, plandidate_b_id)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'current_pair': list(self.current_pair) if self.current_pair else None
        }
    
    @classmethod
    def from_dict(cls, data):
        current_pair = data.get('current_pair')
        if current_pair:
            current_pair = tuple(current_pair)
        return cls(
            user_id=data['user_id'],
            current_pair=current_pair
        )
