# Table of Contents
 - [Install RML Mapper](https://github.com/uwlib-cams/rml/tree/master/getting_started#installing-rml-mapper)
    - [Install using WSL & Ubuntu](https://github.com/uwlib-cams/rml/tree/master/getting_started#install-using-wsl--ubuntu)
    - [Install using Windows PowerShell](https://github.com/uwlib-cams/rml/tree/master/getting_started#install-using-windows-powershell)
 - [Running RML Mapper](https://github.com/uwlib-cams/rml/tree/master/getting_started#running-rml-mapper)
 - [RML property cheat sheet](https://github.com/uwlib-cams/rml/tree/master/getting_started#rml-property-cheat-sheet)
 - [Troubleshooting](https://github.com/uwlib-cams/rml/tree/master/getting_started#troubleshooting)

# Installing RML Mapper

## Install using WSL & Ubuntu
### Install WSL
_For Windows users only_
 - [Instructions for installing WSL on Windows 10 or higher](https://docs.microsoft.com/en-us/windows/wsl/install)
 - [Instructions for installing WSL on older versions](https://docs.microsoft.com/en-us/windows/wsl/install-manual)

### Download Ubuntu
_For Windows users only_
 - [Download Ubuntu](https://ubuntu.com/download/desktop)

### Install maven

 - Run the following commands  
```
$ sudo apt update
$ sudo apt install maven
```

 - Confirm that the installation worked by asking for the version number  
```
$ mvn -v
```

### Clone the [RML Mapper GitHub Repository](https://github.com/RMLio/rmlmapper-java)  
```
$ git clone https://github.com/RMLio/rmlmapper-java.git
```

### Install using maven

 - Navigate to the directory that contains pom.xml

```
$ cd rmlmapper-java
```

  - Run the following command:

```
$ mvn install
```

_Note: the install seems to trip up while running the CSV tests. It may skip them (which is fine, unless you’re transforming CSV data), or the install may fail. If the install fails, instead of `mvn install`, run the following command instead:_

```
$ mvn install -Dmaven.test.skip=true
```

 - Locate the jar file

```
$ cd target
```

 - The directory should contain the following files:  
    - `rmlmapper-[version number].jar`
    - `rmlmapper-[version number]-all.jar`  
 - Try both to see which one works on your computer. (For mcm104, one would only work on WSL, while the other worked for Mac.)
 - Confirm the installation of RML Mapper worked by asking for the help menu

```
$ java -jar rmlmapper-[version number].jar -h
```

 - The .jar file(s) can be renamed using the [mv command](https://en.wikipedia.org/wiki/Mv_(Unix)) for ease of use, e.g. to mapper.jar or rmlmapper.jar

```
$ mv rmlmapper-[version number].jar mapper.jar
```

```
$ mv rmlmapper-[version number]-all.jar mapper.jar
```

## Install using Windows PowerShell

### Install JAVA
 - [Download JAVA](https://www.java.com/download/ie_manual.jsp)
 - Set JAVA_HOME environment variable:

```
System Variable
  Variable name: JAVA_HOME
  Variable value: [path to your jdk]\jdk1.8.0_291  
```

### Install maven
 - [Download binary zip archive](https://maven.apache.org/download.cgi)
 - Unzip to desired location
 - In PowerShell, run:

```
$ Expand-Archive -LiteralPath '<path to maven zip file downloaded above>' -DestinationPath '<path where maven should go>'
```

 - Add maven bin directory to the "Path" environment variable
 - Check to make sure it works
	- This should output maven info:

```
$ mvn-v
```

### Clone the [RML Mapper GitHub Repository](https://github.com/RMLio/rmlmapper-java) 

```
$ git clone https://github.com/RMLio/rmlmapper-java.git
```

### Install using maven
 - Navigate to the directory that contains pom.xml
```
$ cd rmlmapper-java
```
 - Run the following command:
```
$ mvn install -DskipTests
```

 - Locate the jar file

```
$ cd target
```

 - The directory should contain the following files:  
    - `rmlmapper-[version number].jar`
    - `rmlmapper-[version number]-all.jar`
 - The `-all` file is the one to use.
 - Confirm the installation of RML Mapper worked by asking for the help menu

```
$ java -jar rmlmapper-[version number]-all.jar -h
```

 - The .jar file(s) can be renamed using the [cp command](https://en.wikipedia.org/wiki/Cp_(Unix)) for ease of use, e.g. to mapper.jar or rmlmapper.jar

```
$ cp rmlmapper-[version number]-all.jar mapper.jar
```

### (Optional) Create an environment variable
 - If you want to create an environment variable for the path to the jar file, you can
 - Access in PowerShell using $Env
 - For example, if you name the path `rmlm`, you could run the help command like this:
```
$ java -jar $Env:rmlm:mapper.jar -h
```

# Running RML Mapper

```
$ java -jar mapper.jar -m RML_demo_map.ttl -s turtle
```
 - The `-m` variable is followed by the filepath to our RML map
 - The `-s` variable is optional, and chooses our output serialization. The default is nquads, so for ease of reading, you can choose to output in Turtle instead.
 - [See list of all variables here](https://github.com/RMLio/rmlmapper-java#cli)

# RML property cheat sheet
- All triples maps need to be classed as rr:TriplesMap
- All triples need ONE logical source, ONE subject map, and one or more predicate object maps

## Properties in logical sources
- [rml:source](http://semweb.mmlab.be/ns/rml#sourceName)
	- filepath to data for conversion
- [rml:referenceFormulation](http://semweb.mmlab.be/ns/rml#referenceFormulation)
	- ql:XPath, ql:JSONPath, or ql:CSV
- [rml:iterator](http://semweb.mmlab.be/ns/rml#iterator)
	- parent properties (default for our purposes is "RDF/Description")

## Properties in subject map
- [rr:class](http://www.w3.org/ns/r2rml#class)
### When the subject is a resource...
- [rml:reference](http://semweb.mmlab.be/ns/rml#reference)
	- For when the value exists somewhere in the data for conversion
- [rr:constant](http://www.w3.org/ns/r2rml#constant)
	- For constant values that are the same every time
### When the subject is a blank node...
- [rr:termType](http://www.w3.org/ns/r2rml#termType)
  - [rr:BlankNode](http://www.w3.org/ns/r2rml#BlankNode)

## Properties in predicate object map
- [rr:predicate](http://www.w3.org/ns/r2rml#predicate)
- [rr:objectMap](http://www.w3.org/ns/r2rml#objectMap)

## Properties in object map
- rr:termType
	- [rr:Literal](http://www.w3.org/ns/r2rml#Literal) (optional; this is the default)
	- [rr:IRI](http://www.w3.org/ns/r2rml#IRI)
	- [rr:BlankNode](http://www.w3.org/ns/r2rml#BlankNode)
### When the object is an IRI or literal...
- [rml:reference](http://semweb.mmlab.be/ns/rml#reference)
	- For when the value exists somewhere in the data for conversion
- [rr:constant](http://www.w3.org/ns/r2rml#constant)
	- For constant values that are the same every time
### When the object is a blank node...
- [rr:parentTriplesMap](http://www.w3.org/ns/r2rml#parentTriplesMap)
### For literals with language tags...
- [rr:language](http://www.w3.org/ns/r2rml#language)
	- use for constant language tag (e.g. if it will ALWAYS be English, use "en")
- [rml:languageMap](http://semweb.mmlab.be/ns/rml#languageMap)
	- use when the language tag depends on the data for conversion

## Properties in language map:
- [rml:reference](http://semweb.mmlab.be/ns/rml#reference)
	- For when the value exists somewhere in the data for conversion

# Troubleshooting

 - Most error messages in the mapper are not very descriptive, so pay close attention to your mapping!
 - When changing the value for `rml:source` (i.e. the location of your source data), make sure you change it in _every_ triples map in your mapping file!
 - If you have reorganized your files, make sure your mapping is updated so the `rml:source` reflects the new file paths!
 - Sometimes RML gets tripped up on file permissions for the source data or for the mapping document. This can be fixed using `chmod`, e.g.  
`$ chmod u+rwx RML_demo_data.xml`
