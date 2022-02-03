# rda-to-bf-conversion-for-sinopia
The RDA-to-BF transform (rda-to-bf-for-sinopia.py) is a script that pulls RDA data from [Sinopia](https://sinopia.io/) and runs them through [RML Mapper](https://github.com/RMLio/rmlmapper-java) using RML code from UW Libraries to output BIBFRAME data. The script uses [rdflib](https://rdflib.readthedocs.io/en/stable/) to retrieve the RDA data from [Sinopia via their API](https://ld4p.github.io/sinopia_api/) and to serialize it in different formats as necessary throughout the transformation process. Input and output files are saved locally. The [ElementTree XML API](https://docs.python.org/3/library/xml.etree.elementtree.html) is used to update IRIs in the output data with new ones generated using the [UUID Python module](https://docs.python.org/3/library/uuid.html).

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

		### Arguments
		| Argument | Default | Description |
		|---|---|---|
		| -s/--source | <https://api.sinopia.io/resource?limit=1000&group=washington> | URI for RDA data for transformation |
		| -i/--input | RDA | Desired location for RDA files (saved locally during transformation) |
		| -o/--output | BIBFRAME | Desired location for BIBFRAME files (saved locally during transformation) |
		| -v/--version | N/A | Date of last update for transform |

### Running the script
_Note: the RML Mapper `.jar` file must be in the `rml/rda-to-bf-conversion-for-sinopia` directory._

From the `rda-to-bf-conversion` directory, run the script:
```
$ python3 rda-to-bf-for-sinopia.py
```

_Note: this script may take upwards of an hour to complete._
