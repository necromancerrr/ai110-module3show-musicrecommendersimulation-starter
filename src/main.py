"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """
    Load songs from CSV, score them against a user profile, and display
    ranked recommendations with explanations in a formatted CLI output.
    """
    songs = load_songs("data/songs.csv")

    # Taste profile: chill, acoustic, low-energy listener
    user_prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
        "target_valence": 0.60,
        "target_danceability": 0.58,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Format output with clear visual hierarchy
    print("\n" + "=" * 80)
    print("🎵 MUSIC RECOMMENDER SIMULATION")
    print("=" * 80)
    print(f"\n📊 User Profile:")
    print(f"   • Favorite Genre: {user_prefs['genre']}")
    print(f"   • Favorite Mood: {user_prefs['mood']}")
    print(f"   • Target Energy: {user_prefs['energy']}")
    print(f"   • Prefers Acoustic: {'Yes ✓' if user_prefs['likes_acoustic'] else 'No ✗'}")

    print(f"\n📈 Top {len(recommendations)} Recommendations:\n")

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        score_pct = (score / 4.0) * 100  # Normalize to 0-100
        score_bar = "█" * int(score_pct / 5) + "░" * (20 - int(score_pct / 5))

        print(f"{rank}. {song['title']}")
        print(f"   Artist: {song['artist']} | Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.2f}/4.00  [{score_bar}] {score_pct:.0f}%")
        print(f"   Why:   {explanation}")
        print()

    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
