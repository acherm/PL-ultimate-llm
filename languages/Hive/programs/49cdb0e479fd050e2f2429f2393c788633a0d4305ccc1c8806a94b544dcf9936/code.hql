CREATE TABLE docs (line STRING);

CREATE TABLE word_counts AS
SELECT word, count(1) AS count
FROM (
  SELECT explode(split(line, '\s+')) AS word
  FROM docs
) w
GROUP BY word
ORDER BY word;

SELECT * FROM word_counts LIMIT 10;
