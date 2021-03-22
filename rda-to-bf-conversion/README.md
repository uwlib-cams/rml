# rda-to-bf-conversion
This directory contains the transformation script `rda-to-bf_2.9.py` as well as all necessary supplemental Python scripts.

# rda-to-bf_2.9.py
## RDA-to-BF Transform

The RDA-to-BF transform (rda-to-bf_2.9.py) is a script that pulls RDA data from [Sinopia](https://sinopia.io/) and runs them through [RML Mapper](https://github.com/RMLio/rmlmapper-java) using RML code from UW Libraries to output BIBFRAME data. The script uses [rdflib](https://rdflib.readthedocs.io/en/stable/) to retrieve the RDA data from [Sinopia via their API](https://ld4p.github.io/sinopia_api/), serialize it as RDF/XML, and to serialize the RML output BIBFRAME as JSON-LD. Input and output files are saved locally.

### Prerequisites
 - [RML Mapper](https://github.com/RMLio/rmlmapper-java)
    - [Instructions for downloading RML Mapper](https://docs.google.com/document/d/1ufe8nBblVOsVX0HGARHVScPS8arS7cnT0pGPumetdU4/edit?usp=sharing)
 - [rdflib](https://rdflib.readthedocs.io/en/stable/)
    - `$ pip3 install rdflib`
 - [rdflib JSON-LD plugin](https://github.com/RDFLib/rdflib-jsonld)
    - `$ pip3 install rdflib-jsonld`
 - UW Libraries' [RML repository](https://github.com/uwlib-cams/rml)
    - `$ git clone https://github.com/uwlib-cams/rml.git`
 - [progress](https://pypi.org/project/progress/)
    - `$ pip3 install progress`

### Running the script
The RML Mapper jarfile (default: `rmlmapper-java/target/rmlmapper-4.8.1-r262.jar`) must be in the `rml/rda-to-bf-conversion` directory.

From the `rda-to-bf-conversion` directory, run the script:
```
$ python3 rda-to-bf_2.9.py
```

_Note: this script may take upwards of an hour to complete._

When the script is complete, the input RDA files will be in the directory `rda-to-bf-conversion/input_` with the current date appended (e.g. `input_2021_03_22`). The output BIBFRAME will be in the directory `rda-to-bf-conversion/output_` also with the date appended (e.g. `output_2021_03_22`).

# Scripts run within rda-to-bf_2.9.py
## save_rda_locally.py
This script pulls UW resources from [Sinopia via their API](https://ld4p.github.io/sinopia_api/) using [rdflib](https://rdflib.readthedocs.io/en/stable/), and saves them locally as RDF/XML.

_To run separately from rda-to-bf_2.9.py:_
```
$ python3 save_rda_locally.py
```

## remove_extra_descriptions.py
This script removes triples from the RDA/RDF resources that are not describing the resource in question.

For example, this data:
```
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:bflc="https://doi.org/10.6069/uwlib.55.d.4#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>
  <rdf:Description rdf:about="https://api.sinopia.io/resource/0a4ea663-988e-474b-a25e-659b935b65a9">
    <bflc:hasCreatorCharacteristic rdf:resource="http://id.loc.gov/authorities/demographicTerms/dg2015060814"/>
  </rdf:Description>
	<rdf:Description rdf:about="http://id.loc.gov/authorities/demographicTerms/dg2015060814">
    <rdfs:label>Russians</rdfs:label>
  </rdf:Description>
```

Would be corrected to this:
```
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:bflc="https://doi.org/10.6069/uwlib.55.d.4#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>
  <rdf:Description rdf:about="https://api.sinopia.io/resource/0a4ea663-988e-474b-a25e-659b935b65a9">
    <bflc:hasCreatorCharacteristic rdf:resource="http://id.loc.gov/authorities/demographicTerms/dg2015060814"/>
  </rdf:Description>
```

_To run separately from rda-to-bf_2.9.py:_
```
$ python3 remove_extra_descriptions.py
```

## fix_URIs.py

This script looks for URIs in the RDA/RDF data that were mistakenly entered into Sinopia as literals and corrects them.

For example, this data:
```
<rdam:P30002>http://rdaregistry.info/termList/RDAMediaType/1007</rdam:P30002>
```
Would be corrected to this:
```
<rdam:P30002 rdf:resource="http://rdaregistry.info/termList/RDAMediaType/1007"/>
```

_To run separately from rda-to-bf_2.9.py:_
```
$ python3 fix_URIs.py
```

## fix_copyright_dates.py

In our Sinopia application profiles, the character "©" was included as a default value for RDA property P30007, "has copyright date", and catalogers could then edit this value to include the copyright year after the "©". In some of our RDA files, no copyright year was entered, leaving triples like:
```
<rdam:P30007 xml:lang="zxx">©</rdam:P30007>
```
This script goes through our RDA data and removes these meaningless triples.

_To run separately from rda-to-bf_2.9.py:_
```
$ python3 fix_copyright_dates.py
```

## transform_rda_to_bf.py

This script uses the [RML Mapper](https://github.com/RMLio/rmlmapper-java) to transform RDA/RDF data to BIBFRAME. It references RML scripts from [this directory](https://github.com/uwlib-cams/rml/tree/master/generateRML/rmlOutput). It uses [rdflib](https://rdflib.readthedocs.io/en/stable/) to serialize the output as RDF/XML.

_To run separately from rda-to-bf_2.9.py:_
```
$ python3 transform_rda_to_bf.py
```

## type_dates.py

This script goes through the BIBFRAME output and adds datatypes `xsd:dateTime`, `xsd:date`, `xsd:gYearMonth`, and `xsd:gYear` where applicable.

_To run separately from rda-to-bf_2.9.py:_
```
$ python3 type_dates.py
```
