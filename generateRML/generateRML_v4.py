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
    rml:source "/home/mcm104/rml/input/{file_path}.xml";
    rml:referenceFormulation ql:XPath;
    rml:iterator "/RDF/Description[type/@resource='http://rdaregistry.info/Elements/c/C1000{entity_number}']"
  ].\n"""
    return logical_source

def generate_bnode_logical_source(property_number, map_name, not_resource, yes_resource, file_path):
    if not_resource == True:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}[not(@resource)]]\"
  ].\n"""
    elif yes_resource == True:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}[@resource]]\"
  ].\n"""
    else:
        bnode_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_number}]\"
  ].\n"""
    return bnode_logical_source

def generate_provact_logical_source(provact_class, map_name, file_path):
    if provact_class == "Distribution":
        property_numbers = " or ".join(provisionActivityDistributionList)
    elif provact_class == "Manufacture":
        property_numbers = " or ".join(provisionActivityManufactureList)
    elif provact_class == "Production":
        property_numbers = " or ".join(provisionActivityProductionList)
    elif provact_class == "Publication":
        property_numbers = " or ".join(provisionActivityPublicationList)
    provact_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_numbers}]\"
  ].\n"""
    return provact_logical_source

def generate_title_logical_source(map_name, file_path):
    if "work" in file_path.lower():
        property_numbers = " or ".join(work_title_props)
    elif "exp" in file_path.lower():
        property_numbers = " or ".join(expression_title_props)
    elif "mani" in file_path.lower():
        property_numbers = " or ".join(manifestation_title_props)
    elif "item" in file_path.lower():
        property_numbers = " or ".join(item_title_props)
    title_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
    rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
    rml:referenceFormulation ql:XPath;
    rml:iterator \"/RDF/Description[{property_numbers}]\"
  ].\n"""
    return title_logical_source

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

def generate_literal_po_map(property, predicate, map_name, langtag):
    if ":" not in predicate:
        predicate = f"bf:{predicate}"
    if langtag == True:
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
    elif langtag == False:
        literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rml:reference \"{property}[not(@resource)][@lang]\";
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

