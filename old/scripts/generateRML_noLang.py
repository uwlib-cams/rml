import csv
import rdflib
from rdflib import *
import os
from sys import argv
import time

script, csv_dir = argv

"""Lists"""

# no_language_tag_list = ["P10219", "P20214", "P30007", "P30011"]
language_tag_list = [ # non-repeatable properties, aka there can only be one, aka the language tags can't get switched around
	"P30061",
	"P10331",
	"P30054",
	"P10223",
	"P30058",
	"P20315",
	"P30064",
	"P30294",
	"P30057",
	"P30003",
	"P30052",
	"P30059",
	"P30062",
	"P30053",
	"hasCallNumber",
	"P30055",
	"P30260"
]

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

work_variant_title_props = [
	"P10086"
]

expression_title_props = [
	"P20312",
	"P20315"
]

expression_variant_title_props = [
	"P20316"
]

manifestation_title_props = [
	"P30134",
	"P30142",
	"P30156"
]

manifestation_variant_title_props = [
	"P30128",
	"P30129",
	"P30130"
]

manifestation_abbreviated_title_props = [
	"P30131"
]

item_title_props = [
	"P40082",
	"P40085"
]

item_variant_title_props = [
	"P40086"
]

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

def generate_admin_metadata_list(entity):
	admin_metadata_list = [
f"ex:{entity.capitalize()}Map rr:predicateObjectMap [",
"  rr:predicate bf:adminMetadata;",
"  rr:objectMap [",
"	rr:parentTriplesMap ex:AdminMetadataMap",
"  ]",
"].\n",
"ex:AdminMetadataMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"	rml:source \"/home/mcm104/rml/input/!!{entity}ID!!.xml\";",
"	rml:referenceFormulation ql:XPath;",
"	rml:iterator \"/RDF/Description[catalogerID]\"",
"  ].\n",
"ex:AdminMetadataMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:AdminMetadata",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bflc:catalogerID;",
"  rr:objectMap [",
"	rml:reference \"catalogerID[@lang]\";",
"	rr:termType rr:Literal;",
"	rml:languageMap [",
"	  rml:reference \"catalogerID/@lang\"",
"	]",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bflc:catalogerID;",
"  rr:objectMap [",
"	rml:reference \"catalogerID[not(@lang)]\";",
"	rr:termType rr:Literal",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:status;",
"  rr:objectMap [",
"	rr:parentTriplesMap ex:StatusMap",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bflc:encodingLevel;",
"  rr:objectMap [",
"	rml:reference \"encodingLevel/@resource\";",
"	rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:descriptionConventions;",
"  rr:objectMap [",
"	rml:reference \"descriptionConventions/@resource\";",
"	rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:source;",
"  rr:objectMap [",
"	rml:reference \"source/@resource\";",
"	rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:descriptionLanguage;",
"  rr:objectMap [",
"	rml:reference \"descriptionLanguage/@resource\";",
"	rr:termType rr:IRI",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:creationDate;",
"  rr:objectMap [",
"	rml:reference \"creationDate\";",
"	rr:termType rr:Literal",
"  ]",
"].\n",
"ex:AdminMetadataMap rr:predicateObjectMap [",
"  rr:predicate bf:changeDate;",
"  rr:objectMap [",
"	rml:reference \"changeDate\";",
"	rr:termType rr:Literal",
"  ]",
"].\n",
"ex:StatusMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"	rml:source \"/home/mcm104/rml/input/{default_path}.xml\";",
"	rml:referenceFormulation ql:XPath;",
"	rml:iterator \"/RDF/Description[code]\"",
"  ].\n",
"ex:StatusMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Status",
"].\n",
"ex:StatusMap rr:predicateObjectMap [",
"  rr:predicate bf:code;",
"  rr:objectMap [",
"	rml:reference \"code\"",
"  ]",
"].\n"
]
	return admin_metadata_list

