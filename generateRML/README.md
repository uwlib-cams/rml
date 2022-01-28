# generateRML.py
Script that takes in kiegel mappings via CSV files, and outputs RML that will transform RDA data to BIBFRAME according to those kiegel mappings. Takes directory of CSV files as an argument.

```
$ python3 generateRML.py csv_dir
```

## How kiegel is parsed in this script

This scripts takes in a directory with at least one CSV file. The CSV file should be structured with the same columns as the University of Washington's [RDA-to-BIBFRAME-map](https://docs.google.com/spreadsheets/d/1y0coXcJAoVOP2BPtzwmnc9l-OWQbwYujVJ8oXXYpMRc/edit?usp=sharing).

_Example_

| RDA label |	RDA IRI |	pseudo-Turtle |	Kiegel syntax |
|---|---|---|---|
| has category of work (Genre lookup)(RDA 6.3) | <http://rdaregistry.info/Elements/w/P10004> | bf:genreForm <P10004value> .\n\# with literal value\nbf:genreForm\n[ a bf:GenreForm ;\n\trdfs:label "P10004value" ] . | genreForm*\nor\ngenreForm >> GenreForm > rdfs:label |

For each row in this CSV file, this script will create a tuple with the RDA property number (taken from the end of the RDA IRI) and the kiegel, and put all of these tuples into a list.

_Example_
```
("P10004", "genreForm*\nor\ngenreForm >> GenreForm > rdfs:label")
```

The above kiegel actually contains two mappings: one for IRI values, and one for literal values. This kiegel is then separated out into a dictionary like the following:

_Example_
```
{"IRI": ["genreForm*"], "literal": ["genreForm >> GenreForm > rdfs:label"]}
```

These dictionaries are then put into a larger dictionary with each RDA property acting as a key, and the mapping dictionary as its value.

_Example_
```
{"P10004": {"IRI": ["genreForm*"], "literal": ["genreForm >> GenreForm > rdfs:label"]}}
```

This script will then generate a series of [RML triples maps](https://rml.io/specs/rml/#triples-map). Because these maps are composed of RDF triples, each map requires a subject, referred to here as a "map name." The default map name is the RDA entity for a given property (e.g. for P10004, the default map name is "Work"). If the mapping requires a blank node, the map name will be changed to a name generated to represent that blank node. The map name will return to the default before the next mapping.

With the property-kiegel dictionary established, the script then begins to loop through the mapping as follows:
 - For each property... (e.g. "P10004")
 - For each possible value for that property (e.g. "literal")
 - For each mapping for that value (e.g. "genreForm >> GenreForm > rdfs:label")

With all that in place, the script will process each individual mapping.

The first step is to separate the kiegel mapping as a string into a list.

_Example_
["genreForm", ">>", "GenreForm", ">", "rdfs:label"]

Each item in this list will then by assessed by a series of if-then statements.
 - Is there a * in this item?
    - If yes, this item takes an IRI as a value
        - If the current map name is the default map name, generate a standard IRI predicate-object map
        - If the current map name is in the [nosplit_bnode_list](https://github.com/uwlib-cams/rml/tree/master/generateRML#nosplit_bnode_list), generate a "no-split" IRI predicate-object map
        - Otherwise, generate a standard (in this case, a "split") IRI predicate-object map
 - Is there a = in this item?
    - If yes, this item takes a constant as a value
        - If there is a < in this item, generate a constant IRI predicate-object map
        - Otherwise, generate a constant literal predicate-object map
    - Is "Lang" in this map name? (i.e. is this a triples map that requires language tags?)
        - If yes, we need to generate these same predicate-object maps for an equivalent "no language tag" triples map (i.e. a triples map that requires _no_ language tags)
            - If there is a < in this item, generate a constant IRI predicate-object map
            - Otherwise, generate a constant literal predicate-object map
 - Is the item >>?
    - In kiegel, >> denotes a blank node
		- The previous item is the property that takes this blank node as a value
		- The following item is the class for this blank node
		- A map name is generated for this new blank node
            - If this map name contains "Provisionactivity", its map name will follow the format Predicate_Class_, e.g. for P30008 this would be "Provisionactivity_Distribution_"
            - If this map name contains "Title" but does not contain "Variant" or "Abbreviated", its map name will be "Title_"
            - If this map name contains "Dissertation" and it is a Work property, its map name will be "Dissertation_"
            - If the property is in the list [classificationLcc_props](https://github.com/uwlib-cams/rml/tree/master/generateRML#classificationLcc_props), its map name will be "Classification_Lcc_"
            - If the property is in the list [classificationNlm_props](https://github.com/uwlib-cams/rml/tree/master/generateRML#classificationNlm_props), its map name will be "Classification_Nlm_"
            - If the property takes a literal as a value...
                - If the property is in the list [no_language_tag_list](https://github.com/uwlib-cams/rml/tree/master/generateRML#no_language_tag_list), its map name will follow the format Literal_Predicate_PropertyNumber_, e.g. "Literal_GenreForm_10004_"
                - If this blank node only contains a constant value, its map name will follow the format Literal_Constant_Predicate_PropertyNumber_, e.g. "Literal_Constant_GenreForm_10004_"
                - If this property is _not_ in the list [no_language_tag_list](https://github.com/uwlib-cams/rml/tree/master/generateRML#no_language_tag_list), its map name will follow the format Lang_Literal_Predicate_PropertyNumber_, e.g. "Lang_Literal_GenreForm_10004_"
            - If the property takes a literal as a value...
                - If this blank node only contains a constant value but the predicate is not bf:contribution, its map name will follow the format IRI_Constant_Predicate_PropertyNumber_, e.g. "IRI_Constant_GenreForm_10004_"
                - Otherwise, its map name will follow the format IRI_Predicate_PropertyNumber_, e.g. "IRI_GenreForm_10004_"
    - The next step is to determine whether we are creating a new triples map, or are adding more statements to an existing one
        - If we are creating a new triples map, we need to generate...
            - A predicate-object map that links this new triples map as a [parent triples map](https://rml.io/specs/rml/#parent-triples-map) for the default triples map
            - A [logical source](https://rml.io/specs/rml/#logical-source) for the new triples map
            - A [subject map](https://rml.io/specs/rml/#subject-map) for the new triples map
        - The specifics of these maps will be determined by information gleaned from the new triples map's map name, e.g. if the map is "Title_", if it contains "Lang_", etc.
    - The rest of the mapping will run with the map name being the name of this new triples map for the blank node, until instructed otherwise
 - Otherwise...
    - If this is not the last item in the list and the next item is >>, this property takes a blank node. We will pass it during this loop and take care of it in the next loop
    - Otherwise...
        - If this is definitely a property and not a class, generate a literal predicate-object map
