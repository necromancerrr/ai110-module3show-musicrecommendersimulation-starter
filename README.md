# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This simulation builds a content-based music recommender that scores songs against a user's taste profile using weighted feature matching. It prioritizes mood and energy as the primary "vibe" signals, supported by acousticness and genre as texture and style cues. The goal is to recommend songs that feel contextually right — not just popular or generically similar.

---

## How The System Works

Real-world recommenders like Spotify and YouTube use two main strategies: **collaborative filtering** (finding users with similar taste and surfacing what they love) and **content-based filtering** (analyzing the audio attributes of songs to match a listener's established preferences). Production systems combine both, but collaborative filtering requires large amounts of user behavior data that a small simulation cannot replicate. This version focuses on **content-based filtering**: each song is scored purely on how closely its attributes match the user's stated preferences, with no dependency on what other users have done.

This system will prioritize **mood and energy** as the dominant signals — they best capture the "vibe" a listener is seeking in a given context (studying, working out, winding down). Acousticness and genre serve as supporting signals that refine texture and style. All numeric features use a **proximity score** (`1 - |song_value - user_target|`) so that songs closest to the user's target win, rather than songs that are simply louder, faster, or more energetic.

### `Song` features used

| Feature | Type | Role in scoring |
|---|---|---|
| `genre` | `str` | Categorical match — style and instrument family |
| `mood` | `str` | Categorical match — primary vibe signal (weight: 0.35) |
| `energy` | `float` 0.0–1.0 | Proximity to `target_energy` (weight: 0.30) |
| `acousticness` | `float` 0.0–1.0 | Proximity to acoustic preference (weight: 0.20) |
| `valence` | `float` 0.0–1.0 | Emotional positivity — available for future weighting |
| `danceability` | `float` 0.0–1.0 | Rhythmic feel — available for future weighting |
| `tempo_bpm` | `float` | BPM — available for context-specific filtering |

### `UserProfile` fields used

| Field | Type | How it's used |
|---|---|---|
| `favorite_genre` | `str` | Matched against `song.genre` (weight: 0.10) |
| `favorite_mood` | `str` | Matched against `song.mood` (weight: 0.35) |
| `target_energy` | `float` | Proximity score against `song.energy` (weight: 0.30) |
| `likes_acoustic` | `bool` | Maps to acoustic target: 0.8 if True, 0.2 if False (weight: 0.20 + 0.05 bonus) |

### Scoring and ranking

Each song receives a weighted score from 0.0 to 1.0:

```
score = 0.35 × mood_match
      + 0.30 × (1 - |song.energy - user.target_energy|)
      + 0.20 × (1 - |song.acousticness - acoustic_target|)
      + 0.10 × genre_match
      + 0.05 × acoustic_bonus
```

All songs are scored independently, then sorted descending by score. The top `k` results are returned as recommendations.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