P10002_list = [
f"ex:WorkMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"	rr:parentTriplesMap ex:IdentifierMap",
"  ]",
"].\n",
f"ex:WorkMap rr:predicateObjectMap [",
"  rr:predicate bf:identifiedBy;",
"  rr:objectMap [",
"	rml:reference \"P10002/@resource\";",
"	rr:termType rr:IRI",
"  ]",
"].\n",
"ex:IdentifierMap a rr:TriplesMap;",
"  rml:logicalSource [",
f"	rml:source \"/home/mcm104/rml/input/!!workID!!.xml\";",
"	rml:referenceFormulation ql:XPath;",
"	rml:iterator \"/RDF/Description[P10002[not(@resource)]]\"",
"  ].\n",
"ex:IdentifierMap rr:subjectMap [",
"  rr:termType rr:BlankNode;",
"  rr:class bf:Identifier",
"].\n",
"ex:IdentifierMap rr:predicateObjectMap [",
"  rr:predicate rdf:value;",
"  rr:objectMap [",
"	rml:reference \"P10002[not(@resource)]\";",
"	rr:termType rr:Literal",
"  ]",
"].\n"
]

"""Functions to parse CSV"""

def get_work_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	work_files = []
	for file in csv_file_list:
		if "work" in file:
			work_files.append(file)

	work_property_list = []
	for csv_file in work_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/w/') == "P10002": # mapping for this property too complex; writing it in manually
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/w/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					work_property_list.append(prop_num)
				line_count += 1

	return work_property_list

def get_work_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	work_files = []
	for file in csv_file_list:
		if "work" in file:
			work_files.append(file)

	work_kiegel_list = []
	for csv_file in work_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif line[1].strip('http://rdaregistry.info/Elements/w/') == "P10002": # mapping for this property too complex; writing it in manually
					pass
				else:
					kiegel = line[3]

					work_kiegel_list.append(kiegel)
				line_count += 1

	return work_kiegel_list

def get_expression_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	expression_files = []
	for file in csv_file_list:
		if "expression" in file:
			expression_files.append(file)

	expression_property_list = []
	for csv_file in expression_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/e/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					expression_property_list.append(prop_num)
				line_count += 1

	return expression_property_list

def get_expression_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	expression_files = []
	for file in csv_file_list:
		if "expression" in file:
			expression_files.append(file)

	expression_kiegel_list = []
	for csv_file in expression_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				else:
					kiegel = line[3]

					expression_kiegel_list.append(kiegel)
				line_count += 1

	return expression_kiegel_list

def get_manifestation_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	manifestation_files = []
	for file in csv_file_list:
		if "manifestation" in file:
			manifestation_files.append(file)

	manifestation_property_list = []
	for csv_file in manifestation_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/m/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					manifestation_property_list.append(prop_num)
				line_count += 1

	return manifestation_property_list

def get_manifestation_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	manifestation_files = []
	for file in csv_file_list:
		if "manifestation" in file:
			manifestation_files.append(file)

	manifestation_kiegel_list = []
	for csv_file in manifestation_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				else:
					kiegel = line[3]

					manifestation_kiegel_list.append(kiegel)
				line_count += 1

	return manifestation_kiegel_list

def get_item_property_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	item_files = []
	for file in csv_file_list:
		if "item" in file:
			item_files.append(file)

	item_property_list = []
	for csv_file in item_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				else:
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip('http://rdaregistry.info/Elements/i/')
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					item_property_list.append(prop_num)
				line_count += 1

	return item_property_list

def get_item_kiegel_list(csv_dir):
	csv_file_list = os.listdir(csv_dir)
	item_files = []
	for file in csv_file_list:
		if "item" in file:
			item_files.append(file)

	item_kiegel_list = []
	for csv_file in item_files:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				else:
					kiegel = line[3]

					item_kiegel_list.append(kiegel)
				line_count += 1

	return item_kiegel_list

"""Functions to write RML code"""

