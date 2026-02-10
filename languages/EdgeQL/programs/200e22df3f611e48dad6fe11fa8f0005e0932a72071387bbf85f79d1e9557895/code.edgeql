select Movie {
  title,
  year,
  rating,
  director: {
    name
  },
  actors: {
    name
  }
}
filter .year > 2000 and .rating > 7.5
order by .rating desc
limit 10;
