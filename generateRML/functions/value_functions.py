"""Lists"""
from functions.lists import no_language_tag_list
from functions.lists import nosplit_bnode_list
from functions.lists import provisionActivityDistributionList
from functions.lists import provisionActivityManufactureList
from functions.lists import provisionActivityProductionList
from functions.lists import provisionActivityPublicationList

"""Imported Functions"""
from functions.formatting_functions import create_bnode_name
from functions.logical_source_functions import generate_IRI_logical_source
from functions.logical_source_functions import generate_lang_logical_source
from functions.logical_source_functions import generate_lang_nosplit_logical_source
from functions.logical_source_functions import generate_neutral_literal_logical_source
from functions.logical_source_functions import generate_not_lang_logical_source
from functions.logical_source_functions import generate_not_lang_nosplit_logical_source
from functions.logical_source_functions import generate_provact_logical_source
from functions.logical_source_functions import generate_title_logical_source
from functions.po_map_functions import generate_bnode_po_map
from functions.po_map_functions import generate_constant_IRI
from functions.po_map_functions import generate_constant_literal
from functions.po_map_functions import generate_IRI_nosplit_po_map
from functions.po_map_functions import generate_IRI_po_map
from functions.po_map_functions import generate_IRI_split_po_map
from functions.po_map_functions import generate_lang_literal_split_po_map
from functions.po_map_functions import generate_langnotlang_literal_po_map
from functions.po_map_functions import generate_neutral_literal_nosplit_po_map
from functions.po_map_functions import generate_neutral_literal_po_map
from functions.po_map_functions import generate_neutral_literal_split_po_map
from functions.po_map_functions import generate_not_lang_literal_split_po_map
from functions.subject_map_functions import generate_bnode_subject_map

def generate_RML_for_IRI(RML_graph, default_map_name, map_name, node, prop_num, print_check=False):
	if map_name == default_map_name:
		"""Property goes in main map"""
		generate_IRI_po_map(RML_graph, map_name, node, prop_num)
		if print_check == True:
			print("\t\tgenerating IRI predicate object map")

	elif map_name in nosplit_bnode_list:
		"""Property is in 'no split' blank node"""
		# See: https://github.com/uwlib-cams/rml/tree/master/generateRML/functions#nosplit_bnode_list
		generate_IRI_nosplit_po_map(RML_graph, map_name, node, prop_num)
		if print_check == True:
			print("\t\tgenerating IRI no split predicate object map")

	else:
		"""Property goes into blank node"""
		generate_IRI_split_po_map(RML_graph, map_name, node)
		if print_check == True:
			print("\t\tgenerating IRI split predicate object map")

	return RML_graph

def generate_RML_for_constant(RML_graph, map_name, node, print_check=False):
	if "<" in node:
		"""Constant value is an IRI"""
		generate_constant_IRI(RML_graph, map_name, node)
		if print_check == True:
			print("\t\tgenerating constant predicate object map")
			print(f"\t\t\tmap name: {map_name}")
	else:
		"""Constant value is a literal"""
		generate_constant_literal(RML_graph, map_name, node)
		if print_check == True:
			print("\t\tgenerating constant predicate object map")
			print(f"\t\t\tmap name: {map_name}")

	if "Lang" in map_name:
		"""Generate RML code for equivalent 'no lang' blank node"""
		# ! add something to readme and link to it here
		not_lang_map_name = f"Not_{map_name}"
		if "<" in node:
			generate_constant_IRI(RML_graph, not_lang_map_name, node)
			if print_check == True:
				generate_constant_IRI(RML_graph, not_lang_map_name, node)
		else:
			generate_constant_literal(RML_graph, not_lang_map_name, node)
			if print_check == True:
				print("\t\tgenerating constant predicate object map, not lang")

	return RML_graph