def start_RML_map(entity):
	default_map = f"{entity.capitalize()}"
	default_class = f"{entity.capitalize()}"
	default_path = f"!!{entity}ID!!"

	RML_list = []
	for prefix in prefix_list:
		RML_list.append(prefix + "\n")

	main_logical_source = generate_main_logical_source(entity)
	RML_list.append(main_logical_source + "\n")

	main_subject_map = generate_main_subject_map(entity)
	RML_list.append(main_subject_map + "\n")

	admin_metadata_list = generate_admin_metadata_list(entity)

	for line in admin_metadata_list:
		RML_list.append(line + "\n")

	if "w" in entity: # for work RML map
		for line in P10002_list:
			RML_list.append(line + "\n")

	return RML_list

def create_bnode_name(predicate_name, class_name, property_number, kiegel_map):
	map_number = property_number.strip('P')
	bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
	if "Provisionactivity" in bnode_map_name:
		bnode_map_name = "Provisionactivity_" + class_name + "_"
	elif "Title" in bnode_map_name:
		if "Variant" in class_name:
			bnode_map_name = "Variant_Title_"
		elif "Abbreviated" in class_name:
			bnode_map_name = "Abbreviated_Title_"
		else:
			bnode_map_name = "Title_"
	elif "*" not in kiegel_map:
		if property_number in language_tag_list:
			bnode_map_name = f"Lang_{bnode_map_name}"
	return bnode_map_name

# logical sources
def generate_main_logical_source(entity):
	if "w" in entity:
		class_number = "C10001"
	elif "exp" in entity:
		class_number = "C10006"
	elif "mani" in entity:
		class_number = "C10007"
	elif "item" in entity:
		class_number = "C10003"
	lang_logical_source = f"""ex:{entity.capitalize()}Map a rr:TriplesMap;
  rml:logicalSource [
	rml:source \"/home/mcm104/rml/input/!!{entity}ID!!.xml\";
	rml:referenceFormulation ql:XPath;
	rml:iterator \"/RDF/Description[type/@resource='http://rdaregistry.info/Elements/c/{class_number}']\"
  ].\n"""

	return lang_logical_source

def generate_IRI_logical_source(map_name, file_path, property_number):
	IRI_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
	rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
	rml:referenceFormulation ql:XPath;
	rml:iterator \"/RDF/Description[{property_number}[@resource]]\"
  ].\n"""

	return IRI_logical_source

def generate_literal_logical_source(map_name, file_path, property_number):
	if "Variant" in map_name:
		if "work" in file_path:
			property_number = " or ".join(work_variant_title_props)
		elif "expression" in file_path:
			property_number = " or ".join(expression_variant_title_props)
		elif "manifestation" in file_path:
			property_number = " or ".join(manifestation_variant_title_props)
		elif "item" in file_path:
			property_number = " or ".join(item_variant_title_props)

		literal_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
	rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
	rml:referenceFormulation ql:XPath;
	rml:iterator \"/RDF/Description[{property_number}]\"
  ].\n"""

	elif "Abbreviated" in map_name:
	   property_number = " or ".join(manifestation_abbreviated_title_props)

	   literal_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
	rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
	rml:referenceFormulation ql:XPath;
	rml:iterator \"/RDF/Description[{property_number}]\"
  ].\n"""

	else:
	   literal_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
	rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
	rml:referenceFormulation ql:XPath;
	rml:iterator \"/RDF/Description[{property_number}[not(@resource)]]\"
  ].\n"""

	return literal_logical_source

