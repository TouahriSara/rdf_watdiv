SELECT ?movie ?actor ?language ?rating
FROM <http://example.org/movies>
WHERE {
    ?movie <http://schema.org/name> ?name .
    ?movie <http://schema.org/actor> ?actor .
    ?actor <http://schema.org/language> ?language .
    ?movie <http://schema.org/contentRating> ?rating .
    FILTER(?rating = "PG-13")
    OPTIONAL {
        ?movie <http://schema.org/review> ?review .
    }
    UNION {
        ?movie <http://schema.org/genre> ?genre .
    }
}
GROUP BY ?movie ?actor ?language
ORDER BY ?rating DESC
LIMIT 10
OFFSET 0
