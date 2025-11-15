#!/usr/bin/env python3
"""
Quick example/test of the Elo ranking system.
Run this to see how the ranking algorithm works without needing Matrix setup.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from storage import JSONStore, Plandidate
from ranking import EloRanking, PairSelector

def main():
    print("🌱 Planter Bot - Elo Ranking Example\n")
    
    # Create a temporary store
    store = JSONStore("./example_data")
    elo = EloRanking(k_factor=32.0)
    
    print("📝 Adding example plandidates...")
    plandidates = [
        "Implement user authentication",
        "Add mobile app support",
        "Improve search functionality",
        "Create analytics dashboard",
        "Add dark mode"
    ]
    
    for name in plandidates:
        store.add_plandidate(name, "@example:matrix.org")
        print(f"   ✓ {name}")
    
    print("\n📊 Initial rankings (all at 1500 Elo):")
    for p in store.get_plandidates_sorted_by_elo():
        print(f"   {p.name}: {p.elo:.0f}")
    
    # Simulate some votes
    print("\n🗳️  Simulating some votes...\n")
    
    all_plandidates = store.get_all_plandidates()
    votes = [
        (0, 1, 0),  # User prefers 0 over 1
        (0, 2, 0),  # User prefers 0 over 2
        (1, 2, 2),  # User prefers 2 over 1
        (3, 4, 3),  # User prefers 3 over 4
        (0, 3, 0),  # User prefers 0 over 3
    ]
    
    for a_idx, b_idx, winner_idx in votes:
        a = all_plandidates[a_idx]
        b = all_plandidates[b_idx]
        winner = all_plandidates[winner_idx]
        
        print(f"Vote: '{a.name}' vs '{b.name}'")
        print(f"   → User chose: '{winner.name}'")
        
        # Update Elo
        a_won = (winner_idx == a_idx)
        new_elo_a, new_elo_b = elo.update_ratings(a.elo, b.elo, a_won)
        
        print(f"   Elo changes: {a.elo:.0f} → {new_elo_a:.0f}, {b.elo:.0f} → {new_elo_b:.0f}")
        
        store.update_plandidate_elo(a.id, new_elo_a)
        store.update_plandidate_elo(b.id, new_elo_b)
        store.record_vote("@example:matrix.org", a.id, b.id, winner.id)
        
        # Refresh objects
        all_plandidates = store.get_all_plandidates()
        print()
    
    print("📊 Final rankings:")
    for i, p in enumerate(store.get_plandidates_sorted_by_elo(), 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else "  "
        print(f"{i}. {medal} {p.name}: {p.elo:.0f} Elo ({p.votes_count} votes)")
    
    print("\n✨ This demonstrates how the Elo system ranks plandidates based on comparisons!")
    print("   More wins = higher Elo = higher rank\n")
    
    # Cleanup
    import shutil
    shutil.rmtree("./example_data", ignore_errors=True)

if __name__ == "__main__":
    main()
