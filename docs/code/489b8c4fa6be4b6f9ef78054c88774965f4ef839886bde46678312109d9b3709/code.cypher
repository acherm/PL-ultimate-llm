MATCH (person:Person)-[:RATED]->(m:Movie)
WITH person, count(m) as movies, avg(m.rating) as rating
WHERE movies > 10
MATCH (person)-[:RATED]->(m:Movie)
WITH person, m, CASE
  WHEN m.rating > 4.5 THEN 'loved it'
  WHEN m.rating > 3.5 THEN 'liked it'
  ELSE 'did not like it'
END as opinion
RETURN person.name, 
       count(CASE WHEN opinion = 'loved it' THEN 1 END) as loved,
       count(CASE WHEN opinion = 'liked it' THEN 1 END) as liked,
       count(CASE WHEN opinion = 'did not like it' THEN 1 END) as disliked
ORDER BY person.name