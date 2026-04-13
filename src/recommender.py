import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# ---------------------------------------------------------------------------
# Scoring weights (additive, max total = 4.0)
# ---------------------------------------------------------------------------
# Mood is weighted highest: context/vibe matters more than genre family.
# Energy proximity is the primary numeric signal (widest spread in catalog).
# Acousticness separates organic/warm from electronic/produced texture.
# Genre is a tiebreaker, not a gate — a great ambient track beats a bad lofi.
# ---------------------------------------------------------------------------
WEIGHT_MOOD        = 1.40  # +1.40 for exact mood match
WEIGHT_ENERGY      = 1.20  # +0.0–1.20 scaled by proximity
WEIGHT_ACOUSTICNESS= 0.80  # +0.0–0.80 scaled by proximity
WEIGHT_GENRE       = 0.40  # +0.40 for exact genre match
WEIGHT_ACOUSTIC_BONUS = 0.20  # +0.20 when acoustic preference is confirmed
# MAX SCORE = 1.40 + 1.20 + 0.80 + 0.40 + 0.20 = 4.00


def score_song(song: Song, user: UserProfile) -> float:
    """
    Scores a single song against a user profile.
    Returns a float between 0.0 and 4.0.

    Algorithm recipe:
      +1.40  mood match (exact string match)
      +0.00–1.20  energy proximity: 1.20 × (1 - |song.energy - user.target_energy|)
      +0.00–0.80  acousticness proximity: 0.80 × (1 - |song.acousticness - acoustic_target|)
      +0.40  genre match (exact string match)
      +0.20  acoustic texture bonus when song and user agree on acoustic vs. electronic
    """
    score = 0.0

    # --- Mood match (categorical, binary) ---
    if song.mood == user.favorite_mood:
        score += WEIGHT_MOOD

    # --- Energy proximity (numeric, continuous) ---
    # Rewards songs whose energy is CLOSEST to the user's target, not simply highest.
    # Example: target=0.38, song=0.35 → proximity=0.97 → contributes 1.16 pts
    #          target=0.38, song=0.91 → proximity=0.47 → contributes 0.56 pts
    energy_proximity = 1.0 - abs(song.energy - user.target_energy)
    score += WEIGHT_ENERGY * energy_proximity

    # --- Acousticness proximity (numeric, continuous) ---
    # Maps user.likes_acoustic to a target value: True → 0.80, False → 0.20
    acoustic_target = 0.80 if user.likes_acoustic else 0.20
    acousticness_proximity = 1.0 - abs(song.acousticness - acoustic_target)
    score += WEIGHT_ACOUSTICNESS * acousticness_proximity

    # --- Genre match (categorical, binary) ---
    if song.genre == user.favorite_genre:
        score += WEIGHT_GENRE

    # --- Acoustic texture bonus (confirms preference direction) ---
    # Adds a small bonus when the song's acousticness clearly matches the user's
    # preference: acoustic lovers get songs with acousticness > 0.6,
    # electronic lovers get songs with acousticness < 0.4.
    song_is_acoustic = song.acousticness > 0.60
    if song_is_acoustic == user.likes_acoustic:
        score += WEIGHT_ACOUSTIC_BONUS

    return score


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Returns the top-k songs sorted by score (highest first).
        Scoring Rule: score_song() rates each song 0.0–4.0.
        Ranking Rule: sort all scores descending, return first k.
        """
        scored = [(song, score_song(song, user)) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Returns a plain-language explanation of why this song was recommended.
        """
        reasons = []

        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches your '{user.favorite_mood}' preference")

        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches your favourite '{user.favorite_genre}'")

        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.15:
            reasons.append(f"energy ({song.energy}) is close to your target ({user.target_energy})")
        elif energy_diff >= 0.40:
            reasons.append(f"energy ({song.energy}) is far from your target ({user.target_energy})")

        if user.likes_acoustic and song.acousticness >= 0.60:
            reasons.append("has the acoustic texture you prefer")
        elif not user.likes_acoustic and song.acousticness <= 0.30:
            reasons.append("has the electronic texture you prefer")

        if not reasons:
            return f"'{song.title}' is a partial match with a score of {score_song(song, user):.2f}/4.00"

        return f"'{song.title}' was recommended because: " + "; ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Converts raw dicts to Song/UserProfile objects, scores and ranks,
    then returns (song_dict, score, explanation) tuples.
    """
    user = UserProfile(
        favorite_genre=user_prefs.get("genre", ""),
        favorite_mood=user_prefs.get("mood", ""),
        target_energy=float(user_prefs.get("energy", 0.5)),
        likes_acoustic=bool(user_prefs.get("likes_acoustic", False)),
    )

    scored = []
    for song_dict in songs:
        song = Song(
            id=song_dict["id"],
            title=song_dict["title"],
            artist=song_dict["artist"],
            genre=song_dict["genre"],
            mood=song_dict["mood"],
            energy=song_dict["energy"],
            tempo_bpm=song_dict["tempo_bpm"],
            valence=song_dict["valence"],
            danceability=song_dict["danceability"],
            acousticness=song_dict["acousticness"],
        )
        s = score_song(song, user)
        # Build a lightweight recommender to reuse explain_recommendation
        rec = Recommender([song])
        explanation = rec.explain_recommendation(user, song)
        scored.append((song_dict, s, explanation))

    scored.sort(key=lambda triple: triple[1], reverse=True)
    return scored[:k]
