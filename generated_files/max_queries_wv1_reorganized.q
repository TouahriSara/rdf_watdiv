
SELECT ?v0 WHERE {
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/gender> ?v5 .
    ?v0 <http://xmlns.com/foaf/age> ?v4 .
    ?v0 <http://purl.org/dc/terms/Location> ?v3 .
    ?v0 <http://xmlns.com/foaf/givenName> ?v6 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/friendOf> ?v2 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v1 .
}
#EOQ#
SELECT ?v0 WHERE {
    {
        SELECT ?v0 WHERE {
            ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/gender> ?v5 .
            ?v0 <http://xmlns.com/foaf/age> ?v4 .
        }
    }
    ?v0 <http://purl.org/dc/terms/Location> ?v3 .
    ?v0 <http://xmlns.com/foaf/givenName> ?v6 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/friendOf> ?v2 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v1 .
}
#EOQ#
SELECT ?v0 WHERE {
    OPTIONAL { ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v1 . }
    FILTER(BOUND(?v1))
    OPTIONAL { ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/friendOf> ?v2 . }
    FILTER(BOUND(?v2))
    ?v0 <http://purl.org/dc/terms/Location> ?v3 .
    ?v0 <http://xmlns.com/foaf/age> ?v4 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/gender> ?v5 .
    ?v0 <http://xmlns.com/foaf/givenName> ?v6 .
}

#EOQ#
SELECT ?v0 WHERE {
    VALUES ?v0 { 
        <http://example.org/person1> 
        <http://example.org/person2> 
    }
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v1 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/friendOf> ?v2 .
    ?v0 <http://purl.org/dc/terms/Location> ?v3 .
    ?v0 <http://xmlns.com/foaf/age> ?v4 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/gender> ?v5 .
    ?v0 <http://xmlns.com/foaf/givenName> ?v6 .
}

#EOQ#
SELECT ?v0 ?v4 ?v6 ?v7 WHERE {
    ?v0 <http://schema.org/contentRating> ?v3 .
    ?v0 <http://purl.org/stuff/rev#hasReview> ?v4 .
    ?v4 <http://purl.org/stuff/rev#reviewer> ?v6 .
    ?v7 <http://schema.org/actor> ?v6 .
    ?v7 <http://schema.org/language> ?v8 .
    ?v0 <http://schema.org/caption> ?v1 .
    ?v0 <http://schema.org/text> ?v2 .
}
#EOQ#

SELECT ?v0 ?v4 ?v6 ?v7 WHERE {
    {
        SELECT ?v0 WHERE {
            ?v0 <http://schema.org/contentRating> ?v3 .
            ?v0 <http://purl.org/stuff/rev#hasReview> ?v4 .
        }
    }
    ?v4 <http://purl.org/stuff/rev#reviewer> ?v6 .
    ?v7 <http://schema.org/actor> ?v6 .
    ?v7 <http://schema.org/language> ?v8 .
    ?v0 <http://schema.org/caption> ?v1 .
    ?v0 <http://schema.org/text> ?v2 .
}
#EOQ#

