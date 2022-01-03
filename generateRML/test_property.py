"""Python Libraries/Modules/Packages"""
from functions.boolean_functions import class_test
from functions.kiegel_functions import create_kiegel_dict
from functions.logical_source_functions import generate_main_logical_source
from functions.split_by_space import split_by_space
from functions.subject_map_functions import generate_main_subject_map
from functions.start_RML_map import start_RML_map
from functions.value_functions import generate_RML_for_bnode
from functions.value_functions import generate_RML_for_constant
from functions.value_functions import generate_RML_for_IRI
from functions.value_functions import generate_RML_for_literal
from sys import argv

script, prop_num = argv

def kiegel_reader_tester(csv_dir, entity, prop):
	RML_graph = start_RML_map()

	RML_graph = generate_main_logical_source(RML_graph, entity)

	RML_graph = generate_main_subject_map(RML_graph, entity)

	"""For each property in kiegel_dict, convert kiegel map to RML code"""
	kiegel_dict = create_kiegel_dict(csv_dir, entity)

	bnode_po_dict = {}
	logsource_subject_list = []

	default_map_name = entity.capitalize()

	for prop_num in kiegel_dict.keys():
		if prop in prop_num:
			prop_dict = kiegel_dict[prop_num]
			print("prop_dict:")
			for value_type in prop_dict.keys():
				print(value_type)
				for mapping in prop_dict[value_type]:
					print(f" - {mapping}")
			print("\n")

			for value_type in prop_dict.keys(): # value_type == "IRI" or value_type == "literal"
				map_list = prop_dict[value_type]
				for mapping in map_list:
					map_name = default_map_name
					print(mapping)
					#print(f"\tmap name: {map_name}")
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
							print(f"\t{node}: takes an IRI value")
							RML_graph = generate_RML_for_IRI(RML_graph, default_map_name, map_name, node, prop_num, True)


						elif "=" in node:
							"""Property takes a constant value"""
							print(f"\t{node}: takes a constant value")
							RML_graph = generate_RML_for_constant(RML_graph, map_name, node)

						elif node == ">>":
							"""Previous property in kiegel mapping takes a blank node as an object"""
							generate_RML_for_bnode_tuple = generate_RML_for_bnode(RML_graph, bnode_po_dict, logsource_subject_list, entity, prop_num, value_type, mapping, node_list, num, map_name, True)

							print(f"\t{node}: opens a blank node")
							RML_graph = generate_RML_for_bnode_tuple[0]
							bnode_po_dict = generate_RML_for_bnode_tuple[1]
							logsource_subject_list = generate_RML_for_bnode_tuple[2]
							if map_name == default_map_name:
								constant_map_name = generate_RML_for_bnode_tuple[3] # only update for the first bnode in a mapping
							map_name = generate_RML_for_bnode_tuple[3]

						else:
							"""Property takes a literal or a blank node"""
							if num != len(node_list)-1 and node_list[num+1] == ">>":
								"""This property takes a blank node; pass, and get it in the previous elif on the next loop"""
								print(f"\t{node}: takes a blank node")
								pass
							else:
								"""Make sure it's a property, and not a class for a blank node. Otherwise, it takes a literal"""
								its_a_class = class_test(node)
								if its_a_class == False:
									print(f"\t{node}: takes a literal value")
									RML_graph = generate_RML_for_literal(RML_graph, default_map_name, map_name, prop_num, node, True)
	return RML_graph

if prop_num[1] == "1":
	entity = "work"
elif prop_num[1] == "2":
	entity = "expression"
elif prop_num[1] == "3":
	entity = "manifestation"
elif prop_num[1] == "4":
	entity = "item"
graph = kiegel_reader_tester("csv_dir", entity, prop_num)
graph.serialize(destination=f"rmlOutput/{prop_num}RML.ttl", format="turtle")
