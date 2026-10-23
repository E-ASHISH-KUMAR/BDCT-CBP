# Social Media Sentiment Analysis — Big Data Computing Technologies Lab

## Project overview
This project demonstrates an end-to-end sentiment analytics pipeline over labelled tweets. It cleans text, predicts sentiment using a transparent rule-based lexicon, aggregates sentiment counts by platform and subject entity, and displays the results in a browser dashboard.

**Data source:** `data/social_posts.csv` is based on Kaggle's [Twitter Sentiment Analysis dataset](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis), published by passionate-nlp under the CC0: Public Domain license. It contains 61,810 non-empty posts with positive, neutral, or negative labels, selected from the dataset's training and validation CSVs. Rows labelled “Irrelevant” and rows without text are excluded. The source has no post dates, so `post_date` is blank; `platform` is set to Twitter and the source subject is retained in `entity`. These are existing dataset labels, not new annotations or a representative sample of all public opinion.

## Components
- `src/preprocess_and_analyze.py`: dependency-free local pipeline; cleans text, applies lexicon scoring, computes metrics by sentiment, platform, and entity, and writes CSV/JSON outputs.
- `hadoop/mapper.py`, `hadoop/reducer.py`: Hadoop Streaming mapper/reducer for distributed aggregation.
- `hive/01_create_table.sql`, `hive/02_analysis_queries.sql`: Hive table and example analytical queries.
- `dashboard/index.html`: dashboard that reads `../outputs/summary.json` when served from the project root, or you can open it after copying summary data beside it.
- `data/social_posts.csv`: 61,810 labelled posts derived from the Kaggle dataset above.
- `outputs/`: generated results.

## Run locally (Mac/Linux/Windows with Python 3)
From the project root:
```bash
python3 src/preprocess_and_analyze.py
python3 -m http.server 8000
```
Open `http://localhost:8000/dashboard/`. No third-party Python packages are required.

## Data schema
`post_id`, `post_date`, `platform`, `text`, `label`, `entity`. `post_date` is blank because the source does not provide dates. `label` is the Kaggle dataset label; predicted `sentiment` is derived from the text.

## Method
1. Load CSV and validate required columns.
2. Normalize text to lowercase and remove URLs, mentions, punctuation, and repeated whitespace.
3. Score positive and negative terms with a small lexicon; a simple negation rule flips the next sentiment term.
4. Classify as positive, negative, or neutral.
5. Aggregate by sentiment, platform, and entity and export results.
6. Visualize totals and entity distribution.

## Limitations
Rule-based sentiment analysis misses sarcasm, context, slang, multilingual text, emojis, and domain-specific meanings. The lexicon is intentionally small for explainability; its agreement with the dataset labels is only a baseline and should not be presented as model quality. This dataset contains tweets about specific entities and is not representative of all social media users. Social media collection must follow platform terms, privacy rules, and applicable law.
