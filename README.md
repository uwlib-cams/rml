# rml
Assessing the [RDF Mapping Language (RML)](https://rml.io/specs/rml/) and [RML Mapper](https://github.com/RMLio/rmlmapper-java) for use with library data.

# rml.py
## RDA-to-BF Transform

The RDA-to-BF transform (rml.py) is a script that pulls RDA data from [Trellis](https://trellis.sinopia.io/repository/washington) and runs them through [RML Mapper](https://github.com/RMLio/rmlmapper-java) using RML code from UW Libraries to output BIBFRAME data. [rdflib](https://rdflib.readthedocs.io/en/stable/) is used to retrieve the RDA data from Trellis, serialize it as RDF/XML, and to serialize the output BIBFRAME as Turtle. Input and output files are saved locally.

### Prerequisites
 - [RML Mapper](https://github.com/RMLio/rmlmapper-java)
    - [Instructions for downloading RML Mapper](https://docs.google.com/document/d/1ufe8nBblVOsVX0HGARHVScPS8arS7cnT0pGPumetdU4/edit?usp=sharing)
 - [rdflib](https://rdflib.readthedocs.io/en/stable/)
    - `$ pip3 install rdflib`
 - UW Libraries' [RML repository](https://github.com/uwlib-cams/rml)
    - `$ git clone https://github.com/uwlib-cams/rml.git`
 - [progress](https://pypi.org/project/progress/)
    - `$ pip3 install progress`

### Running the script
The RML Mapper jarfile (default: `rmlmapper-java/target/rmlmapper-4.8.1-r262.jar`) must be in the `rml` directory.

From the `rml` directory, run the script:
```
$ python3.6 rml.py
```

Be warned: this script does run slowly. It will take upwards of an hour to complete.

When the script is complete, the input RDA files will be in the directory `rml/input` in a new directory named after the current date (e.g. `2020_8_25`). The output BIBFRAME will be in the directory `rml/output` also in a directory named after the date.

# fix_copyright_dates.py

In our Sinopia application profiles, the character "©" was included as a default value for RDA property P30007, "has copyright date", and catalogers could then input the copyright year after the "©". In some of our RDA files, no copyright year was entered, leaving triples like:
```
<rdam:P30007 xml:lang="zxx">©</rdam:P30007>
```
This script goes through our RDA data and removes these meaningless triples. It is run within `rml.py`.

# fix_URIs.py

As a result of errors while cataloging in Sinopia, some values that should have been entered as URIs were instead recorded as being literals.
For example:
```
<rdam:P30002 rdf:resource="http://rdaregistry.info/termList/RDAMediaType/1007"/>
```
would instead be written as:
```
<rdam:P30002>http://rdaregistry.info/termList/RDAMediaType/1007</rdam:P30002>
```
This script goes through our RDA data and rewrites these lines so URIs are treated as URIs. It is run within `rml.py`.

# langtags.py

In the process of serializing our BIBFRAME output, language tags which are correct in the original RDA-in-RDF/XML are incorrect in our Turtle output (e.g. `@eng`, `@rus`, etc.). This script finds these language tags in our output and replaces them with the correct language tags for the Turtle syntax (e.g. `@eng` becomes `@en`, `@rus` becomes `@ru`, etc.) This script is run within `rml.py`.

# type_dates.py

This script goes through our BIBFRAME data and adds datatypes `xsd:dateTime`, `xsd:date`, `xsd:gYearMonth`, and `xsd:gYear` where applicable. The script is run within `rml.py`.

# findBadFiles.py

In earlier versions of rml.py, an error occurred in which the Trellis identifier which serves as the filename for a given record (e.g. [003c0e59-9ab1-4fc2-8522-1a7b78601fef.ttl](https://github.com/uwlib-cams/rml/blob/master/output/2020_9_2/work_1/003c0e59-9ab1-4fc2-8522-1a7b78601fef.ttl) is the output for the record represented here: [https://trellis.sinopia.io/repository/washington/003c0e59-9ab1-4fc2-8522-1a7b78601fef](https://trellis.sinopia.io/repository/washington/003c0e59-9ab1-4fc2-8522-1a7b78601fef)) did _not_ match the contents of the file. For example, previous rml.py output with filename [0010d9b0-ec29-4ab0-b25a-9a1a87108dd2.ttl](https://github.com/uwlib-cams/rml/blob/master/old/output/2020_8_31/instance/0010d9b0-ec29-4ab0-b25a-9a1a87108dd2.ttl) instead contained the output for [https://trellis.sinopia.io/repository/washington/0b5f373d-a838-49d1-9f92-b65522c741a5](https://trellis.sinopia.io/repository/washington/0b5f373d-a838-49d1-9f92-b65522c741a5).

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

# sample_record.py

This script goes line-by-line through the records in a given directory of RDF/XML files to compile a new RDF/XML file with an example of each RDA property that is present in the sample data. It creates separate files for work, expression, manifestation, and item properties. The output goes to `rml/input/sample_records/`.

Example:
```
$ python3.6 sample_record.py 2020_09_29
```

# type_date.py

This script goes line-by-line through the records in a given directory of Turtle files to add datatypes to values of the following BIBFRAME date properties: bf:date, bf:originDate, bf:legalDate, bf:copyrightDate, bf:changeDate, bf:creationDate, bf:generationDate.

For values formatted as "YYYY", the script adds `^^xsd:gYear`. For values formatted as "YYYY-MM", it adds `^^xsd:gYearMonth`. For values formatted as "YYYY-MM-DD", it adds `^^xsd:date`.

Example:
```
$ python3.6 type_dates.py 2020_09_29
```