def generate_provact_logical_source(class_name, map_name, file_path):
	if class_name == "Distribution":
		property_numbers = " or ".join(provisionActivityDistributionList)
	elif class_name == "Manufacture":
		property_numbers = " or ".join(provisionActivityManufactureList)
	elif class_name == "Production":
		property_numbers = " or ".join(provisionActivityProductionList)
	elif class_name == "Publication":
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
		if "Variant" in map_name:
			property_numbers = " or ".join(work_variant_title_props)
		else:
			property_numbers = " or ".join(work_title_props)
	elif "exp" in file_path.lower():
		if "Variant" in map_name:
			property_numbers = " or ".join(expression_variant_title_props)
		else:
			property_numbers = " or ".join(expression_title_props)
	elif "mani" in file_path.lower():
		if "Variant" in map_name:
			property_numbers = " or ".join(manifestation_abbreviated_title_props)
		elif "Abbreviated" in map_name:
			property_numbers = " or ".join(manifestation_variant_title_props)
		else:
			property_numbers = " or ".join(manifestation_title_props)
	elif "item" in file_path.lower():
		if "Variant" in map_name:
			property_numbers = " or ".join(item_variant_title_props)
		else:
			property_numbers = " or ".join(item_title_props)

	title_logical_source = f"""ex:{map_name}Map a rr:TriplesMap;
  rml:logicalSource [
	rml:source \"/home/mcm104/rml/input/{file_path}.xml\";
	rml:referenceFormulation ql:XPath;
	rml:iterator \"/RDF/Description[{property_numbers}]\"
  ].\n"""

	return title_logical_source

# subject maps

def generate_main_subject_map(entity):
	if entity.lower() == "work":
		class_name = "bf:Work"
	elif entity.lower() == "expression":
		class_name = "bf:Work"
	elif entity.lower() == "manifestation":
		class_name = "bf:Instance"
	elif entity.lower() == "item":
		class_name = "bf:Item"

	main_subject_map = f"""ex:{entity.capitalize()}Map rr:subjectMap [
  rml:reference "@about";
  rr:class {class_name}
].\n"""

	return main_subject_map

def generate_bnode_subject_map(map_name, class_name):
	if ":" not in class_name:
		class_name = f"bf:{class_name}"

	bnode_subject_map = f"""ex:{map_name}Map rr:subjectMap [
  rr:termType rr:BlankNode;
  rr:class {class_name}
].\n"""

	return bnode_subject_map

# predicate object maps

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

def generate_lang_literal_po_map(predicate, map_name, property):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	lang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
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

	return lang_literal_po_map

def generate_not_lang_literal_po_map(predicate, map_name, property):
	if ":" not in predicate:
		predicate = f"bf:{predicate}"

	not_lang_literal_po_map = f"""ex:{map_name}Map rr:predicateObjectMap [
  rr:predicate {predicate};
	rr:objectMap [
	rml:reference \"{property}[not(@resource)]\";
	rr:termType rr:Literal
  ]
].\n"""

	return not_lang_literal_po_map

def generate_IRI_po_map(predicate, map_name, property):
	if "*" in predicate:
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

# constants

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

# template

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
				predicate_class_map = map_list[0]
				predicate_name = predicate_class_map.split(" ")[0]
				class_name = predicate_class_map.split(" ")[2]
				new_map = f"{predicate_name} >> {class_name} {map}"
				new_map_list.append(new_map)
			else:
				new_map_list.append(map)

		new_kiegel = "\nand\n".join(new_map_list)
		return new_kiegel
	else:
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

def fix_broken_constants(constant_list):
	"""Takes in a list of values that ought to be one literal, and outputs them as a single literal"""
	space = " "
	new_literal = space.join(constant_list)
	return new_literal

###

"""Work"""

default_map = "Work"
default_class = "Work"
default_path = "!!workID!!"

work_RML_list = start_RML_map("work")
work_property_list = get_work_property_list(csv_dir)
work_kiegel_list = get_work_kiegel_list(csv_dir)

work_property_range = range(0, len(work_property_list))

work_bnode_list = []

