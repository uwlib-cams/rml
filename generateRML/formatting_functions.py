"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Lists"""
from lists import classificationLcc_props
from lists import classificationNlm_props
from lists import no_language_tag_list

"""Copied & Pasted Functions"""
def constant_only_test(node_list, start_point):
	"""Copied from boolean_functions.py"""
	# ImportError: cannot import name 'constant_only_test' from partially initialized module 'boolean_functions' (most likely due to a circular import)
	num_of_nodes = len(node_list)
	start_num = 0
	bnode = ""
	for num in range(0, num_of_nodes):
		node = node_list[num].strip()
		if node == start_point:
			start_num = 1
		if start_num > 0:
			bnode = bnode + node + " "
		else:
			pass
	bnode_contents = bnode.split(" >> ")[1:]
	bnode_contents = (" >> ").join(bnode_contents)
	bnode_contents_list = split_by_space(bnode_contents)
	if "" in bnode_contents_list:
		bnode_contents_list.remove("")
	only_constants = True
	for node in bnode_contents_list:
		if node[0].isupper() == True: # class
			pass
		elif node == ">":
			pass
		elif node == ">>":
			only_constants = False
		else:
			if "*" in node: # IRI
				only_constants = False
			elif "=" not in node: # literal
				only_constants = False
	return only_constants

"""Functions"""
def convert_string_to_IRI(string):
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
	map_number = property_number.strip('P')
	bnode_map_name = predicate_name.capitalize() + "_" + str(map_number) + "_"
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
	elif value_type == "literal":
		if property_number in no_language_tag_list:
			bnode_map_name = f"{value_type.capitalize()}_{bnode_map_name}"
		#elif constant_only_test(node_list, predicate_name) == True: # and predicate_name != "contribution":
		#	bnode_map_name = f"{value_type.capitalize()}_Constant_{bnode_map_name}"
		elif property_number not in no_language_tag_list:
			bnode_map_name = f"Lang_{value_type.capitalize()}_{bnode_map_name}"
		else:
			print('uh oh 136')
			quit()
	elif value_type == "IRI":
		#if constant_only_test(node_list, predicate_name) == True and predicate_name != "contribution":
		#	bnode_map_name = f"{value_type}_Constant_{bnode_map_name}"
		#else:
		bnode_map_name = f"{value_type}_{bnode_map_name}"
	else:
		print('uh oh 141')
		quit()

#	if constant_only_test(node_list, predicate_name) == True and predicate_name != "contribution":
#		"""New blank node only contains a constant value"""
#		bnode_map_name = f"Constant_{predicate_name.capitalize()}_{class_name}_{property_number}_"

	return bnode_map_name

def replace_semicolons(kiegel_map):
	"""Replace shorthand semicolons in kiegel map with "long-hand" map that is more easily parsed"""
	if ";" in kiegel_map:
		kiegel_map = kiegel_map.replace("; >", ";>")
		kiegel_map = kiegel_map.split(" ; ")

		new_map_list = []

		for map in kiegel_map:
			map = map.replace(";>", "; >")
			map_list = map.split(" ; ")

			num_of_nodes = len(map_list)

			node_range = range(0, num_of_nodes)

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
							fixed_constant = " ".join(broken_constant_list)
							new_map_list.append(fixed_constant)
					else:
						new_map_list.append(item)

		map_list = new_map_list

	return map_list

def set_map_name(entity, prop_num, map_list, mapping, node_list):
	if mapping[0] == ">":
		"""This is an additional part of an existing blank node"""
		num_of_mappings = len(map_list)
		mapping_range = range(0, num_of_mappings)
		use_this_num = -1

		for num in mapping_range:
			current_mapping = map_list[num]
			if current_mapping == mapping:
				use_this_num = num - 1

		existing_bnode = map_list[use_this_num]
		predicate_name = split_by_space(existing_bnode)[0]
		class_name = split_by_space(existing_bnode)[2]
		new_map_name = create_bnode_name(predicate_name, class_name, prop_num, mapping, node_list)
	else:
		"""Use the default map"""
		new_map_name = entity.capitalize()

	return new_map_name

def edit_kiegel(kiegel):
	new_kiegel_dict = {}

	mapping_list = kiegel.split("\nor\n")
	IRI_list = []
	literal_list = []
	for mapping in mapping_list:
		new_mapping_list = mapping.split(" ; ")
		if "*" in mapping:
			for new_mapping in new_mapping_list:
				IRI_list.append(new_mapping)
		else:
			for new_mapping in new_mapping_list:
				literal_list.append(new_mapping)
	if len(IRI_list) > 0:
		new_IRI_list = edit_kiegel_list(IRI_list)
		new_kiegel_dict["IRI"] = new_IRI_list
	if len(literal_list) > 0:
		new_literal_list = edit_kiegel_list(literal_list)
		new_kiegel_dict["literal"] = new_literal_list

	return new_kiegel_dict

def edit_kiegel_list(kiegel_list):
	new_kiegel_list = []

	num_of_mappings = len(kiegel_list)
	mapping_range = range(0, num_of_mappings)

	for num in mapping_range:
		mapping = kiegel_list[num]
		if mapping[0] == ">":
			"""This goes into previous blank node"""
			previous_blank_node_index = num
			previous_blank_node = ">"
			while previous_blank_node[0] == ">":
				previous_blank_node_index = previous_blank_node_index - 1
				previous_blank_node = kiegel_list[previous_blank_node_index]

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
			new_kiegel_list.append(mapping)

	return new_kiegel_list
