# Reddit Post Analysis — NLP on r/AskReddit

## The question

r/AskReddit is one of the largest subreddits on the site, and its front page turns over
constantly. I wanted to know whether there was any structure to what surfaced there:
do the posts that rise cluster into recognizable types, and is there a sentiment
signature to them, or is it mostly noise?

## Approach

Pulled the top 100 posts from r/AskReddit's `hot` listing via the Reddit API (OAuth
password grant), capturing title, body, author, timestamp, upvotes, downvotes, and
comment count.

Pipeline:

1. **Cleaning** — deduplicated on title and body, stripped punctuation
2. **Preprocessing** — tokenization, stopword removal, stemming (Porter) and
   lemmatization (WordNet) via NLTK
3. **Vectorization** — `CountVectorizer` over post titles
4. **Sentiment** — VADER compound scores per title
5. **Clustering** — K-means, k selected via elbow method
6. **Outlier handling** — removed engagement outliers before clustering so a handful of
   viral posts didn't dominate the cluster centroids

## What I found

**Sentiment is close to neutral by construction.** Mean compound score was 0.067, median
exactly 0.0. The distribution is roughly symmetric with a heavy spike at zero. That makes
sense once you look at the content — r/AskReddit posts are questions, and questions
carry less sentiment loading than statements. This was a useful negative result: sentiment
is not a discriminating feature on this subreddit, and any model built on it would be
fitting noise.

## Limitations and what I'd do differently

- **Sample size is small.** 100 posts from a single API call at a single point in time.
  The `hot` listing is heavily time-weighted, so this is a snapshot, not a distribution.
  Anything conclusive would need repeated collection over weeks.
- **`hot` is not `top`.** Reddit's hot ranking blends recency with score, so this measures
  what's currently visible rather than what ultimately performed well. Sampling `top` with
  a time filter would answer the engagement question more directly.
- **CountVectorizer over TF-IDF.** Raw counts let common words dominate. TF-IDF, or
  sentence embeddings, would give better cluster separation on short text like titles.
- **No train/test split or held-out validation** — this was exploratory analysis, not a
  predictive model.

## Status

Not actively maintained. Reddit moved to paid API access in 2023, and the free tier this
was built against no longer supports the collection volume that would make the analysis
worthwhile.

## Running it

```
pip install numpy pandas requests nltk scikit-learn matplotlib
```

Requires a `pass.txt` in the project directory (gitignored) with three lines:

```
<reddit_password>
<client_id>
<client_secret>
```

Register an app at https://www.reddit.com/prefs/apps to get the client credentials.

Then run `reddit_data_project.ipynb` top to bottom.

## Stack

Python, requests, NLTK (VADER, Porter stemmer, WordNet lemmatizer), scikit-learn
(CountVectorizer, KMeans), pandas, matplotlib
