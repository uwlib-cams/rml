"""Python Libraries/Modules/Packages"""
import csv
import os
from rdflib import *

"""Imported Functions"""
from functions.admin_metadata_functions import admin_metadata_mapping
from functions.boolean_functions import class_test
from functions.formatting_functions import edit_kiegel
from functions.split_by_space import split_by_space
from functions.logical_source_functions import generate_main_logical_source
from functions.value_functions import generate_RML_for_bnode
from functions.value_functions import generate_RML_for_constant
from functions.value_functions import generate_RML_for_IRI
from functions.value_functions import generate_RML_for_literal
from functions.start_RML_map import start_RML_map
from functions.subject_map_functions import generate_main_subject_map

"""Functions"""
def get_file_list(csv_dir, entity):
	"""Get list of CSV files for a given entity"""
	csv_file_list = os.listdir(csv_dir)
	file_list = []
	for file in csv_file_list:
		if entity in file:
			file_list.append(file)
	return file_list

def get_property_kiegel_list(csv_dir, entity):
	"""Get list of tuples (property number, kiegel) from CSV files for a given entity"""
	file_list = get_file_list(csv_dir, entity)

	if entity == "work":
		rda_iri = 'http://rdaregistry.info/Elements/w/'
		from functions.lists import skip_work_props as skip_prop_list
	elif entity == "expression":
		rda_iri = 'http://rdaregistry.info/Elements/e/'
		from functions.lists import skip_expression_props as skip_prop_list
	elif entity == "manifestation":
		rda_iri = 'http://rdaregistry.info/Elements/m/'
		from functions.lists import skip_manifestation_props as skip_prop_list
	elif entity == "item":
		rda_iri = 'http://rdaregistry.info/Elements/i/'
		from functions.lists import skip_item_props as skip_prop_list
	else:
		print("Entity not recognized.")
		quit()

	property_kiegel_list = []
	for csv_file in file_list:
		with open(f"{csv_dir}/{csv_file}") as file:
			csv_reader = csv.reader(file, delimiter=',')
			line_count = 0
			for line in csv_reader:
				if line_count == 0: # ignore header row
					pass
				elif "rdf-syntax" in line[1]:
					pass
				elif line[1].strip(rda_iri) in skip_prop_list:
					pass
				elif "P10002" in line[1] or "P20002" in line[1] or "P30004" in line[1] or "P40001" in line[1]:
					pass
				else:
					"""Find property number"""
					prop_IRI = line[1]
					if "rdaregistry" in prop_IRI:
						prop_num = prop_IRI.lstrip(rda_iri)
					else:
						prop_num = prop_IRI.lstrip('https://doi.org/10.6069/uwlib.55.d.4')
						prop_num = prop_num.strip('#')

					"""Find kiegel"""
					kiegel = line[3]
					# remove subclass variables, if they exist
					if ".subclass" in kiegel:
						split_kiegel = kiegel.split("\nor\n")
						for line in split_kiegel:
							if ".subclass" in line:
								split_kiegel.remove(line)
						kiegel = "\nor\n".join(split_kiegel)

					"""Create tuple and add to list"""
					property_kiegel_tuple = (prop_num, kiegel)
					property_kiegel_list.append(property_kiegel_tuple)
				line_count += 1

	return property_kiegel_list

def create_kiegel_dict(csv_dir, entity):
	"""Create dictionary ["property number": [kiegel split into list]"""
	kiegel_dict = {}

	property_kiegel_list = get_property_kiegel_list(csv_dir, entity)
	for tuple in property_kiegel_list:
		property_number = tuple[0]
		kiegel_dict[property_number] = []

		"""Turn kiegel into list"""
		kiegel = tuple[1]
		mapping_dict = edit_kiegel(kiegel)
		kiegel_dict[property_number] = mapping_dict

	return kiegel_dict

def kiegel_reader(csv_dir, entity):
	"""Start RML map"""
	RML_graph = start_RML_map()
	RML_graph = generate_main_logical_source(RML_graph, entity)
	RML_graph = generate_main_subject_map(RML_graph, entity)
	RML_graph = admin_metadata_mapping(RML_graph, entity)
	if entity == "work":
		from functions.identifiedBy_functions import P10002_mapping
		RML_graph = P10002_mapping(RML_graph)
	elif entity == "expression":
		from functions.identifiedBy_functions import P20002_mapping
		RML_graph = P20002_mapping(RML_graph)
	elif entity == "manifestation":
		from functions.identifiedBy_functions import P30004_mapping
		RML_graph = P30004_mapping(RML_graph)
	elif entity == "item":
		from functions.identifiedBy_functions import P40001_mapping
		RML_graph = P40001_mapping(RML_graph)
	else:
		print("Entity not recognized.")
		quit()

	"""For each property in kiegel_dict, convert kiegel map to RML code"""
	kiegel_dict = create_kiegel_dict(csv_dir, entity)

	bnode_po_dict = {}
	logsource_subject_list = []

	default_map_name = entity.capitalize()

	for prop_num in kiegel_dict.keys():
		prop_dict = kiegel_dict[prop_num]
		for value_type in prop_dict.keys(): # value_type == "IRI" or value_type == "literal"
			map_list = prop_dict[value_type]
			for mapping in map_list:
				map_name = default_map_name
				node_list = split_by_space(mapping)
				node_range = range(0, len(node_list))

				for num in node_range:
					node = node_list[num].strip()
					if node == ">":
						pass
					elif node == "not":
						pass
					elif node == "mapped":
						pass

					elif "*" in node:
						"""Property takes an IRI value"""
						RML_graph = generate_RML_for_IRI(RML_graph, default_map_name, map_name, node, prop_num)

					elif "=" in node:
						"""Property takes a constant value"""
						RML_graph = generate_RML_for_constant(RML_graph, map_name, node)

					elif node == ">>":
						"""Previous property in kiegel mapping takes a blank node as an object"""
						generate_RML_for_bnode_tuple = generate_RML_for_bnode(RML_graph, bnode_po_dict, logsource_subject_list, entity, prop_num, value_type, mapping, node_list, num, map_name)

						RML_graph = generate_RML_for_bnode_tuple[0]
						bnode_po_dict = generate_RML_for_bnode_tuple[1]
						logsource_subject_list = generate_RML_for_bnode_tuple[2]
						map_name = generate_RML_for_bnode_tuple[3]

					else:
						"""Property takes a literal or a blank node"""
						if num != len(node_list)-1 and node_list[num+1] == ">>":
							"""This property takes a blank node; pass, and get it in the previous elif on the next loop"""
							pass
						else:
							"""Make sure it's a property, and not a class for a blank node. Otherwise, it takes a literal"""
							its_a_class = class_test(node)
							if its_a_class == False:
								RML_graph = generate_RML_for_literal(RML_graph, default_map_name, map_name, prop_num, node)
	return RML_graph
