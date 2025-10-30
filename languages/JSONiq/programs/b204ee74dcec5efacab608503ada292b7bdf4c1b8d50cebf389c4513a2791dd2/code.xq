for $b in collection("bib")
let $title := $b//bib:title
where $title contains text "s"
order by $title
return $title