# Summary of 2022-01-20 issue

Can RML handle a file with multiple resources in it?

## Example to demonstrate problem

### `multiple_resources.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:rdaw="http://rdaregistry.info/Elements/w/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="https://example.org/Resource1">
    <rdaw:P10223 xml:lang="en">Book 1</rdaw:P10223>
  </rdf:Description>
	<rdf:Description rdf:about="https://example.org/Resource1">
    <rdaw:P10223 xml:lang="fr">Livre 2</rdaw:P10223>
  </rdf:Description>
	<rdf:Description rdf:about="https://example.org/Resource1">
    <rdaw:P10223 xml:lang="ja">本 3</rdaw:P10223>
  </rdf:Description>
</rdf:RDF>
```

### `multi_resource_map.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.
@prefix ex: <http://example.org/rules/>.
@prefix rdaw: <http://rdaregistry.info/Elements/w/>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rml: <http://semweb.mmlab.be/ns/rml#>.
@prefix rr: <http://www.w3.org/ns/r2rml#>.
@prefix ql: <http://semweb.mmlab.be/ns/ql#>.

ex:WorkMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_resources.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description"
	] ;

	rr:subjectMap [
		rml:reference "@about";
		rr:class bf:Work
	] ;

	rr:predicateObjectMap [
		rr:predicate bf:title;
		rr:objectMap [
			rr:parentTriplesMap ex:TitleMap;
			rr:termType rr:BlankNode
		]
	] .

ex:TitleMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_resources.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description"
	] ;

	rr:subjectMap [
		rr:termType rr:BlankNode ;
		rr:class bf:Title
	] ;

	rr:predicateObjectMap [
		rr:predicate rdfs:label;
		rr:objectMap [
			rml:reference "P10223";
			rr:termType rr:Literal;
			rml:languageMap [
				rml:reference "P10223/@lang"
			]
		]
	] .
```

### `multi_resource_output.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://example.org/Resource1> a bf:Work;
  bf:title _:0 .

_:0 a bf:Title;
  rdfs:label "Book 1"@en .

<https://example.org/Resource1> bf:title _:1 .

_:1 a bf:Title;
  rdfs:label "Livre 2"@fr .

<https://example.org/Resource1> bf:title _:2 .

_:2 a bf:Title;
  rdfs:label "本 3"@ja .
```

So in our data we have Resource1, Resource2, and Resource3. The iterator for `ex:WorkMap` (`"/RDF/Description"`) _should_ be iterating over all three of these... and it _is_ iterating over all three! Because it's finding the title (P10023) for each! But for some reason, when it's running the subject map, instead of using the `@about` value for the current `rdf:Description`, it's pulling from the first `rdf:Description` in the document...

We had a similar issue with language tags, where if there were multiple values for a single property all with different language tags, if they were put in the same blank node, they would all just end up with whatever language tag came first, e.g.:

## Example to demonstrate an old, similar problem

### `multiple_lang_tags.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:rdaw="http://rdaregistry.info/Elements/w/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="https://example.org/Resource1">
    <rdaw:P10223 xml:lang="en">Book 1</rdaw:P10223>
    <rdaw:P10223 xml:lang="fr">Livre 2</rdaw:P10223>
    <rdaw:P10223 xml:lang="ja">本 3</rdaw:P10223>
  </rdf:Description>
</rdf:RDF>
```

### `multi_lang_tag_map.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.
@prefix ex: <http://example.org/rules/>.
@prefix rdaw: <http://rdaregistry.info/Elements/w/>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rml: <http://semweb.mmlab.be/ns/rml#>.
@prefix rr: <http://www.w3.org/ns/r2rml#>.
@prefix ql: <http://semweb.mmlab.be/ns/ql#>.

ex:WorkMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_lang_tags.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description"
	] ;

	rr:subjectMap [
		rml:reference "@about";
		rr:class bf:Work
	] ;

	rr:predicateObjectMap [
		rr:predicate bf:title;
		rr:objectMap [
			rr:parentTriplesMap ex:TitleMap;
			rr:termType rr:BlankNode
		]
	] .

ex:TitleMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_lang_tags.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description[P10223]"
	] ;

	rr:subjectMap [
		rr:termType rr:BlankNode ;
		rr:class bf:Title
	] ;

	rr:predicateObjectMap [
		rr:predicate rdfs:label;
		rr:objectMap [
			rml:reference "P10223";
			rr:termType rr:Literal;
			rml:languageMap [
				rml:reference "P10223/@lang"
			]
		]
	] .
```

### `multi_lang_tag_output.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://example.org/Resource1> a bf:Work;
  bf:title _:0 .

_:0 a bf:Title;
  rdfs:label "Book 1"@en, "Livre 2"@en, "本 3"@en .
