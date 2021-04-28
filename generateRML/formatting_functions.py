"""Python Libraries/Modules/Packages"""
from rdflib import *

"""Lists"""
from lists import classificationLcc_props
from lists import classificationNlm_props
from lists import no_language_tag_list

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

def create_bnode_name(predicate_name, class_name, property_number, kiegel_map):
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
	elif "*" not in kiegel_map:
		if property_number not in no_language_tag_list:
			bnode_map_name = f"Lang_{bnode_map_name}"
	elif "*" in kiegel_map:
		bnode_map_name = f"IRI_{bnode_map_name}"

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