def generate_RML_for_bnode(RML_graph, bnode_po_dict, logsource_subject_list, entity, prop_num, value_type, mapping, node_list, num, map_name, print_check=False):
	"""Predicate is previous item in node list, class is next item"""
	predicate_name = node_list[num-1]
	class_name = node_list[num+1]
	if print_check == True:
		print(f"\t\tblank node class: {class_name}")

	"""Generate name for new blank node RML map"""
	bnode_map_name = create_bnode_name(predicate_name, class_name, prop_num, value_type, mapping, node_list)
	if print_check == True:
		print(f"\t\tbnode_map_name: {bnode_map_name}\n")

	"""Default boolean values"""
	generate_new_bnode_po_map = False
	generate_new_logical_source = False
	generate_new_subject_map = False
	"""Determine if we need to generate RML for the current map to add new blank node map as a parentTriplesMap"""
	if map_name in bnode_po_dict.keys():
		if bnode_map_name not in bnode_po_dict[map_name]:
			generate_new_bnode_po_map = True
	else:
		generate_new_bnode_po_map = True
	"""Determine if we need to generate RML for a logical source for this blank node map"""
	if bnode_map_name not in logsource_subject_list:
		generate_new_logical_source = True
		generate_new_subject_map = True

	"""Generate RML based on boolean values"""
	if generate_new_bnode_po_map == True:
		generate_bnode_po_map(RML_graph, map_name, bnode_map_name, predicate_name)
		if print_check == True:
			print(f"\t\tgenerating blank node predicate object map ({map_name} > {bnode_map_name}) 109")

		if "Lang" in map_name:
			"""Generate RML code for equivalent 'no lang' blank node"""
			not_lang_map_name = f"Not_{map_name}"
			generate_bnode_po_map(RML_graph, not_lang_map_name, bnode_map_name, predicate_name)
			if print_check == True:
				print(f"\t\tgenerating blank node predicate object map ({not_lang_map_name} > {bnode_map_name}) 116")

		if "Lang" in bnode_map_name:
			"""Generate RML code for equivalent 'no lang' blank node(s)"""
			not_lang_bnode_map_name = f"Not_{bnode_map_name}"
			generate_bnode_po_map(RML_graph, map_name, not_lang_bnode_map_name, predicate_name)
			if print_check == True:
				print(f"\t\tgenerating blank node predicate object map ({map_name} > {not_lang_bnode_map_name}) 123")

			if "Lang" in map_name:
				not_lang_map_name = f"Not_{map_name}"
				generate_bnode_po_map(RML_graph, not_lang_map_name, not_lang_bnode_map_name, predicate_name)
				if print_check == True:
					print(f"\t\tgenerating blank node predicate object map ({not_lang_map_name} > {not_lang_bnode_map_name}) 129")

	if map_name not in bnode_po_dict.keys():
		bnode_po_dict[map_name] = []
	bnode_po_dict[map_name].append(bnode_map_name)

	if generate_new_logical_source == True:
		# Check for 'no split' blank nodes
		# see explanation here https://github.com/uwlib-cams/rml/tree/master/generateRML#no-split-blank-nodes
		# ! update link after updating readme
		if bnode_map_name == "Dissertation_":
			generate_dissertation_logical_source(RML_graph, bnode_map_name)
			if print_check == True:
				print("\t\tgenerating dissertation logical source")
		elif bnode_map_name == "Title_":
			generate_title_logical_source(RML_graph, entity, bnode_map_name)
			if print_check == True:
				print("\t\tgenerating title logical source")
		elif bnode_map_name[0:18] == "Provisionactivity_":
			generate_provact_logical_source(RML_graph, class_name, bnode_map_name)
			if print_check == True:
				print("\t\tgenerating provision activity logical source")
		elif bnode_map_name in nosplit_bnode_list:
			generate_lang_nosplit_logical_source(RML_graph, entity, bnode_map_name, prop_num)
			if print_check == True:
				print("\t\tgenerating logical source, no split")
			if "Lang" in bnode_map_name:
				"""Generate RML code for equivalent 'no lang' blank node"""
				not_lang_bnode_map_name = f"Not_{bnode_map_name}"
				generate_not_lang_nosplit_logical_source(RML_graph, entity, not_lang_bnode_map_name, prop_num)
				if print_check == True:
					print("\t\tgenerating logical source, no split")
		# If not, check what kind of value the blank node takes
		elif "Constant_" in bnode_map_name:
			"""The value is a constant"""
			generate_constant_logical_source(RML_graph, entity, bnode_map_name, prop_num)
			if print_check == True:
				print("\t\tgenerating constant logical source")
		elif "*" in mapping:
			"""The value is an IRI"""
			generate_IRI_logical_source(RML_graph, entity, bnode_map_name, prop_num)
			if print_check == True:
				print("\t\tgenerating IRI logical source")
		elif prop_num in no_language_tag_list:
			"""The value is a literal, and we do not record a language tag for it"""
			generate_neutral_literal_logical_source(RML_graph, entity, bnode_map_name, prop_num)
			if print_check == True:
				print("\t\tgenerating logical source")
		else:
			"""The value is a literal, and we DO want to record a language tag for it if it exists"""
			generate_lang_logical_source(RML_graph, entity, bnode_map_name, prop_num)
			if print_check == True:
				print(f"\t\tgenerating logical source ({bnode_map_name})")

			if "Lang" in bnode_map_name:
				not_lang_bnode_map_name = f"Not_{bnode_map_name}"
				generate_not_lang_logical_source(RML_graph, entity, not_lang_bnode_map_name, prop_num)
				if print_check == True:
					print(f"\t\tgenerating logical source ({not_lang_bnode_map_name})")

		logsource_subject_list.append(bnode_map_name)

		if generate_new_subject_map == True:
			generate_bnode_subject_map(RML_graph, bnode_map_name, class_name)
			if print_check == True:
				print(f"\t\tgenerating blank node subject map ({bnode_map_name})")

			if "Lang" in bnode_map_name:
				"""Generate RML code for equivalent 'no lang' blank node"""
				not_lang_bnode_map = f"Not_{bnode_map_name}"
				generate_bnode_subject_map(RML_graph, not_lang_bnode_map_name, class_name)
				if print_check == True:
					print(f"\t\tgenerating blank node subject map ({not_lang_bnode_map_name})")

	map_name = bnode_map_name

	return RML_graph, bnode_po_dict, logsource_subject_list, map_name

