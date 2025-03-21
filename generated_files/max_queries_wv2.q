SELECT ?v0 ?v4 ?v6 ?v7 WHERE {
	?v0 <http://schema.org/caption> ?v1 .
	?v0 <http://schema.org/text> ?v2 .
	?v0 <http://schema.org/contentRating> ?v3 .
	?v0 <http://purl.org/stuff/rev#hasReview> ?v4 .
	?v4 <http://purl.org/stuff/rev#title> ?v5 .
	?v4 <http://purl.org/stuff/rev#reviewer> ?v6 .
	?v7 <http://schema.org/actor> ?v6 .
	?v7 <http://schema.org/language> ?v8 .
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
SELECT ?v0 WHERE {
	?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v1 .
	?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/friendOf> ?v2 .
	?v0 <http://purl.org/dc/terms/Location> ?v3 .
	?v0 <http://xmlns.com/foaf/age> ?v4 .
	?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/gender> ?v5 .
	?v0 <http://xmlns.com/foaf/givenName> ?v6 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer11> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer7> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer5> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer1> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer8> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer4> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 		
#EOQ#
SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
	?v0 <http://purl.org/goodrelations/includes> ?v1 .
	<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer3> <http://purl.org/goodrelations/offers> ?v0 .
	?v0 <http://purl.org/goodrelations/price> ?v3 .
	?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
	?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
	?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
	?v0 <http://schema.org/eligibleQuantity> ?v7 .
	?v0 <http://schema.org/eligibleRegion> ?v8 .
	?v0 <http://schema.org/priceValidUntil> ?v9 .
} 	
