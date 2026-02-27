search = (keyword, cb) ->
  host = "http://search.twitter.com/"
  url = "#{host}/search.json?q=#{keyword}&callback=?"
  await $.getJSON url, defer json
  cb json.results

parallelSearch = (keywords, cb) ->
  out = []
  await
    for k,i in keywords
      search k, defer out[i]
  cb out