def generate_RML_for_literal(RML_graph, default_map_name, map_name, prop_num, node, print_check=False):
	if map_name == default_map_name:
		if print_check == True:
			print(f"map name: {map_name}")
			print(f"default map name: {default_map_name}")
		"""The literal is in the main map, not a blank node"""
		if prop_num in no_language_tag_list:
			"""We don't want the language tag(s)"""
			generate_neutral_literal_po_map(RML_graph, map_name, node, prop_num)
			if print_check == True:
				print("\t\tgenerating literal predicate object map (ignore lang tags)")
		else:
			"""We DO want the language tag(s) if they exist"""
			generate_langnotlang_literal_po_map(RML_graph, map_name, node, prop_num)
			if print_check == True:
				print("\t\tgenerating literal predicate object map (record lang tags)")

	# Otherwise, the literal is going into a blank node; check to see what kind
	elif map_name == "Title_":
		"""The literal goes into the blank node for title properties"""
		generate_langnotlang_literal_po_map(RML_graph, map_name, node, prop_num)
		if print_check == True:
			print("\t\tgenerating title predicate object map (record lang tags)")
	elif map_name in nosplit_bnode_list:
		"""The literal goes into a 'no split' blank node"""
		# see explanation here https://github.com/uwlib-cams/rml/tree/master/generateRML#no-split-blank-nodes
		# ! update link after updating readme
		generate_neutral_literal_nosplit_po_map(RML_graph, map_name, node, prop_num)
		if print_check == True:
			print("\t\tgenerating literal predicate object map, no split (ignore lang tags)")
	elif prop_num in no_language_tag_list:
		"""We don't want the language tag(s) for this literal"""
		generate_neutral_literal_split_po_map(RML_graph, map_name, node)
		if print_check == True:
			print("\t\tgenerating literal predicate object map, yes split (ignore lang tags)")

	else:
		"""We DO want the language tag(s) for this literal if they exist"""
		generate_lang_literal_split_po_map(RML_graph, map_name, node)
		if print_check == True:
			print(f"\t\tgenerating literal predicate object map ({map_name})")

		if map_name[0:4] == "Lang":
			"""Generate RML code for equivalent 'no lang' blank node"""
			not_lang_map_name = f"Not_{map_name}"
			generate_not_lang_literal_split_po_map(RML_graph, not_lang_map_name, node, prop_num)
			if print_check == True:
				print(f"\t\tgenerating literal predicate object map, yes split ({not_lang_map_name})")

	return RML_graph
