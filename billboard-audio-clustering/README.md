# Billboard Top 100 — Audio Feature Clustering

## The question

Billboard's year-end Hot 100 is a ranking of commercial performance, not of sound. I
wanted to know whether the songs that chart in a given year share measurable audio
characteristics — and whether those characteristics drift over time.

## Approach

Two-stage data collection, then clustering.

**Stage 1 — Scrape Billboard.** `BeautifulSoup` against Billboard's year-end chart pages,
extracting rank, song, and artist per year. Rate-limited with a 3-second delay between
years.

**Stage 2 — Enrich with Spotify.** For each track, search the Spotify Web API by song
title and artist, then pull the audio feature vector: danceability, energy, key, loudness,
mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration,
and time signature.

**Stage 3 — Cluster.** K-means over the audio features, with k chosen using inertia and
silhouette scores.

## Design decisions worth noting

**Artist name cleaning drove match rate from 78% to 98%.** Billboard credits collaborations
as `"Artist A Featuring Artist B"`, `"Artist A X Artist B"`, `"Artist A & Artist B"`, and
several other formats. Spotify's search doesn't handle these well. Splitting on
collaboration separators and querying only the lead artist was the single highest-impact
fix in the pipeline — a 20-point improvement from about ten lines of string handling.

**Search-by-name instead of batch-by-track-ID.** Spotify's audio features endpoint accepts
up to 100 track IDs per request, which would have been far more efficient. I used
name-based search instead because it requires no pre-existing ID mapping, at the cost of
one request per track plus a 10-second sleep for rate limiting. For a larger run, the
right approach is a first pass to resolve IDs, then batched feature requests.

**Errors are flagged, not dropped.** A `spotify_error` boolean marks unmatched tracks
rather than silently discarding them, so the match rate is measurable and failures are
inspectable.

**Batched by year.** The script processes three years at a time and writes to CSV,
so partial runs are recoverable and datasets can be concatenated later rather than
re-scraping.

## Limitations

- Rate limiting makes full runs slow — roughly 10 seconds per track
- Spotify's audio features are model-derived, not ground truth; `danceability` and
  `valence` in particular are opaque
- Features aren't standardized before K-means, so high-variance features like `tempo`
  and `duration_ms` carry disproportionate weight in the distance calculation. Scaling
  would be the first fix.
- Matching by name will mis-resolve remasters, live versions, and covers

## Running it

```
pip install requests beautifulsoup4 pandas spotipy
```

Set `CLIENT_ID` and `CLIENT_SECRET` in `Audio_features_billboard.py` — register an app at
https://developer.spotify.com/dashboard to get them. Edit the `years` list to pick which
charts to pull, then:

```
python Audio_features_billboard.py
```

Output writes to CSV in the working directory. `Billboard Analysis.html` contains the
clustering analysis and figures.

## Stack

Python, BeautifulSoup, requests, spotipy, pandas, scikit-learn
