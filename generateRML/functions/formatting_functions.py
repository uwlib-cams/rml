"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Lists"""
from functions.lists import classificationLcc_props
from functions.lists import classificationNlm_props
from functions.lists import no_language_tag_list

"""Functions"""
def convert_string_to_IRI(string):
	"""Convert string from kiegel mapping to an rdflib URI"""
	if ":" not in string:
		IRI_output = URIRef(f'http://id.loc.gov/ontologies/bibframe/{string}')
	else:
		string_prefix = string.split(":")[0]
		if string_prefix == "bf":
			IRI_output = URIRef(f'http://id.loc.gov/ontologies/bibframe/{string.split(":")[1]}')
		elif string_prefix == "bflc":
			IRI_output = URIRef(f'http://id.loc.gov/ontologies/bflc/{string.split(":")[1]}')
		elif string_prefix == "dbo":
			IRI_output = URIRef(f'http://dbpedia.org/ontology/{string.split(":")[1]}')
		elif string_prefix == "ex":
			IRI_output = URIRef(f'http://example.org/entity/{string.split(":")[1]}')
		elif string_prefix == "madsrdf":
			IRI_output = URIRef(f'http://www.loc.gov/mads/rdf/v1#{string.split(":")[1]}')
		elif string_prefix == "rdac":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/c/{string.split(":")[1]}')
		elif string_prefix == "rdae":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/e/{string.split(":")[1]}')
		elif string_prefix == "rdai":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/i/{string.split(":")[1]}')
		elif string_prefix == "rdam":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/m/{string.split(":")[1]}')
		elif string_prefix == "rdamdt":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/m/datatype/{string.split(":")[1]}')
		elif string_prefix == "rdau":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/u/{string.split(":")[1]}')
		elif string_prefix == "rdaw":
			IRI_output = URIRef(f'http://rdaregistry.info/Elements/w/{string.split(":")[1]}')
		elif string_prefix == "rdax":
			IRI_output = URIRef(f'https://doi.org/10.6069/uwlib.55.d.4#{string.split(":")[1]}')
		elif string_prefix == "rdf":
			IRI_output = URIRef(f'http://www.w3.org/1999/02/22-rdf-syntax-ns#{string.split(":")[1]}')
		elif string_prefix == "rdfs":
			IRI_output = URIRef(f'http://www.w3.org/2000/01/rdf-schema#{string.split(":")[1]}')
		elif string_prefix == "schema":
			IRI_output = URIRef(f'http://schema.org/{string.split(":")[1]}')
		elif string_prefix == "sin":
			IRI_output = URIRef(f'http://sinopia.io/vocabulary/{string.split(":")[1]}')
		elif string_prefix == "skos":
			IRI_output = URIRef(f'http://www.w3.org/2004/02/skos/core#{string.split(":")[1]}')
		else:
			print(f"Prefix not recognized: {string_prefix}")
			quit()

	return IRI_output

def generate_constant(string):
	"""Convert string from kiegel mapping to an rdflib URI or literal"""
	constant_predicate = string.split("=")[0]
	constant_predicate = convert_string_to_IRI(constant_predicate)

	constant_value = string.split("=")[1]
	if ">" in constant_value:
		constant_value = constant_value.strip("<")
		constant_value = constant_value.strip(">")

		constant_value = URIRef(constant_value)
	else:
		constant_value = constant_value.strip('"')
		constant_value = Literal(constant_value)

	constant_pair = (constant_predicate, constant_value)

	return constant_pair

def create_bnode_name(predicate_name, class_name, property_number, value_type, kiegel_map, node_list):
	"""Create descriptive name for RML triples map for a blank node"""
	# default bnode map name
	map_number = property_number.strip('P')
	bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"

	# for "no-split" blank nodes, replace with pre-established name
	if "Provisionactivity" in bnode_map_name:
		bnode_map_name = "Provisionactivity_" + class_name + "_"
	elif "Title" in bnode_map_name:
		if "Variant" in class_name:
			bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
		elif "Abbreviated" in class_name:
			bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
		else:
			bnode_map_name = "Title_"
	elif "Dissertation" in bnode_map_name and property_number[1] == "1":
		bnode_map_name = "Dissertation_"
	elif property_number in classificationLcc_props:
		bnode_map_name = "Classification_Lcc_"
	elif property_number in classificationNlm_props:
		bnode_map_name = "Classification_Nlm_"

	# for "split" blank nodes, add value type
	elif value_type == "literal":
		# for literal values that use language tags, add "Lang_"
		if property_number in no_language_tag_list:
			bnode_map_name = f"{value_type.capitalize()}_{bnode_map_name}"
		elif property_number not in no_language_tag_list:
			bnode_map_name = f"Lang_{value_type.capitalize()}_{bnode_map_name}"
	elif value_type == "IRI":
		bnode_map_name = f"{value_type}_{bnode_map_name}"

	return bnode_map_name

def edit_kiegel(kiegel):
	"""Turn kiegel string into dictionary"""
	# get rid of extraneous whitespace within the mapping
	kiegel_list = kiegel.split("\n")
	new_kiegel_list = []
	for line in kiegel_list:
		line = line.strip()
		new_kiegel_list.append(line)
	new_kiegel = "\n".join(new_kiegel_list)
	kiegel = new_kiegel

	# create kiegel dictionary and lists
	new_kiegel_dict = {}
	IRI_list = []
	literal_list = []

	# iterate through mappings to add to lists
	mapping_list = kiegel.split("\nor\n")
	for mapping in mapping_list:
		new_mapping_list = mapping.split(" ; ")
		if "*" in mapping:
			for new_mapping in new_mapping_list:
				IRI_list.append(new_mapping)
		else:
			for new_mapping in new_mapping_list:
				literal_list.append(new_mapping)

	# add lists to dictionary (if they are not empty)
	if len(IRI_list) > 0:
		new_IRI_list = edit_kiegel_list(IRI_list)
		new_kiegel_dict["IRI"] = new_IRI_list
	if len(literal_list) > 0:
		new_literal_list = edit_kiegel_list(literal_list)
		new_kiegel_dict["literal"] = new_literal_list

	return new_kiegel_dict

def edit_kiegel_list(kiegel_list):
	"""Determine property for blank node mappings in a list of mappings. Used for mappings previously separated by a semicolon (;)."""
	new_kiegel_list = []

	num_of_mappings = len(kiegel_list)
	mapping_range = range(0, num_of_mappings)
	# iterate through mappings
	for num in mapping_range:
		mapping = kiegel_list[num]
		if mapping[0] == ">":
			"""This is "incomplete" mapping that goes into previous blank node"""
			# determine the previous mapping in mapping list that is "complete", i.e. does not begin with ">"
			previous_blank_node_index = num
			previous_blank_node = ">"
			while previous_blank_node[0] == ">":
				previous_blank_node_index = previous_blank_node_index - 1
				previous_blank_node = kiegel_list[previous_blank_node_index]

			# use predicate and class from previous "complete" mapping
			predicate_name = previous_blank_node.split(' ')[0]
			class_name = previous_blank_node.split(' ')[2]
			if predicate_name == "" or class_name == "":
				print(f"Error: predicate and/or class not found")
				bad_mapping = kiegel_list.join(" ; ")
				print(f"Kiegel: {bad_mapping}")
				quit()
			new_mapping = f"{predicate_name} >> {class_name} {mapping}"
			new_kiegel_list.append(new_mapping)
		else:
			"""This mapping is "complete" and can be added as-is"""
			new_kiegel_list.append(mapping)

	return new_kiegel_list