for number in work_property_range:
	property_number = work_property_list[number]

	kiegel = work_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		map_name = default_map

		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					po_map = generate_IRI_po_map(node, map_name, property_number)
					work_RML_list.append(po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					work_RML_list.append(po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)

					if bnode_map_name not in work_bnode_list:
						# generate po-maps that lead to new bnodes
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						work_RML_list.append(bnode_po_map + "\n")

						# generate logical source(s)
						if "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")
						elif "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							work_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							work_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal
							logical_source = generate_literal_logical_source(bnode_map_name, default_path, property_number)
							work_RML_list.append(logical_source + "\n")

						# generate subject map(s)
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						work_RML_list.append(subject_map + "\n")

						work_bnode_list.append(bnode_map_name)

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = work_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					work_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						work_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if property_number in language_tag_list:
							literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
							work_RML_list.append(literal_po_map + "\n")
						else:
							literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
							work_RML_list.append(literal_po_map + "\n")
					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if property_number in language_tag_list:
								literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
								work_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
								work_RML_list.append(literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/workRML.ttl", "w") as output_file:
	for code in work_RML_list:
		output_file.write(code)

###

"""Expression"""

default_map = "Expression"
default_class = "Expression"
default_path = "!!expressionID!!"

expression_RML_list = start_RML_map("expression")
expression_property_list = get_expression_property_list(csv_dir)
expression_kiegel_list = get_expression_kiegel_list(csv_dir)

expression_property_range = range(0, len(expression_property_list))

expression_bnode_list = []

for number in expression_property_range:
	property_number = expression_property_list[number]

	kiegel = expression_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		map_name = default_map

		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					po_map = generate_IRI_po_map(node, map_name, property_number)
					expression_RML_list.append(po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					expression_RML_list.append(po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)

					if bnode_map_name not in expression_bnode_list:
						# generate po-maps that lead to new bnodes
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						expression_RML_list.append(bnode_po_map + "\n")

						# generate logical source(s)
						if "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")
						elif "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							expression_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							expression_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal
							logical_source = generate_literal_logical_source(bnode_map_name, default_path, property_number)
							expression_RML_list.append(logical_source + "\n")

						# generate subject map(s)
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						expression_RML_list.append(subject_map + "\n")

						expression_bnode_list.append(bnode_map_name)

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = expression_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					expression_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						expression_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if property_number in language_tag_list:
							literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
							expression_RML_list.append(literal_po_map + "\n")
						else:
							literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
							expression_RML_list.append(literal_po_map + "\n")
					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if property_number in language_tag_list:
								literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
								expression_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
								expression_RML_list.append(literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/expressionRML.ttl", "w") as output_file:
	for code in expression_RML_list:
		output_file.write(code)

###

"""Manifestation"""

default_map = "Manifestation"
default_class = "Manifestation"
default_path = "!!manifestationID!!"

manifestation_RML_list = start_RML_map("manifestation")
manifestation_property_list = get_manifestation_property_list(csv_dir)
manifestation_kiegel_list = get_manifestation_kiegel_list(csv_dir)

manifestation_property_range = range(0, len(manifestation_property_list))

manifestation_bnode_list = []

for number in manifestation_property_range:
	property_number = manifestation_property_list[number]

	kiegel = manifestation_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		map_name = default_map

		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					po_map = generate_IRI_po_map(node, map_name, property_number)
					manifestation_RML_list.append(po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					manifestation_RML_list.append(po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)

					if bnode_map_name not in manifestation_bnode_list:
						# generate po-maps that lead to new bnodes
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						manifestation_RML_list.append(bnode_po_map + "\n")

						# generate logical source(s)
						if "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")
						elif "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							manifestation_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							manifestation_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal
							logical_source = generate_literal_logical_source(bnode_map_name, default_path, property_number)
							manifestation_RML_list.append(logical_source + "\n")

						# generate subject map(s)
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						manifestation_RML_list.append(subject_map + "\n")

						manifestation_bnode_list.append(bnode_map_name)

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = manifestation_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					manifestation_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						manifestation_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if property_number in language_tag_list:
							literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
							manifestation_RML_list.append(literal_po_map + "\n")
						else:
							literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
							manifestation_RML_list.append(literal_po_map + "\n")
					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if property_number in language_tag_list:
								literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
								manifestation_RML_list.append(literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/manifestationRML.ttl", "w") as output_file:
	for code in manifestation_RML_list:
		output_file.write(code)

###

"""Item"""

default_map = "Item"
default_class = "Item"
default_path = "!!itemID!!"

item_RML_list = start_RML_map("item")
item_property_list = get_item_property_list(csv_dir)
item_kiegel_list = get_item_kiegel_list(csv_dir)

item_property_range = range(0, len(item_property_list))

item_bnode_list = []

for number in item_property_range:
	property_number = item_property_list[number]

	kiegel = item_kiegel_list[number]

	kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

	for map_1 in kiegel_list:
		map_name = default_map

		new_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statements

		map_list = new_map.split("\nand\n") # split new kiegel maps into separate items in a list

		for map_2 in map_list:
			node_list = split_by_space(map_2)

			node_range = range(0, len(node_list))

			for num in node_range:
				node = node_list[num].strip()

				if node == ">":
					pass

				elif "*" in node: # node takes an IRI value
					po_map = generate_IRI_po_map(node, map_name, property_number)
					item_RML_list.append(po_map + "\n")

				elif "=" in node: # node takes a constant value
					po_map = generate_constant(node, map_name)
					item_RML_list.append(po_map + "\n")

				elif node == ">>":
					predicate_name = node_list[num - 1]
					class_name = node_list[num + 1]
					bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)

					if bnode_map_name not in item_bnode_list:
						# generate po-maps that lead to new bnodes
						bnode_po_map = generate_bnode_po_map(predicate_name, bnode_map_name, map_name)
						item_RML_list.append(bnode_po_map + "\n")

						# generate logical source(s)
						if "*" in map_2: # the blank node takes an IRI
							logical_source = generate_IRI_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")
						elif "Provision" in bnode_map_name:
							logical_source = generate_provact_logical_source(class_name, bnode_map_name, default_path)
							item_RML_list.append(logical_source + "\n")
						elif bnode_map_name == "Title_":
							logical_source = generate_title_logical_source(bnode_map_name, default_path)
							item_RML_list.append(logical_source + "\n")
						else: # the blank node takes a literal
							logical_source = generate_literal_logical_source(bnode_map_name, default_path, property_number)
							item_RML_list.append(logical_source + "\n")

						# generate subject map(s)
						subject_map = generate_bnode_subject_map(bnode_map_name, class_name)
						item_RML_list.append(subject_map + "\n")

						item_bnode_list.append(bnode_map_name)

					map_name = bnode_map_name

				elif node == "not":
					pass
				elif node == "mapped":
					pass
				elif "See" in node:
					pass

				elif "{" in node:
					part_a = property_number
					part_b = item_property_list[number+1]
					node = node.strip("{")
					node = node.strip("}")

					template_po = generate_template_po_map(node, part_a, part_b, map_name)
					item_RML_list.append(template_po + "\n")

					if "Lang" in map_name:
						not_lang_map_name = f"Not_{map_name}"
						second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
						item_RML_list.append(second_template_po + "\n")

				else: # node takes a literal value or blank node
					if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
						if property_number in language_tag_list:
							literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
							item_RML_list.append(literal_po_map + "\n")
						else:
							literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
							item_RML_list.append(literal_po_map + "\n")
					elif node_list[num + 1] == ">>": # it takes a blank node
						pass
					else:
						# make sure it is a property and not a class by seeing if the first letter is capitalized
						if node[0].isupper() == False:
							if property_number in language_tag_list:
								literal_po_map = generate_lang_literal_po_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")
							else:
								literal_po_map = generate_not_lang_literal_po_map(node, map_name, property_number)
								item_RML_list.append(literal_po_map + "\n")

if not os.path.exists(f'rmlOutput/'):
	os.system(f'mkdir rmlOutput')

with open(f"rmlOutput/itemRML.ttl", "w") as output_file:
	for code in item_RML_list:
		output_file.write(code)
