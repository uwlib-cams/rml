# rml
Utilizing the [RDF Mapping Language (RML)](https://rml.io/specs/rml/) and [RML Mapper](https://github.com/RMLio/rmlmapper-java) to transform data from RDA/RDF to BIBFRAME.

# rda-to-bf-conversion
## RDA-to-BF Transform

The RDA-to-BF transform (rml_2.6.py) is a script that pulls RDA data from [Sinopia](https://sinopia.io/) and runs them through [RML Mapper](https://github.com/RMLio/rmlmapper-java) using RML code from UW Libraries to output BIBFRAME data. The script uses [rdflib](https://rdflib.readthedocs.io/en/stable/) to retrieve the RDA data from [Sinopia via their API](https://ld4p.github.io/sinopia_api/), serialize it as RDF/XML, and to serialize the RML output BIBFRAME as JSON-LD. Input and output files are saved locally. The [ElementTree XML API](https://docs.python.org/3/library/xml.etree.elementtree.html) is used to update IRIs in the output data with new ones generated using the [UUID Python module](https://docs.python.org/3/library/uuid.html).

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
$ python3 rml_2.6.py
```

_Note: this script may take upwards of an hour to complete._

When the script is complete, the input RDA files will be in the directory `rml/input` in a new directory named after the current date (e.g. `2020_8_25`). The output BIBFRAME will be in the directory `rml/output` also in a directory named after the date.

# findBadFiles.py

In earlier versions of rml.py, an error occurred in which the identifier which serves as the filename for a given record (e.g. [003c0e59-9ab1-4fc2-8522-1a7b78601fef.ttl](https://github.com/uwlib-cams/rml/blob/master/output/2020_9_2/work_1/003c0e59-9ab1-4fc2-8522-1a7b78601fef.ttl) is the output for the record represented here: [https://trellis.sinopia.io/repository/washington/003c0e59-9ab1-4fc2-8522-1a7b78601fef](https://trellis.sinopia.io/repository/washington/003c0e59-9ab1-4fc2-8522-1a7b78601fef)) did _not_ match the contents of the file. For example, previous rml.py output with filename [0010d9b0-ec29-4ab0-b25a-9a1a87108dd2.ttl](https://github.com/uwlib-cams/rml/blob/master/old/output/2020_8_31/instance/0010d9b0-ec29-4ab0-b25a-9a1a87108dd2.ttl) instead contained the output for [https://trellis.sinopia.io/repository/washington/0b5f373d-a838-49d1-9f92-b65522c741a5](https://trellis.sinopia.io/repository/washington/0b5f373d-a838-49d1-9f92-b65522c741a5).

This error has been addressed in newer versions of rml.py, but this script can be used to ensure that this error has not occurred. For both input and output files for a given date, the script will check that each file contains the data for the record it is named for. It outputs a report to badFileReport.txt. An example of usage:
```
$ python3.6 findBadFiles.py 2020_09_18
```

The output for this command is:
```
Total number of bad files: 0
Bad input files: 0
Bad output files: 0

***
```

For an example with a flawed dataset, a full report for the 2020_8_31 output can be viewed [here](https://github.com/uwlib-cams/rml/blob/master/old/badFileReport.txt).