SELECT ?v0 ?v4 ?v6 ?v7 WHERE {
    OPTIONAL { ?v0 <http://schema.org/contentRating> ?v3 . }
    FILTER(BOUND(?v3))
    OPTIONAL { ?v0 <http://purl.org/stuff/rev#hasReview> ?v4 . }
    FILTER(BOUND(?v4))
    ?v4 <http://purl.org/stuff/rev#reviewer> ?v6 .
    ?v7 <http://schema.org/actor> ?v6 .
    ?v7 <http://schema.org/language> ?v8 .
    ?v0 <http://schema.org/caption> ?v1 .
    ?v0 <http://schema.org/text> ?v2 .
}

#EOQ#
SELECT ?v0 ?v4 ?v6 ?v7 WHERE {
    VALUES ?v7 { 
        <http://example.org/movie1> 
        <http://example.org/movie2> 
    }
    ?v0 <http://schema.org/contentRating> ?v3 .
    ?v0 <http://purl.org/stuff/rev#hasReview> ?v4 .
    ?v4 <http://purl.org/stuff/rev#reviewer> ?v6 .
    ?v7 <http://schema.org/actor> ?v6 .
    ?v7 <http://schema.org/language> ?v8 .
    ?v0 <http://schema.org/caption> ?v1 .
    ?v0 <http://schema.org/text> ?v2 .
}

#EOQ#
SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 ?v7 ?v8 WHERE {
    ?v0 <http://ogp.me/ns#tag> <http://db.uwaterloo.ca/~galuc/wsdbm/Topic154> .
    ?v0 <http://xmlns.com/foaf/homepage> ?v1 .
    ?v2 <http://purl.org/goodrelations/includes> ?v0 .
    ?v0 <http://schema.org/description> ?v4 .
    ?v0 <http://schema.org/contentSize> ?v8 .
    ?v1 <http://schema.org/url> ?v5 .
    ?v1 <http://db.uwaterloo.ca/~galuc/wsdbm/hits> ?v6 .
    ?v1 <http://schema.org/language> <http://db.uwaterloo.ca/~galuc/wsdbm/Language0> .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v0 .
}
#EOQ#

SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 ?v7 ?v8 WHERE {
    {
        SELECT ?v0 WHERE {
            ?v0 <http://ogp.me/ns#tag> <http://db.uwaterloo.ca/~galuc/wsdbm/Topic154> .
            ?v0 <http://xmlns.com/foaf/homepage> ?v1 .
        }
    }
    ?v2 <http://purl.org/goodrelations/includes> ?v0 .
    ?v0 <http://schema.org/description> ?v4 .
    ?v0 <http://schema.org/contentSize> ?v8 .
    ?v1 <http://schema.org/url> ?v5 .
    ?v1 <http://db.uwaterloo.ca/~galuc/wsdbm/hits> ?v6 .
    ?v1 <http://schema.org/language> <http://db.uwaterloo.ca/~galuc/wsdbm/Language0> .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v0 .
}
#EOQ#
SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 ?v7 ?v8 WHERE {
    OPTIONAL { ?v0 <http://ogp.me/ns#tag> <http://db.uwaterloo.ca/~galuc/wsdbm/Topic154> . }
    FILTER(BOUND(?v0))
    OPTIONAL { ?v0 <http://xmlns.com/foaf/homepage> ?v1 . }
    FILTER(BOUND(?v1))
    ?v2 <http://purl.org/goodrelations/includes> ?v0 .
    ?v0 <http://schema.org/description> ?v4 .
    ?v0 <http://schema.org/contentSize> ?v8 .
    ?v1 <http://schema.org/url> ?v5 .
    ?v1 <http://db.uwaterloo.ca/~galuc/wsdbm/hits> ?v6 .
    ?v1 <http://schema.org/language> <http://db.uwaterloo.ca/~galuc/wsdbm/Language0> .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v0 .
}
#EOQ#

SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 ?v7 ?v8 WHERE {
    VALUES ?v0 { 
        <http://example.org/resource1> 
        <http://example.org/resource2> 
    }
    ?v0 <http://ogp.me/ns#tag> <http://db.uwaterloo.ca/~galuc/wsdbm/Topic154> .
    ?v0 <http://xmlns.com/foaf/homepage> ?v1 .
    ?v2 <http://purl.org/goodrelations/includes> ?v0 .
    ?v0 <http://schema.org/description> ?v4 .
    ?v0 <http://schema.org/contentSize> ?v8 .
    ?v1 <http://schema.org/url> ?v5 .
    ?v1 <http://db.uwaterloo.ca/~galuc/wsdbm/hits> ?v6 .
    ?v1 <http://schema.org/language> <http://db.uwaterloo.ca/~galuc/wsdbm/Language0> .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v0 .
}
#EOQ#


SELECT ?v0 ?v3 ?v4 ?v8 WHERE {
    ?v0 <http://schema.org/legalName> ?v1 .
    ?v0 <http://purl.org/goodrelations/offers> ?v2 .
    ?v2 <http://schema.org/eligibleRegion> <http://db.uwaterloo.ca/~galuc/wsdbm/Country5> .
    ?v2 <http://purl.org/goodrelations/includes> ?v3 .
    ?v4 <http://schema.org/jobTitle> ?v5 .
    ?v4 <http://xmlns.com/foaf/homepage> ?v6 .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v7 .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v3 .
    ?v3 <http://purl.org/stuff/rev#hasReview> ?v8 .
    ?v8 <http://purl.org/stuff/rev#totalVotes> ?v9 .
}

#EOQ#
SELECT ?v0 ?v3 ?v4 ?v8 WHERE {
    {
        SELECT ?v0 WHERE {
            ?v0 <http://schema.org/legalName> ?v1 .
            ?v0 <http://purl.org/goodrelations/offers> ?v2 .
            ?v2 <http://schema.org/eligibleRegion> <http://db.uwaterloo.ca/~galuc/wsdbm/Country5> .
        }
    }
    ?v2 <http://purl.org/goodrelations/includes> ?v3 .
    ?v4 <http://schema.org/jobTitle> ?v5 .
    ?v4 <http://xmlns.com/foaf/homepage> ?v6 .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v7 .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v3 .
    ?v3 <http://purl.org/stuff/rev#hasReview> ?v8 .
    ?v8 <http://purl.org/stuff/rev#totalVotes> ?v9 .
}
#EOQ#

SELECT ?v0 ?v3 ?v4 ?v8 WHERE {
    OPTIONAL { ?v0 <http://schema.org/legalName> ?v1 . }
    FILTER(BOUND(?v1))
    OPTIONAL { ?v0 <http://purl.org/goodrelations/offers> ?v2 . }
    FILTER(BOUND(?v2))
    ?v2 <http://schema.org/eligibleRegion> <http://db.uwaterloo.ca/~galuc/wsdbm/Country5> .
    ?v2 <http://purl.org/goodrelations/includes> ?v3 .
    ?v4 <http://schema.org/jobTitle> ?v5 .
    ?v4 <http://xmlns.com/foaf/homepage> ?v6 .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v7 .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v3 .
    ?v3 <http://purl.org/stuff/rev#hasReview> ?v8 .
    ?v8 <http://purl.org/stuff/rev#totalVotes> ?v9 .
}
#EOQ#

SELECT ?v0 ?v3 ?v4 ?v8 WHERE {
    VALUES ?v0 { 
        <http://example.org/company1> 
        <http://example.org/company2> 
    }
    ?v0 <http://schema.org/legalName> ?v1 .
    ?v0 <http://purl.org/goodrelations/offers> ?v2 .
    ?v2 <http://schema.org/eligibleRegion> <http://db.uwaterloo.ca/~galuc/wsdbm/Country5> .
    ?v2 <http://purl.org/goodrelations/includes> ?v3 .
    ?v4 <http://schema.org/jobTitle> ?v5 .
    ?v4 <http://xmlns.com/foaf/homepage> ?v6 .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v7 .
    ?v7 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v3 .
    ?v3 <http://purl.org/stuff/rev#hasReview> ?v8 .
    ?v8 <http://purl.org/stuff/rev#totalVotes> ?v9 .
}
#EOQ#
SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 WHERE {
    ?v0 <http://schema.org/contentRating> ?v1 .
    ?v0 <http://schema.org/contentSize> ?v2 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> <http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre70> .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v5 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseDate> ?v6 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v0 .
}
#EOQ#
SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 WHERE {
    {
        SELECT ?v0 WHERE {
            ?v0 <http://schema.org/contentRating> ?v1 .
            ?v0 <http://schema.org/contentSize> ?v2 .
        }
    }
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> <http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre70> .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v5 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseDate> ?v6 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v0 .
}
#EOQ#

SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 WHERE {
    OPTIONAL { ?v0 <http://schema.org/contentRating> ?v1 . }
    FILTER(BOUND(?v1))
    OPTIONAL { ?v0 <http://schema.org/contentSize> ?v2 . }
    FILTER(BOUND(?v2))
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> <http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre70> .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v5 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseDate> ?v6 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v0 .
}
#EOQ#

SELECT ?v0 ?v1 ?v2 ?v4 ?v5 ?v6 WHERE {
    VALUES ?v0 { 
        <http://example.org/content1> 
        <http://example.org/content2> 
    }
    ?v0 <http://schema.org/contentRating> ?v1 .
    ?v0 <http://schema.org/contentSize> ?v2 .
    ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> <http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre70> .
    ?v4 <http://db.uwaterloo.ca/~galuc/wsdbm/makesPurchase> ?v5 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseDate> ?v6 .
    ?v5 <http://db.uwaterloo.ca/~galuc/wsdbm/purchaseFor> ?v0 .
}
