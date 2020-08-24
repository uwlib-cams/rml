import csv
import rdflib
from rdflib import *
import os
from sys import argv

script, csv_dir = argv

"""Functions to generate RML code"""

def generate_logical_source(map_name, file_path):
    if "work" in file_path:
        entity_number = "1"
    elif "expression" in file_path:
        entity_number = "6"
    elif "manifestation" in file_path:
        entity_number = "7"
    elif "item" in file_path:
        entity_number = "3"
    logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source "/home/mcm104/rml/rdfxml/data/{file_path}.xml";
    rml:referenceFormulation ql:XPath;
    rml:iterator "/RDF/Description[type/@resource='http://rdaregistry.info/Elements/c/C1000{entity_number}']"
  ].\n"""
    return logical_source

def generate_bnode_logical_source(property_number, map_name, not_resource, file_path):
    if not_resource == False:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/rdfxml/data/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}]\"
  ].\n"""
    else:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/rdfxml/data/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}[not(@resource)]]\"
  ].\n"""
    return bnode_logical_source

def generate_subject_map(map_name, class_name, subject_type="main"):
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

def generate_IRI_po_map(property, predicate, map_name):
    predicate = predicate.strip("*")
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

def generate_literal_po_map(property, predicate, map_name):
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

def generate_bnode_po_map(predicate, bnode_map_name, map_name):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    bnode_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:parentTriplesMap ex:{bnode_map_name}Map
  ]
].\n"""
    return bnode_po_map

def generate_constant_IRI(IRI_value, predicate, map_name):
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

def generate_constant_literal(literal_value, predicate, map_name, language="en"):
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

def generate_constant(node, map_name):
    predicate_constant = node.split("=")
    predicate_name = predicate_constant[0]
    constant_value = predicate_constant[1]

    if ">" in constant_value: # the constant is an IRI
        constant_value = constant_value.strip("<")
        constant_value = constant_value.strip(">")

        po_map = generate_constant_IRI(constant_value, predicate_name, map_name)

    else: # the constant is a literal
        po_map = generate_constant_literal(constant_value, predicate_name, map_name)

    return po_map

"""Functions to parse kiegel"""

def not_resource_test(kiegel_list): # test to see if any blank nodes generated need to have not(@resource) in their XPath expressions
    if len(kiegel_list) == 1: # there is only one map, i.e. only one kind of input value type; no differentiation needed
        not_resource = False
    else: # there are different maps for IRIs and literals; differentiation may be needed
        if ">>" in kiegel_list[0]: # there is a blank node in the first map
            first_map_bnode = True
        else:
            first_map_bnode = False

        if ">>" in kiegel_list[1]: # there is a blank node in the second map
            second_map_bnode = True
        else:
            second_map_bnode = False

        if first_map_bnode and second_map_bnode: # both maps have blank nodes in them; differentiation not needed
            not_resource = False
        elif not first_map_bnode and not second_map_bnode:  # neither maps have blank nodes in them; differentiation not needed
            not_resource = False
        else: # only one map has a blank node, and therefore differentiation is needed
            not_resource = True

    return not_resource

def replace_semicolons(map):
    if ";" in map:
        if "; >" in map: # it goes in the first blank node
            map_list = map.split(" ; > ")
            first_map = map_list[0].split(" ")
            predicate_name = first_map[0]
            class_name = first_map[2]
            new_map = f"""{map_list[0]}
and
{predicate_name} >> {class_name} > {map_list[1]}"""
            return new_map

        else: # it does not go in the first blank node
            map_list = map.split(" ; ")
            new_map = f"""{map_list[0]}
and
{map_list[1]}"""
            return new_map
    else: # no semicolons to replace
        return map

def fix_broken_constants(constant_list):
    """Takes in a list of values that ought to be one literal, and outputs them as a single literal"""
    space = " "
    new_literal = space.join(constant_list)
    return new_literal


def split_by_space(map):
    """Takes in a kiegel map as a string, and returns the elements in the map separated as a list"""
    map_list = map.split(" ")

    # some constant literal values will have spaces in them that shouldn't be split; the following code will look for these instances and fix them
    if '="' in map:
        continue_search = False
        new_map_list = []
        for item in map_list:
            if len(item) < 1:
                pass
            else:
                item = item.strip()
                if item.split('=')[-1][0] == '"' and item[-1] != '"': # first character after = is " and the last character of string is NOT "...
                    broken_constant_list = []
                    broken_constant_list.append(item)
                    continue_search = True
                else:
                    if continue_search == True:
                        broken_constant_list.append(item)
                        if item[-1] == '"': # if the last character is ", the broken constant list has all the parts of the literal
                            continue_search = False
                            fixed_constant = fix_broken_constants(broken_constant_list)
                            new_map_list.append(fixed_constant)
                    else:
                        new_map_list.append(item)

        map_list = new_map_list

    return map_list

