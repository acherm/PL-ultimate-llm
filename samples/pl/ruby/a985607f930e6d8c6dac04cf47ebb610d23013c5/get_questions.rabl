collection @questions

attributes :id, :question

child(:answers) do
  attributes :id, :answer, :correct
end

child(:resources) do
  attributes :url, :contains_answer, :media_type, :begin, :end, :article_text
end