```

The solution for this was to iterate over these three titles separately. With the current iterator for the title map, we iterate over every instance of `rdf:Description` that contains the property `rdaw:P10223` (`RDF/Description[P10223]`). Instead, we can change the iterator to iterate over every instance of `rdaw:P10223` (`RDF/Description/P10223`).

## Solution for old, similar problem

### `multi_lang_tag_map_2.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.
@prefix ex: <http://example.org/rules/>.
@prefix rdaw: <http://rdaregistry.info/Elements/w/>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rml: <http://semweb.mmlab.be/ns/rml#>.
@prefix rr: <http://www.w3.org/ns/r2rml#>.
@prefix ql: <http://semweb.mmlab.be/ns/ql#>.

ex:WorkMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_lang_tags.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description"
	] ;

	rr:subjectMap [
		rml:reference "@about";
		rr:class bf:Work
	] ;

	rr:predicateObjectMap [
		rr:predicate bf:title;
		rr:objectMap [
			rr:parentTriplesMap ex:TitleMap;
			rr:termType rr:BlankNode
		]
	] .

ex:TitleMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_lang_tags.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description/P10223"
	] ;

	rr:subjectMap [
		rr:termType rr:BlankNode ;
		rr:class bf:Title
	] ;

	rr:predicateObjectMap [
		rr:predicate rdfs:label;
		rr:objectMap [
			rml:reference ".";
			rr:termType rr:Literal;
			rml:languageMap [
				rml:reference "self::node()/@lang"
			]
		]
	] .
```

### `multi_lang_tag_output.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://example.org/Resource1> a bf:Work;
  bf:title _:0 .

_:0 a bf:Title;
  rdfs:label "Book 1"@en .

<https://example.org/Resource1> bf:title _:1 .

_:1 a bf:Title;
  rdfs:label "Livre 2"@fr .

<https://example.org/Resource1> bf:title _:2 .

_:2 a bf:Title;
  rdfs:label "本 3"@ja .
```
Iterating over each P10223 separately puts them into separate blank nodes (which is often what we want anyway!), and each gets the correct language tag!

HOWEVER. I'm not sure how we would apply this lesson to the problem of getting the correct subjects when we have multiple resources in one file...

It seems like this should already be happening, because the iterator for the work map is already going over each `rdf:Description`. I even tried going over each resource IRI by changing the `ex:WorkMap` iterator to `"RDF/Description/@about"`, but this didn't change the output.

## Trying and failing to apply old solution to new problem

### `multi_resource_map_2.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.
@prefix ex: <http://example.org/rules/>.
@prefix rdaw: <http://rdaregistry.info/Elements/w/>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rml: <http://semweb.mmlab.be/ns/rml#>.
@prefix rr: <http://www.w3.org/ns/r2rml#>.
@prefix ql: <http://semweb.mmlab.be/ns/ql#>.

ex:WorkMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_resources.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description/@about"
	] ;

	rr:subjectMap [
		rml:reference ".";
		rr:class bf:Work
	] ;

	rr:predicateObjectMap [
		rr:predicate bf:title;
		rr:objectMap [
			rr:parentTriplesMap ex:TitleMap;
			rr:termType rr:BlankNode
		]
	] .

ex:TitleMap a rr:TriplesMap;
	rml:logicalSource [
		rml:source "multiple_resources.xml";
		rml:referenceFormulation ql:XPath;
		rml:iterator "/RDF/Description[P10223]/@about"
	] ;

	rr:subjectMap [
		rr:termType rr:BlankNode ;
		rr:class bf:Title
	] ;

	rr:predicateObjectMap [
		rr:predicate rdfs:label;
		rr:objectMap [
			rml:reference "../P10223";
			rr:termType rr:Literal;
			rml:languageMap [
				rml:reference "../P10223/@lang"
			]
		]
	] .
```

### `multi_resource_output_2.ttl`
```
@prefix bf: <http://id.loc.gov/ontologies/bibframe/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://example.org/Resource1> a bf:Work;
  bf:title _:0 .

_:0 a bf:Title;
  rdfs:label "Book 1"@en .

<https://example.org/Resource1> bf:title _:1 .

_:1 a bf:Title;
  rdfs:label "Livre 2"@fr .

<https://example.org/Resource1> bf:title _:2 .

_:2 a bf:Title;
  rdfs:label "本 3"@ja .
```

I thought after the meeting that there was something complicated happening that made the way RML was generating this make sense, but now that I've played around without, nah. It's definitely just an issue.

The question now is: do we bring this up with the RML Mapper team? OR do we just let it go and continue with our one-resource-per-file method?

Even if we did bring this up with the RML Mapper team, I'm not sure I would want to change the way we process things one at a time. I'm not sure what the benefit would be! The downside would be rewriting our transformation code. It would be easy enough to change how we load our RDF/XML into the mapper, but there would be a lot of changes to how we process the resulting BIBFRAME in one big file before pushing it to Sinopia... I definitely don't think it would be worth it unless there was some benefit.