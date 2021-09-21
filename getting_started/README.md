# Installing RML Mapper

## Install maven

 - Run the following commands  
`$ sudo apt update`  
`$ sudo apt install maven`

 - Confirm that the installation worked by asking for the version number  
`$ mvn -v`

## Clone the [RML Mapper GitHub Repository](https://github.com/RMLio/rmlmapper-java)  
`$ git clone https://github.com/RMLio/rmlmapper-java.git`

## Install using maven

 - Navigate to the directory that contains pom.xml  
`$ cd rmlmapper-java`

  - Run the following command:  
`$ mvn install`

_Note: the install seems to trip up while running the CSV tests. It may skip them (which is fine, unless you’re transforming CSV data), or the install may fail. If the install fails, instead of `mvn install`, run the following command instead:_  
`$ mvn install -Dmaven.test.skip=true`

 - Locate the jar file  
`$ cd target`

 - The directory should contain the following files:  
    - `original-rmlmapper-4.7.0-r152.jar`
    - `rmlmapper-4.7.0-r152.jar`  
_The numbers with these files may be different with future versions of RML Mapper._  

 - Try both to see which one works on your computer. (For mcm104, one would only work on WSL, while the other worked for Mac.)
 - Confirm the installation of RML Mapper worked by asking for the help menu  
`$ java -jar rmlmapper-4.7.0-r152.jar -h`

# Running RML Mapper

`java -jar rmlmapper-4.7.0-r152.jar -m RML_demo_map.ttl -s turtle`
_Name of jar file may be different on your computer_

# RML property cheat sheet
- All triples maps need to be classed as rr:TriplesMap
- All triples need ONE logical source, ONE subject map, and one or more predicate object maps

Properties in logical sources:
- [rml:source](http://semweb.mmlab.be/ns/rml#sourceName)
	- filepath to data for conversion
- [rml:referenceFormulation](http://semweb.mmlab.be/ns/rml#referenceFormulation)
	- ql:XPath, ql:JSONPath, or ql:CSV
- [rml:iterator](http://semweb.mmlab.be/ns/rml#iterator)
	- parent properties (default for our purposes is "RDF/Description")

Properties in subject map:
- When the subject is a resource...
	- [rml:reference](http://semweb.mmlab.be/ns/rml#reference)
		- For when the value exists somewhere in the data for conversion
	- [rr:constant](http://www.w3.org/ns/r2rml#constant)
		- For constant values that are the same every time
- When the subject is a blank node...
	- [rr:termType](http://www.w3.org/ns/r2rml#termType)
	  - [rr:BlankNode](http://www.w3.org/ns/r2rml#BlankNode)
- [rr:class](http://www.w3.org/ns/r2rml#class)

Properties in predicate object map:
- [rr:predicate](http://www.w3.org/ns/r2rml#predicate)
- [rr:objectMap](http://www.w3.org/ns/r2rml#objectMap)

Properties in object map:
- When the object is an IRI or literal...
	- [rml:reference](http://semweb.mmlab.be/ns/rml#reference)
		- For when the value exists somewhere in the data for conversion
	- [rr:constant](http://www.w3.org/ns/r2rml#constant)
		- For constant values that are the same every time
- When the object is a blank node...
	- [rr:parentTriplesMap](http://www.w3.org/ns/r2rml#parentTriplesMap)
- rr:termType
	- [rr:Literal](http://www.w3.org/ns/r2rml#Literal) (optional; this is the default)
	- [rr:IRI](http://www.w3.org/ns/r2rml#IRI)
	- [rr:BlankNode](http://www.w3.org/ns/r2rml#BlankNode)
- For literals with language tags...
	- [rr:language](http://www.w3.org/ns/r2rml#language)
		- use for constant language tag (e.g. if it will ALWAYS be English, use "en")
	- [rml:languageMap](http://semweb.mmlab.be/ns/rml#languageMap)
		- use when the language tag depends on the data for conversion

Properties in language map:
- [rml:reference](http://semweb.mmlab.be/ns/rml#reference)
	- For when the value exists somewhere in the data for conversion

# Troubleshooting

 - Most error messages in the mapper are not very descriptive, so pay close attention to your mapping!
 - When changing the value for `rml:source` (i.e. the location of your source data), make sure you change it in _every_ triples map in your mapping file!
 - If you have reorganized your files, make sure your mapping is updated so the `rml:source` reflects the new file paths!
 - Sometimes RML gets tripped up on file permissions for the source data or for the mapping document. This can be fixed using `chmod`, e.g.  
`$ chmod u+rwx RML_demo_data.xml`
