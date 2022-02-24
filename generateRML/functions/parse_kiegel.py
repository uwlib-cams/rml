"""Lists"""
from functions.lists import entity_prefixes

"""Imported Functions"""
from functions.admin_metadata_functions import admin_metadata_mapping
from functions.boolean_functions import class_test
from functions.kiegel_functions import create_kiegel_dict
from functions.split_by_space import split_by_space
from functions.logical_source_functions import generate_main_logical_source
from functions.value_functions import generate_RML_for_bnode
from functions.value_functions import generate_RML_for_constant
from functions.value_functions import generate_RML_for_IRI
from functions.value_functions import generate_RML_for_literal
from functions.start_RML_map import start_RML_map
from functions.subject_map_functions import generate_main_subject_map

def kiegel_reader(csv_dir, entity):
	"""Start RML map"""
	RML_graph = start_RML_map()
	RML_graph = generate_main_logical_source(RML_graph, entity)
	RML_graph = generate_main_subject_map(RML_graph, entity)
	RML_graph = admin_metadata_mapping(RML_graph, entity)

	"""Add RML for 'has identifier for work'/'expression'/'manifestation'/'item'"""
	# MCM: mappings for these properties in UW's RDA-to-BIBFRAME-map don't really work with our RML generator or transform, so the RML for these properties has been written manually rather than being generated. See...
	# -UW's RDA-to-BIBFRAME-map https://docs.google.com/spreadsheets/d/1y0coXcJAoVOP2BPtzwmnc9l-OWQbwYujVJ8oXXYpMRc/edit#gid=0
	# -identifiedBy_functions.py
	# -RML GitHub issue #8 https://github.com/uwlib-cams/rml/issues/8
	# -RML GitHub issue #15 https://github.com/uwlib-cams/rml/issues/15
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

	"""For each property in kiegel_dict, convert kiegel map to RML code"""
	kiegel_dict = create_kiegel_dict(csv_dir, entity) # dictionary of mappings from UW's RDA-to-BIBFRAME-map

	bnode_po_dict = {}
	logsource_subject_list = []

	default_map_name = entity.capitalize()

	for prop_num in kiegel_dict.keys(): # RDA property
		prop_dict = kiegel_dict[prop_num] # dictionary of possible mapping(s) for RDA property

		"""Determine prefix for RDA property"""
		first_two_characters = prop_num[0:2]
		if first_two_characters in entity_prefixes.keys():
			prefix = entity_prefixes[first_two_characters]
		else:
			prefix = "rdax"

		"""Iterate through possible mappings for RDA property"""
		for value_type in prop_dict.keys(): # value_type == "IRI" or value_type == "literal"
			map_list = prop_dict[value_type] # list of possible mapping(s) for RDA property that takes a given value type
			"""Iterate through possible mappings for value type"""
			for mapping in map_list:
				map_name = default_map_name # set map name to default, e.g. ex:WorkMap
				node_list = split_by_space(mapping) # separate the "nodes" of kiegel mapping into a list
				node_range = range(0, len(node_list))

				"""Iterate through nodes in kiegel mapping"""
				for num in node_range:
					node = node_list[num].strip()
					# Skips
					if node == ">":
						pass
					elif node == "not":
						pass
					elif node == "mapped":
						pass

					# IRIs
					elif "*" in node:
						"""Property takes an IRI value"""
						RML_graph = generate_RML_for_IRI(RML_graph, default_map_name, map_name, node, f"{prefix}:{prop_num}")

					# Constants
					elif "=" in node:
						"""Property takes a constant value"""
						RML_graph = generate_RML_for_constant(RML_graph, map_name, node)

					# Blank Nodes
					elif node == ">>":
						"""Previous property in kiegel mapping takes a blank node as an object"""
						generate_RML_for_bnode_tuple = generate_RML_for_bnode(RML_graph, bnode_po_dict, logsource_subject_list, entity, f"{prefix}:{prop_num}", value_type, mapping, node_list, num, map_name)

						RML_graph = generate_RML_for_bnode_tuple[0]
						bnode_po_dict = generate_RML_for_bnode_tuple[1]
						logsource_subject_list = generate_RML_for_bnode_tuple[2]
						map_name = generate_RML_for_bnode_tuple[3]

					# Literals
					else:
						"""Property takes a literal or a blank node"""
						if num != len(node_list)-1 and node_list[num+1] == ">>":
							"""This property takes a blank node; pass, and get it in the next loop with the previous elif"""
							pass
						else:
							"""Make sure it's a property, and not a class for a blank node. Otherwise, it takes a literal"""
							its_a_class = class_test(node)
							if its_a_class == False:
								RML_graph = generate_RML_for_literal(RML_graph, default_map_name, map_name, f"{prefix}:{prop_num}", node)
	return RML_graph
