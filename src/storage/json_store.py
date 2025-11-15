"""JSON-based storage for the Planter bot."""

import json
import os
from typing import List, Dict, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime
import uuid
import asyncio

from .models import Plandidate, Vote, UserVotingSession


class JSONStore:
    """Simple JSON file-based storage."""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.plandidates_file = self.data_dir / "plandidates.json"
        self.votes_file = self.data_dir / "votes.json"
        self.user_votes_file = self.data_dir / "user_votes.json"
        self.sessions_file = self.data_dir / "sessions.json"
        
        # Locks to prevent concurrent file access
        self._plandidates_lock = asyncio.Lock()
        self._votes_lock = asyncio.Lock()
        self._user_votes_lock = asyncio.Lock()
        self._sessions_lock = asyncio.Lock()
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Create empty JSON files if they don't exist."""
        if not self.plandidates_file.exists():
            self._write_json(self.plandidates_file, [])
        if not self.votes_file.exists():
            self._write_json(self.votes_file, [])
        if not self.user_votes_file.exists():
            self._write_json(self.user_votes_file, {})
        if not self.sessions_file.exists():
            self._write_json(self.sessions_file, {})
    
    def _read_json(self, file_path: Path) -> any:
        """Read and parse JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _write_json(self, file_path: Path, data: any):
        """Write data to JSON file atomically."""
        # Write to a temporary file first, then rename (atomic operation)
        temp_file = file_path.with_suffix('.tmp')
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
            # Atomic rename
            temp_file.replace(file_path)
        except Exception as e:
            # Clean up temp file on error
            if temp_file.exists():
                temp_file.unlink()
            raise e
    
    # Plandidate operations
    
    def add_plandidate(self, name: str, added_by: str) -> Plandidate:
        """Add a new plandidate."""
        plandidates = self._read_json(self.plandidates_file)
        
        # Check if plandidate with same name already exists
        for p in plandidates:
            if p['name'].lower() == name.lower():
                return Plandidate.from_dict(p)
        
        plandidate = Plandidate(
            id=str(uuid.uuid4()),
            name=name,
            added_by=added_by,
            added_at=datetime.now().isoformat()
        )
        
        plandidates.append(plandidate.to_dict())
        self._write_json(self.plandidates_file, plandidates)
        
        return plandidate
    
    def get_all_plandidates(self) -> List[Plandidate]:
        """Get all plandidates."""
        plandidates_data = self._read_json(self.plandidates_file)
        return [Plandidate.from_dict(p) for p in plandidates_data]
    
    def get_plandidate_by_id(self, plandidate_id: str) -> Optional[Plandidate]:
        """Get a specific plandidate by ID."""
        plandidates = self.get_all_plandidates()
        for p in plandidates:
            if p.id == plandidate_id:
                return p
        return None
    
    def update_plandidate_elo(self, plandidate_id: str, new_elo: float):
        """Update a plandidate's Elo rating."""
        plandidates = self._read_json(self.plandidates_file)
        
        for p in plandidates:
            if p['id'] == plandidate_id:
                p['elo'] = new_elo
                p['votes_count'] = p.get('votes_count', 0) + 1
                break
        
        self._write_json(self.plandidates_file, plandidates)
    
    def get_plandidates_sorted_by_elo(self) -> List[Plandidate]:
        """Get all plandidates sorted by Elo rating (highest first)."""
        plandidates = self.get_all_plandidates()
        return sorted(plandidates, key=lambda p: p.elo, reverse=True)
    
    # Vote operations
    
    def record_vote(self, user_id: str, plandidate_a_id: str, 
                   plandidate_b_id: str, winner_id: str) -> Vote:
        """Record a pairwise vote."""
        votes = self._read_json(self.votes_file)
        
        vote = Vote(
            user_id=user_id,
            plandidate_a_id=plandidate_a_id,
            plandidate_b_id=plandidate_b_id,
            winner_id=winner_id,
            timestamp=datetime.now().isoformat()
        )
        
        votes.append(vote.to_dict())
        self._write_json(self.votes_file, votes)
        
        # Update user votes tracking
        self._add_user_vote(user_id, plandidate_a_id, plandidate_b_id)
        
        return vote
    
    def get_all_votes(self) -> List[Vote]:
        """Get all votes."""
        votes_data = self._read_json(self.votes_file)
        return [Vote.from_dict(v) for v in votes_data]
    
    # User vote tracking
    
    def _add_user_vote(self, user_id: str, plandidate_a_id: str, plandidate_b_id: str):
        """Mark that a user has voted on this pair."""
        user_votes = self._read_json(self.user_votes_file)
        
        if user_id not in user_votes:
            user_votes[user_id] = []
        
        # Store as sorted pair to ensure consistency
        pair = tuple(sorted([plandidate_a_id, plandidate_b_id]))
        if pair not in [tuple(p) for p in user_votes[user_id]]:
            user_votes[user_id].append(list(pair))
        
        self._write_json(self.user_votes_file, user_votes)
    
    def get_user_voted_pairs(self, user_id: str) -> Set[Tuple[str, str]]:
        """Get all pairs a user has voted on."""
        user_votes = self._read_json(self.user_votes_file)
        
        if user_id not in user_votes:
            return set()
        
        return {tuple(pair) for pair in user_votes[user_id]}
    
    # Session management
    
    def save_session(self, session: UserVotingSession):
        """Save a user's voting session."""
        sessions = self._read_json(self.sessions_file)
        sessions[session.user_id] = session.to_dict()
        self._write_json(self.sessions_file, sessions)
    
    def get_session(self, user_id: str) -> Optional[UserVotingSession]:
        """Get a user's voting session."""
        sessions = self._read_json(self.sessions_file)
        
        if user_id in sessions:
            return UserVotingSession.from_dict(sessions[user_id])
        
        return None
    
    def clear_session(self, user_id: str):
        """Clear a user's voting session."""
        sessions = self._read_json(self.sessions_file)
        
        if user_id in sessions:
            del sessions[user_id]
            self._write_json(self.sessions_file, sessions)
    
    # Reset operations
    
    def reset_all(self):
        """Reset everything: delete all plandidates, votes, and user vote history."""
        self._write_json(self.plandidates_file, [])
        self._write_json(self.votes_file, [])
        self._write_json(self.user_votes_file, {})
        self._write_json(self.sessions_file, {})
    
    def reset_rankings(self):
        """Reset all Elo rankings and votes, but keep the plandidates."""
        # Reset all plandidates to default Elo
        plandidates = self._read_json(self.plandidates_file)
        for p in plandidates:
            p['elo'] = 1500.0
            p['votes_count'] = 0
        self._write_json(self.plandidates_file, plandidates)
        
        # Clear all votes and user vote history
        self._write_json(self.votes_file, [])
        self._write_json(self.user_votes_file, {})
        self._write_json(self.sessions_file, {})
