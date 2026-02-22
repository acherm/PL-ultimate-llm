-- Retrieve authors with their published books count
-- and average rating, for books published after 2000

SELECT a.name,
       COUNT(b) AS bookCount,
       AVG(b.rating) AS avgRating,
       MAX(b.publicationYear) AS latestBook
FROM Author a
JOIN a.books b
WHERE b.publicationYear > 2000
  AND b.rating IS NOT NULL
GROUP BY a.id, a.name
HAVING COUNT(b) >= 3
   AND AVG(b.rating) > 4.0
ORDER BY avgRating DESC, bookCount DESC