"""Get property numbers and kiegel mappings from CSV"""

#csv_files = [csv_file_path_work, csv_file_path_expression, csv_file_path_manifestation, csv_file_path_item]
csv_file_list = os.listdir(csv_dir)
csv_file_list = sorted(csv_file_list)
csv_files = []
csv_ext_files = []
for file in csv_file_list:
    if "_ext_" in file:
        csv_ext_files.append(file)
    else:
        csv_files.append(file)

index_number = 0

for csv_file in csv_files:
    if "work" in csv_file:
        entity_number = 1
    elif "expression" in csv_file:
        entity_number = 2
    elif "manifestation" in csv_file:
        entity_number = 3
    elif "item" in csv_file:
        entity_number = 4

    property_number_list = ["P20065"]

    kiegel_mapping_list = ["""notation*
or
notation >> Script > rdfs:label"""]

    with open(f"{csv_dir}/{csv_file}") as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for line in csv_reader:
            if line_count == 0: # ignore header row
                pass
            else:
                prop_IRI = line[1]
                if entity_number == 1:
                    prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/w/')
                elif entity_number == 2:
                    prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/e/')
                elif entity_number == 3:
                    prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/m/')
                elif entity_number == 4:
                    prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/i/')
                property_number_list.append(prop_num)

                kiegel = line[3]
                kiegel_mapping_list.append(kiegel)
            line_count = line_count + 1

    with open(f"{csv_dir}/{csv_ext_files[index_number]}") as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for line in csv_reader:
            if line_count == 0: # ignore header row
                pass
            else:
                prop_IRI = line[1]
                prop_num = "h" + prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4#') # it takes off the h for some reason
                property_number_list.append(prop_num)

                kiegel = line[3]
                kiegel_mapping_list.append(kiegel)
            line_count = line_count + 1

    """Start main RML map"""

    if entity_number == 1:
        default_map = "Work"
        default_class = "Work"
        default_path = "!!workID!!"
    elif entity_number == 2:
        default_map = "Expression"
        default_class = "Work"
        default_path = "!!expressionID!!"
    elif entity_number == 3:
        default_map = "Manifestation"
        default_class = "Instance"
        default_path = "!!manifestationID!!"
    elif entity_number == 4:
        default_map = "Item"
        default_class = "Item"
        default_path = "!!itemID!!"

    RML_list = []

    prefix_list = [
    "@prefix bf: <http://id.loc.gov/ontologies/bibframe/>.",
    "@prefix bflc: <http://id.loc.gov/ontologies/bflc/>.",
    "@prefix dbo: <http://dbpedia.org/ontology/>.",
    "@prefix ex: <http://example.org/rules/>.",
    "@prefix madsrdf: <http://www.loc.gov/mads/rdf/v1#>.",
    "@prefix rdac: <http://rdaregistry.info/Elements/c/>.",
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

    for prefix in prefix_list:
        RML_list.append(prefix + "\n")

    main_logical_source = generate_logical_source(default_map, default_path)
    RML_list.append(main_logical_source + "\n")

    main_subject_map = generate_subject_map(default_map, default_class)
    RML_list.append(main_subject_map + "\n")

    admin_metadata_list = [
    f"ex:{default_map}Map rr:predicateObjectMap [",
    "  rr:predicate bf:adminMetadata;",
    "  rr:objectMap [",
    "    rr:parentTriplesMap ex:AdminMetadataMap",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap a rr:TriplesMap;",
    "  rml:logicalSource [",
    f"    rml:source \"/home/mcm104/rml/rdfxml/data/{default_path}.xml\";",
    "    rml:referenceFormulation ql:XPath;",
    "    rml:iterator \"/RDF/Description[catalogerID]\"",
    "  ].\n",
    "ex:AdminMetadataMap rr:subjectMap [",
    "  rr:termType rr:BlankNode;",
    "  rr:class bf:AdminMetadata",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bflc:catalogerID;",
    "  rr:objectMap [",
    "    rml:reference \"catalogerID\";",
    "    rr:termType rr:Literal",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bf:status;",
    "  rr:objectMap [",
    "    rr:parentTriplesMap ex:StatusMap",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bflc:encodingLevel;",
    "  rr:objectMap [",
    "    rml:reference \"encodingLevel/@resource\";",
    "    rr:termType rr:IRI",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bf:descriptionConventions;",
    "  rr:objectMap [",
    "    rml:reference \"descriptionConventions/@resource\";",
    "    rr:termType rr:IRI",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bf:source;",
    "  rr:objectMap [",
    "    rml:reference \"source/@resource\";",
    "    rr:termType rr:IRI",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bf:descriptionLanguage;",
    "  rr:objectMap [",
    "    rml:reference \"descriptionLanguage/@resource\";",
    "    rr:termType rr:IRI",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bf:creationDate;",
    "  rr:objectMap [",
    "    rml:reference \"creationDate\";",
    "    rr:termType rr:Literal",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bf:changeDate;",
    "  rr:objectMap [",
    "    rml:reference \"changeDate\";",
    "    rr:termType rr:Literal",
    "  ]",
    "].\n",
    "ex:StatusMap a rr:TriplesMap;",
    "  rml:logicalSource [",
    f"    rml:source \"/home/mcm104/rml/rdfxml/data/{default_path}.xml\";",
    "    rml:referenceFormulation ql:XPath;",
    "    rml:iterator \"/RDF/Description[code]\"",
    "  ].\n",
    "ex:StatusMap rr:subjectMap [",
    "  rr:termType rr:BlankNode;",
    "  rr:class bf:Status",
    "].\n",
    "ex:StatusMap rr:predicateObjectMap [",
    "  rr:predicate bf:code;",
    "  rr:objectMap [",
    "    rml:reference \"code\"",
    "  ]",
    "].\n"
    ]

    for line in admin_metadata_list:
        RML_list.append(line + "\n")

    """Iterate through kiegel mappings and generate RML"""

    num_of_properties = len(property_number_list)

    property_range = range(0, num_of_properties)

    map_number = 1

    bnode_list = []

    for number in property_range:
        property_number = property_number_list[number]

        kiegel = kiegel_mapping_list[number]

        kiegel_list = kiegel.split("\nor\n") # for properties that have different mapping options

        not_resource = not_resource_test(kiegel_list)

        for map in kiegel_list:
            map = replace_semicolons(map) # replaces shorthand ; with full kiegel maps separated with "and"

            map_list = map.split("\nand\n") # split new kiegel maps into separate items in a list

            for map in map_list:
                node_list = split_by_space(map)

                num_of_nodes = len(node_list)

                node_range = range(0, num_of_nodes)

                map_name = default_map

                for num in node_range:
                    node = node_list[num].strip()

                    if node == ">":
                        pass

                    elif "*" in node: # node takes a literal value
                        po_map = generate_IRI_po_map(property_number, node, map_name)
                        RML_list.append(po_map + "\n")

                    elif "=" in node: # node takes a constant value
                        po_map = generate_constant(node, map_name)
                        RML_list.append(po_map + "\n")

                    elif node == ">>":
                        predicate_name = node_list[num - 1]
                        bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
                        po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
                        RML_list.append(po_map + "\n")

                        generate_new_bnode = True

                        for bnode_name in bnode_list:
                            if bnode_name == bnode_map_name: # i.e. the bnode already exists
                                generate_new_bnode = False

                        if generate_new_bnode == True:
                            logical_source = generate_bnode_logical_source(property_number, bnode_map_name, not_resource, default_path)
                            RML_list.append(logical_source + "\n")

                            class_name = node_list[num + 1]
                            subject_map = generate_subject_map(bnode_map_name, class_name, "bnode")
                            RML_list.append(subject_map + "\n")

                        map_name = bnode_map_name
                        bnode_list.append(bnode_map_name)

                    elif node == "not":
                        pass

                    elif node == "mapped":
                        pass

                    else: # node takes a literal value or blank node
                        if num == num_of_nodes - 1: # it's the last node and cannot be a blank node, takes a literal
                            po_map = generate_literal_po_map(property_number, node, map_name)
                            RML_list.append(po_map + "\n")
                        elif node_list[num + 1] == ">>": # it takes a blank node...
                            pass
                        else: # make sure it is a property and not a class
                            is_class = False
                            for letter in node:
                                if letter.isupper() == True:
                                    is_class = True

                            if is_class == True:
                                pass
                            else:# it takes a literal
                                po_map = generate_literal_po_map(property_number, node, map_name)
                                RML_list.append(po_map + "\n")

            map_number = map_number + 1

    if not os.path.exists(f'rmlOutput/'):
        os.system(f'mkdir rmlOutput')

    with open(f"rmlOutput/{default_map.lower()}RML.ttl", "w") as output_file:
        for code in RML_list:
            output_file.write(code)

    index_number = index_number + 1
