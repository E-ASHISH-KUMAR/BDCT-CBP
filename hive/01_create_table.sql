-- Hive external table for cleaned/structured social media posts.
-- Adjust LOCATION to the HDFS directory used in your lab.
CREATE EXTERNAL TABLE IF NOT EXISTS social_posts (
  post_id STRING,
  post_date STRING,
  platform STRING,
  text STRING,
  clean_text STRING,
  label STRING,
  entity STRING,
  sentiment STRING,
  score INT,
  positive_terms INT,
  negative_terms INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/student/sentiment/processed'
TBLPROPERTIES ('skip.header.line.count'='1');
