"""
Command line runner for the Music Recommender Simulation.

This file tests the recommender with multiple user profiles to evaluate
system accuracy, identify biases, and stress-test edge cases.
"""

from src.recommender import load_songs, recommend_songs


def format_recommendations(user_name: str, user_prefs: dict, recommendations: list) -> None:
    """
    Format and display recommendations with visual scoring bars.

    Args:
        user_name: Profile name for display
        user_prefs: User preference dictionary
        recommendations: List of (song, score, explanation) tuples
    """
    print("\n" + "=" * 90)
    print(f"🎵 PROFILE: {user_name}")
    print("=" * 90)
    print(f"\n📊 Preferences:")
    print(f"   • Genre: {user_prefs['genre']}")
    print(f"   • Mood: {user_prefs['mood']}")
    print(f"   • Energy: {user_prefs['energy']}")
    print(f"   • Acoustic: {'Yes ✓' if user_prefs.get('likes_acoustic', False) else 'No ✗'}")

    print(f"\n📈 Top 5 Recommendations:\n")

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        score_pct = (score / 4.0) * 100
        score_bar = "█" * int(score_pct / 5) + "░" * (20 - int(score_pct / 5))

        print(f"{rank}. {song['title']}")
        print(f"   {song['artist']} | {song['genre']} | {song['mood']} | Energy: {song['energy']}")
        print(f"   Score: {score:.2f}/4.00  [{score_bar}] {score_pct:.0f}%")
        print(f"   → {explanation[:100]}...")
        print()


def main() -> None:
    """
    Load songs and test recommender against diverse user profiles.
    """
    songs = load_songs("data/songs.csv")

    # Define test profiles: baseline + stress tests
    profiles = {
        "Chill Lofi Listener (Baseline)": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "likes_acoustic": True,
        },
        "High-Energy Pop Dancer": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "likes_acoustic": False,
        },
        "Intense Rock Headbanger": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.90,
            "likes_acoustic": False,
        },
        "Peaceful Classical Listener": {
            "genre": "classical",
            "mood": "peaceful",
            "energy": 0.25,
            "likes_acoustic": True,
        },
        "Conflicting Preferences (Edge Case)": {
            # Energy 0.95 (very high) but mood "sad" (usually low valence)
            # Tests how competing signals are weighted
            "genre": "metal",
            "mood": "sad",
            "energy": 0.95,
            "likes_acoustic": False,
        },
    }

    # Run recommender for each profile
    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        format_recommendations(profile_name, user_prefs, recommendations)

    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
