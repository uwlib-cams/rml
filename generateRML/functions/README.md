# Functions
These functions are utilized in [generate_RML.py](https://github.com/uwlib-cams/rml/tree/master/generateRML) to convert mappings written in kiegel into RML code.

## Table of Contents
 - [admin_metadata_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#admin_metadata_functionspy)
 - [boolean_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#boolean_functionspy)
 - [formatting_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#formatting_functionspy)
 - [identifiedBy_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#identifiedby_functionspy)
 - [kiegel_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#kiegel_functionspy)
 - [lists.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#listspy)
 - [logical_source_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#logical_source_functionspy)
 - [parse_kiegel.py](https://github.com/uwlib-cams/rml/blob/master/generateRML/functions#parse_kiegelpy)
 - [po_map_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#po_map_functionspy)
 - [split_by_space.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#split_by_spacepy)
 - [start_RML_map.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#start_rml_mappy)
 - [subject_map_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#subject_map_functionspy)
 - [value_functions.py](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#value_functionspy)

## admin_metadata_functions.py
### admin_metadata_mapping
Generates the RML to map the administrative metadata from BIBFRAME to BIBFRAME.

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## boolean_functions.py
### class_test
Takes in a given node, and tests to see if it's a class or a property.

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## formatting_functions.py
### convert_string_to_IRI
Converts a URI written as a string into an [RDFLIB URIRef](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#urirefs).

### generate_constant
Converts the mapping for a [constant value](https://rml.io/specs/rml/#constant) into RDFLIB terms. The predicate is turned into an [RDFLIB URIRef](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#urirefs), and the object is turned into an [RDFLIB URIRef](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#urirefs) or an [RDFLIB Literal](https://rdflib.readthedocs.io/en/stable/rdf_terms.html#literals). It is returned as a tuple.

Example:  
Input:
```
"role=<http://id.loc.gov/vocabulary/relators/ppm>"
```

Output:
```
(URIRef('http://id.loc.gov/ontologies/bibframe/role'), URIRef('http://id.loc.gov/vocabulary/relators/ppm'))
```

### create_bnode_name
Create a descriptive title for a blank node based on the predicate that takes that blank node as an object, the class of the blank node, and the value(s) that will populate that blank node.

### edit_kiegel
Takes in a kiegel mapping, and expands it into a dictionary where mappings that take an IRI as a value becomes values for an "IRI" key, and mappings that take a literal as a value becomes values for a "literal" key.

### edit_kiegel_list
Used with [edit_kiegel](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#edit_kiegel) to make sure kiegel statements are going into the correct blank node.

Example:  
Kiegel mapping that goes into edit_kiegel:
```
contribution >> Contribution > agent >> Organization > rdfs:label ; > role=<http://id.loc.gov/vocabulary/relators/prn>
or
contribution >> Contribution > agent* > role=<http://id.loc.gov/vocabulary/relators/prn>
```

List that goes into edit_kiegel_list:
```
['contribution >> Contribution > agent >> Organization > rdfs:label', '> role=<http://id.loc.gov/vocabulary/relators/prn>']
```

Each item in this list gets iterated over; if it begins with a `>`, like this:
```
> role=<http://id.loc.gov/vocabulary/relators/prn>
```

It locates the previous blank node (i.e. the previous item in the list that contains `>>`), which in this case is:
```
contribution >> Contribution > agent >> Organization > rdfs:label
```

It takes the property and class of this blank node, resulting in this:
```
contribution >> Contribution > role=<http://id.loc.gov/vocabulary/relators/prn>
```

And the new kiegel list that gets returned to edit_kiegel is this:
```
['contribution >> Contribution > agent >> Organization > rdfs:label', 'contribution >> Contribution > role=<http://id.loc.gov/vocabulary/relators/prn>']
```

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## identifiedBy_functions.py
Functions that generate the RML for RDA properties [rdaw:P10002](http://rdaregistry.info/Elements/w/P10002), [rdae:P20002](http://rdaregistry.info/Elements/e/P20002), [rdam:P30004](http://rdaregistry.info/Elements/m/P30004), and [rdai:P40001](http://rdaregistry.info/Elements/i/P40001).

### P10002_mapping
Generates the RML to map the value(s) of [rdaw:P10002](http://rdaregistry.info/Elements/w/P10002) to a blank node classed as [bf:Identifier](https://id.loc.gov/ontologies/bibframe.html#c_Identifier).

### P20002_mapping
Generates the RML to map the value(s) of [rdae:P20002](http://rdaregistry.info/Elements/e/P20002) to a blank node classed as [bf:Identifier](https://id.loc.gov/ontologies/bibframe.html#c_Identifier).

### P30004_mapping
Generates the RML to map the value(s) of [rdam:P30004](http://rdaregistry.info/Elements/m/P30004) to a blank node classed as [bf:Identifier](https://id.loc.gov/ontologies/bibframe.html#c_Identifier).

### P40001_mapping
Generates the RML to map the value(s) of [rdai:P40001](http://rdaregistry.info/Elements/i/P40001) to a blank node classed as [bf:Identifier](https://id.loc.gov/ontologies/bibframe.html#c_Identifier).

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## kiegel_functions.py
Functions necessary to parse kiegel mappings.

### Table of Contents
 - [get_file_list](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#get_file_list)
 - [get_property_kiegel_list](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#get_property_kiegel_list)
 - [create_kiegel_dict](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#create_kiegel_dict)

_Python Libraries/Modules/Packages_
 - _[csv](https://docs.python.org/3/library/csv.html)_
 - _[os](https://docs.python.org/3/library/os.html)_
 - _[rdflib](https://rdflib.readthedocs.io/en/stable/)_

### get_file_list
Creates list of CSV files containing mappings for a given entity.

### get_property_kiegel_list
Creates list of tuples containing an RDA property and its respective mapping(s) for a given entity.

### create_kiegel_dict
Creates dictionary with RDA property numbers as keys and its mapping(s) as values. These values are themselves dictionaries, with either "IRI" or "literal" as the key, depending on what type of value the mapping will take.

_See [edit_kiegel](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#edit_kiegel)_

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## lists.py
Lists used throughout the generation process.

### Table of Contents
 - Work lists
	 - [work_title_props](#)
	 - [skip_work_props](#)
   - [dissertationList](#)
 - Expression lists
   - [expression_title_props](#)
	 - [skip_expression_props](#)
 - Manifestation lists
   - [manifestation_title_props](#)
	 - [skip_manifestation_props](#)
   - [provisionActivityList](#)
   - [provisionActivityDistributionList](#)
	 - [provisionActivityManufactureList](#)
	 - [provisionActivityProductionList](#)
	 - [provisionActivityPublicationList](#)
 - Item lists
   - [item_title_props](#)
	 - [skip_item_props](#)
 - Extension properties lists
   - [classification_props](#)
	 - [classificationLcc_props](#)
	 - [classificationNlm_props](#)
 - Misc lists
   - [entities](#)
	 - [entity_prefixes](#)
	 - [nosplit_bnode_list](#)
	 - [no_language_tag_list](#)

### entities
List of RDA entities used in mappings.

### entity_prefixes
List of prefixes used for RDA properties.

### nosplit_bnode_list
Names of blank nodes for RDA properties that, when multiple values for that property exist, map into the same blank node in BIBFRAME, as opposed to being "split" into their own blank nodes.

### no_language_tag_list
RDA properties whose language tags should be ignored, even when they exist in the RDA/RDF data.

### provisionActivityDistributionList
RDA properties that map into the same blank node, classed as [bf:Distribution](https://id.loc.gov/ontologies/bibframe.html#c_Distribution).

### provisionActivityManufactureList
RDA properties that map into the same blank node, classed as [bf:Manufacture](https://id.loc.gov/ontologies/bibframe.html#c_Manufacture).

### provisionActivityProductionList
RDA properties that map into the same blank node, classed as [bf:Production](https://id.loc.gov/ontologies/bibframe.html#c_Production).

### provisionActivityPublicationList
RDA properties that map into the same blank node, classed as [bf:Publication](https://id.loc.gov/ontologies/bibframe.html#c_Publication).

### provisionActivityList
Combination of provisionActivityDistributionList, provisionActivityManufactureList, provisionActivityProductionList, and provisionActivityPublicationList.

### dissertationList
RDA properties that map into the same blank node, classed as [bf:Dissertation](https://id.loc.gov/ontologies/bibframe.html#c_Dissertation).

### work_title_props
[RDA work](http://rdaregistry.info/Elements/c/C10001) properties that map into the same blank node, classed as [bf:Title](https://id.loc.gov/ontologies/bibframe.html#c_Title).

### expression_title_props
[RDA expression](http://rdaregistry.info/Elements/c/C10006) properties that map into the same blank node, classed as [bf:Title](https://id.loc.gov/ontologies/bibframe.html#c_Title).

### manifestation_title_props
[RDA manifestation](http://rdaregistry.info/Elements/c/C10007) properties that map into the same blank node, classed as [bf:Title](https://id.loc.gov/ontologies/bibframe.html#c_Title).

### item_title_props
[RDA item](http://rdaregistry.info/Elements/c/C10003) properties that map into the same blank node, classed as [bf:Title](https://id.loc.gov/ontologies/bibframe.html#c_Title).

### classificationLcc_props
RDA properties that map into the same blank node, classed as [bf:ClassificationLcc](https://id.loc.gov/ontologies/bibframe.html#c_ClassificationLcc).

### classificationNlm_props
RDA properties that map into the same blank node, classed as [bf:ClassificationNlm](https://id.loc.gov/ontologies/bibframe.html#c_ClassificationNlm).

### classification_props
Combination of classificationLcc_props and classificationNlm_props.

### skip_work_props
Work properties that should be skipped while generating RML.

### skip_expression_props
Expression properties that should be skipped while generating RML.

### skip_manifestation_props
Manifestation properties that should be skipped while generating RML.

### skip_item_props
Item properties that should be skipped while generating RML.

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## logical_source_functions.py
Functions that generate an [RML logical source](https://rml.io/specs/rml/#logical-source).

_Python Libraries/Modules/Packages_
 - _[rdflib](https://rdflib.readthedocs.io/en/stable/)_

### generate_main_logical_source
Generates an RML logical source for the "main" [RML triples map](https://rml.io/specs/rml/#triples-map), i.e. the ex:WorkMap, the ex:ExpressionMap, the ex:ManifestationMap, or the ex:ItemMap.

### generate_IRI_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps properties with IRI values.

### generate_neutral_literal_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps properties with literal values, and ignores any possible language tags for those values (i.e. "neutral").

### generate_lang_literal_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps properties with literal values that have a language tag.

### generate_constant_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that maps properties that take a [constant value](https://rml.io/specs/rml/#constant), rather than one referenced from the original RDA/RDF data.

### generate_not_lang_literal_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps properties with literal values that do _not_ have a language tag.

### generate_provact_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps RDA properties that map to a blank node classed as one of the subclasses of [bf:ProvisionActivity](https://id.loc.gov/ontologies/bibframe.html#c_ProvisionActivity):
 - [bf:Distribution](https://id.loc.gov/ontologies/bibframe.html#c_Distribution)
 - [bf:Manufacture](https://id.loc.gov/ontologies/bibframe.html#c_Manufacture)
 - [bf:Production](https://id.loc.gov/ontologies/bibframe.html#c_Production)
 - [bf:Publication](https://id.loc.gov/ontologies/bibframe.html#c_Publication)

 - _See [provisionActivityDistributionList](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#provisionActivityDistributionList)_
 - _See [provisionActivityManufactureList](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#provisionActivityManufactureList)_
 - _See [provisionActivityProductionList](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#provisionActivityProductionList)_
 - _See [provisionActivityPublicationList](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#provisionActivityPublicationList)_

### generate_title_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps RDA properties that map to a blank node classed as [bf:Title](https://id.loc.gov/ontologies/bibframe.html#c_Title).

 - _See [work_title_props](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#work_title_props)_
 - _See [expression_title_props](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#expression_title_props)_
 - _See [manifestation_title_props](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#manifestation_title_props)_
 - _See [item_title_props](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#item_title_props)_

### generate_classification_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps RDA properties that map to a blank node classed as one the of subclasses of [bf:Classification](https://id.loc.gov/ontologies/bibframe.html#c_Classification):
 - [bf:ClassificationLcc](https://id.loc.gov/ontologies/bibframe.html#c_ClassificationLcc)
 - [bf:ClassificationNlm](https://id.loc.gov/ontologies/bibframe.html#c_ClassificationNlm)

 - _See [classificationLcc_props](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#classificationLcc_props)_
 - _See [classificationNlm_props](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#classificationNlm_props)_

### generate_lang_nosplit_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) in which multiple values for a single RDA/RDF properties are mapped into the same blank node in BIBFRAME, i.e. "no split" because they are not split apart. This logical source can be used for IRIs or literals that have language tags.

### generate_not_lang_nosplit_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) in which multiple values for a single RDA/RDF properties are mapped into the same blank node in BIBFRAME, i.e. "no split" because they are not split apart. This logical source can be used for IRIs or literals that do _not_ have language tags.

### generate_dissertation_logical_source
Generates an RML logical source for an [RML triples map](https://rml.io/specs/rml/#triples-map) that only maps RDA properties that map to a blank node classed as a [bf:Dissertation](https://id.loc.gov/ontologies/bibframe.html#c_Dissertation).

 - _See [dissertationList](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#dissertationList)_

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## parse_kiegel.py
### kiegel_reader

Iterates through dictionary of kiegel mappings created by the function [create_kiegel_dict](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#create_kiegel_dict) and generates RML for each mapping.

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## po_map_functions.py
Functions that generate an [RML predicate-object map](https://rml.io/specs/rml/#predicate-object-map).

### generate_bnode_po_map
Generates a predicate-object map where the object is a blank node.

### generate_langnotlang_literal_po_main_map
Generates two predicate-object maps where the object is a literal -- one that requires a language tag, and one that requires no language tag (i.e. lang/not lang).

### generate_neutral_literal_po_map
Generates a predicate-object map where the object is a literal. It does not record any language tags (i.e. "neutral").

### generate_IRI_po_map
Generates a predicate-object map where the object is an IRI.

### generate_lang_literal_split_po_map
Generates a predicate-object map where the object is a literal with a language tag. This literal will go into a "split" blank node, which is when multiple values for the same RDA property are put into their own blank nodes in BIBFRAME rather than all being in the same blank node (i.e. they are "split" apart).

### generate_not_lang_literal_split_po_map
Generates a predicate-object map where the object is a literal with no language tag. This literal will go into a "split" blank node, which is when multiple values for the same RDA property are put into their own blank nodes in BIBFRAME rather than all being in the same blank node (i.e. they are "split" apart).

### generate_neutral_literal_split_po_map
Generates a predicate-object map where the object is a literal. No language tag is recorded (i.e. "neutral"). This literal will go into a "split" blank node, which is when multiple values for the same RDA property are put into their own blank nodes in BIBFRAME rather than all being in the same blank node (i.e. they are "split" apart).

### generate_IRI_split_po_map
Generates a predicate-object map where the object is an IRI. This IRI will go into a "split" blank node, which is when multiple values for the same RDA property are put into their own blank nodes in BIBFRAME rather than all being in the same blank node (i.e. they are "split" apart).

### generate_lang_literal_nosplit_po_map
Generates a predicate-object map where the object is a literal with a language tag. This literal will go into a "no split" blank node, which is when multiple values for the same RDA property are all put into the same blank node in BIBFRAME, rather than being in their own blank nodes (i.e. they are _not_ "split" apart).

### generate_not_lang_literal_nosplit_po_map
Generates a predicate-object map where the object is a literal with no language tag. This literal will go into a "no split" blank node, which is when multiple values for the same RDA property are all put into the same blank node in BIBFRAME, rather than being in their own blank nodes (i.e. they are _not_ "split" apart).

### generate_neutral_literal_nosplit_po_map
Generates a predicate-object map where the object is a literal. No language tag is recorded (i.e. "neutral"). This literal will go into a "no split" blank node, which is when multiple values for the same RDA property are all put into the same blank node in BIBFRAME, rather than being in their own blank nodes (i.e. they are _not_ "split" apart).

### generate_IRI_nosplit_po_map
Generates a predicate-object map where the object is an IRI. This IRI will go into a "no split" blank node, which is when multiple values for the same RDA property are all put into the same blank node in BIBFRAME, rather than being in their own blank nodes (i.e. they are _not_ "split" apart).

### generate_constant_IRI
Generates a predicate-object map where the object is a [constant](https://rml.io/specs/rml/#constant) IRI.

### generate_constant_literal
Generates a predicate-object map where the object is a [constant](https://rml.io/specs/rml/#constant) literal. The default language tag is "en".

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## split_by_space.py

### split_by_space
Takes in a kiegel map as a string, and returns the elements in the map separated into a list.

Example:  
Kiegel mapping input:
```
note >> Note > rdfs:label > noteType="numeric designation for musical work"
```
List output:
```
['note', '>>', 'Note', '>', 'rdfs:label', '>', 'noteType="numeric designation for musical work"']
```

## start_RML_map.py

### start_RML_map
Creates a graph using [rdflib](https://rdflib.readthedocs.io/en/stable/) and binds to it all possible namespaces from the RDA/RDF data that the RML will transform.

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## subject_map_functions.py
Functions that generate an [RML subject map](https://rml.io/specs/rml/#subject-map).

_Python Libraries/Modules/Packages_
 - _[rdflib](https://rdflib.readthedocs.io/en/stable/)_

### generate_main_subject_map
Generates an RML subject map for the "main" [RML triples map](https://rml.io/specs/rml/#triples-map), i.e. the ex:WorkMap, the ex:ExpressionMap, the ex:ManifestationMap, or the ex:ItemMap.

### generate_bnode_subject_map
Generates an RML subject map for a blank node.

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_

## value_functions.py

### generate_RML_for_IRI
Generates the necessary RML for a property that takes an IRI as a value.

 - _See [generate_IRI_po_main_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_IRI_po_main_map)_
 - _See [generate_IRI_nosplit_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_IRI_nosplit_po_map)_
 - _See [generate_IRI_split_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_IRI_split_po_map)_

### generate_RML_for_constant
Generates the necessary RML for a property that takes a [constant value](https://rml.io/specs/rml/#constant).

 - _See [generate_constant_IRI](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_constant_IRI)_
 - _See [generate_constant_literal](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_constant_literal)_

### generate_RML_for_bnode
Generates the necessary RML for a property that takes a blank node as a value.

 - _See [create_bnode_name](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#create_bnode_name)_
 - _See [generate_bnode_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_bnode_po_map)_
 - _See [generate_dissertation_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_dissertation_logical_source)_
 - _See [generate_title_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_title_logical_source)_
 - _See [generate_lang_nosplit_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_lang_nosplit_logical_source)_
 - _See [generate_not_lang_nosplit_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_not_lang_nosplit_logical_source)_
 - _See [generate_constant_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_constant_logical_source)_
 - _See [generate_IRI_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_IRI_logical_source)_
 - _See [generate_neutral_literal_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_neutral_literal_logical_source)_
 - _See [generate_lang_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_lang_logical_source)_
 - _See [generate_not_lang_logical_source](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#[generate_not_lang_logical_source)_
 - _See [generate_bnode_subject_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_bnode_subject_map)_

### generate_RML_for_literal
Generates the necessary RML for a property that takes a literal as a value.

 - _See [generate_neutral_literal_po_main_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_neutral_literal_po_main_map)_
 - _See [generate_langnotlang_literal_po_main_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_langnotlang_literal_po_main_map)_
 - _See [generate_neutral_literal_nosplit_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_neutral_literal_nosplit_po_map)_
 - _See [generate_neutral_literal_split_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_neutral_literal_split_po_map)_
 - _See [generate_lang_literal_split_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_lang_literal_split_po_map)_
 - _See [generate_not_lang_literal_split_po_map](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#generate_not_lang_literal_split_po_map)_

_[Back to top](https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#functions)_
