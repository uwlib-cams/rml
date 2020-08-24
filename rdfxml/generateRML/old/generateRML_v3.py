import csv
import rdflib
from rdflib import *
import os
from sys import argv

script, csv_file_path = argv

"""Lists"""

prefix_list = [
"@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.",
"@prefix bflc: <http://id.loc.gov/ontologies/bflc/>.",
"@prefix dbo: <http://dbpedia.org/ontology/>.",
"@prefix ex: <http://example.org/rules/>.",
"@prefix madsrdf: <http://www.loc.gov/mads/rdf/v1#>.",
"@prefix rdae: <http://rdaregistry.info/Elements/e/>.",
"@prefix rdai: <http://rdaregistry.info/Elements/i/>.",
"@prefix rdam: <http://rdaregistry.info/Elements/m/>.",
"@prefix rdamdt: <http://rdaregistry.info/Elements/m/datatype/>.",
"@prefix rdau: <http://rdaregistry.info/Elements/u/>.",
"@prefix rdaw: <http://rdaregistry.info/Elements/w/>.",
"@prefix rdax: <https://doi.org/10.6069/uwlib.55.d.4#>.",
"@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.",
"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.",
"@prefix rml: <http://semweb.mmlab.be/ns/rml#>.",
"@prefix rr: <http://www.w3.org/ns/r2rml#>.",
"@prefix ql: <http://semweb.mmlab.be/ns/ql#>.",
"@prefix schema: <http://schema.org/>.",
"@prefix sin: <http://sinopia.io/vocabulary/>.",
"@prefix skos: <http://www.w3.org/2004/02/skos/core#>.\n"
]

"""Functions to generate RML code"""

def generate_logical_source(map_name="Work", file_path="!!workID!!"):
    logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source "/home/mcm104/{file_path}.xml";
    rml:referenceFormulation ql:XPath;
    rml:iterator "/RDF/Description[type/@resource='http://rdaregistry.info/Elements/c/C10001']"
  ].\n"""
    return logical_source

def generate_bnode_logical_source(property_number, map_name, not_resource=False, file_path="!!workID!!"):
    if not_resource == False:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}]\"
  ].\n"""
    else:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}[not(@resource)]]\"
  ].\n"""
    return bnode_logical_source

def generate_subject_map(map_name="Work", subject_type="main", class_name="Work"):
    if ":" not in class_name:
        class_name = f"bf:{class_name}"
    if subject_type == "main":
        line_2 = 'rml:reference "@about"'
    elif subject_type == "bnode":
        line_2 = "rr:termType rr:BlankNode"
    else:
        print('Subject map error: Subject type must be "main" or "bnode"')
    subject_map = f"""ex:{map_name}Map rr:subjectMap [
  {line_2};
  rr:class {class_name}
].\n"""
    return subject_map

def generate_IRI_po_map(property, predicate, map_name="Work"):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    IRI_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rml:reference \"{property}/@resource\";
    rr:termType rr:IRI
  ]
].\n"""
    return IRI_po_map

def generate_literal_po_map(property, predicate, map_name="Work"):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rml:reference \"{property}[not(@resource)][@lang]\";
    rr:termType rr:Literal;
    rml:languageMap [
      rml:reference \"{property}/@lang\"
    ]
  ]
].

ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rml:reference \"{property}[not(@resource) and not(@lang)]\";
    rr:termType rr:Literal
  ]
].\n"""
    return literal_po_map

def generate_bnode_po_map(predicate, bnode_map_name, map_name="Work"):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    bnode_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:parentTriplesMap ex:{bnode_map_name}Map
  ]
].\n"""
    return bnode_po_map

def generate_constant_IRI(IRI_value, predicate, map_name="Work"):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    constant_IRI_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:constant \"{IRI_value}\";
    rr:termType rr:IRI
  ]
].\n"""
    return constant_IRI_po_map

def generate_constant_literal(literal_value, predicate="rdfs:label", map_name="Work", language="en"):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    constant_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:constant {literal_value};
    rr:termType rr:Literal;
    rr:language \"{language}\"
  ]
].\n"""
    return constant_literal_po_map

"""Get property numbers and kiegel mappings from CSV"""

property_number_list = ["P10008"]

kiegel_mapping_list = ["""contribution >> Contribution > agent >> Organization > rdfs:label ; > role=<http://id.loc.gov/vocabulary/relators/prn>"""]

