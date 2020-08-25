# RDA-to-BF Transform

The RDA-to-BF transform (rml.py) is a script that pulls RDA data from [Trellis](https://trellis.sinopia.io/repository/washington) and runs them through [RML Mapper](https://github.com/RMLio/rmlmapper-java) using RML code from UW Libraries to output BIBFRAME data. [rdflib](https://rdflib.readthedocs.io/en/stable/) is used to retrieve the RDA data from Trellis, serialize it as RDF/XML, and to serialize the output BIBFRAME as Turtle. Input and output files are saved locally.

# Prerequisites
 - [RML Mapper](https://github.com/RMLio/rmlmapper-java)
 --- [Instructions for downloading RML Mapper](https://docs.google.com/document/d/1ufe8nBblVOsVX0HGARHVScPS8arS7cnT0pGPumetdU4/edit?usp=sharing)
 - [rdflib](https://rdflib.readthedocs.io/en/stable/)
 --- `$ pip install rdflib`
 - UW Libraries' [RML repository](https://github.com/uwlib-cams/rml)
 --- `$ git clone https://github.com/uwlib-cams/rml.git`

# Running the script
The RML Mapper jarfile (default: `rmlmapper-java/target/rmlmapper-4.8.1-r262.jar`) must be in the `rdfxml` directory of the UW RML repository (`rml/rdfxml/`).

From the `rdfxml` directory, run the script:
```python3.6 rml.py```

Be warned: this script does run slowly. It will take a while to complete.

When the script is complete, the input RDA files will be in the directory `rml/rdfxml/input` in a new directory named after the current date (e.g. `2020_8_25`). The output BIBFRAME will be in the directory `rml/rdfxml/output` also in a directory named after the date.

The namespaces in both the input and output files will have default names (e.g. `ns1`). These can be replaced with descriptive namespaces using the scripts `namespace_xml.py` and `namespace_ttl.py`. These scripts each take as an argument the name of the directory containing the files to be edited. For example:
`python3.6 namespace_xml.py 2020_8_25`
`python3.6 namespace_ttl.py 2020_8_25`
