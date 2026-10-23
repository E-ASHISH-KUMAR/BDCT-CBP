-- 1. Overall sentiment distribution
SELECT sentiment, COUNT(*) AS post_count
FROM social_posts
GROUP BY sentiment
ORDER BY post_count DESC;

-- 2. Sentiment by platform
SELECT platform, sentiment, COUNT(*) AS post_count
FROM social_posts
GROUP BY platform, sentiment
ORDER BY platform, sentiment;

-- 3. Daily sentiment trend (the Kaggle source has no dates, so this is empty until dates are supplied)
SELECT post_date, sentiment, COUNT(*) AS post_count
FROM social_posts
WHERE post_date <> ''
GROUP BY post_date, sentiment
ORDER BY post_date, sentiment;

-- 4. Compare predicted sentiment with the Kaggle dataset labels
SELECT label, sentiment, COUNT(*) AS records
FROM social_posts
GROUP BY label, sentiment
ORDER BY label, sentiment;

-- 5. Sentiment by subject entity
SELECT entity, sentiment, COUNT(*) AS post_count
FROM social_posts
GROUP BY entity, sentiment
ORDER BY entity, sentiment;
