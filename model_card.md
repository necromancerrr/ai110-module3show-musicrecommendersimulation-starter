# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatcher 1.0**

A content-based music recommender that scores songs by proximity to a user's stated mood, energy, and acoustic preferences.

---

## 2. Intended Use  

VibeMatcher generates personalized music recommendations for listeners based on four preference inputs: favorite genre, desired mood, target energy level, and preference for acoustic vs. electronic texture. 

**Who it's for:** Classroom simulation to demonstrate how streaming platforms think about matching music to listeners. **Not for real users.**

**Key assumptions:** 
- Users can clearly articulate their mood preference
- Energy level is a good proxy for intensity across all genres
- Mood is more important than genre (35% of score)
- A small catalog (18 songs) is sufficient to test the logic

---

## 3. How the Model Works  

Imagine you tell a friend: "I want something chill, with acoustic guitar, around energy 0.4, in the lofi genre." The recommender treats this like a shopping list and scores every song by checking:

1. **Does the mood match?** (+1.40 points for exact match, 0 otherwise)
2. **How close is the energy?** (Up to +1.20 points — a song at energy 0.38 when you want 0.38 gets more than one at 0.80)
3. **Is it acoustic or electronic like you prefer?** (Up to +0.80 points for proximity, +0.20 bonus if it's clearly the right texture)
4. **Is it the right genre?** (+0.40 points for match — a soft signal, not a gate)

Each song gets a score 0.0 to 4.0. The recommender sorts all songs by score and shows you the top 5.

**Key design choice:** Mood is the heaviest signal because listeners often say "I want something *chill*" more than "I want something *by RÜFÜS DU SOL*" — context beats genre.

---

## 4. Data  

**Catalog:** 18 songs (expanded from 10 starter tracks)

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, hip-hop, r&b, metal, classical, reggae, electronic, soul (15 total)

**Moods represented:** happy, chill, intense, relaxed, focused, moody, nostalgic, uplifting, sad, angry, peaceful, dreamy, romantic (13 total)

**Notable gaps:** 
- Only 1 song per unique mood (happy, sad, peaceful, nostalgic, etc.) — limits variety for users seeking those moods
- No K-pop, country, blues, or spiritual genres
- Energy range: 0.21–0.97 (good spread)
- Acousticness range: 0.05–0.98 (excellent coverage)

**Data was curated** to include underrepresented genres and moods missing from the starter set, but the small size remains a key limitation.

---

## 5. Strengths  

✅ **Genre-flexible matching:** A classical lover recommending peaceful mood gets ambient tracks too, not just classical. The energy/mood match matters more than genre purity.

✅ **Energy proximity works:** Two songs of the same genre but different energy (e.g., gentle folk vs. upbeat folk) are correctly differentiated. The recommender rewards *closeness*, not *extremes*.

✅ **Acoustic texture is captured:** Users can clearly separate organic (high acousticness) from electronic (low acousticness) recommendations. A person saying "I want acoustic" reliably gets 0.60+ acousticness songs.

✅ **Explanations are clear:** Each recommendation includes specific reasons (mood match, energy gap, acoustic texture), making results interpretable.

✅ **Works well for "typical" listeners:** High-energy pop dancers, chill lofi fans, intense rock fans, peaceful classical listeners all get sensible top-1 recommendations that match their profile exactly.

---

## 6. Limitations and Bias 

🔴 **Mood over-dominance creates filter bubbles:** The heaviest signal (1.40 points for mood match, 35% of total score) means a listener seeking "sad" music is almost guaranteed to get the only sad song in the catalog, even if other songs match all their other preferences better. This is less serendipity, more "take what we have."

**Real-world impact:** If you use mood as your primary signal, you artificially limit cross-genre discovery. A person who wants "sad jazz" but there's only "sad r&b" available will get r&b instead of a sad jazz song, even if that jazz track exists but has a different mood tag.

🔴 **Genre as soft weight, not a signal:** To avoid hard filtering, genre only adds 0.40 points (10% of score). This means pop listeners often see indie pop, synthwave fans see electronic, and rock fans see metal—all "close enough" substitutes. Some users may find this discovery-positive; others may find it confusing.

**Real-world impact:** If I say "I only like rock," I'm probably not looking for metal suggestions, but the recommender treats them almost equivalently after energy/mood matching.

🔴 **Small catalog breaks the model:** With only 1 "peaceful" and 1 "sad" song, a peaceful listener gets a 3.81 score for the only match, then a dramatic cliff to 2.07 for unrelated substitutes. In a real catalog with thousands of peaceful songs, the top 5 would all be peaceful—here, you get forced diversity through scarcity, not by design.

🔴 **Mood labels are absolute, not continuous:** "Happy" and "uplifting" are semantically close but scored as completely different (0 or 1.40 points). A song tagged "uplifting" never gets partial credit toward a "happy" preference. Real systems use mood embeddings or hierarchies to capture these relationships.

🔴 **No context awareness:** Static preference profile means the same recommendations every time. In reality, you might want "calm" at midnight and "energetic" at 6 AM. This recommender gives the same answer always.

---

## 7. Evaluation  

**Profiles tested (5 total):**
1. Chill Lofi Listener (baseline)
2. High-Energy Pop Dancer
3. Intense Rock Headbanger
4. Peaceful Classical Listener
5. Conflicting Preferences (sad + high energy) — edge case

**Observations:**

| Profile | Top Result | Verdict |
|---|---|---|
| Chill Lofi | Library Rain (3.92/4.00) matching on all axes | ✅ Perfect — mood + genre + energy + acoustic all match |
| Pop Dancer | Sunrise City (3.95/4.00) matching on all axes | ✅ Perfect — high energy + happy mood dominate |
| Rock Fan | Storm Runner (3.91/4.00) matching on all axes | ✅ Perfect — but note: Gym Hero ranks 2nd despite mood mismatch, shows energy can overcome |
| Classical Fan | String Quartet (3.81/4.00) perfect match | ✅ Works, but 1.74-point drop to 2nd shows isolation |
| Edge Case: Sad + High Energy | Broken Clocks (2.74/4.00) sad but low energy | 🔴 PROBLEM — mood (1.40 pts) beat energy need; user gets low-energy sad songs instead |

**Surprise discovery:** The edge case revealed that conflicting preferences are mishandled. A user who tags "sad" mood + "0.95" energy wants something contradictory (uncommon but real — think industrial metal or aggressive electronic). Instead of searching for high-energy hard songs that *feel* sad/moody, the recommender defaults to sad songs regardless of energy, wasting the high-energy need.

**Verdict:** System works well for "aligned" preferences (happy + high energy, calm + low energy) but struggles with conflicting signals or rare mood tags.

---

## 8. Future Work  

**Short-term improvements:**
- Add mood similarity Matrix: treat "happy" and "uplifting" as semantically close, not binary
- Implement session context: time of day, device, recent activity
- Add diversity constraint: don't recommend the same artist twice in top 5

**Medium-term:**
- Expand catalog to 500+ songs to reduce filter bubble effects by sheer numbers
- Add hybrid: mix content-based (what we have) with collaborative filtering (what similar users liked)
- Implement conflict resolution: when energy and mood contradict, weight the user's most recent signal

**Long-term:**
- Use neural embeddings to learn mood similarity from data rather than hard-coding it
- Add explainability for negative recommendations: "We didn't pick X because..."
- Build A/B test framework to measure user satisfaction vs. algorithmic precision

---

## 9. Personal Reflection  

**What I learned:** Recommender systems are deceptively complex because preferences are multi-dimensional and often contradictory. A single weight change (mood from 1.40 to 1.0) cascades through the entire ranking. The edge case of conflicting preferences taught me that systems need to be designed for *realistic* user behavior, not just the happy path.

**Surprise:** I expected genre to be the strongest signal (people usually say "I want blues" or "I want indie"). Instead, I found that mood—something less explicit in how people talk—was much more predictive of satisfaction. This mirrors what Spotify research shows: "What do you want to feel right now?" beats "What's your favorite genre?"

**How this changed my thinking:** Recommender systems aren't neutral. By choosing mood as 35% of the score, I created a world where mood matters more than anything else. That's a design decision with real consequences for users with rare mood preferences or complex emotional states. Real systems like Spotify solve this with *billions* of interactions; here, I see how a small dataset and simple weights can accidentally create filter bubbles for edge cases.
