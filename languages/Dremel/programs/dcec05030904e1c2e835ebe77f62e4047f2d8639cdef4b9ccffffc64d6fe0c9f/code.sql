-- Dremel: Nested Data Query Examples
-- Schema: Document table with nested links and name fields

-- Query 1: Find documents with English content
SELECT docid, name.url
FROM Document
WHERE name.language.code = 'en';

-- Query 2: Aggregate access patterns by country
SELECT
  name.language.country,
  COUNT(DISTINCT docid) AS num_docs,
  COUNT(name.url) AS num_urls
FROM Document
WHERE name.language.country IS NOT NULL
GROUP BY name.language.country
ORDER BY num_docs DESC;

-- Query 3: Analyze forward links
SELECT
  docid,
  COUNT(links.forward) AS num_forward_links,
  COUNT(links.backward) AS num_backward_links
FROM Document
GROUP BY docid
HAVING COUNT(links.forward) > 5
ORDER BY num_forward_links DESC;