#with open(str(csv_file_path)) as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=',')
#    line_count = 0
#    for line in csv_reader:
#        if line_count == 0: # ignore header row
#            pass
#        else:
#            prop_IRI = line[1]
#            prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/w/')
#            property_number_list.append(prop_num)

#            kiegel = line[3]
#            kiegel_mapping_list.append(kiegel)
#        line_count = line_count + 1

"""Start main RML map"""

RML_list = []

for prefix in prefix_list:
    RML_list.append(prefix + "\n")

main_logical_source = generate_logical_source()
RML_list.append(main_logical_source + "\n")

main_subject_map = generate_subject_map()
RML_list.append(main_subject_map + "\n")

"""Iterate through kiegel mappings and generate RML"""

num_of_properties = len(property_number_list)

property_range = range(0, num_of_properties)

bnode_map_number = 1

for number in property_range:
    property_number = property_number_list[number]

    kiegel = kiegel_mapping_list[number]

    kiegel_list = kiegel.split("\nor\n")

#    for map in kiegel_list: # i shouldn't need this anymore with commas in map being replaces w semicolons
#        new_kiegel_list = []
#        if "," in map:
#            if '"' not in map:
#                comma_split = map.split(", ")
#                for map in comma_split:
#                    new_kiegel_list.append(map)
#            else:
#                new_kiegel_list.append(map)
#        else:
#            new_kiegel_list.append(map)

    kiegel_list = new_kiegel_list

    if len(kiegel_list) > 1: # if there are different maps for IRIs and literals
        if ">>" in kiegel_list[0]: # if there is a blank node in the first map
            if ">>" in kiegel_list[1]:  # if there is a blank node in the second map
                not_resource = False
            else:
                not_resource = True
        else:
            not_resource = True
    else:
        not_resource = False

    for map in kiegel_list:
        if "Title" in map:
            not_resource = False

        map_list = map.split(" ")

        map_list_length = len(map_list)

        map_list_range = range(0, map_list_length)

        index_list = []

        # this loop makes sure that string literals that contain spaces are not separated
        for n in map_list_range:
            literal_value = "x"

            item = map_list[n]

            if len(item) > 0: # make sure it has characters to check
                continue_search = True
            else:
                continue_search = False

            if continue_search == True:
                if "=" in item: # check if constant
                    continue_search = True
                else:
                    continue_search = False
            else:
                pass

            if continue_search == True:
                if '"' in item: # check if literal constant
                    continue_search = True
                else:
                    continue_search = False

            if continue_search == True:
                if item[-1] != '"': # check if the last character is "; if not, the rest has been cut off
                    literal_value = item # start new literal
                    index_list.append(n) # record index in list
                    continue_search = True
                else:
                    continue_search = False

            while continue_search == True:
                n = n + 1
                item = map_list[n]
                literal_value = literal_value + " " + item # add to literal
                index_list.append(n) # record index in list

                if item[-1] != '"': # check if the literal is over now
                    continue_search = True
                else:
                    continue_search = False

            if len(literal_value) > 1:
                for num in reversed(index_list):
                    map_list.pop(num)
                map_list.insert(index_list[0], literal_value)
                break

        if len(map_list) == 1:
            if "*" in map: # if there is a *, i.e. if it takes an IRI value...
                predicate_name = map.strip("*") # remove the * to get the property name

                po_map = generate_IRI_po_map(property_number, predicate_name)

            else: # it takes a literal value
                predicate_name = map
                po_map = generate_literal_po_map(property_number, predicate_name)

            RML_list.append(po_map + "\n")

        elif len(map_list) > 1:
            predicate_name = map_list[0]

            semicolon_test = False

            for item in map_list:
                if item == ";":
                    semicolon_test = True

            if semicolon_test == True:
                print("CODE MISSING: 306")

            else:
                if map_list[1] == ">>":
                    # generate a predicate-object map that opens a blank node
                    bnode_map_name = predicate_name.capitalize() + "_" + str(bnode_map_number) + "_"
                    bnode_map_number = bnode_map_number + 1
                    po_map = generate_bnode_po_map(predicate_name, bnode_map_name)
                    RML_list.append(po_map + "\n")

                    # generate a new triples map
                    bnode_logical_source = generate_bnode_logical_source(property_number, bnode_map_name, not_resource)
                    RML_list.append(bnode_logical_source + "\n")

                    # generate a subject map for the new triples map
                    class_name = map_list[2]
                    subject_map = generate_subject_map(bnode_map_name, "bnode", class_name)
                    RML_list.append(subject_map + "\n")

                    # populate the blank node
                    rest_of_mapping = range(4, len(map_list)) # start with 4 because map_list[3] will always be > in this scenario

                    start_bnode_here = 0

                    for num in rest_of_mapping:
                        item = map_list[num]

                        if item == ">":
                            pass

                        elif "*" in item: # it takes an IRI value...
                            predicate_name = item.strip("*") # remove the * to get the property name
                            po_map = generate_IRI_po_map(property_number, predicate_name, bnode_map_name)
                            RML_list.append(po_map + "\n")

                        elif "=" in item: # it's a constant value...
                            predicate_constant = item.split("=")
                            predicate_name = predicate_constant[0]
                            constant_value = predicate_constant[1]

                            if ">" in constant_value: # the constant is an IRI
                                constant_value = constant_value.strip("<")
                                constant_value = constant_value.strip(">")

                                po_map = generate_constant_IRI(constant_value, predicate_name, bnode_map_name)
                                RML_list.append(po_map + "\n")

                            else: # the constant is a literal
                                po_map = generate_constant_literal(constant_value, predicate_name, bnode_map_name)
                                RML_list.append(po_map + "\n")

                        elif item == "rdfs:label": # it takes a literal value...
                            predicate_name = "rdfs:label"
                            po_map = generate_literal_po_map(property_number, predicate_name, bnode_map_name)
                            RML_list.append(po_map + "\n")

                        elif item == ">>": # blank node within a blank node
                            start_bnode_here = num - 1
                            break

                        else:
                            predicate_name = item
                            po_map = generate_literal_po_map(property_number, predicate_name, bnode_map_name)
                            RML_list.append(po_map + "\n")

                    if start_bnode_here > 0: # opening a blank node within a blank node
                        predicate_name = map_list[start_bnode_here]
                        bnode_map_name_2 = predicate_name.capitalize() + "_" + str(bnode_map_number) + "_"
                        po_map = generate_bnode_po_map(predicate_name, bnode_map_name_2, bnode_map_name)
                        RML_list.append(po_map + "\n")

                        bnode_logical_source = generate_bnode_logical_source(property_number, bnode_map_name_2)
                        RML_list.append(bnode_logical_source + "\n")

                        class_name = map_list[start_bnode_here + 2] # because + 1 would be the >>

                        bnode_subject_map = generate_subject_map(bnode_map_name_2, "bnode", class_name)
                        RML_list.append(bnode_subject_map + "\n")

                        # start_bnode_here + 3 = ">"

                        rest_of_mapping_2 = range(start_bnode_here+4, len(map_list))

                        for num in rest_of_mapping_2:
                            item = map_list[num] # map_list[10] = rdfs:label

                            if item == ">":
                                pass

                            elif "*" in item: # it takes an IRI value...
                                predicate_name = item.strip("*") # remove the * to get the property name
                                po_map = generate_IRI_po_map(property_number, predicate_name, bnode_map_name_2)
                                RML_list.append(po_map + "\n")

                            elif "=" in item:
                                predicate_constant = item.split("=")
                                predicate_name = predicate_constant[0]
                                constant_value = predicate_constant[1]

                                if ">" in constant_value: # the constant is an IRI
                                    constant_value = constant_value.strip("<")
                                    constant_value = constant_value.strip(">")

                                    po_map = generate_constant_IRI(constant_value, predicate_name, bnode_map_name_2)
                                    RML_list.append(po_map + "\n")

                                elif item == "rdfs:label":
                                    predicate_name = "rdfs:label"
                                    po_map = generate_literal_po_map(property_number, predicate_name, bnode_map_name_2)
                                    RML_list.append(po_map + "\n")

                                else:
                                    pass

                            elif "label" in item:
                                predicate_name = "rdfs:label"
                                po_map = generate_literal_po_map(property_number, predicate_name, bnode_map_name_2)
                                RML_list.append(po_map + "\n")

                            elif item == ">>": # blank node within a blank node
                                print("CODE MISSING: 426")

                            else:
                                pass

                        start_bnode_here = 0
                else:
                    print("CODE MISSING: 433")

with open("rml_output.ttl", "w") as output_file:
    for code in RML_list:
        output_file.write(code)
