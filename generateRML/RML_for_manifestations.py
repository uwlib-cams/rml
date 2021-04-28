import csv
import os
from rdflib import *

"""Namespaces"""
bf = Namespace('http://id.loc.gov/ontologies/bibframe/')
bflc = Namespace('http://id.loc.gov/ontologies/bflc/')
dbo = Namespace('http://dbpedia.org/ontology/')
ex = Namespace('http://example.org/entity/')
madsrdf = Namespace('http://www.loc.gov/mads/rdf/v1#')
ql = Namespace('http://semweb.mmlab.be/ns/ql#')
rdac = Namespace('http://rdaregistry.info/Elements/c/')
rdae = Namespace('http://rdaregistry.info/Elements/e/')
rdai = Namespace('http://rdaregistry.info/Elements/i/')
rdam = Namespace('http://rdaregistry.info/Elements/m/')
rdamdt = Namespace('http://rdaregistry.info/Elements/m/datatype/')
rdau = Namespace('http://rdaregistry.info/Elements/u/')
rdaw = Namespace('http://rdaregistry.info/Elements/w/')
rdax = Namespace('https://doi.org/10.6069/uwlib.55.d.4#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
rml = Namespace('http://semweb.mmlab.be/ns/rml#')
rr = Namespace('http://www.w3.org/ns/r2rml#')
schema = Namespace('http://schema.org/')
sin = Namespace('http://sinopia.io/vocabulary/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

"""Lists"""
from lists import classification_props
from lists import no_language_tag_list
from lists import nosplit_bnode_list
from lists import skip_manifestation_props
from lists import manifestation_title_props

"""Imported Functions"""
from admin_metadata_functions import admin_metadata_mapping

from boolean_functions import class_test
from boolean_functions import constant_only_test

from formatting_functions import create_bnode_name
from formatting_functions import generate_constant
from formatting_functions import replace_semicolons
from formatting_functions import split_by_space

from identifiedBy_functions import P30004_mapping

from kiegel_functions import get_manifestation_kiegel_list
from kiegel_functions import get_manifestation_property_list

from logical_source_functions import generate_IRI_logical_source
from logical_source_functions import generate_classification_logical_source
from logical_source_functions import generate_constant_logical_source
from logical_source_functions import generate_lang_logical_source
from logical_source_functions import generate_lang_nosplit_logical_source
from logical_source_functions import generate_main_logical_source
from logical_source_functions import generate_not_lang_logical_source
from logical_source_functions import generate_not_lang_nosplit_logical_source
from logical_source_functions import generate_provact_logical_source
from logical_source_functions import generate_title_logical_source

from po_map_functions import generate_IRI_nosplit_po_map
from po_map_functions import generate_IRI_po_main_map
from po_map_functions import generate_IRI_split_po_map
from po_map_functions import generate_bnode_po_map
from po_map_functions import generate_constant_IRI
from po_map_functions import generate_constant_literal
from po_map_functions import generate_lang_literal_split_po_map
from po_map_functions import generate_langnotlang_literal_po_main_map
from po_map_functions import generate_neutral_literal_nosplit_po_map
from po_map_functions import generate_neutral_literal_po_main_map
from po_map_functions import generate_not_lang_literal_split_po_map

from start_RML_map import start_RML_map

from subject_map_functions import generate_bnode_subject_map
from subject_map_functions import generate_main_subject_map

###

def generate_rml_for_manifestations(csv_dir):
	default_map = "Manifestation"

	RML_graph = start_RML_map()
	generate_main_logical_source(RML_graph, "manifestation")
	generate_main_subject_map(RML_graph, "manifestation")
	admin_metadata_mapping(RML_graph, "manifestation")

	P30004_mapping(RML_graph)

	manifestation_property_list = get_manifestation_property_list(csv_dir)
	manifestation_kiegel_list = get_manifestation_kiegel_list(csv_dir)

	manifestation_property_range = range(0, len(manifestation_property_list))

	manifestation_bnode_po_dict = {}
	manifestation_logsource_subject_list = []

	for number in manifestation_property_range:
		property_number = manifestation_property_list[number]

		kiegel = manifestation_kiegel_list[number]

		kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

		for map_1 in kiegel_list: ## i want a more descriptive variable instead of map_1...
			extended_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statetments

			map_list = extended_map.split("\nand\n") # split new kiegel maps into separate items in a list

			for map_2 in map_list:
				map_name = default_map

				node_list = split_by_space(map_2)

				node_range = range(0, len(node_list))

				for num in node_range:
					node = node_list[num].strip()

					if node == ">":
						pass

					elif "*" in node: # node takes an IRI value
						if map_name == default_map:
							generate_IRI_po_main_map(RML_graph, map_name, node, property_number)
						elif map_name in nosplit_bnode_list:
							generate_IRI_nosplit_po_map(RML_graph, map_name, node, property_number)
						else:
							generate_IRI_split_po_map(RML_graph, map_name, node)

						if "Lang" in map_name:
							not_lang_map = f"Not_{map_name}"
							generate_IRI_split_po_map(RML_graph, not_lang_map, node)

					elif "=" in node: # node takes a constant value
						if "<" in node:
							generate_constant_IRI(RML_graph, map_name, node)
						else:
							generate_constant_literal(RML_graph, map_name, node)

						if "Lang" in map_name:
							not_lang_map = f"Not_{map_name}"
							if "<" in node:
								generate_constant_IRI(RML_graph, not_lang_map, node)
							else:
								generate_constant_literal(RML_graph, not_lang_map, node)

					elif node == ">>":
						predicate_name = node_list[num - 1]
						class_name = node_list[num + 1]
						bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)
						if constant_only_test(node_list, predicate_name) == True:
							if predicate_name != "contribution":
								bnode_map_name = f"Constant_{predicate_name.capitalize()}_{property_number}_"

						generate_new_bnode_po_map = False
						generate_new_logical_source = False
						generate_new_subject_map = False

						if map_name in manifestation_bnode_po_dict.keys():
							if bnode_map_name not in manifestation_bnode_po_dict[map_name]:
								generate_new_bnode_po_map = True
						else:
							generate_new_bnode_po_map = True

						if bnode_map_name not in manifestation_logsource_subject_list:
							generate_new_logical_source = True
							generate_new_subject_map = True

						if generate_new_bnode_po_map == True:
							generate_bnode_po_map(RML_graph, map_name, bnode_map_name, predicate_name)

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								generate_bnode_po_map(RML_graph, not_lang_map_name, bnode_map_name, predicate_name)

							if "Lang" in bnode_map_name:
								not_lang_bnode_map_name = f"Not_{bnode_map_name}"
								generate_bnode_po_map(RML_graph, map_name, not_lang_bnode_map_name, predicate_name)

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									generate_bnode_po_map(RML_graph, not_lang_map_name, not_lang_bnode_map_name, predicate_name)

						if map_name not in manifestation_bnode_po_dict.keys():
							manifestation_bnode_po_dict[map_name] = []
						manifestation_bnode_po_dict[map_name].append(bnode_map_name)

						if generate_new_logical_source == True: ###
							if "Provisionactivity" in bnode_map_name:
								generate_provact_logical_source(RML_graph, class_name, bnode_map_name)
							elif bnode_map_name == "Classification_Lcc_" or bnode_map_name == "Classification_Nlm_":
								generate_classification_logical_source(RML_graph, "manifestation", bnode_map_name)
							elif bnode_map_name == "Title_":
								generate_title_logical_source(RML_graph, "manifestation", bnode_map_name)
							elif bnode_map_name in nosplit_bnode_list:
								generate_lang_nosplit_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)

								if "Lang" in bnode_map_name:
									not_lang_bnode_map_name = f"Not_{bnode_map_name}"
									generate_not_lang_nosplit_logical_source(RML_graph, "manifestation", not_lang_bnode_map_name, property_number)
							elif "Constant_" in bnode_map_name:
								generate_constant_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)
							elif "*" in map_2: # the blank node takes an IRI
								generate_IRI_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)
							elif property_number in no_language_tag_list: # the blank node takes a literal, lang tag doesn't matter
								logical_source = generate_neutral_literal_logical_source(bnode_map_name, default_path, property_number)
								manifestation_RML_list.append(logical_source + "\n")
							else: # the blank node takes a literal, lang tag does matter
								generate_lang_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)

								if "Lang" in bnode_map_name:
									not_lang_bnode_map_name = f"Not_{bnode_map_name}"
									generate_not_lang_logical_source(RML_graph, "manifestation", not_lang_bnode_map_name, property_number)

							manifestation_logsource_subject_list.append(bnode_map_name)

						if generate_new_subject_map == True:
							generate_bnode_subject_map(RML_graph, bnode_map_name, class_name)

							if "Lang" in bnode_map_name:
								not_lang_bnode_map = f"Not_{bnode_map_name}"
								generate_bnode_subject_map(RML_graph, not_lang_bnode_map_name, class_name)

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
							if map_name == default_map:
								if property_number in no_language_tag_list:
									generate_neutral_literal_po_main_map(RML_graph, map_name, node, property_number)
								else:
									generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
							elif map_name == "Title_":
								generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
							elif map_name in nosplit_bnode_list:
								generate_neutral_literal_nosplit_po_map(RML_graph, map_name, node, property_number)
							elif property_number in no_language_tag_list:
								literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
								manifestation_RML_list.append(literal_po_map + "\n")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
									manifestation_RML_list.append(second_literal_po_map + "\n")
							else:
								generate_lang_literal_split_po_map(RML_graph, map_name, node, property_number.split(':')[-1])

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									generate_not_lang_literal_split_po_map(RML_graph, not_lang_map_name, node, property_number.split(':')[-1])

						elif node_list[num + 1] == ">>": # it takes a blank node
							pass
						else:
							# make sure it is a property and not a class by seeing if the first letter is capitalized
							its_a_class = class_test(node)
							if its_a_class == False:
								if map_name == default_map:
									if property_number in no_language_tag_list:
										generate_neutral_literal_po_main_map(RML_graph, map_name, node, property_number)
									else:
										generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
								elif map_name == "Title_":
									generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
								elif map_name in nosplit_bnode_list:
									generate_neutral_literal_nosplit_po_map(RML_graph, map_name, node, property_number)
								elif property_number in no_language_tag_list:
									literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
									manifestation_RML_list.append(literal_po_map + "\n")

									if "Lang" in map_name:
										not_lang_map_name = f"Not_{map_name}"
										second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
										manifestation_RML_list.append(second_literal_po_map + "\n")
								else:
									generate_lang_literal_split_po_map(RML_graph, map_name, node, property_number.split(':')[-1])

									if "Lang" in map_name:
										not_lang_map_name = f"Not_{map_name}"
										generate_not_lang_literal_split_po_map(RML_graph, not_lang_map_name, node, property_number.split(':')[-1])
	return RML_graph

