# generateRML_v5.py

Script that takes in kiegel mappings via CSV files, and outputs RML that will transform RDA data to BIBFRAME according to those kiegel mappings. Takes directory of CSV files as an argument.

`$ python3.6 generateRML_v5.py csv_dir`

## Version 5 notes

### "No-split" blank nodes

Specific blank nodes that are designated as having multiple properties mapped into a single blank node, notably for provision activity properties and for title properties (exluding variant titles, which are being "split"). Properties that ought to be mapped into a single blank node can be accommodated into the script by request.

Anything that is _not_ in this list will be "split", i.e. in its own distinct blank node. This includes cases in which there are multiple instances of a single property in the original RDA-in-RDF/XML, which in previous versions of generateRML would be mapped into the same blank node.

Note: Due to limitations of RML, these "no-split" blank nodes do not contain mapping for language tags. This means that provision activity properties and title properties (excluding variant title properties) will not have language tags in BIBFRAME.

### "No language tag" list

A list of RDA properties that may have language tags in the original RDA-in-RDF/XML, but these language tags were added by accident or by default in Sinopia and should be ignored by our mapping, e.g. properties that only contain dates. Properties can be added to this list by request.

### Manually-written RML code

For several properties, rather than creating specific Python code to interpret the kiegel from UW's [RDA-to-BIBFRAME map](https://docs.google.com/spreadsheets/d/1y0coXcJAoVOP2BPtzwmnc9l-OWQbwYujVJ8oXXYpMRc/edit?usp=sharing), manually-written RML is inserted into the output instead. Because of this, if changes are made to the RDA-to-BIBFRAME map, these changes will not automatically update in future output of generateRML. If changes to these properties are made, the manually-written RML in can be updated by request.

#### Properties currently being written manually:
 - P10002 (has identifier for work)
 - P10331 (has authorized access point for work)
 - P10332 (has variant access point for work)
 - P20313 (has authorized access point for expression)
 - P20314 (has variant access point for expression)
 - P30294 (has authorized access point for manifestation)
 - P30295 (has variant access point for manifestation)
 - P40083 (has authorized access point for item)
 - P40084 (has variant access point for item)

# csv_dir

Directory of CSV files downloaded from our [RDA-to-BIBFRAME map](https://docs.google.com/spreadsheets/d/1y0coXcJAoVOP2BPtzwmnc9l-OWQbwYujVJ8oXXYpMRc/edit?usp=sharing) and our [RDA extension map](https://docs.google.com/spreadsheets/d/1qSarnhzENkJOhIKDiZtHAIVZgTFNd_ZMUZnBl2TNsN8/edit?usp=sharing).

# rmlOutput

Directory containing most recent output of `generateRML_v5.py`.
