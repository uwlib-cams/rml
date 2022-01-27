# rml
This repository is used by the University of Washington Linked Data Team to utilize the [RDF Mapping Language (RML)](https://rml.io/specs/rml/) and [RML Mapper](https://github.com/RMLio/rmlmapper-java) to transform data from RDA/RDF to BIBFRAME.

## [generateRML](https://github.com/uwlib-cams/rml/tree/master/generateRML)
Contains the code for converting UW's [RDA-to-BIBFRAME-map](https://docs.google.com/spreadsheets/d/1y0coXcJAoVOP2BPtzwmnc9l-OWQbwYujVJ8oXXYpMRc/edit?usp=sharing) into RML triples maps.

## [input](https://github.com/uwlib-cams/rml/tree/master/input)
UW's RDA/RDF data, created by UW catalogers in [Sinopia](https://sinopia.io/) as part of [LD4P2](https://wiki.lyrasis.org/display/LD4P2). Data in this directory is organized by the date when the data was pulled from Sinopia.

## [output](https://github.com/uwlib-cams/rml/tree/master/output)
UW's BIBFRAME data, created by transforming our RDA/RDF data using RML code. Data in this directory is organized by the date when the transformation was performed.

## [rda-to-bf-conversion-for-sinopia](https://github.com/uwlib-cams/rml/tree/master/rda-to-bf-conversion-for-sinopia)
Contains the code for transforming RDA/RDF data into BIBFRAME using the RML generated in [generateRML](https://github.com/uwlib-cams/rml/tree/master/generateRML).