def generate_rml_for_testing_manifestation_prop(csv_dir, prop):
	default_map = "Manifestation"

	RML_graph = start_RML_map()
	generate_main_logical_source(RML_graph, "manifestation")
	generate_main_subject_map(RML_graph, "manifestation")

	manifestation_property_list = get_manifestation_property_list(csv_dir)
	manifestation_kiegel_list = get_manifestation_kiegel_list(csv_dir)

	manifestation_property_range = range(0, len(manifestation_property_list))

	manifestation_bnode_po_dict = {}
	manifestation_logsource_subject_list = []

	for number in manifestation_property_range:
		property_number = manifestation_property_list[number]

		if property_number in prop:
			kiegel = manifestation_kiegel_list[number]

			kiegel_list = kiegel.split("\nor\n") # separate literal vs. IRI mappings

			for map_1 in kiegel_list: ## i want a more descriptive variable instead of map_1...
				extended_map = replace_semicolons(map_1) # replaces shorthand ; with easier-to-parse "and" statetments

				map_list = extended_map.split("\nand\n") # split new kiegel maps into separate items in a list

				for map_2 in map_list:
					print(map_2)
					map_name = default_map

					node_list = split_by_space(map_2)

					node_range = range(0, len(node_list))

					for num in node_range:
						node = node_list[num].strip()

						if node == ">":
							pass

						elif "*" in node: # node takes an IRI value
							print(f"\t{node}: takes an IRI value")
							if map_name == default_map:
								generate_IRI_po_main_map(RML_graph, map_name, node, property_number)
								print("\t\tgenerating IRI predicate object map")
							elif map_name in nosplit_bnode_list:
								generate_IRI_nosplit_po_map(RML_graph, map_name, node, property_number)
								print("\t\tgenerating IRI no split predicate object map")
							else:
								generate_IRI_split_po_map(RML_graph, map_name, node)
								print("\t\tgenerating IRI split predicate object map")

							if "Lang" in map_name:
								not_lang_map = f"Not_{map_name}"
								generate_IRI_split_po_map(RML_graph, not_lang_map, node)
								print("\t\tgenerating IRI predicate object map, not lang")

						elif "=" in node: # node takes a constant value
							print(f"\t{node}: takes a constant value")
							if "<" in node:
								generate_constant_IRI(RML_graph, map_name, node)
							else:
								generate_constant_literal(RML_graph, map_name, node)
							print("\t\tgenerating constant predicate object map")

							if "Lang" in map_name:
								not_lang_map = f"Not_{map_name}"
								if "<" in node:
									generate_constant_IRI(RML_graph, not_lang_map, node)
								else:
									generate_constant_literal(RML_graph, not_lang_map, node)
								print("\t\tgenerating constant predicate object map, not lang")

						elif node == ">>":
							print(f"\t{node}: opens a blank node")
							predicate_name = node_list[num - 1]
							class_name = node_list[num + 1]
							print(f"\t\t{class_name}: blank node class")
							bnode_map_name = create_bnode_name(predicate_name, class_name, property_number, map_2)
							if constant_only_test(node_list, predicate_name) == True:
								if predicate_name != "contribution":
									bnode_map_name = f"Constant_{predicate_name.capitalize()}_{property_number}_"

							generate_new_bnode_po_map = False
							generate_new_logical_source = False
							generate_new_subject_map = False

							if map_name in manifestation_bnode_po_dict.keys():
								if bnode_map_name not in manifestation_bnode_po_dict[map_name]:
									generate_new_bnode_po_map = True
							else:
								generate_new_bnode_po_map = True

							if bnode_map_name not in manifestation_logsource_subject_list:
								generate_new_logical_source = True
								generate_new_subject_map = True

							if generate_new_bnode_po_map == True:
								generate_bnode_po_map(RML_graph, map_name, bnode_map_name, predicate_name)
								print("\t\tgenerating blank node predicate object map")

								if "Lang" in map_name:
									not_lang_map_name = f"Not_{map_name}"
									generate_bnode_po_map(RML_graph, not_lang_map_name, bnode_map_name, predicate_name)
									print("\t\tgenerating blank node predicate object map")

								if "Lang" in bnode_map_name:
									not_lang_bnode_map_name = f"Not_{bnode_map_name}"
									generate_bnode_po_map(RML_graph, map_name, not_lang_bnode_map_name, predicate_name)
									print("\t\tgenerating blank node predicate object map")

									if "Lang" in map_name:
										not_lang_map_name = f"Not_{map_name}"
										generate_bnode_po_map(RML_graph, not_lang_map_name, not_lang_bnode_map_name, predicate_name)
										print("\t\tgenerating blank node predicate object map")

							if map_name not in manifestation_bnode_po_dict.keys():
								manifestation_bnode_po_dict[map_name] = []
							manifestation_bnode_po_dict[map_name].append(bnode_map_name)

							if generate_new_logical_source == True: ###
								if "Dissertation" in bnode_map_name:
									generate_dissertation_logical_source(RML_graph, bnode_map_name)
									print("\t\tgenerating dissertation logical source")
								elif bnode_map_name == "Title_":
									generate_title_logical_source(RML_graph, "manifestation", bnode_map_name)
									print("\t\tgenerating title logical source")
								elif bnode_map_name in nosplit_bnode_list:
									generate_lang_nosplit_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)
									print("\t\tgenerating logical source, no split")

									if "Lang" in bnode_map_name:
										not_lang_bnode_map_name = f"Not_{bnode_map_name}"
										generate_not_lang_nosplit_logical_source(RML_graph, "manifestation", not_lang_bnode_map_name, property_number)
										print("\t\tgenerating logical source, no split")
								elif "Constant_" in bnode_map_name:
									generate_constant_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)
									print("\t\tgenerating constant logical source")
								elif "*" in map_2: # the blank node takes an IRI
									generate_IRI_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)
									print("\t\tgenerating IRI logical source")
								elif property_number in no_language_tag_list: # the blank node takes a literal, lang tag doesn't matter
									logical_source = generate_neutral_literal_logical_source(bnode_map_name, default_path, property_number)
									print("\t\tgenerating logical source")
									manifestation_RML_list.append(logical_source + "\n")
								else: # the blank node takes a literal, lang tag does matter
									generate_lang_logical_source(RML_graph, "manifestation", bnode_map_name, property_number)
									print("\t\tgenerating logical source")

									if "Lang" in bnode_map_name:
										not_lang_bnode_map_name = f"Not_{bnode_map_name}"
										generate_not_lang_logical_source(RML_graph, "manifestation", not_lang_bnode_map_name, property_number)
										print("\t\tgenerating logical source")

								manifestation_logsource_subject_list.append(bnode_map_name)

							if generate_new_subject_map == True:
								generate_bnode_subject_map(RML_graph, bnode_map_name, class_name)
								print("\t\tgenerating blank node subject map")

								if "Lang" in bnode_map_name:
									not_lang_bnode_map = f"Not_{bnode_map_name}"
									generate_bnode_subject_map(RML_graph, not_lang_bnode_map_name, class_name)
									print("\t\tgenerating blank node subject map")

							map_name = bnode_map_name

						elif node == "not":
							pass
						elif node == "mapped":
							pass
						elif "See" in node:
							pass

						elif "{" in node:
							print(f"\t{node}: creates a template")
							part_a = property_number
							part_b = manifestation_property_list[number+1]
							node = node.strip("{")
							node = node.strip("}")

							template_po = generate_template_po_map(node, part_a, part_b, map_name)
							print("\t\tgenerating template predicate object map")
							manifestation_RML_list.append(template_po + "\n")

							if "Lang" in map_name:
								not_lang_map_name = f"Not_{map_name}"
								second_template_po = generate_template_po_map(node, part_a, part_b, not_lang_map_name)
								print("\t\tgenerating template predicate object map")
								manifestation_RML_list.append(second_template_po + "\n")

						else: # node takes a literal value or blank node
							if num == (len(node_list) - 1): # it's the last node and cannot be a blank node, takes a literal
								print(f"\t{node}: takes a literal value")
								if map_name == default_map:
									if property_number in no_language_tag_list:
										generate_neutral_literal_po_main_map(RML_graph, map_name, node, property_number)
										print("\t\tgenerating literal predicate object map")
									else:
										generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
										print("\t\tgenerating literal predicate object map")
								elif map_name == "Title_":
									generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
									print("\t\tgenerating title predicate object map")
								elif map_name in nosplit_bnode_list:
									generate_neutral_literal_nosplit_po_map(RML_graph, map_name, node, property_number)
									print("\t\tgenerating literal predicate object map, no split")
								elif property_number in no_language_tag_list:
									literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
									print("\t\tgenerating literal predicate object map, yes split")
									manifestation_RML_list.append(literal_po_map + "\n")

									if "Lang" in map_name:
										not_lang_map_name = f"Not_{map_name}"
										second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
										print("\t\tgenerating literal predicate object map, yes split")
										manifestation_RML_list.append(second_literal_po_map + "\n")
								else:
									generate_lang_literal_split_po_map(RML_graph, map_name, node, prop)
									print("\t\tgenerating literal predicate object map, yes split")

									if "Lang" in map_name:
										not_lang_map_name = f"Not_{map_name}"
										generate_not_lang_literal_split_po_map(RML_graph, not_lang_map_name, node, prop)
										print("\t\tgenerating literal predicate object map, yes split")

							elif node_list[num + 1] == ">>": # it takes a blank node
								print(f"\t{node}: takes a blank node")
								pass
							else:
								# make sure it is a property and not a class
								its_a_class = class_test(node)
								if its_a_class == False:
									print(f"\t{node}: is a property")
									if map_name == default_map:
										if property_number in no_language_tag_list:
											generate_neutral_literal_po_main_map(RML_graph, map_name, node, property_number)
											print("\t\tgenerating literal predicate object map")
										else:
											generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
											print("\t\tgenerating literal predicate object map")
									elif map_name == "Title_":
										generate_langnotlang_literal_po_main_map(RML_graph, map_name, node, property_number)
										print("\t\tgenerating title predicate object map")
									elif map_name in nosplit_bnode_list:
										generate_neutral_literal_nosplit_po_map(RML_graph, map_name, node, property_number)
										print("\t\tgenerating literal predicate object map, no split")
									elif property_number in no_language_tag_list:
										literal_po_map = generate_neutral_literal_split_po_map(node, map_name)
										print("\t\tgenerating literal predicate object map, yes split")
										manifestation_RML_list.append(literal_po_map + "\n")

										if "Lang" in map_name:
											not_lang_map_name = f"Not_{map_name}"
											second_literal_po_map = generate_neutral_literal_split_po_map(node, not_lang_map_name)
											print("\t\tgenerating literal predicate object map, yes split")
											manifestation_RML_list.append(second_literal_po_map + "\n")
									else:
										generate_lang_literal_split_po_map(RML_graph, map_name, node, prop)
										print("\t\tgenerating literal predicate object map, yes split")

										if "Lang" in map_name:
											not_lang_map_name = f"Not_{map_name}"
											generate_not_lang_literal_split_po_map(RML_graph, not_lang_map_name, node, prop)
											print("\t\tgenerating literal predicate object map, yes split")
	return RML_graph
