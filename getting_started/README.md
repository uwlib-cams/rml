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
_The numbers with this file may be different with future versions of RML Mapper._  

 - The correct jar file is the latter (`rmlmapper-4.7.0-r152.jar`)
 - Confirm the installation of RML Mapper worked by asking for the help menu  
`$ java -jar rmlmapper-4.7.0-r152.jar -h`

# Running RML Mapper

`java -jar rmlmapper-4.7.0-r152.jar -m RML_demo_map.ttl -s turtle`

# Troubleshooting

 - Most error messages in the mapper are not very descriptive, so pay close attention to your mapping!
 - When changing the value for `rml:source` (i.e. the location of your source data), make sure you change it in _every_ triples map in your mapping file!
 - If you have reorganized your files, make sure your mapping is updated so the `rml:source` reflects the new file paths!
 - Sometimes RML gets tripped up on file permissions for the source data or for the mapping document. This can be fixed using `chmod`, e.g.  
`$ chmod u+rwx RML_demo_data.xml`