def generate_template_po_map(predicate, part_a, part_b, map_name, format=""):
    open_curly_brace = "{"
    close_curly_brace = "}"

    po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
  rr:objectMap [
    rr:template \"{open_curly_brace}{part_a}{close_curly_brace}{format}{open_curly_brace}{part_b}{close_curly_brace}\";
    rr:termType rr:Literal
  ]
]."""
    return po_map

"""Functions to parse kiegel"""

def not_resource_test(kiegel_list): # test to see if any blank nodes generated need to have not(@resource) in their XPath expressions
    if len(kiegel_list) == 1: # there is only one map, i.e. only one kind of input value type; no differentiation needed
        not_resource = False
    else: # there are different maps for IRIs and literals; differentiation may be needed
        join_format = " "
        kiegel = join_format.join(kiegel_list)
        not_resource = False
        if "*" not in kiegel:
            not_resource = True

    return not_resource

def yes_resource_test(kiegel_list): # test to see if any blank nodes generated need to have not(@resource) in their XPath expressions
    if len(kiegel_list) == 1: # there is only one map, i.e. only one kind of input value type; no differentiation needed
        yes_resource = False
    else: # there are different maps for IRIs and literals; differentiation may be needed
        join_format = " "
        kiegel = join_format.join(kiegel_list)
        yes_resource = False
        if "*" in kiegel:
            if ">>" in kiegel:
                yes_resource = True

    return yes_resource


def fix_broken_constants(constant_list):
    """Takes in a list of values that ought to be one literal, and outputs them as a single literal"""
    space = " "
    new_literal = space.join(constant_list)
    return new_literal

def replace_semicolons(kiegel_map):
    """Replace shorthand semicolons in kiegel map with "long-hand" map that is more easily parsed"""
    if ";" in kiegel_map:
        map_list = kiegel_map.split(" ; ")

        num_of_nodes = len(map_list)

        node_range = range(0, num_of_nodes)

        new_map_list = []

        for num in node_range:
            map = map_list[num]
            if map[0] == ">": # if the first character is >, i.e. it was "; >"
                predicate_class_map = map_list[num-1]
                predicate_name = predicate_class_map.split(" ")[0]
                class_name = predicate_class_map.split(" ")[2]
                new_map = f"{predicate_name} >> {class_name} {map}"
                new_map_list.append(new_map)
            else:
                new_map_list.append(map)

        new_kiegel = "\nand\n".join(new_map_list)
        return new_kiegel

    else: # no semicolons to replace
        return kiegel_map


def split_by_space(map):
    """Takes in a kiegel map as a string, and returns the elements in the map separated as a list"""
    map = map.strip()
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

no_language_tag_list = ["P10219", "P20214", "P30007", "P30011"]

provisionActivityDistributionList = [
	"P30008",
	"P30017",
	"P30068",
	"P30080",
	"P30085",
	"P30089",
	"P30173",
	"P30348",
	"P30359",
	"P30377",
	"P30388",
	"P30406",
	"P30417",
	"P30435",
	"P30446"
]

provisionActivityManufactureList = [
	"P30010",
	"P30049",
	"P30069",
	"P30070",
	"P30071",
	"P30072",
	"P30073",
	"P30074",
	"P30075",
	"P30076",
	"P30077",
	"P30078",
	"P30082",
	"P30087",
	"P30090",
	"P30175",
	"P30215",
	"P30349",
	"P30350",
	"P30351",
	"P30352",
	"P30353",
	"P30354",
	"P30355",
	"P30356",
	"P30357",
	"P30358",
	"P30361",
	"P30364",
	"P30378",
	"P30379",
	"P30380",
	"P30381",
	"P30382",
	"P30383",
	"P30384",
	"P30385",
	"P30386",
	"P30387",
	"P30390",
	"P30393",
	"P30407",
	"P30408",
	"P30409",
	"P30410",
	"P30411",
	"P30412",
	"P30413",
	"P30414",
	"P30415",
	"P30416",
	"P30419",
	"P30422",
	"P30436",
	"P30437",
	"P30438",
	"P30439",
	"P30440",
	"P30441",
	"P30442",
	"P30443",
	"P30444",
	"P30445",
	"P30448",
	"P30451"
]

provisionActivityProductionList = [
	"P30009",
	"P30081",
	"P30086",
	"P30091",
	"P30094",
	"P30174",
	"P30360",
	"P30389",
	"P30418",
	"P30447"
]

provisionActivityPublicationList = [
	"P30011",
	"P30067",
	"P30083",
	"P30088",
	"P30092",
	"P30095",
	"P30176",
	"P30347",
	"P30362",
	"P30376",
	"P30391",
	"P30405",
	"P30420",
	"P30434",
	"P30449"
]

provisionActivityList = provisionActivityDistributionList + provisionActivityManufactureList + provisionActivityProductionList + provisionActivityPublicationList

work_title_props = [
	"P10012",
	"P10088",
	"P10223"
]

expression_title_props = [
	"P20312",
	"P20315"
]

manifestation_title_props = [
	"P30134",
	"P30142",
	"P30156"
]

item_title_props = [
	"P40082",
	"P40085"
]

for csv_file in csv_files:
    if "work" in csv_file:
        entity_number = 1
    elif "expression" in csv_file:
        entity_number = 2
    elif "manifestation" in csv_file:
        entity_number = 3
    elif "item" in csv_file:
        entity_number = 4

    property_number_list = []

    kiegel_mapping_list = []

    with open(f"{csv_dir}/{csv_file}") as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for line in csv_reader:
            if line_count == 0: # ignore header row
                pass
            elif line[1].lstrip('http://rdaregistry.info/Elements/w/') == "P10002": # mapping for this property too complex; writing it in manually
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

    if len(csv_ext_files) > 0:
        with open(f"{csv_dir}/{csv_ext_files[index_number]}") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                if line_count == 0: # ignore header row
                    pass
                else:
                    prop_IRI = line[1]
                    prop_num = prop_IRI.lstrip(f'https://doi.org/10.6069/uwlib.55.d.4')
                    prop_num = prop_num.strip('#')
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
    f"    rml:source \"/home/mcm104/rml/input/{default_path}.xml\";",
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
    "    rml:reference \"catalogerID[@lang]\";",
    "    rr:termType rr:Literal;",
    "    rml:languageMap [",
    "      rml:reference \"catalogerID/@lang\"",
    "    ]",
    "  ]",
    "].\n",
    "ex:AdminMetadataMap rr:predicateObjectMap [",
    "  rr:predicate bflc:catalogerID;",
    "  rr:objectMap [",
    "    rml:reference \"catalogerID[not(@lang)]\";",
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
    f"    rml:source \"/home/mcm104/rml/input/{default_path}.xml\";",
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

    if entity_number == 1:
        P10002_list = [
        f"ex:{default_map}Map rr:predicateObjectMap [",
        "  rr:predicate bf:identifiedBy;",
        "  rr:objectMap [",
        "    rr:parentTriplesMap ex:IdentifierMap",
        "  ]",
        "].\n",
        f"ex:{default_map}Map rr:predicateObjectMap [",
        "  rr:predicate bf:identifiedBy;",
        "  rr:objectMap [",
        "    rml:reference \"P10002/@resource\";",
        "    rr:termType rr:IRI",
        "  ]",
        "].\n",
        "ex:IdentifierMap a rr:TriplesMap;",
        "  rml:logicalSource [",
        f"    rml:source \"/home/mcm104/rml/input/{default_path}.xml\";",
        "    rml:referenceFormulation ql:XPath;",
        "    rml:iterator \"/RDF/Description[P10002[not(@resource)]]\"",
        "  ].\n",
        "ex:IdentifierMap rr:subjectMap [",
        "  rr:termType rr:BlankNode;",
        "  rr:class bf:Identifier",
        "].\n",
        "ex:IdentifierMap rr:predicateObjectMap [",
        "  rr:predicate rdf:value;",
        "  rr:objectMap [",
        "    rml:reference \"P10002[not(@resource)][@lang]\";",
        "    rr:termType rr:Literal;",
        "    rml:languageMap [",
        "      rml:reference \"P10002/@lang\"",
        "    ]",
        "  ]",
        "].\n",
        "ex:IdentifierMap rr:predicateObjectMap [",
        "  rr:predicate rdf:value;",
        "  rr:objectMap [",
        "    rml:reference \"P10002[not(@resource) and not(@lang)]\";",
        "    rr:termType rr:Literal",
        "  ]",
        "].\n"
        ]

        for line in P10002_list:
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

        for map in kiegel_list:
            map = replace_semicolons(map) # replaces shorthand ; with full kiegel maps separated with "and"

            map_list = map.split("\nand\n") # split new kiegel maps into separate items in a list

            for map in map_list:
                node_list = split_by_space(map)

                not_resource = not_resource_test(node_list)

                if not_resource == False:
                    yes_resource = yes_resource_test(node_list)
                else:
                    yes_resource = False

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
                        if "Provisionactivity" in bnode_map_name:
                            class_name = node_list[num + 1]
                            bnode_map_name = "Provisionactivity_" + class_name + "_"
                        if "Title" in bnode_map_name:
                            class_name = node_list[num + 1]
                            if "Variant" in class_name:
                                pass
                            elif "Abbreviated" in class_name:
                                pass
                            else:
                                bnode_map_name = "Title_"
                        po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
                        RML_list.append(po_map + "\n")

                        generate_new_bnode = True

                        for bnode_name in bnode_list:
                            if bnode_name == bnode_map_name: # i.e. the bnode already exists
                                generate_new_bnode = False

                        if generate_new_bnode == True:
                            if "Provisionactivity" in bnode_map_name:
                                logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
                                RML_list.append(logical_source + "\n")
                            elif "Title" in bnode_map_name:
                                if "Variant" in class_name:
                                    pass
                                elif "Abbreviated" in class_name:
                                    pass
                                else:
                                    logical_source = generate_title_logical_source(bnode_map_name, default_path)
                                    RML_list.append(logical_source + "\n")
                            else:
                                logical_source = generate_bnode_logical_source(property_number, bnode_map_name, not_resource, yes_resource, default_path)
                                RML_list.append(logical_source + "\n")

                            class_name = node_list[num + 1]
                            subject_map = generate_subject_map(bnode_map_name, class_name, "bnode")
                            RML_list.append(subject_map + "\n")

                        map_name = bnode_map_name
                        if bnode_map_name not in bnode_list:
                            bnode_list.append(bnode_map_name)

                    elif node == "not":
                        pass

                    elif node == "mapped":
                        pass

                    elif "See" in node:
                        pass

                    elif "{" in node:
                        part_a = property_number
                        part_b = property_number_list[number+1]
                        node = node.strip("{")
                        node = node.strip("}")
                        po_map = generate_template_po_map(node, part_a, part_b, map_name)
                        RML_list.append(po_map + "\n")
                    else: # node takes a literal value or blank node
                        if num == num_of_nodes - 1: # it's the last node and cannot be a blank node, takes a literal
                            if property_number in no_language_tag_list:
                                langtag = False
                            else:
                                langtag = True

                            po_map = generate_literal_po_map(property_number, node, map_name, langtag)
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
                                if property_number in no_language_tag_list:
                                    langtag = False
                                else:
                                    langtag = True

                                po_map = generate_literal_po_map(property_number, node, map_name, langtag)
                                RML_list.append(po_map + "\n")

            map_number = map_number + 1

    if not os.path.exists(f'rmlOutput/'):
        os.system(f'mkdir rmlOutput')

    with open(f"rmlOutput/{default_map.lower()}RML.ttl", "w") as output_file:
        for code in RML_list:
            output_file.write(code)

    index_number = index_number + 1
