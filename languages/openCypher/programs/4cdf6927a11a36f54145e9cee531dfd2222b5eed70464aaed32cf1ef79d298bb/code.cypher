// Find all direct friends and friends-of-friends of a person
MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(friend:Person)
OPTIONAL MATCH (friend)-[:KNOWS]->(fof:Person)
WHERE fof <> p AND NOT (p)-[:KNOWS]->(fof)
WITH friend, collect(DISTINCT fof) AS friendsOfFriends
RETURN friend.name AS directFriend,
       [x IN friendsOfFriends | x.name] AS suggestions
ORDER BY friend.name