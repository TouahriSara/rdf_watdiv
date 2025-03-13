SELECT ?nomStagiaire ?domaine ?nomProf
WHERE {
  ?stagiaire ex:aPourNom ?nomStagiaire .
  ?stagiaire ex:etudieDansLeDomaine ?domaine .
  ?stagiaire ex:encadrePar ?professeur .
  ?professeur ex:aPourNom ?nomProf .
}
#EQO#
SELECT ?nomStagiaire ?domaine ?nomProf
WHERE {
  ?stagiaire ex:aPourNom ?nomStagiaire .
  ?stagiaire ex:etudieDansLeDomaine ?domaine .
  ?stagiaire ex:encadrePar ?professeur .
  ?professeur ex:aPourNom ?nomProf .
}
#EQO#
SELECT ?nomStagiaire ?domaine ?nomProf
WHERE {
  ?stagiaire ex:aPourNom ?nomStagiaire .
  ?stagiaire ex:etudieDansLeDomaine ?domaine .
  ?stagiaire ex:encadrePar ?professeur .
  ?professeur ex:aPourNom ?nomProf .
}